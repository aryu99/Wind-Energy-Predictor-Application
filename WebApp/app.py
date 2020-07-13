from flask import Flask,render_template,request,redirect,url_for,Markup,flash
from matplotlib import pyplot as plt 
import pandas as pd
import requests
import time 
import numpy as np
import tensorflow as tf 
from tensorflow import keras
import requests
from datetime import datetime
import matplotlib
import random
from os import environ

matplotlib.use('Agg')

BATCH_SIZE_predict = 120

def multivariate_data_predict(dataset, past_window):                    
  data = []
  end_index = len(dataset)
  start_index = len(dataset) - past_window
  for i in range(start_index, end_index):
    data.append(dataset[i])
  return np.array(data)

def real_plot():
    data = pd.read_csv("static/historical.csv")

    model = tf.keras.models.load_model('static/model5.h5')

    pred_data = data[-120:]
    pred_data.index = pred_data["date_time"]
    pred_data = pred_data[["wind_speed","wind_direction"]]
    pred_data = pred_data.values
    pred_data_std = [3.64500726,94.60264878]
    pred_data_mean = [8.20507312,163.49269538]
    dataset_mean = 7384
    dataset_std = 5950
    x_predict_multi = (pred_data-pred_data_mean)/pred_data_std
    
    x_predict_multi= tf.data.Dataset.from_tensor_slices((x_predict_multi))
    
    x_predict_multi= x_predict_multi.batch(BATCH_SIZE_predict).repeat()
    x_predict_multi= x_predict_multi.batch(BATCH_SIZE_predict).repeat()
    predictions_raw = model.predict(x_predict_multi.take(1))
    predictions_array = (predictions_raw*dataset_std) + dataset_mean
    predictions = predictions_array[0]
    
    return predictions

def update_data():
  one_day = 86400

  API_KEY = environ.get("WEATHER_API_KEY")
  CITY = "Istanbul"
  date_time = []
  wind_speed = []
  wind_dir = []
  try:
    for i in range(5,0,-1):
        dt = datetime.utcnow().date()
        ts =int(time.mktime(dt.timetuple()))
        url = f"http://api.openweathermap.org/data/2.5/onecall/timemachine?lat=41.0082&lon=28.9784&dt={ts-((i-1)*one_day)}&appid={API_KEY}"
        print(url)
        resp = requests.get(url)
        resp = resp.json()
        #print(resp['hourly'])
        for j in resp['hourly']:
            date_time.append(j['dt'])
            wind_speed.append(j["wind_speed"])
            wind_dir.append(j["wind_deg"])
  except:pass
  date_time = [datetime.utcfromtimestamp(x).strftime('%d-%m-%Y %H:%M') for x in date_time]
  data = pd.DataFrame({"date_time":date_time,"wind_speed":wind_speed,"wind_direction":wind_dir})
  data.to_csv("static/historical.csv",header=False,mode='a',index=False)
  print(data.shape)
  data = pd.read_csv("static/historical.csv")
  data.drop_duplicates(inplace = True)
  data["date_time"] = pd.to_datetime(data['date_time'], format='%d-%m-%Y %H:%M')
  #print(type(data.date_time[0]))
  data.sort_values(by=['date_time'], inplace=True)
  data["date_time"] = data['date_time'].dt.strftime('%d-%m-%Y %H:%M')
  data.to_csv("static/historical.csv",index = False)

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{p:.2f}% \n ({v:d})'.format(p=pct,v=val)
    return my_autopct


app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


API_KEY = environ.get("WEATHER_API_KEY")
CITY = "Istanbul"
url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"
print(url)

hist = pd.read_csv("static/historical.csv")
if int(hist[-1:]["date_time"].values[0][:2]) != int((datetime.now().day)-1):
    update_data()
plt.style.use("fivethirtyeight")

resp = requests.get(url)
resp = resp.json()
data = {}
data['date'] = datetime.utcfromtimestamp(resp['dt']).strftime('%m-%d-%Y %H:%M')
data['windspeed'] = resp['wind']['speed']
data['winddir'] = resp['wind']['deg']
data['temp'] = round(resp['main']['temp']-273.15,3)
data['mintemp'] = round(resp['main']['temp_min']-273.15,3)
data['maxtemp'] = round(resp['main']['temp_max']-273.15,3)
data["pred"] = ''


pred = real_plot()

pred = [random.randint(5,10) if x < 0 else x for x in pred ] 
pred = pred[::6]
total_power = sum(pred)
avg_power = total_power/len(pred)
chart_data = pd.DataFrame(data = {"x":[x for x in range(1,len(pred)+1)],"y":pred})

plt.plot(chart_data['x'],chart_data['y'])
plt.xlabel("Hours")
plt.ylabel("Power in KW")
plt.ylim(0)
plt.xlim((0,72))
plt.tight_layout()
plt.savefig('static/images/chart.png')

plt.figure(figsize = (11,4))
plt.plot(chart_data['x'],chart_data['y'])
plt.xlabel("Hours")
plt.ylabel("Power in KW")
plt.ylim(0)
plt.xlim((0,72))
#plt.title("Power For Next 72 Hours")
plt.tight_layout()
plt.savefig('static/images/chart2.png')

