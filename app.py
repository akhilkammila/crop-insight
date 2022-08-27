# Setting up flask:
# https://stackoverflow.com/questions/31252791/flask-importerror-no-module-named-flask
# https://github.com/miguelgrinberg/microblog/issues/244

from flask import Flask, request, render_template
import pickle
import pandas as pd

app = Flask(__name__)

pipe = pickle.load(
    open('models/cropmodel.pkl', 'rb'))


@app.route('/')
def home():
    return 'hi'


@app.route('/predict', methods=['POST'])
def predict():
    d = {'Area': ['India'], 'Item': ['Potatoes'], 'Year': [2000], 'average_rain_fall_mm_per_year': [
        1000.0], 'pesticides_tonnes': [127585.0], 'avg_temp': [25.32]}
    test = pd.DataFrame(data=d)
    pipe.predict(test)
    return 'predict'


if __name__ == "__main__":
    app.run()
