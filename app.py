# -*- coding: utf-8 -*-
"""
Created on Sun Oct 30 10:01:30 2022

@author: kotcherlakota
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score, confusion_matrix, classification_report
import json
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request
app = Flask(__name__)

UPLOAD_FOLDER = 'C:/Users/kotcherlakota/Desktop\Prj_nfl/Uploads/'
ALLOWED_EXTENSIONS = set(['csv'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024 * 1024
app.secret_key = 'super secret key'


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_file(path):
    try:
        global df
        df = pd.read_csv(path)
        #print('Success')
        return df
    except:
        print('Could not read file.')

def dataset_overview(df):
    shape = df.shape
    rows, cols = shape[0], shape[1]
    missing_values_sum = df.isnull().sum().sum()
    desc_stat = df.describe().to_string().split('\n')
    return rows, cols, missing_values_sum, desc_stat


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        if 'file' not in request.files:
            return render_template('index.html', alert=0)
        file = request.files['file']

        if file.filename == '':
            return render_template('index.html', alert=0)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            path_to_file = 'C:/Users/kotcherlakota/Desktop\Prj_nfl/Uploads/' + filename
            df = read_file(path_to_file)
            rows, cols, missing_values_sum, desc_stat = dataset_overview(df)
            col_names = df.columns.tolist()
            data = {'Columns': df.isnull().sum().index.values.tolist(),
                    'Missing Values': df.isnull().sum().values.tolist(),
                    'Data Type': df.dtypes.tolist()
                   }
            mv_table = pd.DataFrame(data)
            return render_template('index.html', alert=1, filename=filename,
                                   rows=rows, cols=cols, col_names=col_names,
                                   mv_table=mv_table.to_html(classes='data table'),
                                   missing_values_sum=missing_values_sum,
                                   desc_table=df.head(10).to_html(classes='data table', header='true')
                                  )

        else:
            return render_template('index.html', alert=0)

@app.route('/preprocess', methods=['POST'])
def column_selection():
        if request.method == 'POST':
            a1=request.form.getlist('paramodel')
            a2= request.form.getlist('nonparamodel')
            a3=request.form.getlist('emodel')
            a4= request.form.getlist('pena')
            a5= request.form.getlist('imbalance')
            a6= request.form.getlist('cv')
            data={'paramodel':a1,'nonparamodel':a2,'emodel':a3,'pena':a4,'imbalance':a5,'cross validation':a6}
            print(data)
            with open("res.json", "w") as outfile:
                json.dump(data, outfile)

        return render_template('index.html')



@app.route('/')
def homePage():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
    