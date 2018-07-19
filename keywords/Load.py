import xlrd

def parseName(s):
    s = s.strip()
    l = s.split(' ')
    #delete empty words and lists
    l = [s for s in l if s!='']
    l = [t[0].upper() + t[1:].lower() for t in l]
    #finally join the correctly parsed word list into a single word
    return ' '.join(l)

def stateMap():
    wb = xlrd.open_workbook('state-code-name.xls')
    ws  = wb.sheet_by_index(0)

    #sc = state code, cc = country code, sn = state name
    cc = ws.col_values(0)[1:]
    sc = ws.col_values(1)[1:]
    sn = [parseName(s) for s in ws.col_values(2)[1:]]

    id = [sc[i] + ' ' + cc[i] for i in range(len(sc))]
    #create empty mapping
    id.append('')
    sn.append('')
    map = dict(zip(id, sn))
    return map

def countryMap():
    wb = xlrd.open_workbook('country-code-name.xls')
    ws = wb.sheet_by_index(0)

    #cc = country code, cn = country name
    cc = ws.col_values(0)[1:]
    cn = [parseName(s) for s in ws.col_values(1)[1:]]

    map = dict(zip(cc, cn))
    return map

#state map and country map
SM = stateMap()
CM = countryMap()

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



def special_characters(n, ls):
    l = []
    for s in range(len(ls)):
        for i in ls[s]:
            if (not i.isalnum()) and i != ' ':
                l.append(i)
    l = list(set(l))
    l = ''.join(l)
    f = open('specialChars.txt','a')
    f.write(n + " special characters are: \n")
    f.write(str(l)+'\n\n')
    f.close()


def load():
    wb = xlrd.open_workbook(INPUT)
    ws = wb.sheet_by_index(0)
    #hotel codes
    hc = [s.strip() for s in ws.col_values(HOTEL_CODE_INDEX)[1:]]
    #hotel names
    hn = [s.strip() for s in ws.col_values(HOTEL_NAME_INDEX)[1:]]
    l = []
    for s in range(len(hn)):
        hn[s] = hn[s].replace("&", "&amp;")
    #city names
    cities = [s.strip() for s in ws.col_values(CITY_INDEX)[1:]]
    #state names
    states = [s.strip() for s in ws.col_values(STATE_NAME_INDEX)[1:]]
    #state code
    sc = [s.strip() for s in ws.col_values(STATE_CODE_INDEX)[1:]]
    #country names
    countries = [s.strip() for s in ws.col_values(COUNTRY_NAME_INDEX)[1:]]
    #country code
    cc = [s.strip() for s in ws.col_values(COUNTRY_CODE_INDEX)[1:]]
    #brand names
    brand = [s.strip() for s in ws.col_values(BRAND_INDEX)[1:]]
    #general room names
    grt = [s.strip() for s in ws.col_values(GRT_NAME_INDEX)[1:]]
    #grt codes
    grtc = [s.strip() for s in ws.col_values(GRT_CODE_INDEX)[1:]]
    #physical room names
    prt = [s.strip() for s in ws.col_values(PRT_NAME_INDEX)[1:]]
    #prtcode
    prtc = [s.strip() for s in ws.col_values(PRT_CODE_INDEX)[1:]]
    #dictionary
    mapping = dict(zip(["hotelCode", "hotelName", "city", "state", "stateCode", "country", "countryCode", "brand", "room", "roomCode", "prt", "prtCode"],[hc, hn, cities, states, sc, countries, cc, brand, grt ,grtc, prt, prtc]))
    return mapping




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



def strDigit(i):
    i = i%1000
    if len(str(i)) == 1:
        return "00" + str(i)
    elif len(str(i)) == 2:
        return "0" + str(i)
    else:
        return str(i)

def genNum(l):
    nums = [0]
    counter = 0
    for i in range(1,len(l)):
        if l[i] != l[i-1]:
            counter += 1
        nums.append(counter)
    return nums

#index of excel fields:
INPUT = 'hotelCode-GRT-PRT.xls'
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
DATA = load()
hotelCodes = DATA["hotelCode"]
hotelNames = DATA["hotelName"]
hotelNumbers = genNum(hotelNames)
cities = DATA["city"]
stateNames = DATA["state"]
stateCodes = DATA["stateCode"]
countryNames = DATA["country"]
countryCodes = DATA["countryCode"]
companyName = ["Radisson Hotel Group" for s in range(len(hotelCodes))]
digitCode = ["000" for i in range(len(hotelCodes))]
brands = DATA["brand"]
grt = DATA["room"]
grtCode = DATA["roomCode"]
prt = DATA["prt"]
prtCode = DATA["prtCode"]
DIRECTORY = "C:\\Users\\gf174cq\\projects\\RHG\\keywords\\keywords\\"
KEYHOTELNAME = DIRECTORY + "keyHotelName.xml"
KEYCOUNTRY = DIRECTORY + "keyCountry.xml"
KEYSTATE = DIRECTORY + "keyState.xml"
KEYCITY = DIRECTORY + "keyCity.xml"
KEYBRAND = DIRECTORY + "keyBrand.xml"
KEYROOM = DIRECTORY + "keyRoom.xml"
KEYNAV = DIRECTORY + "keyNav.xml"
OUTPUT = 'C:\\Users\\gf174cq\\projects\\RHG\\xsd\\keywordTest.xlsx'
LEN = len(hotelCodes) #length of all lists

