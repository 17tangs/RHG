import xlrd
import os
import xlsxwriter
import time
from Keyword import Keyword
from Load import * #hotelCodes, hotelNames, cities, stateNames, stateCodes, countryNames, countryCodes, brands, grt, grtCode, prt, prtCode, INPUT, COUNTRY_CODE_INDEX, STATE_CODE_INDEX

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
LEN = len(hotelCodes)



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


def genRoomNameTree():
    tree = []
    #country
    for i in range(len(countryNames)):
        if not exist(tree, countryNames[i]):
            k = Keyword(countryNames[i], countryNames[i], '', "Yes", 1)
            tree.append(k)

    #states
    for i in range(len(stateNames)):
        ci = ind(tree, countryNames[i])
        v = stateNames[i]+', '+countryNames[i]
        if stateNames[i] != '':
            if not exist(tree[ci].children, v):
                k = Keyword(v, stateNames[i], '', "Yes", 3)
                tree[ci].children.append(k)

    #city
    for i in range(len(cities)):
        ci = ind(tree, countryNames[i])
        s = stateNames[i] + ', ' + countryNames[i]
        v = cities[i] + ', ' + stateNames[i]+', '+countryNames[i] if stateNames[i] != '' else cities[i] + ', ' + countryNames[i]
        if stateNames[i] == '':
            if not exist(tree[ci].children,v):
                k = Keyword(v, cities[i], '', "Yes", 3)
                tree[ci].children.append(k)
        else:
            si = ind(tree[ci].children, s)
            if not exist(tree[ci].children[si].children, v):
                k = Keyword(v, cities[i], '', "Yes", 4)
                tree[ci].children[si].children.append(k)

    #hotel
    for i in range(len(hotelNames)):
        ci = ind(tree, countryNames[i])
        v = cities[i] + ', ' + stateNames[i]+', '+countryNames[i] if stateNames[i] != '' else cities[i] + ', ' + countryNames[i]
        s = stateNames[i] + ', ' + countryNames[i]
        if stateNames[i] == '':
            cii = ind(tree[ci].children, v)
            if not exist(tree[ci].children[cii].children, hotelNames[i]):
                k = Keyword(hotelNames[i], hotelNames[i], hotelCodes[i], "Yes", 4)
                tree[ci].children[cii].children.append(k)
        else:
            si = ind(tree[ci].children, s)
            cii = ind(tree[ci].children[si].children, v)
            if not exist(tree[ci].children[si].children[cii].children, hotelNames[i]):
                k = Keyword(hotelNames[i], hotelNames[i], hotelCodes[i], "Yes", 5)
                tree[ci].children[si].children[cii].children.append(k)

    #rooms
    for i in range(len(grt)):
        #country index
        ci = ind(tree, countryNames[i])
        #value of city
        v = cities[i] + ', ' + stateNames[i]+', '+countryNames[i] if stateNames[i] != '' else cities[i] + ', ' + countryNames[i]
        #value of state
        s = stateNames[i] + ', ' + countryNames[i]
        if stateNames[i] == '':
            #city index
            cii = ind(tree[ci].children, v)
            #hotel index
            hi = ind(tree[ci].children[cii].children, hotelNames[i])
            if not exist(tree[ci].children[cii].children[hi].children, grt[i]):
                k = Keyword(hotelCodes[i] + '-' + grt[i], grt[i], hotelCodes[i] + '-' + grtCode[i], "Yes", 5)
                tree[ci].children[cii].children[hi].children.append(k)
        else:
            si = ind(tree[ci].children, s)
            cii = ind(tree[ci].children[si].children, v)
            hi = ind(tree[ci].children[si].children[cii].children, hotelNames[i])
            if not exist(tree[ci].children[si].children[cii].children[hi].children, grt[i]):
                k = Keyword(hotelCodes[i] + '-' + grt[i], grt[i], hotelCodes[i] + '-' + grtCode[i], "Yes", 6)
                tree[ci].children[si].children[cii].children[hi].children.append(k)

    for i in range(len(grt)):
        #country index
        ci = ind(tree, countryNames[i])
        #value of city
        v = cities[i] + ', ' + stateNames[i]+', '+countryNames[i] if stateNames[i] != '' else cities[i] + ', ' + countryNames[i]
        #value of state
        s = stateNames[i] + ', ' + countryNames[i]
        if stateNames[i] == '':
            #city index
            cii = ind(tree[ci].children, v)
            #hotel index
            hi = ind(tree[ci].children[cii].children, hotelNames[i])
            #room index
            ri = ind(tree[ci].children[cii].children[hi].children, hotelCodes[i] + '-' + grt[i])
            if not exist(tree[ci].children[cii].children[hi].children[ri].children, prt[i]):
                v = hotelCodes[i] + '-' + grt[i] if prt[i] == '' else hotelCodes[i] + '-' + prt[i]
                k = Keyword(v, prt[i], hotelCodes[i] + '-' + prtCode[i], "No", 6)
                tree[ci].children[cii].children[hi].children[ri].children.append(k)
        else:
            si = ind(tree[ci].children, s)
            cii = ind(tree[ci].children[si].children, v)
            hi = ind(tree[ci].children[si].children[cii].children, hotelNames[i])
            ri = ind(tree[ci].children[si].children[cii].children[hi].children, hotelCodes[i] + '-' + grt[i])
            if not exist(tree[ci].children[si].children[cii].children[hi].children[ri].children, prt[i]):
                v = hotelCodes[i] + '-' + grt[i] if prt[i] == '' else hotelCodes[i] + '-' + prt[i]
                k = Keyword(v, prt[i], hotelCodes[i] + '-' + prtCode[i], "No", 7)
                tree[ci].children[si].children[cii].children[hi].children[ri].children.append(k)
    return tree



def genHotelNameTree():
    wb = xlsxwriter.Workbook(OUTPUT)
    worksheet = wb.add_worksheet()
    worksheet.set_column('A:A', 20)
    worksheet.set_column('B:B', 30)
    worksheet.set_column('C:C', 40)
    worksheet.set_column('D:D', 10)
    worksheet.set_column('E:E', 50)
    worksheet.set_column('F:F', 50)
    tree = []
    worksheet.write(0,0, "CountryNames")
    counter = 1
    for i in range(len(countryNames)):
        if not exist(tree, countryNames[i]):
            k = Keyword(countryNames[i], countryNames[i], '', "Yes", 1)
            tree.append(k)
            KEYLIST.append(k)
            worksheet.write(counter, 0, countryNames[i])
            counter += 1
    counter = 1
    worksheet.write(0,1,"StateNames")
    for i in range(len(stateNames)):
        ci = ind(tree, countryNames[i])
        v = stateNames[i]+', '+countryNames[i]
        if stateNames[i] != '':
            if not exist(tree[ci].children, v):
                k = Keyword(v, stateNames[i], '', "Yes", 3)
                worksheet.write(counter, 1, v)
                tree[ci].children.append(k)
                KEYLIST.append(k)
                counter += 1

    #city
    counter = 1
    worksheet.write(0,2,"Cities")
    for i in range(len(cities)):
        ci = ind(tree, countryNames[i])
        s = stateNames[i] + ', ' + countryNames[i]
        v = cities[i] + ', ' + stateNames[i]+', '+countryNames[i] if stateNames[i] != '' else cities[i] + ', ' + countryNames[i]
        if stateNames[i] == '':
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

    worksheet.write(0,3,"Brands")
    b = list(set(brands))
    for i in range(len(b)):
        worksheet.write(i+1, 3, b[i])

    counter = 1
    worksheet.write(0,4,"Hotel Name")
    for i in range(len(hotelNames)):
        ci = ind(tree, countryNames[i])
        v = cities[i] + ', ' + stateNames[i]+', '+countryNames[i] if stateNames[i] != '' else cities[i] + ', ' + countryNames[i]
        s = stateNames[i] + ', ' + countryNames[i]
        if stateNames[i] == '':
            cii = ind(tree[ci].children, v)
            if not exist(tree[ci].children[cii].children, hotelNames[i]):
                k = Keyword(hotelNames[i], hotelNames[i], hotelCodes[i], "No", 4, None, True)
                tree[ci].children[cii].children.append(k)
                KEYLIST.append(k)
                worksheet.write(counter, 4, hotelNames[i])
                counter += 1
        else:
            si = ind(tree[ci].children, s)
            cii = ind(tree[ci].children[si].children, v)
            if not exist(tree[ci].children[si].children[cii].children, hotelNames[i]):
                k = Keyword(hotelNames[i], hotelNames[i], hotelCodes[i], "No", 5, None, True)
                tree[ci].children[si].children[cii].children.append(k)
                KEYLIST.append(k)
                worksheet.write(counter, 4, hotelNames[i])
                counter += 1
    worksheet.write(0,5, "Room Name")
    l = grt
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

