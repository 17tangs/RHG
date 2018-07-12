METADATA_ID = "tcm:4-124-512"

class Keyword:
    def __init__(self, v="", d="", k="", a="No", i=0, l=None, m_hasMeta = False):
        self.value = v
        self.des = d
        self.key = k
        self.abst = a
        self.indent = i
        self.children = l if l != None else []
        self.hasMeta = m_hasMeta

    def __str__(self):
        if self.hasMeta:
            beg = ["<Keyword>", "\t<value>" + self.value + "</value>", "\t<description>" + self.des + "</description>", "\t<key>" + self.key + "</key>","\t<isAbstract>"+ self.abst+"</isAbstract>", "\t<Metadata ID=\"" + METADATA_ID + "\"></Metadata>"]
        else:
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
