import os

directory = os.fsencode("C:\\Users\\gf174cq\\rhg-xsd\\xsdGenerator\\typeFiles")

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"):
        f = open("C:\\Users\\gf174cq\\rhg-xsd\\xsdGenerator\\typeFiles\\"+filename, "r")
        k = f.readlines()
        f.close()
        f =  open("C:\\Users\\gf174cq\\rhg-xsd\\xsdGenerator\\typeFiles\\"+filename, "w")
        for l in k:
            if l != "yn":
                f.write(l)
        f.close()
        # print(os.path.join(directory, filename))
  #      f.close()
        pass




