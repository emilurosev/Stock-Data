Pokretanjem skripte main.py se svlaci oko 50k berzanskih podataka za 10 velikih svetskih kompanija preko Alpha Vantage API-ja, koji se dalje smestaju u Mongo bazu i json fajlove.

Prati pocetnu, maksimalnu, minimalnu i zavrsnu cenu deonice, kao i volumen unutar jednog vremenskog uzorka. 

Ova skripta skida podatke u dva razlicita vremenska intervala(vremenska zona US/Eastern):

1.) Na svakih 60 min, svaki radni dan od 9:30 do 15:30. Frekvencija upisa je 7 dokumenata dnevno po kompaniji. Pomocu cron-a moze se zakazati, na svakih sat vremena od 10:00 do 16:00 (zbog moguceg kasnjenja API-ja od pola sata) radnim danima, task koji pokrece skriptu i kupi poslednji podatak iz niza, koji se zatim lako upisuje u bazu.

2.) Svaki radni dan u ponoc - Istorijski podaci. Ova skripta je dobavlja istorijske podatke od 2000 do 2020 za svih 10 kompanija. Frekvencija je upisa je 1 dokument dnevno po kompaniji.

U dodatku su dva Jupyter Notebook-a u kojima su vizuelno prikazani svi prikupljeni podaci, kao i njihov export u csv fajlove.   
