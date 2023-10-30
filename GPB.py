get_ipython().system('pip install boto3')
get_ipython().system('pip install thefuzz')
get_ipython().system('pip install googlemap')


# In[279]:


import boto3 as boto3
import googlemaps
import pandas as pd
import plotly.express as px
import os
from thefuzz import fuzz, process


# In[292]:


# Reemplaza estas variables con tus propias credenciales y nombres de bucket y archivo
AWS_ACCESS_KEY_ID = 'AKIA6N4KQVAWMFTHHHSZ'
AWS_SECRET_ACCESS_KEY = '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'
BUCKET_NAME = 'groupbtest'
FOLDER_PATH = './Untitled Folder'
REMOTE_FILE_NAME = 'Prueba.txt'
GMAPS_KEY = 'AIzaSyA5UtvbK6lYWGjJbZtU3prV-U88EG0jRKs'
df = pd.DataFrame(columns=['Direccion']) 


# In[303]:


s3 = boto3.client('s3', aws_access_key_id = AWS_ACCESS_KEY_ID ,aws_secret_access_key = AWS_SECRET_ACCESS_KEY)


# In[294]:


# List all files in the specified folder
file_names = os.listdir(FOLDER_PATH)

# Print the file names
for file_name in file_names:
    try:
        s3.upload_file(f'{FOLDER_PATH}/{file_name}',BUCKET_NAME,file_name)
        print(f'{FOLDER_PATH}/{file_name} se ha subido exitosamente a {BUCKET_NAME} como {file_name}')
    except FileNotFoundError:
        print(f'El archivo {FOLDER_PATH}/{file_name} no se encontró')
    except NoCredentialsError:
        print('No se encontraron credenciales de AWS')


# In[271]:


def direccionesAlternas(direccion):
    direcciones = []
    if direccion[4] == '-':
        direcciones.append('Carrera ' + direccion[1] + ' # ' + direccion[3] + ' ' + direccion[5])
        direcciones.append('Carrera ' + direccion[1] + ' Nro ' + direccion[3] + ' - ' + direccion[5])
        direcciones.append('Carrera ' + direccion[1] + ' Numero ' + direccion[3] + ' - ' + direccion[5])
        direcciones.append('Carrera ' + direccion[1] + ' Num ' + direccion[3] + ' - ' + direccion[5])
        direcciones.append('Kra ' + direccion[1] + ' Num ' + direccion[3] + ' - ' + direccion[5])
        direcciones.append('Calle ' + direccion[1] + ' Num ' + direccion[3] + ' - ' + direccion[5])
        direcciones.append('Trasversal ' + direccion[1] + ' Num ' + direccion[3] + ' - ' + direccion[5])

    if direccion[4] != '-':
        direcciones.append('Carrera ' + direccion[1] + ' # ' + direccion[3] + ' ' + direccion[4])
        direcciones.append('Carrera ' + direccion[1] + ' Nro ' + direccion[3] + ' - ' + direccion[4])
        direcciones.append('Carrera ' + direccion[1] + ' Numero ' + direccion[3] + ' - ' + direccion[4])
        direcciones.append('Carrera ' + direccion[1] + ' Num ' + direccion[3] + ' - ' + direccion[4])
        direcciones.append('Kra ' + direccion[1] + ' Num ' + direccion[3] + ' - ' + direccion[4])
        direcciones.append('Calle ' + direccion[1] + ' Num ' + direccion[3] + ' - ' + direccion[4])
        direcciones.append('Trasversal ' + direccion[1] + ' Num ' + direccion[3] + ' - ' + direccion[4])

    return direcciones


# In[314]:


def calcularPorcentaje(diroriginal):
    direccion = diroriginal
    direcciones = direccionesAlternas(direccion)
    temporal = " ".join(diroriginal)


    for direccionFictica in direcciones:
        
        print(temporal)
        print(direccionFictica)
        print(fuzz.ratio(temporal.lower(),direccionFictica.lower()))
        ratio = fuzz.partial_ratio(temporal.lower(),direccionFictica.lower())
        if ratio >= 90:
            df.loc[len(df)] = direccionFictica.strip()
        print(ratio)
        print(fuzz.token_sort_ratio(temporal.lower(),direccionFictica.lower()))
        print(fuzz.token_set_ratio(temporal.lower(),direccionFictica.lower()))
        
        print('**************')


# In[315]:


response = s3.list_objects_v2(Bucket=BUCKET_NAME)

for obj in response.get('Contents', []):
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=obj['Key'])
        data = response['Body'].read()
        # If you want to decode it as a string (assuming it's a text file)
        data_str = data.decode('utf-8').strip()
        print(data_str)
        diroriginal = data_str.split(' ')
        calcularPorcentaje(diroriginal)
        
    except Exception as e:
        print(f"An error occurred: {e}")




print(df)


# In[317]:


gmaps_key = googlemaps.Client(key = GMAPS_KEY)


# In[318]:


df['LAT'] = None
df['LON'] = None
df['Color'] = 1
df['Tamaño'] = 1

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


# In[319]:


df


# In[320]:


fig = px.scatter_mapbox(df, lon = df['LON'], lat = df['LAT'], zoom = 10, color = df['Color'] , size = df['Tamaño'], width=900 , height=600 ,title='DIRECTIONS MAP')
fig.update_layout(mapbox_style = "open-street-map")
fig.update_layout(margin = {"r":0,"t":50,"l":0,"b":10})
fig.show()


# In[ ]:




