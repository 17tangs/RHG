import xlrd 
from mapping import SM, CM
INPUT = 'hotelCode-GRT-PRT.xls'


def parseName(s):
    s = s.strip()
    l = []
    st = ""
    for i in s:
        #deliminters to separate words
        if i not in ":;[]{}|><?,/.!@#$%^&*() ":
            st += i
        else:
            l.append(st)
            st = ""
    if st != "":
        l.append(st)
    #delete empty words and lists
    l = [s for s in l if s!='']
    l = [t[0].upper() + t[1:].lower() for t in l]
    #finally join the correctly parsed word list into a single word
    return ' '.join(l)
def indices():
    wb = xlrd.open_workbook(INPUT)
    ws = wb.sheet_by_index(0)
    headers = [''.join(s.lower().strip().split(' ')) for s in ws.row_values(0)]
    IHC = headers.index("hotelcode")
    IHN = headers.index("hotelname")
    ICI = headers.index("city")
    ICO = headers.index("country")
    IST = headers.index("state")
    ISN = headers.index("statename")
    ICN = headers.index("countryname")
    IBD = headers.index("brand")
    IGD = headers.index("grtdescription")
    IGC = headers.index("grtcode")
    IPD = headers.index("prtdescription")
    IPC = headers.index("prtcode")
    return [IHC, IHN, ICI, ICO, IST, ISN, ICN, IBD, IGD, IGC, IPD, IPC]

#index of excel fields:
I = indices()
HOTEL_CODE_INDEX = I[0]
HOTEL_NAME_INDEX = I[1]
CITY_INDEX = I[2]
COUNTRY_CODE_INDEX = I[3]
STATE_CODE_INDEX = I[4]
STATE_NAME_INDEX = I[5]
COUNTRY_NAME_INDEX = I[6]
BRAND_INDEX = I[7]
GRT_NAME_INDEX = I[8]
GRT_CODE_INDEX = I[9]
PRT_NAME_INDEX = I[10]
PRT_CODE_INDEX = I[11]


def special_characters(n, ls):
    l = []
    for s in range(len(ls)):
        for i in ls[s]:
            if (not i.isalnum()) and i != ' ':
                l.append(i)
    l = list(set(l))
    l = ''.join(l)
    print(n + " special characters are: ")
    print(l)
    print('')


def load():
    wb = xlrd.open_workbook(INPUT)
    ws = wb.sheet_by_index(0)
    #hotel codes
    hc = [s.strip() for s in ws.col_values(HOTEL_CODE_INDEX)[1:]]
    #hotel names
    hn = [s.strip() for s in ws.col_values(HOTEL_NAME_INDEX)[1:]]
    special_characters("hotel", hn)
    l = []
    for s in range(len(hn)):
        hn[s] = hn[s].replace("&", "&amp;")
    #city names
    cities = [s.strip() for s in ws.col_values(CITY_INDEX)[1:]]
    special_characters("cities", cities)
    #parse the city names to correct format
    for s in range(len(cities)):
        cities[s] = parseName(cities[s])
    #state names
    states = [s.strip() for s in ws.col_values(STATE_NAME_INDEX)[1:]]
    special_characters("states", states)
    for s in range(len(states)):
        states[s] = parseName(states[s])
    #state code
    sc = [s.strip() for s in ws.col_values(STATE_CODE_INDEX)[1:]]
    #country names
    countries = [s.strip() for s in ws.col_values(COUNTRY_NAME_INDEX)[1:]]
    special_characters("countries", countries)
    for s in range(len(countries)):
        countries[s] = parseName(countries[s])
    #country code
    cc = [s.strip() for s in ws.col_values(COUNTRY_CODE_INDEX)[1:]]
    #brand names
    brand = [s.strip() for s in ws.col_values(BRAND_INDEX)[1:]]
    grt = [s.strip() for s in ws.col_values(GRT_NAME_INDEX)[1:]]
    special_characters("grt", grt)
    for s in range(len(grt)):
        grt[s] = grt[s].replace("&", "&amp;")
    grtc = [s.strip() for s in ws.col_values(GRT_CODE_INDEX)[1:]]
    prt = [s.strip() for s in ws.col_values(PRT_NAME_INDEX)[1:]]
    special_characters("prt", prt)
    for i in range(len(prt)):
        prt[i] = prt[i].replace("&", "&amp;")
    prtc = [s.strip() for s in ws.col_values(PRT_CODE_INDEX)[1:]]
    pair = dict(zip(["hotelCode", "hotelName", "city", "state", "stateCode", "country", "countryCode", "brand", "room", "roomCode", "prt", "prtCode"],[hc, hn, cities, states, sc, countries, cc, brand, grt ,grtc, prt, prtc]))
    return pair

data = load()
hotelCodes = data["hotelCode"]
hotelNames = data["hotelName"]
cities = data["city"]
stateNames = data["state"]
stateCodes = data["stateCode"]
countryNames = data["country"]
countryCodes = data["countryCode"]
brands = data["brand"]
grt = data["room"]
grtCode = data["roomCode"]
prt = data["prt"]
prtCode = data["prtCode"]



def genCountryNames():
    wb = xlrd.open_workbook(INPUT)
    ws = wb.sheet_by_index(0)
    cn = ws.col_values(COUNTRY_CODE_INDEX)[1:]
    f = open('cn.txt', 'w')
    for code in cn:
        f.write(CM[code]+'\n')
    f.close()

def genStateNames():
    wb = xlrd.open_workbook(INPUT)
    ws = wb.sheet_by_index(0)
    stateCodes = ws.col_values(STATE_CODE_INDEX)[1:]
    countryCodes = ws.col_values(COUNTRY_CODE_INDEX)[1:]
    id = []
    for i in range(len(stateCodes)):
        if stateCodes[i] == '':
            id.append('')
        else:
            id.append(stateCodes[i]+ ' ' + countryCodes[i])
    f = open('sn.txt', 'w')
    for code in id:
        f.write(SM[code]+'\n')
    f.close()


