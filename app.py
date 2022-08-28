from flask import Flask, request, render_template, jsonify
import flask
import pickle
import pandas as pd
import numpy as np
from datetime import date

import python_weather
import asyncio
import os

app = Flask(__name__)

pipe = pickle.load(
    open('models/cropmodel.pkl', 'rb'))


@app.route('/')
def home():
    return 'hi'


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    # https://www.ncei.noaa.gov/cag/global/time-series/globe/land_ocean/ytd/7/2012-2022
    country = request.args.get('country')

    def run_model(year_subtraction: int, item: str):
        d = {'Area': [country], 'Item': [item], 'Year': [2022-year_subtraction], 'average_rain_fall_mm_per_year': [
            1000.0], 'pesticides_tonnes': [3000-year_subtraction*100], 'avg_temp': [20.54262658451951]}

        test = pd.DataFrame(data=d)
        prediction = pipe.predict(test)

        return prediction[0]

    crops = ['Maize', 'Sweet potatoes', 'Wheat', 'Cassava', 'Potatoes',
             'Rice, paddy', 'Sorghum', 'Soybeans', 'Yams',
             'Plantains and others']

    total = 0.0
    answ = []

    for i in range(len(crops)):
        crop = crops[i]

        current = run_model(0, crop)
        last_5 = run_model(15, crop)
        last_30 = run_model(30, crop)

        curr = []
        curr.append((current-last_5)/last_5)
        curr.append((current-last_30)/last_30)

        total += ((current-last_5)/last_5)

        answ.append(curr)

    for row in answ:
        row.append((row[0]+total/10)*3)

    # comparison to last 5 years for that crop worldwide (2013)

    # comparison to last 30 years for that crop worldwide
    print(answ)
    return answ


if __name__ == "__main__":
    app.run()
