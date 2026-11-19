
import pandas as pd        # Importē bibliotēku kas lauj strādāt ar CSV failiem tostarp tos nolasīt, apstrādāt un izveidot jaunus
from pathlib import Path

# Nosaka projekta mapes un sākotnējā CSV faila atrašanās vietu.
projekta_mape = Path(__file__).parent
datu_mape = projekta_mape / "dati"

csv_faili = list(datu_mape.glob("*.csv"))

if len(csv_faili) != 1:
    raise RuntimeError("Mapē 'dati' jābūt tieši vienam CSV failam.")

ievades_fails = csv_faili[0]
izvades_fails = projekta_mape / "tirs.csv"

# Nolasa sākotnējos datus, nemainot oriģinālo failu.
df = pd.read_csv(ievades_fails)

sakuma_rindu_skaits = len(df)

print("Sākotnējais fails:", ievades_fails.name)
print("Rindu skaits pirms tīrīšanas:", sakuma_rindu_skaits)

# Pārvērš gadu un interneta lietošanas rādītāju skaitliskā formātā.
df["Year"] = pd.to_numeric(df["Year"], errors="coerce")

merka_kolonna = "Share of the population using the Internet"
df[merka_kolonna] = pd.to_numeric(df[merka_kolonna], errors="coerce")

# Saglabā tikai ierakstus no 1990. līdz 2020. gadam.
df = df[df["Year"].between(1990, 2020)]

# Izveido visu nepieciešamo gadu sarakstu no 1990. līdz 2020. gadam.
nepieciesamie_gadi = set(range(1990, 2021))

# Pārbauda, vai katrai valstij ir dati par visiem 31 gadiem.
pilnigas_valstis = []

for valsts, dati in df.groupby("Entity"):
    valsts_gadi = set(dati["Year"].astype(int))

    # Atzīmē tās valstis, kurām nav iztrūkstošu gadu.
    if valsts_gadi == nepieciesamie_gadi:
        pilnigas_valstis.append(valsts)

# Izņem visas valstis, kurām trūkst dati izvēlētajā periodā.
df = df[df["Entity"].isin(pilnigas_valstis)]

# Sakārto datus pēc valsts un gada.
df = df.sort_values(by=["Entity", "Year"])

# Saglabā rezultātu jaunā CSV failā.
df.to_csv(izvades_fails, index=False, encoding="utf-8")

beigu_rindu_skaits = len(df)

# Izvada tīrīšanas rezultātus.
print("\n--- Datu tīrīšanas rezultāts ---")
print("Rindu skaits pirms tīrīšanas:", sakuma_rindu_skaits)
print("Rindu skaits pēc tīrīšanas:", beigu_rindu_skaits)
print("Noņemtās rindas:", sakuma_rindu_skaits - beigu_rindu_skaits)
print("Pilnīgo valstu skaits:", len(pilnigas_valstis))

print("\nFails saglabāts:", izvades_fails)
