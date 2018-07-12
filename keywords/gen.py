import xlrd
import os
import xlsxwriter
from mapping import SM, CM
import time
from Keyword import Keyword
START = time.time()

#keyword xml locations
DIRECTORY = "C:\\Users\\gf174cq\\projects\\RHG\\keywords\\keywords\\"
KEYHOTELNAME = DIRECTORY + "keyHotelName.xml"
KEYCOUNTRY = DIRECTORY + "keyCountry.xml"
KEYSTATE = DIRECTORY + "keyState.xml"
KEYCITY = DIRECTORY + "keyCity.xml"
KEYBRAND = DIRECTORY + "keyBrand.xml"
KEYROOM = DIRECTORY + "keyRoom.xml"

#file io file names
OUTPUT = 'C:\\Users\\gf174cq\\projects\\RHG\\xsd\\keywords.xlsx'

#Global variables
KEYLIST = []




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
    sc = ws.col_values(STATE_CODE_INDEX)[1:]
    cc = ws.col_values(COUNTRY_CODE_INDEX)[1:]
    id = []
    for i in range(len(sc)):
        if sc[i] == '':
            id.append('')
        else:
            id.append(sc[i]+ ' ' + cc[i])
    f = open('sn.txt', 'w')
    for code in id:
        f.write(SM[code]+'\n')
    f.close()

genCountryNames()
genStateNames()

#parse the name of the countries, states, and city to have capital first letter and lower case rest for each word
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

#load keywords from EXCEL
def load():
    wb = xlrd.open_workbook(INPUT)
    ws = wb.sheet_by_index(0)
    #hotel codes
    hc = [s.strip() for s in ws.col_values(HOTEL_CODE_INDEX)[1:]]
    #hotel names
    hn = [s.strip() for s in ws.col_values(HOTEL_NAME_INDEX)[1:]]
    for i in range(len(hn)):
        hn[i] = hn[i].replace("&", "&amp;")
    #city names
    cities = [s.strip() for s in ws.col_values(CITY_INDEX)[1:]]
    #parse the city names to correct format
    for s in range(len(cities)):
        cities[s] = parseName(cities[s])
    #state names
    states = [s.strip() for s in ws.col_values(STATE_NAME_INDEX)[1:]]
    for s in range(len(states)):
        states[s] = parseName(states[s])
    #state code
    sc = [s.strip() for s in ws.col_values(STATE_CODE_INDEX)[1:]]
    #country names
    countries = [s.strip() for s in ws.col_values(COUNTRY_NAME_INDEX)[1:]]
    for s in range(len(countries)):
        countries[s] = parseName(countries[s])
    #country code
    cc = [s.strip() for s in ws.col_values(COUNTRY_CODE_INDEX)[1:]]
    #brand names
    brand = [s.strip() for s in ws.col_values(BRAND_INDEX)[1:]]
    grt = [s.strip() for s in ws.col_values(GRT_NAME_INDEX)[1:]]
    for i in range(len(grt)):
        grt[i] = grt[i].replace("&", "&amp;")
    grtc = [s.strip() for s in ws.col_values(GRT_CODE_INDEX)[1:]]
    prt = [s.strip() for s in ws.col_values(PRT_NAME_INDEX)[1:]]
    for i in range(len(prt)):
        prt[i] = prt[i].replace("&", "&amp;")
    prtc = [s.strip() for s in ws.col_values(PRT_CODE_INDEX)[1:]]
    pair = dict(zip(["hotelCode", "hotelName", "city", "state", "stateCode", "country", "countryCode", "brand", "room", "roomCode", "prt", "prtCode"],[hc, hn, cities, states, sc, countries, cc, brand, grt ,grtc, prt, prtc]))
    return pair


#return the index of the target (tar) in the list (l)
def ind(l, tar):
    for i in range(len(l)):
        if l[i].value == tar:
            return i
    print("INDEX NOT FOUND")
    #return invalid character if not found
    return 'a'

#return true if target (tar) is in list (l)
def exist(l, tar):
    for i in l:
        if i.value == tar:
            return True
    return False


