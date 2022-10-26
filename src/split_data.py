#split the clean data 
# save it in the data/processed folder

import os
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from get_data import read_params, get_data

def split_and_save_data(config_path):
    config= read_params(config_path)
    clean_data_path= config['load_data']['clean_dataset_csv']
    train_data_path= config['split_data']['train_path']
    test_data_path= config['split_data']['test_path']
    split_ratio= config['split_data']['test_size']
    random_state= config['base']['random_state']
    
    df= pd.read_csv(clean_data_path, sep=',')
    train, test= train_test_split(
        df,
        test_size= split_ratio,
        random_state= random_state)
    
    train.to_csv(train_data_path, sep=',', index=False, encoding='utf-8')
    test.to_csv(test_data_path, sep=',', index=False, encoding='utf-8')
    

if __name__ == '__main__':
    args=argparse.ArgumentParser()
    args.add_argument('--config', default='params.yaml')
    parsed_args= args.parse_args()
    split_and_save_data(config_path=parsed_args.config)