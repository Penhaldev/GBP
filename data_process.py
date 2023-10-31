from config_google import *
from thefuzz import fuzz, process

#Method that passes as a parameter the address extracted from the file in the bucket and gives us alternative addresses as indicated in the document.
def alternate_address(address):
    addresses = []
    if address[4] == '-':
        addresses.append('Carrera ' + address[1] + ' # ' + address[3] + ' ' + address[5])
        addresses.append('Carrera ' + address[1] + ' Nro ' + address[3] + ' - ' + address[5])
        addresses.append('Carrera ' + address[1] + ' Numero ' + address[3] + ' - ' + address[5])
        addresses.append('Carrera ' + address[1] + ' Num ' + address[3] + ' - ' + address[5])
        addresses.append('Kra ' + address[1] + ' Num ' + address[3] + ' - ' + address[5])
        addresses.append('Calle ' + address[1] + ' Num ' + address[3] + ' - ' + address[5])
        addresses.append('Trasversal ' + address[1] + ' Num ' + address[3] + ' - ' + address[5])

    if address[4] != '-':
        addresses.append('Carrera ' + address[1] + ' # ' + address[3] + ' ' + address[4])
        addresses.append('Carrera ' + address[1] + ' Nro ' + address[3] + ' - ' + address[4])
        addresses.append('Carrera ' + address[1] + ' Numero ' + address[3] + ' - ' + address[4])
        addresses.append('Carrera ' + address[1] + ' Num ' + address[3] + ' - ' + address[4])
        addresses.append('Kra ' + address[1] + ' Num ' + address[3] + ' - ' + address[4])
        addresses.append('Calle ' + address[1] + ' Num ' + address[3] + ' - ' + address[4])
        addresses.append('Trasversal ' + address[1] + ' Num ' + address[3] + ' - ' + address[4])

    return addresses

#Method that calculates the % of coincidence with the original address if it is greater or equal to 90% it adds it to a dataframe, the dataframe will be our data storage source.
def calculate_percentage(original_address,df):
    address = original_address
    addresses = alternate_address(address)
    temporal = " ".join(original_address)

    for temporal_address in addresses:
        ratio = fuzz.partial_ratio(temporal.lower(),temporal_address.lower())
        if ratio >= 90:
            df.loc[len(df)] = temporal_address.strip()

#Method that adds to the dataframe the coordinates of the addresses that gave us a % greater than or equal to 90       
def add_coordinates_df(df):
    df['LAT'] = None
    df['LON'] = None
    df['Color'] = 1
    df['Size'] = 1

    for i in range (0,len(df),1):
        geocode_result = gmaps_key.geocode(df.iat[i,0])
        try:
            lat = geocode_result[0]["geometry"]["location"]["lat"]
            lon = geocode_result[0]["geometry"]["location"]["lng"]
            df.iat[i,df.columns.get_loc("LAT")] = lat
            df.iat[i,df.columns.get_loc("LON")] = lon
        except:
            lat = None
            lon = None