def genRoomNameTree(data):
    hc = data["hotelCode"]
    hn = data["hotelName"]
    cities = data["city"]
    states = data["state"]
    sc = data["stateCode"]
    countries = data["country"]
    cc = data["countryCode"]
    brand = data["brand"]
    rooms = data["room"]
    rc = data["roomCode"]
    prt = data["prt"]
    prtc = data["prtCode"]
    tree = []
    #country
    for i in range(len(countries)):
        if not exist(tree, countries[i]):
            k = Keyword(countries[i], countries[i], '', "Yes", 1)
            tree.append(k)

    #states
    for i in range(len(states)):
        ci = ind(tree, countries[i])
        v = states[i]+', '+countries[i]
        if states[i] != '':
            if not exist(tree[ci].children, v):
                k = Keyword(v, states[i], '', "Yes", 3)
                tree[ci].children.append(k)

    #city
    for i in range(len(cities)):
        ci = ind(tree, countries[i])
        s = states[i] + ', ' + countries[i]
        v = cities[i] + ', ' + states[i]+', '+countries[i] if states[i] != '' else cities[i] + ', ' + countries[i]
        if states[i] == '':
            if not exist(tree[ci].children,v):
                k = Keyword(v, cities[i], '', "Yes", 3)
                tree[ci].children.append(k)
        else:
            si = ind(tree[ci].children, s)
            if not exist(tree[ci].children[si].children, v):
                k = Keyword(v, cities[i], '', "Yes", 4)
                tree[ci].children[si].children.append(k)

    #hotel
    for i in range(len(hn)):
        ci = ind(tree, countries[i])
        v = cities[i] + ', ' + states[i]+', '+countries[i] if states[i] != '' else cities[i] + ', ' + countries[i]
        s = states[i] + ', ' + countries[i]
        if states[i] == '':
            cii = ind(tree[ci].children, v)
            if not exist(tree[ci].children[cii].children, hn[i]):
                k = Keyword(hn[i], hn[i], hc[i], "Yes", 4)
                tree[ci].children[cii].children.append(k)
        else:
            si = ind(tree[ci].children, s)
            cii = ind(tree[ci].children[si].children, v)
            if not exist(tree[ci].children[si].children[cii].children, hn[i]):
                k = Keyword(hn[i], hn[i], hc[i], "Yes", 5)
                tree[ci].children[si].children[cii].children.append(k)

    #rooms
    for i in range(len(rooms)):
        #country index
        ci = ind(tree, countries[i])
        #value of city
        v = cities[i] + ', ' + states[i]+', '+countries[i] if states[i] != '' else cities[i] + ', ' + countries[i]
        #value of state
        s = states[i] + ', ' + countries[i]
        if states[i] == '':
            #city index
            cii = ind(tree[ci].children, v)
            #hotel index
            hi = ind(tree[ci].children[cii].children, hn[i])
            if not exist(tree[ci].children[cii].children[hi].children, rooms[i]):
                k = Keyword(hc[i] + '-' + rooms[i], rooms[i], hc[i] + '-' + rc[i], "Yes", 5)
                tree[ci].children[cii].children[hi].children.append(k)
        else:
            si = ind(tree[ci].children, s)
            cii = ind(tree[ci].children[si].children, v)
            hi = ind(tree[ci].children[si].children[cii].children, hn[i])
            if not exist(tree[ci].children[si].children[cii].children[hi].children, rooms[i]):
                k = Keyword(hc[i] + '-' + rooms[i], rooms[i], hc[i] + '-' + rc[i], "Yes", 6)
                tree[ci].children[si].children[cii].children[hi].children.append(k)

    for i in range(len(rooms)):
        #country index
        ci = ind(tree, countries[i])
        #value of city
        v = cities[i] + ', ' + states[i]+', '+countries[i] if states[i] != '' else cities[i] + ', ' + countries[i]
        #value of state
        s = states[i] + ', ' + countries[i]
        if states[i] == '':
            #city index
            cii = ind(tree[ci].children, v)
            #hotel index
            hi = ind(tree[ci].children[cii].children, hn[i])
            #room index
            ri = ind(tree[ci].children[cii].children[hi].children, hc[i] + '-' + rooms[i])
            if not exist(tree[ci].children[cii].children[hi].children[ri].children, prt[i]):
                k = Keyword(hc[i] + '-' + prt[i], prt[i], hc[i] + '-' + prtc[i], "No", 6)
                tree[ci].children[cii].children[hi].children[ri].children.append(k)
        else:
            si = ind(tree[ci].children, s)
            cii = ind(tree[ci].children[si].children, v)
            hi = ind(tree[ci].children[si].children[cii].children, hn[i])
            ri = ind(tree[ci].children[si].children[cii].children[hi].children, hc[i] + '-' + rooms[i])
            if not exist(tree[ci].children[si].children[cii].children[hi].children[ri].children, prt[i]):
                k = Keyword(hc[i] + '-' + prt[i], prt[i], hc[i] + '-' + rc[i], "No", 7)
                tree[ci].children[si].children[cii].children[hi].children[ri].children.append(k)
    return tree



