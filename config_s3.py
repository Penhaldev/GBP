from config_google import *
from dotenv import load_dotenv
import os
import boto3 as boto3
from data_process import *

load_dotenv()

#Connection of S3
s3 = boto3.client('s3', aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID') ,aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY'))


def upload_file(s3):
    file_names = os.listdir(os.getenv('FOLDER_PATH'))
    for file_name in file_names:
        try:
            s3.upload_file(f'{os.getenv('FOLDER_PATH')}/{file_name}',os.getenv('BUCKET_NAME'),file_name)
            print(f'{os.getenv('FOLDER_PATH')}/{file_name} se ha subido exitosamente a {os.getenv('BUCKET_NAME')} como {file_name}')
        except FileNotFoundError:
            print(f'El archivo {os.getenv('FOLDER_PATH')}/{file_name} no se encontró')
        except:
            print('No se encontraron credenciales de AWS')


def obtain_files(s3):
    files_s3 = s3.list_objects_v2(Bucket=os.getenv('BUCKET_NAME'))
    return files_s3

def read_files(df):
    files_s3 = obtain_files(s3)
    for obj in files_s3.get('Contents', []):
        try:
            files_s3 = s3.get_object(Bucket=os.getenv('BUCKET_NAME'), Key=obj['Key'])
            data = files_s3['Body'].read()
            data_str = data.decode('utf-8').strip()
            original_address = data_str.split(' ')
            calculate_percentage(original_address,df)
            
        except Exception as e:
            print(f"An error occurred: {e}")