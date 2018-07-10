def parseC(s):
    return ''.join(e for e in s if e.isalnum())



    
class Element:
    def __init__(self, n="", c=False, t="xs:string", mv="No", ma="Yes",ch = None, e=None, r =None, s = False):
        self.name = n
        self.complex = c
        self.includes = []
        self.children = ch if ch != None else []
        if self.children != []:
            for c in self.children:
                self.includes += c.includes
        self.ty = self.parseType(t)
        if "yes" in ma.lower():
            self.man = ""
        elif "no" in ma.lower():
            self.man = " minOccurs=\"0\" "
        else:
            print("ERROR: MANDATORY FIELD NOT BOOLEAN")
        if "yes" in mv.lower():
            self.mult = " maxOccurs=\"unbounded\" "
        elif "no" in mv.lower():
            self.mult = ""
        else:
            print("ERROR: MULTIVALUE FIELD NOT BOOLEAN")
        self.rang = r if r != None else []
        if self.rang != []:
            f = open('ex.txt','a')
            f.write("range of " + self.name + " is " + str(self.rang)+'\n')
            f.close()
        self.enum = e if e != None else []
        if self.enum != []:
            f = open('ex.txt','a')
            f.write("enum of " + self.name + " is " + str(self.enum)+'\n')
            f.close()
        self.t = s
        
    def parseType(self, s):
        t = s.lower()
        if("keyword" in t):
            return "xs:string"
        elif(t.strip()=="number"):
            return "xs:int"
        elif("string" in t or "rich" in t):
            return "xs:string"
        elif("image" in t or "pdf" in t or "iconClass" in t or "blank" in t or "seo" in t or "externalurl" in t):
            return "xs:string"
        elif("component" in t or "embedded" in t):
            x = parseC(s[s.index('(')+1:s.index(')')])
            self.includes.append(x)
            return x
        elif "multimedia" in t:
            return "xs:string"
        else:
            return s


    def genSimpleElement(self):
        if self.enum != []:
            s = "<xs:element name=\"" + self.name + "\">\n"
            s += self.genEnum()
            s += "</xs:element>\n"
        elif self.rang != []:
            s = "<xs:element name=\"" + self.name + "\">\n"
            s += self.genRange()
            s += "</xs:element>\n"
        else:
            s =  "<xs:element name=\"" + self.name + "\" type= \""  +  self.ty + "\""+ self.man + self.mult + "/>" + "\n"
        return s

    def genEnum(self):
        s = "<xs:simpleType>\n\t<xs:restriction base = \"" + self.ty + "\">\n"
        for e in self.enum:
            s += "\t\t<xs:enumeration value = \"" + e + "\"/>\n"
        s += "\t</xs:restriction>\n</xs:simpleType>\n"
        return s

    def genRange(self):
        s = "<xs:simpleType>\n\t<xs:restriction base = \"" + self.ty + "\">\n"
        if len(self.rang) == 1:
            s += "\t\t<xs:minInclusive value = \"" + self.rang[0] + "\"/>\n"
        else:
            s += "\t\t<xs:minInclusive value = \"" + self.rang[0] + "\"/>\n\t\t<xs:maxInclusive value = \"" + self.rang[1] + "\"/>\n"
        s += "\t</xs:restriction>\n</xs:simpleType>\n"
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
        s = "<xs:complexType name = \"" + self.name + "\">\n\t<xs:sequence>\n"
        for i in range(len(self.children)):
            s += self.children[i].gen()
        s+= "\t</xs:sequence>\n</xs:complexType>\n"
        return s

    
    def genElement(self):
        if self.complex == False:
            s = self.genSimpleElement()
        elif self.complex == True:
            s = self.genComplexElement()
        return s

    def gen(self):
        if self.t == True:
            return self.genType()
        else:
            return self.genElement()
    



   