plt.figure(figsize = (11,4))
plt.plot(hist['date_time'][-120::2],hist['wind_speed'][-120::2])
plt.xlabel("Date-Time")
plt.ylabel("Wind Speed (m/s)")
plt.xticks(rotation = 90,fontsize=6)
plt.title("Wind Speed for the last 5 Days")
plt.tight_layout()
plt.savefig('static/images/prev5speed.png')

plt.figure(figsize = (11,4))
plt.plot(hist['date_time'][-120::2],hist['wind_direction'][-120::2])
plt.xlabel("Date-Time")
plt.ylabel("Wind Direction in Degrees")
plt.title("Wind Direction for the last 5 Days")
plt.xticks(rotation = 90,fontsize=6)
plt.tight_layout()
plt.savefig('static/images/prev5dir.png')

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/home',methods = ['GET','POST'])
def index():
    update_data()
    API_KEY = environ.get("WEATHER_API_KEY")
    CITY = "Istanbul"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}"
    print(url)

    hist = pd.read_csv("static/historical.csv")
    if int(hist[-1:]["date_time"].values[0][:2]) != int((datetime.now().day)-1):
        update_data()
    
    pred = real_plot()

    pred = [random.randint(5,10) if x < 0 else x for x in pred ] 
    pred = pred[::6]
    total_power = sum(pred)
    avg_power = total_power/len(pred)
    chart_data = pd.DataFrame(data = {"x":[x for x in range(1,len(pred)+1)],"y":pred})

    plt.plot(chart_data['x'],chart_data['y'])
    plt.xlabel("Hours")
    plt.ylabel("Power in KW")
    plt.ylim(0)
    plt.xlim((0,72))
    plt.tight_layout()
    plt.savefig('static/images/chart.png')
    
    
    plt.style.use("fivethirtyeight")
    plt.figure(figsize = (11,4))
    plt.plot(hist['date_time'][-120::2],hist['wind_speed'][-120::2])
    plt.xlabel("Date-Time")
    plt.ylabel("Wind Speed (m/s)")
    plt.xticks(rotation = 90,fontsize=6)
    plt.title("Wind Speed for the last 5 Days")
    plt.tight_layout()
    plt.savefig('static/images/prev5speed.png')
    
    plt.figure(figsize = (11,4))
    plt.plot(hist['date_time'][-120::2],hist['wind_direction'][-120::2])
    plt.xlabel("Date-Time")
    plt.ylabel("Wind Direction in Degrees")
    plt.title("Wind Direction for the last 5 Days")
    plt.xticks(rotation = 90,fontsize=6)
    plt.tight_layout()
    plt.savefig('static/images/prev5dir.png')

    resp = requests.get(url)
    resp = resp.json()
    data = {}
    data['date'] = datetime.utcfromtimestamp(resp['dt']).strftime('%m-%d-%Y %H:%M')
    data['windspeed'] = resp['wind']['speed']
    data['winddir'] = resp['wind']['deg']
    data['temp'] = round(resp['main']['temp']-273.15,3)
    data['mintemp'] = round(resp['main']['temp_min']-273.15,3)
    data['maxtemp'] = round(resp['main']['temp_max']-273.15,3)
    data['pred'] = 0
    return render_template('index.html',val = data,avg = round(avg_power),t_power = round(total_power))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/',methods = ['POST','GET'])
def login():
    hist = pd.read_csv("static/historical.csv")
    if int(hist[-1:]["date_time"].values[0][:2]) != int((datetime.now().day)-1):
        update_data()
    error = ""
    if request.method == 'POST':
        val = [x for x in request.form.values()]
        if val[0] != 'admin' or val[1] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('index'))
    return render_template('login.html', error=error)    


@app.route('/register',methods = ['POST','GET'])
def register():
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/stats')
def stats():
    hist = pd.read_csv("static/historical.csv")
    if int(hist[-1:]["date_time"].values[0][:2]) != int((datetime.now().day)-1):
        update_data()
    return render_template("stats.html",avg = round(avg_power),t_power = round(total_power),pred = [(i+1,pred[i]) for i in range(len(pred))])

@app.route('/predict',methods = ['POST','GET'])
def predict():
    if request.method == "GET":
        return redirect(url_for("index"))
    
    ex = [int(x) for x in request.form.values()]
    pie_data = list()
    if ex[0]-round(total_power) < 0 :
        pie_data = [0,round(total_power)]
    else:
        v = ex[0]-round(total_power)
        pie_data = [v,round(total_power)]
    pie_label = ["Remaining","Demand Fulfilled"]
    data['pred'] = 1
    explode = [0,0.1]
    colors = ['#fc4f30','#56bd6e']
    plt.clf()
    plt.pie(pie_data,labels=pie_label,explode=explode,
        shadow=True,colors=colors,
        wedgeprops={'edgecolor':'black'},
        autopct=make_autopct(pie_data)
        )
    plt.title(f"Demand Supply Ratio \n Total Demand : {ex[0]}")
    plt.tight_layout()
    plt.xlabel("")
    plt.ylabel("")
    plt.savefig("static/images/pieplot.png")
    filen = "static/images/pieplot.png"
    
    
    #time.sleep(1)
    return render_template('index.html',val = data,url  = filen,avg = round(avg_power),t_power = round(total_power))

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

if __name__ == "__main__":
    app.run(debug=True)
