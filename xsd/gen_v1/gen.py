from Element import Element
import sys

def readt():
    fin = open("C:\\Users\\gf174cq\\RHG\\xsd\\gen_v1\\typeFiles\\"+sys.argv[1], 'r')
    content = fin.read()
    k = content.split('\n')
    l = []
    name = k[0]
    for line in k[1:]:
        if(line != ''):
            l.append(line)
    fin.close()
    return [[name, 'y'], l]

def reade():
    fin = open("C:\\Users\\gf174cq\\RHG\\xsd\\gen_v1\\elementFiles\\"+sys.argv[1], 'r')
    content = fin.read()
    k = content.split('\n')
    l = []
    name = k[0]
    for line in k[1:]:
        if(line != ''):
            l.append(line)
    fin.close()
    return [[name, 'n'], l]    

types = []
def parse(s):
    s = s.split('\t')
    del s[1]
    return s

def genContent(ls):
    el = ls[1]
    name = ls[0][0]
    ct = True if ls[0][1] == 'y' else False
    chs = []
    for s in el:
        l = parse(s)
        enums = None
        rang = None
        if '[' in l[4]:
            enums = l[4][l[4].index('[')+1:l[4].index(']')].split(',')
        elif '{' in l[4]:
            rang = l[4][l[4].index('{')+1:l[4].index('}')].split(':')
        e = Element(l[0], False, l[1], l[2], "No", None, enums, rang)
        chs.append(e)
    A = Element(name, True, "", "yes", "no", chs, None, None, ct)
    includes = "".join("\t\t<xs:include schemaLocation=\"general/" + t + ".xsd\"/>\n" for t in list(set(A.includes)))
    return includes+A.gen()

def read():
    if sys.argv[2] == "1":
        return readt()
    else:
        return reade()



def gen():
    ls = read()
    f = open(ls[0][0]+'.xsd', 'w')
    header  = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n\t<xs:schema xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" elementFormDefault=\"qualified\" attributeFormDefault=\"unqualified\">\n"
    content = genContent(ls)
    footer = "</xs:schema>"
    f.write(header+content+footer)
    f.close()

gen()
