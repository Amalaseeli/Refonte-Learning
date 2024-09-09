from app import app
from flask import render_template, jsonify, request
import os
import pandas as pd
import json

DATASETS_DIR="datasets"
FEATURE_COLUMN_FILE="features.json"

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
    
def load_features_columns():
    if os.path.exists(FEATURE_COLUMN_FILE):
        with open(FEATURE_COLUMN_FILE, 'r') as f:
            json.load(f)
    return []

def save_feature_columns(columns):
    with open(FEATURE_COLUMN_FILE, 'w') as file:
        json.dump(columns, file)

@app.route('/features', methods=['POST'])
def save_columns():
    data=request.json
    selected_columns=data.get('selected',[])
    print('selected_columns',selected_columns)
    save_feature_columns(selected_columns)
    return jsonify({'success': True, 'features':selected_columns})

@app.route('/features', methods=['GET'])
def get_features():
    feature_columns=load_features_columns()
    return jsonify({'feature_columns': feature_columns})

@app.route('/get_unselected_columns', methods=['POST'])
def get_unselected_columns():
    dataset_name=request.form['dataset_name']
    dataset_path=os.path.join(DATASETS_DIR, dataset_name)

    if os.path.exists(dataset_path):
        df=pd.read_csv(dataset_path)
        all_columns=set(df.columns)
        selcted_columns=set(load_features_columns())
        unselcted_columns=list(all_columns-selcted_columns)
        print("unselcted_columns", unselcted_columns)
        return jsonify({'unselcted_columns':unselcted_columns})
    else:
        return jsonify({'error':'Dataset Not Found'}), 404

    

