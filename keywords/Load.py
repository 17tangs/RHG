INPUT = 'hotelCode-GRT-PRT.xls'

def indices():
    wb = xlrd.open_workbook(INPUT)
    ws = wb.sheet_by_index(0)
    headers = [''.join(s.lower().strip().split(' ')) for s in ws.row_values(0)]
    IHC = headers.index("hotelcode")
    IHN = headers.index("hotelname")
    ICI = headers.index("city")
    ICO = headers.index("country")
    IST = headers.index("state")
    ISN = headers.index("statename")
    ICN = headers.index("countryname")
    IBD = headers.index("brand")
    IGD = headers.index("grtdescription")
    IGC = headers.index("grtcode")
    IPD = headers.index("prtdescription")
    IPC = headers.index("prtcode")
    return [IHC, IHN, ICI, ICO, IST, ISN, ICN, IBD, IGD, IGC, IPD, IPC]

#index of excel fields:
I = indices()
HOTEL_CODE_INDEX = I[0]
HOTEL_NAME_INDEX = I[1]
CITY_INDEX = I[2]
COUNTRY_CODE_INDEX = I[3]
STATE_CODE_INDEX = I[4]
STATE_NAME_INDEX = I[5]
COUNTRY_NAME_INDEX = I[6]
BRAND_INDEX = I[7]
GRT_NAME_INDEX = I[8]
GRT_CODE_INDEX = I[9]
PRT_NAME_INDEX = I[10]
PRT_CODE_INDEX = I[11]
