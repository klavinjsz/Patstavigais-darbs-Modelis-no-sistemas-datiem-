# Patstavigais-darbs-Modelis-no-sistemas-datiem-
Ceturtā kursa (2026) patstāvīgais darbs priekšmetā: Makslīgā intelekta tehnoloģijas

Sākotnējā avota cvs failā vairākām valstīm nav dati par katru gadu, fails tirisana.py iztīra no avota csv faila valstis ar nepilnīgiem datiem periodā no 1990. līdz 2020. gadam


Failā modelis.py izmantoju Random Forest klasifikācijas modeli
Lai izpildītu uzdevuma nosacījumus un lai scikit-learn modelis spētu prognozēt datus, kas avota csv failā ir procentuāli es tos failā modelis.py pārveidoju no procentuāliem lielumiem - trijās kategorijās: 
Zems interneta lietotāju daudzums: mazāk par 30%.
Vidējs interneta lietotāju daudzums: no 30% līdz mazāk par 70%.
Augsts interneta lietotāju daudzums: 70% vai vairāk.


Lai palaistu failu tirisana.py nepieciesams instalēt biblioteku "pandas", termināli palaižot komandu - pip install pandas
Lai palaistu failu modelis.py nepieciešams instalēt biblioteku "pandas scikit-learn", termināli palaižot komandu - pip install pandas scikit-learn
