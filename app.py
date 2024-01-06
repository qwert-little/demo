import numpy as np
import pandas as pd
import re
from flask import Flask, render_template, request
import pickle, json, random

app = Flask(__name__)

with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

with open("suggestions.json", 'r') as f:
    suggestions = json.load(f)


def clean_text(response):
  response = response.split(',')
  return response

def analyseSentiment(resp):
    resp = [resp]
    y_pred = model.predict(resp)
    pred = y_pred[0]
    for suggestion in suggestions['suggestions']:
            if suggestion['label'] == '0':
                spos = random.choice(suggestion['response'])
            else:
                sneu = random.choice(suggestion['response'])

    if pred==0:
        result = "Legitimate transaction"
        sugg = spos
    else:
        result = "Fraudulent transaction"
        sugg = sneu

    return result, sugg

@app.route('/')
def home():
    return render_template("home.html")
@app.route('/result', methods=['GET', 'POST'])
def result():
    txt = request.form.get("txt")
    print(txt)
    if request.method=='POST':
        if txt!="":
            res = clean_text(txt)
            print(res)
            result, sugg = analyseSentiment(res)
            return render_template("result.html", result = result, sugg = sugg, txt=txt)
        else:
            return render_template('home.html')
    else:
        return render_template('home.html')

if __name__ == "__main__":
    app.run(debug = True)