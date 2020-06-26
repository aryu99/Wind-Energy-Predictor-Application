from flask import Flask,render_template,request
import pandas as pd 
from sklearn.linear_model import LinearRegression
import numpy as np
import requests
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    API_KEY = "dac73cd4aa6d251af51224cd3e8983c9"
    CITY = "Istanbul"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"
    print(url)
    resp = requests.get(url)
    resp = resp.json()
    data = {}
    data['date'] = datetime.utcfromtimestamp(resp['dt']).strftime('%m-%d-%Y %H:%M')
    data['windspeed'] = resp['wind']['speed']
    data['winddir'] = resp['wind']['deg']
    data['temp'] = round(resp['main']['temp']-273.15,3)
    data['mintemp'] = round(resp['main']['temp_min']-273.15,3)
    data['maxtemp'] = round(resp['main']['temp_max']-273.15,3)
    data["pred"] = ""
    return render_template('index.html',val = data)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/stats')
def stats():
    return render_template("stats.html")

@app.route('/predict',methods = ['POST','GET'])
def predict():
    # data = pd.read_csv("Salary_Data.csv")
    # x = np.array(data['YearsExperience']).reshape(-1,1)
    # lr = LinearRegression()
    # lr.fit(x,np.array(data['Salary']))
    ex = [int(x) for x in request.form.values()]
    print(ex)
    # ex = np.array(ex).reshape(1,-1) #CHANGE EX !!!!!!!
    # pred = lr.predict(ex)[0]
    op = f"ENERGY THAT WILL BE GENERATED WILL BE {ex[0]*10+ex[1]*10}KW"

    return render_template('index.html', val = {"pred":op})

if __name__ == "__main__":
    app.run(debug=True)