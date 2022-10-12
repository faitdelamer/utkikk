import pandas as pd
import json
from flask import Flask, redirect, url_for, request
from flask_cors import CORS


app = Flask(__name__, static_folder="..\\build", static_url_path="/") # hvorfor static_url_path ?
CORS(app, resources={r"/api/*": {"origins": "*"}})

pdTyper = {"int64": "int", "object": "str", "float64": "float", "bool": "bool"}

data = pd.read_csv('..\\45784.csv')
data = data.rename(columns={'seq': 'id', 'name/first': 'namefirst', 'name/last': 'namelast'}) #for enklere håndtering mellom front og backend

kolonner = [col for col in data]

sok_kolonne = [col for col in data if data[col].dtype == "object"]

def unike(dataframe, column):
    # hent ut unike tilfeller av en pandas.series
    # returnerer en liste over unike tilfeller
    # df.nunique() gjør nesten samme? .index[i] = key, .values[i] = verdi
    unik = dataframe[column].unique()
    unik = unik.tolist()
    unik.sort() #denne er mulig unødvendig, undersøk med frontend
    return unik

def hent_meta(dataFrame, dictionary:dict): 
    # funksjon som legger en nested dict for metainformasjon til en eksisterende dict
    # format {kolonne: {kolonne: antall}} 
    for column in dataFrame:
        serie = dataFrame[column]
        dataType = pdTyper[str(serie.dtype)]
        antallUnike = len(unike(dataFrame, column))
        antall = len(serie)
        hyppighet = {"antall": int(serie.value_counts().iloc[0])}
        if antallUnike/antall > 0.99: #dersom mer enn 99% er unike verdier
            hyppighet["hyppigst"] = "for mange unike verdier"
            hyppighet["antall"] = "N/A"
        else:
            hyppighet["hyppigst"] = str(serie.value_counts().index[0])
        if serie.dtype == "int64":
            minimum = int(serie.min())
            maksimum = int(serie.max())
            snitt = int(serie.mean())
        elif serie.dtype == "float64":
            minimum = float(serie.min())
            maksimum = float(serie.max())
            snitt = float(serie.mean())
        elif serie.dtype == "object":
            minimum = serie.min()
            maksimum = serie.max()
            snitt = "N/A"
        else:
            minimim = "N/A"
            maksimum = "N/A"
            snitt = "N/A"
        
        info = {
            "antall-verdier": antall,
            "antall-unike": antallUnike,
            "type": dataType,
            "min-verdi": minimum,
            "maks-verdi": maksimum,
            "gjennomsnitt": snitt,
            "flest-antall": hyppighet
        }
        dictionary[column] = info

