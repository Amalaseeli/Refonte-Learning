from app import app
from flask import render_template, jsonify, request
import os
import pandas as pd
import json

DATASETS_DIR="datasets"

@app.route('/')
def Home():
    return render_template("index.html",title="Home", message="Hello User, Welcome!")

@app.route('/datasets', methods=['GET'])
def get_datasets():
    datasets=[f for f in os.listdir(DATASETS_DIR) if f.endswith('csv') ]
    return jsonify(datasets)

@app.route('/datasets', methods=['POST'])
def post_dataset():
    dataset_name=request.form['dataset_name']
    dataset_path=os.path.join(DATASETS_DIR, dataset_name)

    if os.path.exists(dataset_path):
        df=pd.read_csv(dataset_path)
        first_10_rows=df.head(10).to_json(orient='records')
        return jsonify({'data':first_10_rows})
    else:
        return jsonify({'error':'Dataset Not Found'}), 404
    

