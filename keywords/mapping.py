import xlrd

def parseName(s):
    s = s.strip()
    l = s.split(' ')
    #delete empty words and lists
    l = [s for s in l if s!='']
    l = [t[0].upper() + t[1:].lower() for t in l]
    #finally join the correctly parsed word list into a single word
    return ' '.join(l)

def stateMap():
    wb = xlrd.open_workbook('state-code-name.xls')
    ws  = wb.sheet_by_index(0)

    #sc = state code, cc = country code, sn = state name
    cc = ws.col_values(0)[1:]
    sc = ws.col_values(1)[1:]
    sn = [parseName(s) for s in ws.col_values(2)[1:]]

    id = [sc[i] + ' ' + cc[i] for i in range(len(sc))]
    #create empty mapping
    id.append('')
    sn.append('')
    map = dict(zip(id, sn))
    return map

def countryMap():
    wb = xlrd.open_workbook('country-code-name.xls')
    ws = wb.sheet_by_index(0)

    #cc = country code, cn = country name
    cc = ws.col_values(0)[1:]
    cn = [parseName(s) for s in ws.col_values(1)[1:]]

    map = dict(zip(cc, cn))
    return map

#state map and country map
SM = stateMap()
CM = countryMap()