def genCityTree():
    tree = []
    for i in range(len(countryNames)):
        if not exist(tree, countryNames[i]):
            k = Keyword(countryNames[i], countryNames[i], parseKeyFrom(countryNames[i]), "Yes", 1)
            tree.append(k)
    for i in range(len(stateNames)):
        ci = ind(tree, countryNames[i])
        v = stateNames[i]+', '+countryNames[i]
        if stateNames[i] != '':
            if not exist(tree[ci].children, v):
                k = Keyword(v, stateNames[i], parseKeyFrom(stateNames[i] + ' ' + countryCodes[i]), "Yes", 3)
                tree[ci].children.append(k)
    for i in range(len(cities)):
        ci = ind(tree, countryNames[i])
        s = stateNames[i] + ', ' + countryNames[i]
        v = cities[i] + ', ' + stateNames[i]+', '+countryNames[i] if stateNames[i] != '' else cities[i] + ', ' + countryNames[i]
        if stateNames[i] == '':
            if not exist(tree[ci].children,v):
                k = Keyword(v, cities[i], parseKeyFrom(cities[i] + ' ' + stateCodes[i] + ' ' + countryCodes[i]), "No", 3)
                tree[ci].children.append(k)
        else:
            si = ind(tree[ci].children, s)
            if not exist(tree[ci].children[si].children, v):
                k = Keyword(v, cities[i], parseKeyFrom(cities[i] + ' ' + stateCodes[i] + ' ' + countryCodes[i]), "No", 4)
                tree[ci].children[si].children.append(k)
    return tree

def genStateTree():
    tree = []
    for i in range(len(countryNames)):
        if not exist(tree, countryNames[i]):
            if stateNames[i] != '':
                k = Keyword(countryNames[i], countryNames[i], countryCodes[i].upper(), "Yes", 1)
                tree.append(k)
    for i in range(len(stateNames)):
        if stateNames[i] != '':
            ci = ind(tree, countryNames[i])
            v = stateNames[i]+', '+countryNames[i]
            if not exist(tree[ci].children, v):
                k = Keyword(v, stateNames[i], countryCodes[i] + '-' + stateCodes[i].upper(), "No", 3)
                tree[ci].children.append(k)
    return tree

def genCountryTree():
    tree = []
    for i in range(len(countryNames)):
        if not exist(tree, countryNames[i]):
            k = Keyword(countryNames[i], countryNames[i], countryCodes[i].upper(), "No", 1)
            tree.append(k)
    return tree

def genBrandTree():
    tree = []
    for i in range(len(brands)):
        if not exist(tree, brands[i]):
            k = Keyword(brands[i], brands[i], brands[i], "No", 1)
            tree.append(k)
    return tree