def frame_sider(dataFrame, lengde):
    #funksjon returnerer antall sider som skal genereres ut fra lengde på listen
    antSider = ((len(dataFrame)-1) // lengde)+1
    if antSider < 1:
        antSider = 1
    return antSider

def frame_slice(dataFrame, side, lengde):
    # returnerer utvalg av en dataFrame for behandling av frontend
    dataLengde = len(dataFrame)
    if (side-1)*lengde >= dataLengde: #hvis sidetall er utenfor tabellen
        side = dataLengde // lengde
    if side < 1: #hvis sidetall er mindre enn tabellen, vis side 1
        side = 1
    start = (side-1)*lengde
    return dataFrame[start:start+lengde]

def send_soek(data, sokeStreng):
    #Funksjon som søker i fastsatte kolonner, tenkt utvidet til dynamisk flersøk men usikker på hvordan det skal foregå. ny dataframe hvor alle kolonnene er tekst? Søker ikke i alder...
    #mye hjelp fra https://stackoverflow.com/questions/36266390/how-to-query-pandas-dataframe-using-a-specific-value?noredirect=1&lq=1
    return data[data.namefirst.str.contains(sokeStreng, case=False) | data.namelast.str.contains(sokeStreng, case=False) | data.city.str.contains(sokeStreng) | data.street.str.contains(sokeStreng, case=False) | data.state.str.contains(sokeStreng, case=False)]
    #vei som ikke ble fulgt men trolig er fruktbar: //https://stackoverflow.com/questions/26640129/search-for-string-in-all-pandas-dataframe-columns-and-filter

@app.route('/')
def index():
    return app.send_static_file('index.html') #forwarder ???

@app.route('/api/eksempel')
def giEksempel():
    #sender to JSON objekter, index 0 er data og index 1 er info
    start = 0
    lengde = 40
    return data[start:start+lengde].to_json(orient='records')#, {"results": {len(data)}}

@app.route('/api/meta') 
def giMeta():
    # Sender data om unike verdier i kolonner
    #if not request.values.get('column'):
    #    print('verdi felt!')
    dataInfo = {}
    hent_meta(data, dataInfo)
    return dataInfo #, request.values.get('column')

@app.route('/api/search')
def utforSok():
    #søkefunksjon for flere statiske kolonner
    if request.values.get('sok'):
        sokeStreng = request.values.get('sok')
    else:
        sokeStreng = "ma"
    sokTreff = send_soek(data, sokeStreng)
    return sokTreff[0:10].to_json(orient='records')+f'["searchphrase":"{sokeStreng}", "antall_treff": {len(sokTreff)}]'

@app.route('/api/data')
def giData():
    '''
    Dette er hoved-API for bruk i tabell-spørringer.
    *find* brukes for å søke i kolonnene name/first, name/last, city, street og state.
    *size* brukes for å bestemme tabellstørrelse, *curPage* brukes for å beregne hvilken index data hentes fra.
    *sort* brukes til å sortere etter kolonner, og *order* brukes for å velge stigende eller synkende.
    '''
    #hovedfunksjon, presenterer data. Skill ut funksjonen i en mer generell sak <--

    # filter, filtrer datatable i forkant av søk. Hvordan velge flere kolonner? for-loop? dict for å matche kolonne og søkeparameter?

    # søk, justerer datafeltet før det sendes til paginering
    phrase = ""
    if request.values.get('find'):
        phrase = request.values.get('find')
    soktData = send_soek(data, phrase) #utvalg i dataframe

    # paginering, hvordan beregne responsen
    if not request.values.get('size'):
        tabellLengde = 10
    else: 
        tabellLengde = int(request.values.get('size'))
        if tabellLengde > 100: #maksbegrensning for å unngå for store HTTP-forsendelser
            tabellLengde = 100
    if not request.values.get('side'):
        side = 1
    else:
        side = int(request.values.get('side'))
    tabellSide = frame_sider(soktData, tabellLengde) # Antall sider i datasettet
    if tabellSide < side:
        side = tabellSide
    #metadata om query / tabell for bruk av frontend
    tabellInfo = {"totalResults": len(soktData), "totalPages": tabellSide, "currentPage": side} #hvilken info må med?

    # sort & slice, sorter og velg ut slice fra frame. flere sorteringsmuligheter ikke kodet inn fra frontend
    sort = request.args.getlist('sort')
    if sort:
        if not sort[0]:
            sort = []
        for i, col in enumerate(sort):
            if not col in kolonner:
                sort.pop(i)
                if not sort:
                    sort = []
                    break
                
    order = request.args.getlist('order')
    if order and order[0] != "": # and len(order) > 0:
        #denne er sårbar for å motta andre ting enn ints. Forsøkt løst med try/except men det funka ikke så bra
        order = [int(i) for i in list(order)]
    else:
        order = []

    #logikk for å matche lengden på sort og order
    if len(sort) != len(order):
        if len(sort) > len(order):
            for i in range(len(sort)-len(order)):
                order.append(1)
        else:
            order = order[:len(order)-(len(order)-len(sort))] 
            # rekkefølgen av sortering kommer enten fra frontend ved å sende order i revers, eventuelt så kan dette gjøres med 

    #håndter sort
    if len(sort) > 0:
        sortData = soktData.sort_values(sort, ascending=order)
    else:
        sortData = soktData
    
    #håndter slice
    utsnitt = frame_slice(sortData, side, tabellLengde)

    # send info, gi json-data for tabellinnhold (data) samt json-data for tabell-metadata (tabelldata)
    svar = utsnitt.to_json(orient='records')
    svar = '{"data": ['+svar[1:-1]+'], "info": '+json.dumps(tabellInfo)+'}'

    return svar 

@app.route('/test')
def testData():
    if request.args:
        sort = request.args.getlist('sort') 
        order = [int(i) for i in list(request.values.get('order'))] #order må være heltall, 1= True, 0= False
        
        if not len(sort) == len(order):
            if len(sort) > len(order):
                for i in range(len(sort)-len(order)):
                    order.append(1)
            else:
                order = order[:len(order)-(len(order)-len(sort))]

        # sortType = [int(i) for i in sortType]
        ex_data = data.sort_values(sort, ascending=order)
        return ex_data[0:10].T.to_dict()
    else:
        return "Hello world!"