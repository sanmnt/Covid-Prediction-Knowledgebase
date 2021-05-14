from flask import Flask, request
from flask_cors import CORS, cross_origin
from keras.models import Sequential, load_model
import numpy as np
import pandas as pd
from csv import writer
import csv
from dotenv import load_dotenv
from generator import counter
from populate import populate
import os

load_dotenv()

app = Flask(__name__)
CORS(app)
model = load_model("Dense_Sequential_Model_1.hdf5")

def minMaxTemp(val):
    return (val - 33.5) / 6.1

def minMaxPulse(val):
    return (val - 35) / 125

@app.route('/nn-submit', methods=['POST'])
@cross_origin()
def nn_submit():
    body = request.get_json()

    data = [
        body['age'] / 100,
        body['high_risk_exposure_occupation'],
        body['high_risk_interactions'],
        body['diabetes'],
        body['chd'],
        body['htn'],
        body['cancer'],
        body['asthma'],
        body['copd'],
        body['autoimmune_dis'],
        body['smoker'],
        minMaxTemp(body['temperature']),
        minMaxPulse(body['pulse']),
        body['labored_respiration'],
        body['cough'],
        body['fever'],
        body['sob'],
        body['diarrhea'],
        body['fatigue'],
        body['headache'],
        body['loss_of_smell'],
        body['loss_of_taste'],
        body['runny_nose'],
        body['muscle_sore'],
        body['sore_throat']
    ]

    junk0 = [0 for i in range(25)]
    junk1 = [1 for i in range(25)]

    columns = ['age',
               'high_risk_exposure_occupation', 'high_risk_interactions', 'diabetes',
               'chd', 'htn', 'cancer', 'asthma', 'copd', 'autoimmune_dis', 'smoker',
               'temperature', 'pulse', 'labored_respiration', 'cough', 'fever', 'sob',
               'diarrhea', 'fatigue', 'headache', 'loss_of_smell', 'loss_of_taste',
               'runny_nose', 'muscle_sore', 'sore_throat']
    binary_features = ['diabetes', 'chd', 'htn', 'cancer', 'asthma', 'copd', 'autoimmune_dis', 'high_risk_exposure_occupation', 'high_risk_interactions', 'smoker', 'labored_respiration', 'cough',
                       'fever', 'sob', 'diarrhea', 'fatigue', 'headache', 'loss_of_smell', 'loss_of_taste', 'runny_nose', 'muscle_sore', 'sore_throat']

    df = pd.DataFrame([data, junk0, junk1], columns=columns)

    for col in binary_features:
        df[col] = df[col] * 1

    dummy_cols = list(set(df[binary_features]))
    df = pd.get_dummies(df, columns=dummy_cols)
    df = df.drop(index=[1,2])
    predictions = model.predict(df)
    data.append(predictions[0][0].item())
    data.insert(0, counter())
    with open('user.csv', 'w') as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(['id','age',
               'high_risk_exposure_occupation', 'high_risk_interactions', 'diabetes',
               'chd', 'htn', 'cancer', 'asthma', 'copd', 'autoimmune_dis', 'smoker',
               'temperature', 'pulse', 'labored_respiration', 'cough', 'fever', 'sob',
               'diarrhea', 'fatigue', 'headache', 'loss_of_smell', 'loss_of_taste',
               'runny_nose', 'muscle_sore', 'sore_throat','prediction'])
        writer_object.writerow(data)
        f_object.close()
    populate()
    return {'prediction': predictions[0][0].item()}

if __name__ == '__main__':
    app.run()
