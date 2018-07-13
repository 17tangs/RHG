import xlrd
import os
import xlsxwriter
import time
from Keyword import Keyword
from Load import *
from structure import *
from parse import *

START = time.time()

#return the index of the target (tar) in the list (l)
def ind(l, tar):
    for i in range(len(l)):
        if l[i].value == tar:
            return i
    #return invalid character if not found
    return 'a'


#return true if target (tar) is in list (l)
def exist(l, tar):
    for i in l:
        if i.value == tar:
            return True
    return False


def write2Excel():
    wb = xlsxwriter.Workbook(OUTPUT)
    worksheet = wb.add_worksheet()
    worksheet.set_column('A:A', 20)
    worksheet.set_column('B:B', 30)
    worksheet.set_column('C:C', 40)
    worksheet.set_column('D:D', 10)
    worksheet.set_column('E:E', 50)
    worksheet.set_column('F:F', 50)
    worksheet.write(0,0,"CountryNames")
    worksheet.write(0,1,"StateNames")
    worksheet.write(0,2,"Cities")
    worksheet.write(0,3,"Brands")
    worksheet.write(0,4,"Hotel Name")
    worksheet.write(0,5,"Room Name")
    st = []
    ct = []
    for i in range(LEN):
        ct.append([parseField(s, i) for s in cityStructure[len(cityStructure)-1]][0])
        st.append([parseField(s, i) for s in stateStructure[len(stateStructure)-1]][0])
    co = [s for s in list(set(countryNames)) if s != '']
    br = [s for s in list(set(brands)) if s != '']
    hn = [s for s in list(set(hotelNames)) if s != '']
    rn = [s for s in list(set(grt)) if s != '']
    st = [s for s in list(set(st)) if s != '']
    ct = [s for s in list(set(ct)) if s != '']
    for i in range(len(co)):
        worksheet.write(i+1, 0, co[i])
    for i in range(len(br)):
        worksheet.write(i+1, 3, br[i])
    for i in range(len(hn)):
        worksheet.write(i+1, 4, hn[i])
    for i in range(len(rn)):
        worksheet.write(i+1, 5, rn[i])
    for i in range(len(st)):
        worksheet.write(i+1, 1, st[i])
    for i in range(len(ct)):
        worksheet.write(i+1, 2, ct[i])
    wb.close()


def genTree(structure):
    depth = len(structure)
    tree = []
    for d in range(depth):
        isAbstract = "No" if d == depth - 1 else "Yes"
        for i in range(LEN):
            data = [[parseField(f, i) for f in layer] for layer in structure]
            meta = True if structure[d][0][0].split('|')[0] == "hotelNames" else False
            values = data[d]
            l = tree
            offset = 0
            for j in range(d):
                if ind(l, data[j][0]) != 'a':
                    l = l[ind(l, data[j][0])].children
                else:
                    offset += 1
            if (not exist(l, values[0])) and values[1]!= '':
                k = Keyword(values[0], values[1], values[2], isAbstract, d-offset, None, meta)
                l.append(k)
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


def genFile(sn,xmln, fn):
    #sn = structure name
    #xmln = xml name
    #fn = output file name
    tree = genTree(sn)
    header = genHeader(xmln)
    content = ""
    for i in tree:
        content += str(i)
    footer = genFooter()
    output = header + content + footer
    f = open(fn, 'w')
    f.write(output)
    f.close()


def gen():
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)
    genFile(brandStructure, "Brand", KEYBRAND)
    genFile(countryStructure, "Country", KEYCOUNTRY)
    genFile(stateStructure, "State", KEYSTATE)
    genFile(cityStructure, "City", KEYCITY)
    genFile(hotelStructure, "Hotel Name", KEYHOTELNAME)
    genFile(roomStructure, "Room Type", KEYROOM)


def display_runtime():
    print("\n-------------%s seconds ----------------" % (time.time()-START))



gen()
display_runime()
#genCountryNames()
#write2Excel()
#genStateNames()

