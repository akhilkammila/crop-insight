from flask import Flask, request, render_template, jsonify
import flask
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

pipe = pickle.load(
    open('models/cropmodel.pkl', 'rb'))


@app.route('/')
def home():
    return 'hi'


@app.route('/predict', methods=['GET', 'POST'])
def predict():

    item = [x for x in request.form.values()]
    country = request.args.get('country')
    year = 2020

    d = {'Area': ['India'], 'Item': ['Potatoes'], 'Year': [2020], 'average_rain_fall_mm_per_year': [
        1000.0], 'pesticides_tonnes': [127585.0], 'avg_temp': [25.32]}
    test = pd.DataFrame(data=d)
    prediction = pipe.predict(test)
    print(prediction)
    return [1, 2]


if __name__ == "__main__":
    app.run()