def genHotelNameTree(data):
    wb = xlsxwriter.Workbook(OUTPUT)
    worksheet = wb.add_worksheet()
    worksheet.set_column('A:A', 20)
    worksheet.set_column('B:B', 30)
    worksheet.set_column('C:C', 40)
    worksheet.set_column('D:D', 10)
    worksheet.set_column('E:E', 50)
    worksheet.set_column('F:F', 50)
    hc = data["hotelCode"]
    hn = data["hotelName"]
    cities = data["city"]
    states = data["state"]
    sc = data["stateCode"]
    countries = data["country"]
    cc = data["countryCode"]
    brand = data["brand"]
    rooms = data["room"]
    tree = []
    worksheet.write(0,0, "Countries")
    counter = 1
    for i in range(len(countries)):
        if not exist(tree, countries[i]):
            k = Keyword(countries[i], countries[i], '', "Yes", 1)
            tree.append(k)
            KEYLIST.append(k)
            worksheet.write(counter, 0, countries[i])
            counter += 1
    counter = 1
    worksheet.write(0,1,"States")
    for i in range(len(states)):
        ci = ind(tree, countries[i])
        v = states[i]+', '+countries[i]
        if states[i] != '':
            if not exist(tree[ci].children, v):
                k = Keyword(v, states[i], '', "Yes", 3)
                worksheet.write(counter, 1, v)
                tree[ci].children.append(k)
                KEYLIST.append(k)
                counter += 1

    #city
    counter = 1
    worksheet.write(0,2,"Cities")
    for i in range(len(cities)):
        ci = ind(tree, countries[i])
        s = states[i] + ', ' + countries[i]
        v = cities[i] + ', ' + states[i]+', '+countries[i] if states[i] != '' else cities[i] + ', ' + countries[i]
        if states[i] == '':
            if not exist(tree[ci].children,v):
                k = Keyword(v, cities[i], '', "Yes", 3)
                worksheet.write(counter, 2, v)
                counter += 1
                tree[ci].children.append(k)
                KEYLIST.append(k)
        else:
            si = ind(tree[ci].children, s)
            if not exist(tree[ci].children[si].children, v):
                k = Keyword(v, cities[i], '', "Yes", 4)
                tree[ci].children[si].children.append(k)
                KEYLIST.append(k)
                worksheet.write(counter, 2, v)
                counter += 1

    worksheet.write(0,3,"Brand")
    brand = list(set(brand))
    for i in range(len(brand)):
        worksheet.write(i+1, 3, brand[i])

    counter = 1
    worksheet.write(0,4,"Hotel Name")
    for i in range(len(hn)):
        ci = ind(tree, countries[i])
        v = cities[i] + ', ' + states[i]+', '+countries[i] if states[i] != '' else cities[i] + ', ' + countries[i]
        s = states[i] + ', ' + countries[i]
        if states[i] == '':
            cii = ind(tree[ci].children, v)
            if not exist(tree[ci].children[cii].children, hn[i]):
                k = Keyword(hn[i], hn[i], hc[i], "No", 4, None, True)
                tree[ci].children[cii].children.append(k)
                KEYLIST.append(k)
                worksheet.write(counter, 4, hn[i])
                counter += 1
        else:
            si = ind(tree[ci].children, s)
            cii = ind(tree[ci].children[si].children, v)
            if not exist(tree[ci].children[si].children[cii].children, hn[i]):
                k = Keyword(hn[i], hn[i], hc[i], "No", 5, None, True)
                tree[ci].children[si].children[cii].children.append(k)
                KEYLIST.append(k)
                worksheet.write(counter, 4, hn[i])
                counter += 1
    worksheet.write(0,5, "Room Name")
    l = rooms
    l = list(set(l))
    for i in range(len(l)):
        worksheet.write(i+1, 5, l[i])
    wb.close()
    return tree

def parseKeyFrom(s):
    s = ''.join(i for i in s if i!='\'')
    l = []
    w = ""
    for i in s:
        if i not in ' ,':
            w += i
        else:
            l.append(w)
            w = ""
    l.append(w)
    return '-'.join([t.strip().lower() for t in l if t != ""])

