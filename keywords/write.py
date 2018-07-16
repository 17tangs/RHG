from gen import *


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


write2Excel()
