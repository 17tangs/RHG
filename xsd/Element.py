
def parseName(s):
    s = s.strip()
    l = []
    st = ""
    for i in s:
        if i not in ":;[]{}|><?,/.!@#$%^&*()+ ":
            st += i
        else:
            l.append(st)
            st = ""
    if st != "":
        l.append(st)
    l = [s for s in l if s!='']
    l = [t[0].upper() + t[1:].lower() for t in l]
    return ''.join(l)


#handle mandatory field
def hman(ma):
    if "yes" in ma.lower():
        m = ""
    elif "no" in ma.lower():
        m = " minOccurs=\"0\" "
    else:
        m = "ERROR"
        print("ERROR: MANDATORY FIELD NOT BOOLEAN")
    return m

#handle multiple value field
def hmv(mv, n):
    if "yes" in mv.lower():
        m = " maxOccurs=\"unbounded\" "
    elif "no" in mv.lower():
        m = ""
    else:
        m = "ERROR"
        print("ERROR: " + n + " MULTIVALUE FIELD NOT BOOLEAN")
    return m

#handle range field exceptions
def special(n, isEnum):
    if isEnum:
        f = open('enum.txt', 'r')
        l = [s.split('\t') for s in f.read().split('\n')]
        names = [s[0] for s in l]
        if n in names:
            return l[names.index(n)][1:]
    else:
        f = open('range.txt', 'r')
        l = [s.split('\t') for s in f.read().split('\n')]
        names = [s[0] for s in l]
        if n in names:
            return l[names.index(n)][1:]
    return []





class Element:
    def __init__(self, m_name="", m_description = "", m_type="xs:string", m_isMultivalued="No", m_isMandatory="Yes", m_isComp = False, m_children = None, m_isComplex = False, m_isType = False, m_path = None, m_enumList=None):
        self.name = m_name
        self.complex  = m_isComplex
        self.description = m_description
        self.children = m_children if m_children!=None else []
        self.includes = self.define_includes()
        self.ty = self.parseType(m_type)
        self.mand = hman(m_isMandatory)
        self.mult = hmv(m_isMultivalued, m_name)
        self.rang = special(m_name, False)
        self.enum = special(m_name, True) if m_enumList == None else m_enumList
        self.component = m_isComp
        self.isType = m_isType
        self.path = m_path if m_path != None else []


    def define_includes(self):
        includes = []
        if self.children != []:
            for c in self.children:
                includes += c.includes
        return includes


    def parseType(self, s):
        t = s.strip().lower()
        if t == "":
            r = ""
        elif t == "number":
            r = "xs:int"
        elif t == "rich text" or t[:6] == "string":
            r = "xs:string"
        elif '(' in t:
            if t[:10] == "multimedia":
                r = "xs:string"
            elif t[:9] == "component" or t[:8] == "embedded":
                if "seo" in t:
                    r = "xs:string"
                else:
                    x = parseName(s[s.index('(')+1:s.index(')')])
                    self.includes.append("../general/" + x + ".xsd")
                    r = x
            elif t[:7] == "keyword":
                x = "key"+parseName(s[s.index(':')+1:s.index(')')])
                f=open('hi.txt', 'a')
                f.write(x+'\n')
                f.close()
                self.includes.append("../keywords/" + x + ".xsd")
                r = x
        return r


    def genSimpleElement(self):
        if self.enum!=[] or self.rang  != []:
            s = "\t\t<xs:element name=\"" + self.name + "\">\n"
            s += self.genSimpleType()
            s += "\t\t</xs:element>\n"
        else:
            s =  "\t\t<xs:element name=\"" + self.name + "\" type= \""  +  self.ty + "\""+ self.mand + self.mult + "/>" + "\n"
        return s

    def genSimpleType(self):
        if self.enum!=[]:
            return self.genEnum()
        elif self.rang != []:
            return self.genRange()
        else:
            return "\t\t<xs:simpleType name = \"" + self.name + "\" type = \"" + self.ty + "\"/>\n"

    def genEnum(self):
        s = "\t\t<xs:simpleType name = \"" + self.name + "\">\n\t\t\t<xs:restriction base = \"" + self.ty + "\">\n"
        for e in self.enum:
            s += "\t\t\t\t<xs:enumeration value = \"" + e + "\"/>\n"
        s += "\t\t\t</xs:restriction>\n\t\t</xs:simpleType>\n"
        return s

    def genRange(self):
        s = "\t\t<xs:simpleType>\n\t\t\t<xs:restriction base = \"" + self.ty + "\">\n"
        if len(self.rang) == 1:
            s += "\t\t\t\t<xs:minInclusive value = \"" + self.rang[0] + "\"/>\n"
        else:
            s += "\t\t\t\t<xs:minInclusive value = \"" + self.rang[0] + "\"/>\n\t\t<xs:maxInclusive value = \"" + self.rang[1] + "\"/>\n"
        s += "\t\t\t</xs:restriction>\n\t\t</xs:simpleType>\n"
        return s

    def genSequence(self):
        s = "<xs:complexType>\n\t<xs:sequence>\n"
        for i in range(len(self.children)):
            s += self.children[i].gen()
        s += "\t</xs:sequence>\n</xs:complexType>\n"
        return s

    def genComplexElement(self):
        s = "<xs:element name = \"" + self.name + "\">\n"
        s += self.genSequence()
        s += "</xs:element>\n"
        return s

    def genType(self):
        if self.complex == True:
            s = "<xs:complexType name = \"" + self.name + "\">\n\t<xs:sequence>\n"
            if self.component == True:
                s += "\t\t<xs:attribute name = \"schema\" type = \"xs:string\" fixed = \""+ self.name +"\"/>\n"
            for i in range(len(self.children)):
                s += self.children[i].gen()
            s+= "\t</xs:sequence>\n</xs:complexType>\n"
            return s
        else:
            return self.genSimpleType()


    def genElement(self):
        if self.complex == False:
            s = self.genSimpleElement()
        elif self.complex == True:
            s = self.genComplexElement()
        return s

    def gen(self):
        if self.name == "":
            return ""
        if self.isType == True:
            return self.genType()
        else:
            return self.genElement()
