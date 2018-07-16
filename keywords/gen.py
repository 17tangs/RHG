import xlrd, os, xlsxwriter, time
from Keyword import Keyword
from Load import *
from structure import *
from parse import *

START = time.time()


def ind(l, tar): #return the index of the target (tar) in the list (l)
    for i in range(len(l)):
        if l[i].value == tar:
            return i
    #return invalid character if not found
    return 'a'


def exist(l, tar):  #return true if target (tar) is in list (l)
    for i in l:
        if i.value == tar:
            return True
    return False

#generate tree structure
def genTree(structure):
    depth = len(structure)
    tree = []
    data = [[[parseField(f, i) for f in layer] for layer in structure] for i in range(LEN)]
    for d in range(depth):
        isAbstract = "No" if d == depth - 1 else "Yes"
        for i in range(LEN):
            row = data[i]
            meta = True if structure[d][0][0].split('|')[0] == "hotelNames" and d == depth-1 else False
            values = row[d]
            l = tree
            offset = 0
            for j in range(d):
                if ind(l, row[j][0]) != 'a':
                    l = l[ind(l, row[j][0])].children
                else:
                    offset += 1
            if (not exist(l, values[0])) and values[1]!= '':
                k = Keyword(values[0], values[1], values[2], isAbstract, d-offset, None, meta)
                l.append(k)
    return tree

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


if __name__ == "__main__":
    gen()
    display_runtime()
#genCountryNames()
#write2Excel()
#genStateNames()

