# Utkikk

Dette er en prosjektidé for å løse et case med å visualisere data fra en CSV-fil.

Utkikk er en webapp som er tiltenkt å gjøre en hel del enkle analyser på datasett med hjelp av python-biblioteket Pandas, GeoPandas og Matplotlib. Informasjonen fra analysen presenteres for en bruker gjennom nettleseren i en side bygget med ReactJS.

Foreløpig er søk implementert. Sortering og filtrering er påbegynt men er enn så lenge ikke implementert.
Det gjenstår en god del før programmet når en eventuell MVP, inkludert "rensking" av kode og kommentarer.

## Bygge programmet
Koden krever at systemet har installert Python3 (usikker hvilken versjon som er nødvendig, ble programmert i 3.10).
Av python-pakker trenger man flask, flask_cors (for å sende forespørsler mellom frontend og backend, dårlig løsning og må fikses før produksjon), pandas og json (kommer vel som standard men brukes eksplisitt i koden), samt pakken waitress for å kjøre backend-scriptet. På sikt trengs også matplotlib (for å lage grafikk) og geopandas (for å gjøre analyser av posisjonsdata).

For å kjøre frontend trengs nodeJS (npm/npx) og yarn for å kjøre frontend-serveren slik den ligger nå. Tanken er å tjene frontend via nginx i produksjon, men så langt har jeg ikke kommet ennå. For å skaffe nødvendige pakker brukes koden ***npm install*** og kjøres i utviklingsmodus med koden ***yarn start***. Produksjonsfiler bygges med ***yarn build***, og filene i mappen 'utkikk/build/' skal kunne tjenes videre.

Når applikasjonen er ferdig utviklet i MVP er tanken å få programmene inn i docker-containere sånn at det skal være enkelt å kjøre opp og ned tjenestene med riktig konfigurering.

## Kjøre programmet
For å kjøre analyse-API'et brukes kodesnutten under i et shell (bash/powershell)
> ./utkikk/api/waitress-serve --listen=127.0.0.1:5000 wsgi:app

API'et serves da på localhost:5000/ og den primære forlengelsen er 'api/data'. Et utdrag fra dataen finnes på ***localhost:5000/api/eksempel*** 

For å kjøre frontend under utviklingen har jeg brukt kodesnutten under i et shell (bash/powershell)
> ./utkikk/yarn start
 
Frontend tjenes da på localhost:3000. Til produksjon vil applikasjonen bygges med "yarn build", og innhold i './utkikk/build' er det som brukes for videre tjening. 

Backend kjører som sagt på port 5000, mens frontend er i produksjon tiltenkt kjørt med nginx, og da tjenes via http(80)/https(443).

Se forøvrig prosjektidé og arbeidsliste.md for arbeidslogg og underveis idémyldring.