def split(s):
    #this little section ensures the phrase starts with a word and not a special character
    while not s[0].isalnum():
        s = s[1:]
    words = []
    symbols = []
    word = ""
    symbol = ""
    for i in s:
        if i not in " \t.-,&()/;:":
            symbols.append(symbol)
            symbol = ""
            word += i
        else:
            words.append(word)
            word = ""
            symbol += i
    words.append(word)
    symbols.append(symbol)
    words = [s for s in words if s != '']
    symbols = [s for s in symbols if s != '']
    return [words, symbols]



def parseWord(s, f):
    #s is the word, f is the flag (s = standard, u = upper, l = lower)
    if f == 's':
        return s[0].upper() + s[1:].lower()
    elif f == 'u':
        return s.upper()
    elif f == 'l':
        return s.lower()

def join(w, s):
    #w is the word list, s is the symbol list
    phrase = ""
    for i in range(len(w)):
        #note this function always assume the phrase starts with a word
        phrase += w[i]
        #in case the phrase ends with a word not a symbol
        phrase += s[i] if i < len(s) else ''


print(split("hello, my name's Sam; To be precise Sam-wu & Tang;  (haha)"))
print(split(" hello, my name's Sam; To be precise Sam-wu & Tang;  (haha)"))
print(split("$ .dl;'hello, my name's Sam; To be precise Sam-wu & Tang;  (haha)"))

def parsePhrase(s, i):
    s = s.split('|')
    name = s[0]
    flag = s[1]
    concat = s[2]
    if name == '':
        return ''
    phrase = globals()[s[1]]
    if flag == 'd':
        return phrase
    words = split(phrase)[0]
    separators = split(phrase)[1]
    words = [parseWord(word, flag) for word in words]
    if concat != '':
        return concat.join(words)
    else:
        return join(wrods, separators)



def parseValue(template, index):
    pass



def trunk(structure, isAbstract):
    tree = []
    for i in range(LEN):
        values = [parse(a, i) for a in structure]
        if not exist(tree, values[0]):
            k = Keyword(values[0], values[1], values[2], isAbstract, 1)
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

def genHotelName():
    tree = genHotelNameTree()
    header = genHeader("Hotel")
    content = ""
    for i in tree:
        content += str(i)
    footer = genFooter()
    output = header + content + footer
    f = open(KEYHOTELNAME, 'w')
    f.write(output)
    f.close()


def genCity():
    tree = genCityTree()
    header = genHeader("City")
    content = ""
    for i in tree:
        content += str(i)
    footer = genFooter()
    output = header + content + footer
    f = open(KEYCITY, 'w')
    f.write(output)
    f.close()


def genState():
    tree = genStateTree()
    header = genHeader("State")
    content = ""
    for i in tree:
        content += str(i)
    footer = genFooter()
    output = header + content + footer
    f = open(KEYSTATE, 'w')
    f.write(output)
    f.close()

def genCountry():
    tree = genCountryTree()
    header = genHeader("Country")
    content = ""
    for i in tree:
        content += str(i)
    footer = genFooter()
    output = header + content + footer
    f = open(KEYCOUNTRY, 'w')
    f.write(output)
    f.close()

def genBrand():
    tree = genBrandTree()
    header = genHeader("Hotel brand")
    content = ""
    for i in tree:
        content += str(i)
    footer = genFooter()
    output = header + content + footer
    f = open(KEYBRAND, 'w')
    f.write(output)
    f.close()

def genRoom():
    tree = genRoomNameTree()
    header = genHeader("Room type")
    content = ""
    for i in tree:
        content += str(i)
    footer = genFooter()
    output = header + content + footer
    f = open(KEYROOM, 'w')
    f.write(output)
    f.close()

def gen():
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)
    # genHotelName()
    # genCity()
    # genState()
    # genCountry()
    # genRoom()
    genBrand()

#gen()
# genCountryNames()
# genStateNames()

print("\n-------------%s seconds ----------------" % (time.time()-START))



