import boto3 as boto3
import pandas as pd
from config_google import *
from config_s3 import *
from draw_map import *

df = pd.DataFrame(columns=['address'])

def main():
    upload_file(s3)
    obtain_files(s3)
    read_files(df)
    add_coordinates_df(df)
    draw_map(df)   

main()




