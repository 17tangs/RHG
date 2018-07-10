import xlrd


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
        for j in range(self.indent):
            end = '\t' + end
            for i in range(len(beg)):
                beg[i] = '\t' + beg[i]
        r = ""
        for s in beg:
            r += s + "\n"
        for i in range(len(self.children)):
            r += str(self.children[i])
        r += end + '\n'
        return r

wb = xlrd.open_workbook('hotelCode-GRT-PRT.xls')

ws = wb.sheet_by_index(0)

#hotel codes
hc = [s.strip() for s in ws.col_values(0)[1:]]

#hotel names
hn = [s.strip() for s in ws.col_values(1)[1:]]

cities = [s.strip() for s in ws.col_values(2)[1:]]

states = [s.strip() for s in ws.col_values(3)[1:]]
countries = [s.strip() for s in ws.col_values(4)[1:]]

brand = [s.strip() for s in ws.col_values(5)[1:]]

#number of hotels
r = len(hn)

def ind(l, tar):
    for i in range(len(l)):
        if l[i].value == tar:
            return i
    return 'a'

def exist(l, tar):
    for i in l:
        if i.value == tar:
            return True
    return False

KEY = []
for i in range(r):
    if not exist(KEY, brand[i]):
        k = Keyword(brand[i], brand[i], '', "Yes", 1)
        KEY.append(k)

for i in range(r):
    brand_index = ind(KEY, brand[i])
    if not exist(KEY[brand_index].children, countries[i]):
        k = Keyword(countries[i], countries[i], '', "Yes", 2)
        KEY[brand_index].children.append(k)

for i in range(r):
    bi = ind(KEY, brand[i])
    ci = ind(KEY[bi].children, countries[i])
    if states[i] != '':
        if not exist(KEY[bi].children[ci].children, states[i]):
            k = Keyword(states[i], states[i], '', "Yes", 3)
            KEY[bi].children[ci].children.append(k)

for i in range(r):
    bi = ind(KEY, brand[i])
    ci = ind(KEY[bi].children, countries[i])
    if states[i] == '':
        if not exist(KEY[bi].children[ci].children, cities[i]):
            k = Keyword(cities[i], cities[i], '', "Yes", 3)
            KEY[bi].children[ci].children.append(k)
    else:
        si = ind(KEY[bi].children[ci].children, states[i])
        if not exist(KEY[bi].children[ci].children[si].children, cities[i]):
            k = Keyword(cities[i], cities[i], '', "Yes", 4)
            KEY[bi].children[ci].children[si].children.append(k)


for i in range(r):
    bi = ind(KEY, brand[i])
    ci = ind(KEY[bi].children, countries[i])
    if states[i] == '':
        cii = ind(KEY[bi].children[ci].children, cities[i])
        if not exist(KEY[bi].children[ci].children[cii].children, hn[i]):
            k = Keyword(hn[i], hn[i], hc[i], "No", 4)
            KEY[bi].children[ci].children[cii].children.append(k)
    else:
        si = ind(KEY[bi].children[ci].children, states[i])
        cii = ind(KEY[bi].children[ci].children[si].children, cities[i])
        if not exist(KEY[bi].children[ci].children[si].children[cii].children, hn[i]):
            k = Keyword(hn[i], hn[i], hc[i], "No", 5)
            KEY[bi].children[ci].children[si].children[cii].children.append(k)

st = "<Category name = \"Hotel\" xmlName = \"Hotel\" isPublishable = \"Yes\">\n"
for i in KEY:
    st += str(i)
st+= "<\Category>\n"
f = open('keywords.txt', 'w')
f.write(st)
f.close()
