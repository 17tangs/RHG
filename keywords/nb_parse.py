import xlrd
import xlsxwriter

#keyword xml names
KEYHOTELNAME = "keyHotelName.xml"
KEYCOUNTRY = "keyCountry.xml"
KEYSTATE = "keyState.xml"
KEYCITY = "keyCity.xml"

#file io file names
INPUT = 'hotelCode-GRT-PRT-states-noroom.xls'
OUTPUT = 'keywords.xlsx'

#Global variables
KEYLIST = []
class Keyword:
    def __init__(self, v="", d="", k="", a="No", i=0, l=None):
        self.value = v
        self.des = d
        self.key = k
        self.abst = a
        self.indent = i
        self.children = l if l != None else []

    def __str__(self):
        beg = ["<Keyword>", "\t<value>" + self.value + "</value>", "\t<description>" + self.des + "</description>", "\t<key>" + self.key + "</key>","\t<isAbstract>"+ self.abst+"</isAbstract>"]
        end = "</Keyword>"
        #add indent to the keyword
        for j in range(self.indent):
            end = '\t' + end
            for i in range(len(beg)):
                beg[i] = '\t' + beg[i]
        #concatenate the list of beginning fields
        r = ""
        for s in beg:
            r += s + "\n"
        #add the children keywords
        for i in range(len(self.children)):
            r += str(self.children[i])
        #add footer to finish tag
        r += end + '\n'
        return r

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
    hc = [s.strip() for s in ws.col_values(0)[1:]]
    #hotel names
    hn = [s.strip() for s in ws.col_values(1)[1:]]
    for i in range(len(hn)):
        hn[i] = hn[i].replace("&", "&amp;")
    #city names
    cities = [s.strip() for s in ws.col_values(2)[1:]]
    #parse the city names to correct format
    for s in range(len(cities)):
        cities[s] = parseName(cities[s])
    #state names
    states = [s.strip() for s in ws.col_values(3)[1:]]
    for s in range(len(states)):
        states[s] = parseName(states[s])
    #state code
    sc = [s.strip() for s in ws.col_values(4)[1:]]
    #country names
    countries = [s.strip() for s in ws.col_values(5)[1:]]
    for s in range(len(countries)):
        countries[s] = parseName(countries[s])
    #country code
    cc = [s.strip() for s in ws.col_values(6)[1:]]
    #brand names
    brand = [s.strip() for s in ws.col_values(7)[1:]]
    return [hc, hn, cities, states, sc, countries, cc, brand]

#number of hotels
r = 0


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


def genHotelNameTree(data):
    wb = xlsxwriter.Workbook(OUTPUT)
    worksheet = wb.add_worksheet()
    worksheet.set_column('A:A', 20)
    worksheet.set_column('B:B', 30)
    worksheet.set_column('C:C', 40)
    worksheet.set_column('D:D', 10)
    worksheet.set_column('E:E', 50)
    hc = data[0]
    hn = data[1]
    cities = data[2]
    states = data[3]
    sc = data[4]
    countries = data[5]
    cc = data[6]
    brand = data[7]
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
                k = Keyword(hn[i], hn[i], hc[i], "No", 4)
                tree[ci].children[cii].children.append(k)
                KEYLIST.append(k)
                worksheet.write(counter, 4, hn[i])
                counter += 1
        else:
            si = ind(tree[ci].children, s)
            cii = ind(tree[ci].children[si].children, v)
            if not exist(tree[ci].children[si].children[cii].children, hn[i]):
                k = Keyword(hn[i], hn[i], hc[i], "No", 5)
                tree[ci].children[si].children[cii].children.append(k)
                KEYLIST.append(k)
                worksheet.write(counter, 4, hn[i])
                counter += 1
    wb.close()
    return tree

def parseKeyFrom(s):
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
    cities = data[2]
    states = data[3]
    sc = data[4]
    countries = data[5]
    cc = data[6]
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
    states = data[3]
    sc = data[4]
    countries = data[5]
    cc = data[6]
    tree = []
    for i in range(len(countries)):
        if not exist(tree, countries[i]):
            k = Keyword(countries[i], countries[i], cc[i], "Yes", 1)
            tree.append(k)
    for i in range(len(states)):
        ci = ind(tree, countries[i])
        v = states[i]+', '+countries[i]
        if states[i] != '':
            if not exist(tree[ci].children, v):
                k = Keyword(v, states[i], sc[i], "No", 3)
                tree[ci].children.append(k)
    return tree

def genCountryTree(data):
    countries = data[5]
    cc = data[6]
    tree = []
    for i in range(len(countries)):
        if not exist(tree, countries[i]):
            k = Keyword(countries[i], countries[i], cc[i], "No", 1)
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

def genHeader():
    return "<?xml version=\"1.0\" encoding = \"utf-8\"?>\n<Category name = \"Hotel\" xmlName = \"Hotel\" isPublishable = \"Yes\">\n"

def genFooter():
    return "</Category>\n"

def genHotelName():
    data = load()
    tree = genHotelNameTree(data)
    header = genHeader()
    content = ""
    for i in tree:
        content += str(i)
    footer = genFooter()
    output = header + content + footer
    f = open('keyHotelName.xml', 'w')
    f.write(output)
    f.close()


def genCity():
    data = load()
    tree = genCityTree(data)
    header = genHeader()
    content = ""
    for i in tree:
        content += str(i)
    footer = genFooter()
    output = header + content + footer
    f = open('keyCity.xml', 'w')
    f.write(output)
    f.close()


def genState():
    data = load()
    tree = genStateTree(data)
    header = genHeader()
    content = ""
    for i in tree:
        content += str(i)
    footer = genFooter()
    output = header + content + footer
    f = open('keyState.xml', 'w')
    f.write(output)
    f.close()

def genCountry():
    data = load()
    tree = genCountryTree(data)
    header = genHeader()
    content = ""
    for i in tree:
        content += str(i)
    footer = genFooter()
    output = header + content + footer
    f = open('keyCountry.xml', 'w')
    f.write(output)
    f.close()

def gen():
    genHotelName()
    genCity()
    genState()
    genCountry()

gen()





