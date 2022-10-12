# Utkikk

Dette er en prosjektidé for å løse et case med å visualisere data fra en CSV-fil.

Utkikk er en webapp som er tiltenkt å gjøre en hel del enkle analyser på datasett med hjelp av python-biblioteket Pandas, GeoPandas og Matplotlib. Informasjonen fra analysen presenteres for en bruker gjennom nettleseren i en side bygget med ReactJS.

Foreløpig er søk implementert. Sortering og filtrering er påbegynt men er enn så lenge ikke implementert

Koden er kjørbar og krever at systemet har installert Python3 (usikker hvilken versjon som er nødvendig, ble programmert i 3.10) for å kjøre analyse-API'et, nodeJS og yarn for å kjøre frontend-serveren. Det kan sikkert hostes på andre måter, men det er sånn jeg har kjørt det i utviklingen

Ambisjonen er å få programmene inn i docker-containere sånn at det skal være enkelt å kjøre opp og ned tjenestene med riktig konfigurering.

Backend kjører på port 5000, mens frontend kjører på port 3000. Veien med å forwarde porter til de mer brukte HTTP og HTTPS er påtenkt, men jeg har ikke kommet så langt ennå.

Se forøvrig prosjektidé og arbeidsliste.md for arbeidslogg og underveis idémyldring.