def genCityTree(data):
    cities = data["city"]
    states = data["state"]
    sc = data["stateCode"]
    countries = data["country"]
    cc = data["countryCode"]
    tree = []
    for i in range(len(countries)):
        if not exist(tree, countries[i]):
            k = Keyword(countries[i], countries[i], parseKeyFrom(countries[i]), "Yes", 1)
            tree.append(k)
    for i in range(len(states)):
        ci = ind(tree, countries[i])
        v = states[i]+', '+countries[i]
        if states[i] != '':
            if not exist(tree[ci].children, v):
                k = Keyword(v, states[i], parseKeyFrom(states[i] + ' ' + cc[i]), "Yes", 3)
                tree[ci].children.append(k)
    for i in range(len(cities)):
        ci = ind(tree, countries[i])
        s = states[i] + ', ' + countries[i]
        v = cities[i] + ', ' + states[i]+', '+countries[i] if states[i] != '' else cities[i] + ', ' + countries[i]
        if states[i] == '':
            if not exist(tree[ci].children,v):
                k = Keyword(v, cities[i], parseKeyFrom(cities[i] + ' ' + sc[i] + ' ' + cc[i]), "No", 3)
                tree[ci].children.append(k)
        else:
            si = ind(tree[ci].children, s)
            if not exist(tree[ci].children[si].children, v):
                k = Keyword(v, cities[i], parseKeyFrom(cities[i] + ' ' + sc[i] + ' ' + cc[i]), "No", 4)
                tree[ci].children[si].children.append(k)
    return tree

def genStateTree(data):
    states = data["state"]
    sc = data["stateCode"]
    countries = data["country"]
    cc = data["countryCode"]
    tree = []
    for i in range(len(countries)):
        if not exist(tree, countries[i]):
            k = Keyword(countries[i], countries[i], cc[i].upper(), "Yes", 1)
            tree.append(k)
    for i in range(len(states)):
        ci = ind(tree, countries[i])
        v = states[i]+', '+countries[i]
        if states[i] != '':
            if not exist(tree[ci].children, v):
                k = Keyword(v, states[i], sc[i].upper(), "No", 3)
                tree[ci].children.append(k)
    return tree

def genCountryTree(data):
    countries = data["country"]
    cc = data["countryCode"]
    tree = []
    for i in range(len(countries)):
        if not exist(tree, countries[i]):
            k = Keyword(countries[i], countries[i], cc[i].upper(), "No", 1)
            tree.append(k)
    return tree

def genBrandTree(data):
    brands = data["brand"]
    tree = []
    for i in range(len(brands)):
        if not exist(tree, brands[i]):
            k = Keyword(brands[i], brands[i], brands[i], "No", 1)
            tree.append(k)
    return tree


def validation(l):
    dups = []
    for i in range(len(l)):
        for j in range(i+1, len(l)):
            if l[i].value == l[j].value:
                dups.append(l[i])
                print(l[i].value)
    return dups

def genHeader(s):
    return "<?xml version=\"1.0\" encoding = \"utf-8\"?>\n<Category name = \"" + s + "\" xmlName = \"" + s + "\" isPublishable = \"Yes\">\n"

def genFooter():
    return "</Category>\n"

def genHotelName(data):
    tree = genHotelNameTree(data)
    header = genHeader("Hotel")
    content = ""
    for i in tree:
        content += str(i)
    footer = genFooter()
    output = header + content + footer
    f = open(KEYHOTELNAME, 'w')
    f.write(output)
    f.close()


def genCity(data):
    tree = genCityTree(data)
    header = genHeader("City")
    content = ""
    for i in tree:
        content += str(i)
    footer = genFooter()
    output = header + content + footer
    f = open(KEYCITY, 'w')
    f.write(output)
    f.close()


def genState(data):
    tree = genStateTree(data)
    header = genHeader("State")
    content = ""
    for i in tree:
        content += str(i)
    footer = genFooter()
    output = header + content + footer
    f = open(KEYSTATE, 'w')
    f.write(output)
    f.close()

def genCountry(data):
    tree = genCountryTree(data)
    header = genHeader("Country")
    content = ""
    for i in tree:
        content += str(i)
    footer = genFooter()
    output = header + content + footer
    f = open(KEYCOUNTRY, 'w')
    f.write(output)
    f.close()

def genBrand(data):
    tree = genBrandTree(data)
    header = genHeader("Brand")
    content = ""
    for i in tree:
        content += str(i)
    footer = genFooter()
    output = header + content + footer
    f = open(KEYBRAND, 'w')
    f.write(output)
    f.close()

def genRoom(data):
    tree = genRoomNameTree(data)
    header = genHeader("Room")
    content = ""
    for i in tree:
        content += str(i)
    footer = genFooter()
    output = header + content + footer
    f = open(KEYROOM, 'w')
    f.write(output)
    f.close()

def gen():
    data = load()
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)
    genHotelName(data)
    genCity(data)
    genState(data)
    genCountry(data)
    genBrand(data)
    genRoom(data)

gen()

print("\n-------------%s seconds ----------------" % (time.time()-START))



