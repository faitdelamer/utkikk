# Prosjektidé
Datavisualisering og analyseverktøy kan være litt kompliserte å forstå seg på. Jeg vil lage en app som gir hurtig informasjon om en CSV-fil, og beskriver datasettet på en enkel måte. Jeg tenkte umiddelbart på analysepakken Pandas til python, og bygger analysen rundt det.

Når det kommer til brukergrensesnitt så må jeg spille på de tingene jeg har noe kompetanse på, og det blir derfor en webapp, da jeg har noe erfaring med webutvikling. Jeg ønsker å bruke rammeverket React fordi jeg har hørt lovord om dette, men det blir en utfordring da jeg ikke har brukt det tidligere.

For å sette dette i drift tenker jeg å legge pakkene inn i en docker-container sånn at det relativt enkelt kan settes i drift. Dette har jeg heller ikke gjort før, så det kan bli en utfordring.

# BACKEND API
Flask skal primært fungere som et API og sende data til frontend. 

Dataene behandles som pandas.DataFrame og sendes til flask som dictionaries, som flask så konverterer til JSON som kan brukes av react frontend. Mulighet for å erstatte pandas med database, men for kjappe analyser har jeg valgt pandas.

På grunn av store datamengder må backend sende kun utvalg fra analysen. Det kan bli svært store HTTP-forsendelser med uheldig bruk men tar ikke høyde for det under utvikling til MVP.

## 1. Presenter statisk data
    1. Send eksempeldata i et API | dep

## 2. Presenter data fra fil
    1. Les CSV og presenter data fra den | done
    2. Send data fra CSV | done
    3. Motta start og lengde på svar | Lagt til funksjon som henter parametre start og lengde fra get-request

## 3. Presenter data fra metaanalyse
    > '/api/meta'
    1. Send statisk data | done
        * Sender en dict med metainfo
    2. Lag en funksjon som gjør analysen på data 
        * trengs for senere analyse av kolonner

## 4. Sorter DataFrame og presenter data
    > '/api/search'
    1. Enkel kolonnesortering, sorter én kolonne | done
    2. Flerkolonnesortering, mulighet til å sortere etter flere kolonner
    3. Lag en funksjon som tar høyde for andre kolonner og kolonnetyper
        * implementert backend i /api/data med bruk av parametre i get. Rekkefølgen ting sorteres i følger rekkefølgen argumentene kommer i og må følges opp i frontend.

## 5. Filtrer (søk) DataFrame og vis data
    > '/api/data'
    1. Statiske kolonnefilter, ett filter for hver kolonne
    2. Flere statiske kolonnefilter, mulighet til å legge på filtre i flere kolonner samtidig
    3. Dynamiske kolonnefiltre, filtrer i alle kolonner

## 6. Presenter data fra mesoanalyse

## 7. Presenter data fra mikroanalyse

## 8. Mulighet til å laste opp nye CSV-filer?
    1. overskriv informasjon i dataframe
    2. flere dataframe, velge mellom dataframes
    3. lagre csv-filer på server

___

# FRONTEND React
React skal presentere data for brukeren og tilby muligheten å behandle data på forskjellige måter
Dataene håndteres med tre nivå av analyser:

## Nivå 1 - Metaanalyse, beskrivelse av datasettet
Den overordnede analysen skal vise oversiktsinformasjon om datasettet.

Datasettets navn
- Kolonnenavn
    - Antall unike oppføringer i den enkelte kolonne
    - Rader uten informasjon 
    - 

## Nivå 2 - Mesoanalyse, beksrivelse av serie (kolonne)

- Seriens navn
- Antall individer i serien
- List opp unike oppføringer fra de andre seriene
    - Rader uten informasjon

## Nivå 3 - Mikroanalyse, beskrivelse av individ (rad)
Sammenhenger med andre rader

- Liste over serier
    - Antall individer som deler verdi i gitt rad
    - 
