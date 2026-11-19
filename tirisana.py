
import pandas as pd
from pathlib import Path

# Nosaka projekta mapes atrašanās vietu.
"Patstavigais-darbs-Modelis-no-sistemas-datiem" = Path(__file__).parent
datu_mape = "Patstavigais-darbs-Modelis-no-sistemas-datiem" / "dati"

# Atrod CSV failu datu mapē, neiekļaujot jau sagatavoto failu.
csv_faili = [
    fails for fails in datu_mape.glob("*.csv")
    if fails.name.lower() != "tirs.csv"
]

if not csv_faili:
    raise FileNotFoundError("Mapē 'dati' nav atrasts sākotnējais CSV fails.")

if len(csv_faili) > 1:
    raise RuntimeError("Mapē 'dati' ir vairāki CSV faili. Atstāj vienu sākotnējo datu failu.")

ievades_fails = csv_faili[0]
izvades_fails = "Patstavigais-darbs-Modelis-no-sistemas-datiem" / "tirs.csv"      # Nosaka ka izvades fails būs īstajā mapē un to sauks tirs.csv

# Nolasa sākotnējos datus, izmantojot UTF-8 kodējumu.
df = pd.read_csv(ievades_fails)

sakuma_rindu_skaits = len(df)

print("Sākotnējais fails:", ievades_fails.name)
print("Rindu skaits pirms tīrīšanas:", sakuma_rindu_skaits)
print("\nSākotnējo datu informācija:")
print(df.info())

# Pārvērš gadu skaitliskā formātā, jo tas nepieciešams datu analīzei.
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

# Noņem rindas bez gada, jo bez laika informācijas nav iespējams korekti analizēt rādītāju attīstību.
df = df.dropna(subset=["Year"])

# Atrod interneta lietošanas rādītāja kolonnu.
merka_kolonnas = [
    kolonna for kolonna in df.columns
    if "Share of the population using the Internet" in kolonna.lower()
]

if len(merka_kolonnas) != 1:
    raise ValueError(
        "Neizdevās viennozīmīgi atrast interneta lietošanas rādītāja kolonnu."
    )

merka_kolonna = merka_kolonnas[0]

# Pārvērš interneta lietošanas procentus skaitliskā formātā.
df[merka_kolonna] = pd.to_numeric(
    df[merka_kolonna], errors="coerce"
)

# Izņem rindas bez interneta lietošanas rādītāja, jo tās nevar izmantot tā analīzei vai prognozēšanai.
df = df.dropna(subset=[merka_kolonna])

# Izņem dublikātus, jo vienai valstij vai reģionam vienā gadā jābūt tikai vienam rādītājam.
df = df.drop_duplicates(subset=["Entity", "Year"])

# Izņem ierakstus ar neiespējamām procentu vērtībām (ja tādas ir), jo interneta lietotāju īpatsvars nevar būt ārpus 0–100%.
df = df[
    df[merka_kolonna].between(0, 100)
]

# Sakārto datus pēc reģiona un gada, lai tos būtu vieglāk analizēt.
df = df.sort_values(by=["Entity", "Year"])

# Saglabā sakārtotos datus jaunā CSV failā, nemainot oriģinālo datu kopu.
df.to_csv(izvades_fails, index=False, encoding="utf-8")

beigu_rindu_skaits = len(df)

print("\nDatu tīrīšanas rezultāts:")
print("Rindu skaits pirms tīrīšanas:", sakuma_rindu_skaits)
print("Rindu skaits pēc tīrīšanas:", beigu_rindu_skaits)
print("Noņemtās rindas:", sakuma_rindu_skaits - beigu_rindu_skaits)
print("Sagatavotais fails:", izvades_fails)

print("\nSakārtoto datu informācija:")
print(df.info())
