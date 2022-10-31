from flask import Flask, request, app, jsonify, url_for, render_template 
import pandas as pd
import numpy as np
import joblib
import json
import yaml
import os
from babel.numbers import format_currency

params_path= "params.yaml"
webapp_root= "webapp"

def read_params(config_path):
    with open(config_path) as yaml_file:
        config= yaml.safe_load(yaml_file)
    return config

config= read_params(params_path)

model_dir_path= config["webapp_model_dir"]
cleaned_data_path= config["webapp_cleandata_dir"]
static_dir= os.path.join(webapp_root, "static")
template_dir= os.path.join(webapp_root, "templates")


app=Flask(__name__, static_folder=static_dir, template_folder=template_dir)
#load model pipeline
model_pipe=joblib.load(model_dir_path)
df= pd.read_csv(cleaned_data_path) 

@app.route('/')
def home():
    locations = sorted(df['AREA'].unique())
    sales = sorted(df['SALE_COND'].unique())
    parkings = sorted(df['PARK_FACIL'].unique())
    buildtypes = sorted(df['BUILDTYPE'].unique())
    utilities = sorted(df['UTILITY_AVAIL'].unique())
    streets = sorted(df['STREET'].unique())
    zones = sorted(df['MZZONE'].unique())
    return render_template('index.html', locations=locations, sales=sales, parkings=parkings, 
                           buildtypes=buildtypes, utilities=utilities, streets=streets, zones=zones)


@app.route('/predict',methods=['POST'])
def predict():
    location = request.form.get('location')
    total_sqft= int(request.form.get('total_sqft'))
    dist= int(request.form.get('dist'))
    bedroom= int(request.form.get('bedroom'))
    bathroom= int(request.form.get('bathroom'))
    room= int(request.form.get('room'))
    sale_cond= request.form.get('sale_cond')
    parking= request.form.get('parking')
    Buildtype= request.form.get('Buildtype')
    utility= request.form.get('utility')
    street= request.form.get('street')
    zone= request.form.get('zone')
    House_age= int(request.form.get('House_age'))
    
    print(location, total_sqft,dist,bedroom,bathroom,room,sale_cond,parking,Buildtype,utility,street,zone,House_age)
    input=pd.DataFrame([[location, total_sqft,dist,bedroom,bathroom,room,sale_cond,parking,Buildtype,utility,street,zone,House_age]], 
                       columns=['AREA','INT_SQFT','DIST_MAINROAD','N_BEDROOM','N_BATHROOM','N_ROOM','SALE_COND','PARK_FACIL','BUILDTYPE','UTILITY_AVAIL','STREET','MZZONE','HOUSE_AGE'])
    
    output=model_pipe.predict(input)[0]
    print(np.round(output, 2))
    return render_template("index.html",prediction_text="The Predicted House Price is : {}".format(format_currency(output, 'INR', locale='en_IN')))


@app.route('/predict_api',methods=['POST'])
def predict_api():
    json_ = request.json["data"]
    print(json_.values())
    query_df = pd.DataFrame([json_.values()], columns=['AREA','INT_SQFT','DIST_MAINROAD','N_BEDROOM','N_BATHROOM','N_ROOM','SALE_COND','PARK_FACIL','BUILDTYPE','UTILITY_AVAIL','STREET','MZZONE','HOUSE_AGE'])
    print(query_df)
    output=model_pipe.predict(query_df)[0]
    print(output)
    predicted="The Predicted House Price is : {}".format(output)
    return jsonify(predicted)


if __name__=='__main__':
    app.run(debug=True)