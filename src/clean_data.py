# read the data from data source 
# clean the data by handling null values & date columns, convert float to integer
# removing unwanted columns
# save it in the data/cleaned for further process


import os
import pandas as pd
from get_data import get_data, read_params
import argparse


def clean_and_load(config_path):
    config=read_params(config_path)
    df=get_data(config_path)
    df=df.fillna(df.mean())
    
    df['HOUSE_AGE']=pd.to_datetime(df['DATE_SALE'], format='%d-%m-%Y' )-pd.to_datetime(df['DATE_BUILD'], format='%d-%m-%Y')
    for index in df.index:
        df.loc[index,'HOUSE_AGE'] = df.loc[index,'HOUSE_AGE'].days
    df['HOUSE_AGE'] = df['HOUSE_AGE'].apply(pd.to_numeric)
    
    df=df.drop(['PRT_ID','DATE_BUILD','DATE_SALE','QS_ROOMS','QS_BEDROOM','QS_BATHROOM','QS_OVERALL','REG_FEE','COMMIS'], axis=1)
        
    for col in df.columns:
        if df[col].dtype=='float':
            df[col]=df[col].apply(int)            
    #print(df.head())
    
    clean_data_path= config["load_data"]["clean_dataset_csv"]
    df.to_csv(clean_data_path, sep=',', index=False)
    

if __name__=='__main__':
    args=argparse.ArgumentParser()
    args.add_argument('--config', default='params.yaml')
    parsed_args= args.parse_args()
    clean_and_load(config_path=parsed_args.config)