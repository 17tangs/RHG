import xlrd
import os
from Element import Element

FILE = "Entities_Webextra_v3.xlsx"
DIRECTORY = "C:\\Users\\gf174cq\\projects\\RHG\\xsd\\hotel\\"
if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)

def parseExcel(filename):
    wb = xlrd.open_workbook(filename)

    #component link sheet
    gcs = wb.sheet_by_index(1)

    #embedded component sheet
    ecs = wb.sheet_by_index(2)

    sheets = []
    for i in range(3, wb.nsheets):
        #entity sheet
        ets = wb.sheet_by_index(i)
        sheets.append(ets)
    return [[gcs, ecs], sheets]


def parseComponentList(sheet):
    #components
    cs = []
    #component
    c = []
    for i in range(1, sheet.nrows):
        #list of row values with no empty values
        v = [s for s in sheet.row_values(i)[:6] if s!='']
        #if not an empty line then it belows to component c
        if v!=[]:
            c.append(v)
        #else delete the header row then append to component list
        else:
            if c!= []:
                del c[1]
                cs.append(c)
                c = []
    #take care of the last component then return 
    if c != []:
        del c[1]
        cs.append(c)
    return cs

def test():
    l = parse_entity(parse_Excel(FILE)[1][17])
    for i in l:
        print(i)

def parseEntity(sheet):
    #list of rows
    c = []
    for i in range(sheet.nrows):
        #list of row values with no empty values
        v = [s for s in sheet.row_values(i)[:7] if s!='']
        c.append(v)
    #detect header row and delete it
    for i in c:
        if "Mandatory" in i:
            del c[c.index(i)]
    #s[1:] deletes ID, c[1:] preserves entity name, len(s)==7 deletes useless lines
    p = [c[0]]+[c[1]]+[s[1:] for s in c[2:] if len(s)==7]
   # for i in p:
   #     print(i)
    return p


#parse the elements in the component into metadata and general
def parseComponent(l):
    meta = []
    general = []
    for i in l:
        if i[5] == "General":
            general.append(i)
        else:
            meta.append(i)
    return [general, meta]

#parsing the generla/meta component to decide whether to include or not
def cl(general, meta):
    if general == None and meta == None:
        return None
    elif general == None:
        return [meta]
    elif meta == None:
        return [general]
    else:
        return [general, meta]


def parseName(s):
    s = s.strip()
    l = []
    st = ""
    for i in s:
        if i not in ":;[]{}|><?,/.!@#$%^&*() ":
            st += i
        else:
            l.append(st)
            st = ""
    if st != "":
        l.append(st)
    l = [s for s in l if s!='']
    l = [t[0].upper() + t[1:].lower() for t in l]
    return ''.join(l)


def genContent(l, isComp, isElement):
    if isElement:
        #the path denotes the folder where the xsd elements should go. This is stored in the second line of the excel file so we have to handle for that
        path = l[1]
        #general list
        gl = parseComponent(l[2:])[0]
        #meta list
        ml = parseComponent(l[2:])[1]
    else:
        #if it's not an element, then it's a component which stays in the general folder
        path = ["general"]
        #general list
        gl = parseComponent(l[1:])[0]
        #meta list
        ml = parseComponent(l[1:])[1]
    #ed = element data 
    #field list (ge = general elements)
    ge = []
    for ed in gl:
        #always not mandatory, each element is not a component and not complex 
        element = Element(ed[0],ed[1], ed[2], ed[3], "No", False)
        ge.append(element)
    general = Element("General", "", "", "No", "No", False, ge, True, False) if ge != [] else None
    #meta elements = me
    me = []
    for ed in ml:
        #always not mandatory, each element is not a component and not complex 
        element = Element(ed[0],ed[1], ed[2], ed[3], "No", False)
        me.append(element)
    meta = Element("Meta", "", "", "No", "No", False, me, True, False) if me != [] else None
    #parsing the general and meta elements
    ls = cl(general, meta)
    #if it's an element create Element, if it's not create type (last parameter boolean)
    name = parseName(l[0][0])
    if isElement:
        comp = Element(name, "", "","No", "No", isComp, ls, True, False, path) if l != None else Element()
    else:
        comp = Element(name, "", "","No", "No", isComp, ls, True, True, path) if l != None else Element()
    return comp

def genIncludes(l):
    #include text
    i = ""
    for inc in l:
        i += "\t<xs:include schemaLocation = \"" + inc + "\"/>\n"
    return i

def genHeader():
    return "<?xml version = \"1.0\" encoding= \"UTF-8\"?>\n<xs:schema xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" elementFormDefault=\"qualified\" attributeFormDefault=\"unqualified\">\n"

def genFooter():
    return "</xs:schema>"

def writeout(comp):
    content = comp.gen()
    if content == None:
        print(comp.name)
    includeList = list(set(comp.includes))
    includes = genIncludes(includeList)
    header = genHeader()
    footer = genFooter()
    output = header + includes + content + footer

    if comp.path == []:
        direct = DIRECTORY
        filename = comp.name + ".xsd"
        f = open(direct+filename, 'w')
        f.write(output)
        f.close()
    elif comp.path[0] == "IGNORE":
        return
    else:
        for i in range(len(comp.path)):
            direct = DIRECTORY + comp.path[i] + "\\"
            filename = comp.name + ".xsd"
            if not os.path.exists(direct):
                os.makedirs(direct)
            f = open(direct+filename, 'w')
            f.write(output)
            f.close()


def genKeywords():
    wb = xlrd.open_workbook("keywords.xlsx")
    sheet = wb.sheet_by_index(0)
    keywords = []
    for i in range(sheet.ncols):
        v = sheet.col_values(i)
        v = [s for s in v if s!='']
        keywords.append(v)
    for k in keywords:
        name = "key" + parseName(k[0])
        values = k[1:]
        for i in range(len(values)):
            values[i] = values[i].replace("&", "&amp;")
        key = Element(name, "", "string", "No", "No",False,None, False, True, ["keywords"], values)
        direct = DIRECTORY + "keywords" + "\\"
        filename = name + ".xsd"
        if not os.path.exists(direct):
            print(True)
            os.makedirs(direct)
        f=open(direct+filename, 'w')
        output = genHeader() + key.gen() + genFooter()
        f.write(output)
        f.close()
    f = open('keywords.txt','r')
    keys = [t for t in f.read().split('\n') if t != ""]
    for k in keys:
        direct = DIRECTORY + "keywords" + "\\"
        filename = direct + k + ".xsd"
        f = open(direct + k + ".xsd", 'w')
        key = Element(k, "", "string", "No","No", False, None, False, True, ["keywords"])
        output = genHeader() + key.gen() + genFooter()
        f.write(output)
        f.close()


def gen():
    genKeywords()
    #data in excel file in a list of sheet
    data = parseExcel(FILE)
    #component sheets
    cdata = data[0]
    #parsing sheets into list format
    #GC = general component, EC = embedded component
    GC = parseComponentList(cdata[0])
    EC = parseComponentList(cdata[1])
    #parsing the entities into list format
    entities = [parseEntity(s) for s in data[1]][:-1]
    #for i in entities:
    #    print(i)
    for i in GC:
        #genContent(list of data, isComponent, isElement)
        comp = genContent(i, True, False)
        writeout(comp)
    for i in EC:
        comp = genContent(i, False, False)
        writeout(comp)
    for i in entities:
        comp = genContent(i, False, True)
        writeout(comp)




gen()
