from gen import *

def genList(tree, l):
    for i in range(len(tree)):
        l[0].append(tree[i].value)
        l[1].append(tree[i].key)
        if tree[i].children == None:
            return
        else:
            genList(tree[i].children,l)

def printDuplicates(tree, name):
    l = [[],[]]
    genList(tree, l)
    values = l[0]
    keys = l[1]
    #vd = value duplicaes, kd similar
    vd= []
    kd = []
    for i in range(len(values)):
        for j in range(i+1, len(values)):
            if values[i] == values[j]:
                vd.append("position 1: " + str(i) +  " position 2: " + str(j) + "   " + values[i])
            if keys[i] == keys[j] and keys[i] != '':
                kd.append("position 1: " + str(i) +  " position 2: " + str(j) + "   " + keys[i])

    if vd == [] and kd == []:
        print("------No duplicates found in " + name + " category ------")
    else:
        for v in vd:
            print("Duplicate value found: " + v)
        for k in kd:
            print("Duplicate key found: " + k)
        print("Total of " + str(len(vd) + len(kd)) + " found")

def testDuplicates():
    brandTree = genTree(brandStructure)
    countryTree = genTree(countryStructure)
    stateTree = genTree(stateStructure)
    cityTree = genTree(cityStructure)
    hotelTree = genTree(hotelStructure)
    roomTree = genTree(roomStructure)
    printDuplicates(brandTree, "brand")
    printDuplicates(countryTree, "country")
    printDuplicates(stateTree, "state")
    printDuplicates(cityTree, "city")
    printDuplicates(hotelTree, "hotel")
    printDuplicates(roomTree, "rooms")



testDuplicates()
