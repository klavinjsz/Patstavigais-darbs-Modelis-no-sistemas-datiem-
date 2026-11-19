import pandas as pd

# importē scikit-learn bibliotēkas funkcijas
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.metrics import accuracy_score

# Nolasa sagatavotos datus no CSV faila.
df = pd.read_csv("tirs.csv")

# Nosaka prognozējamo kolonnu.
merka_kolonna = "Share of the population using the Internet"

# Pārveido procentuālos rādītājus trīs klasēs.
def klasificet(procenti):
    if procenti < 30:
        return "Zems"
    elif procenti < 70:
        return "Videjs"
    else:
        return "Augsts"

df["Limenis"] = df[merka_kolonna].apply(klasificet)

# Izvēlas pazīmes, pēc kurām modelis mēģinās prognozēt interneta lietojuma līmeni.
X = df[["Entity", "Year"]]

# Nosaka prognozējamo rezultātu.
y = df["Limenis"]

# Sadala datus 80% apmācībai un 20% pārbaudei.
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Pārveido valstu nosaukumus skaitliskā formātā, lai modelis tos varētu izmantot.
apstrade = ColumnTransformer(
    transformers=[
        ("valsts", OneHotEncoder(handle_unknown="ignore"), ["Entity"]),
        ("gads", "passthrough", ["Year"])
    ]
)

# Izveido Random Forest klasifikācijas modeli.
modelis = Pipeline(steps=[
    ("apstrade", apstrade),
    ("klasifikators", RandomForestClassifier(
        n_estimators=100,
        random_state=42
    ))
])

# Apmāca modeli, izmantojot treniņa datus.
modelis.fit(X_train, y_train)

# Veic prognozes testa datiem.
prognozes = modelis.predict(X_test)

# Aprēķina modeļa precizitāti.
modela_precizitate = accuracy_score(y_test, prognozes)

# Izveido bāzes līniju, kas vienmēr prognozē biežāko klasi.
bazes_modelis = DummyClassifier(strategy="most_frequent")
bazes_modelis.fit(X_train, y_train)

# Aprēķina bāzes līnijas precizitāti uz tiem pašiem testa datiem.
bazes_prognozes = bazes_modelis.predict(X_test)
bazes_precizitate = accuracy_score(y_test, bazes_prognozes)

# Izvada abu modeļu rezultātus salīdzināšanai.
print("\n--- MODEĻA REZULTĀTI ---")
print("Izmantotais modelis: Random Forest Classifier")
print("Treniņa datu skaits:", len(X_train))
print("Testa datu skaits:", len(X_test))

print("\nPrecizitātes salīdzinājums:")
print(f"Random Forest modelis: {modela_precizitate:.2%}")
print(f"Bāzes līnija:          {bazes_precizitate:.2%}")

# Nosaka, vai modelis pārspēj biežākās atbildes bāzes līniju.
if modela_precizitate > bazes_precizitate:
    print("\nSecinājums: Modelis pārspēj bāzes līniju.")
elif modela_precizitate == bazes_precizitate:
    print("\nSecinājums: Modelis sasniedz tādu pašu rezultātu kā bāzes līnija.")
else:
    print("\nSecinājums: Modelis nepārspēj bāzes līniju.")

print("\nPrognozējamo klašu sadalījums:")
print(y.value_counts()) 