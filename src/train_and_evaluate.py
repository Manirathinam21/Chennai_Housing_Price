# load the train and test data
# train algorithm with train data
# save the metrics and params

import os
import sys
import argparse
import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from get_data import read_params
import joblib
import json


def eval_metrics(actual, pred):
    rmse= np.sqrt(mean_squared_error(actual, pred))
    mae= mean_absolute_error(actual, pred)
    r2= r2_score(actual, pred)
    return rmse, mae, r2

def train_and_evaluate(config_path):
    config=read_params(config_path)
    train_data_path= config['split_data']['train_path']
    test_data_path= config['split_data']['test_path']
    random_state = config['base']['random_state']
    model_dir= config['model_dir']
    
    
    max_depth= config['estimators']['RandomForest']['params']['max_depth']
    max_features= config['estimators']['RandomForest']['params']['max_features']
    n_estimators= config['estimators']['RandomForest']['params']['n_estimators']
    
    target= [config['base']['target_col']]
    
    train= pd.read_csv(train_data_path, sep=',')
    test= pd.read_csv(test_data_path, sep=',')
    
    train_x= train.drop(target, axis=1)
    test_x= test.drop(target, axis=1)
    
    train_y= train[target] 
    test_y= test[target]
    
    #Feature Engineering- standardscaler, onehot encoding categorical values
    scaler=StandardScaler()
    column_trans= make_column_transformer((OneHotEncoder(sparse=False), ['AREA','SALE_COND','PARK_FACIL','BUILDTYPE', 'UTILITY_AVAIL','STREET','MZZONE']), remainder='passthrough')
    rf= RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, max_features=max_features)    
    
    #making pipeline
    pipe= make_pipeline(column_trans, scaler, rf)
    pipe.fit(train_x, train_y)
    
    y_pred= pipe.predict(test_x)
    (rmse, mae, r2)= eval_metrics(test_y, y_pred)
    
    print("Randomforest model (max_depth=%f, max_features=%f, n_estimators=%f):" % (max_depth, max_features, n_estimators))
    print("  RMSE: %s" % rmse)
    print("  MAE: %s" % mae)
    print("  R2: %s" % r2)

################################################################################################################################    

    params_file= config["reports"]["params"]
    scores_file= config["reports"]["scores"]

    with open(scores_file, "w") as f:
        scores= { 
            "rmse": rmse, 
            "mae": mae, 
            "r2": r2
        }
        json.dump(scores, f, indent=4)
    
    with open(params_file, "w") as f:
        params= {
            "alpha": alpha,
            "l1_ratio": l1_ratio
        }
        json.dump(params, f, indent=4)


################################################################################################################################

    os.makedirs(model_dirs, exist_ok=True)
    model_path=os.path.join(model_dirs, 'pipeline.joblib')
    
    joblib.dump(pipe, model_path)


if __name__ == '__main__':
    args=argparse.ArgumentParser()
    args.add_argument('--config', default='params.yaml')
    parsed_args= args.parse_args()
    train_and_evaluate(config_path= parsed_args.config)