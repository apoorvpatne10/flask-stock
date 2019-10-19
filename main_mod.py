# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import requests
import datetime
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler

def check_threshold(content, phone_no):
    url = "https://alerts.solutionsinfini.com/api/v4/index.php"

    querystring = {"method":"sms","message":content,"sender":"HACKAT","api_key":"A342de8ff9a5e571b3741374183c22146","to":f"{phone_no}"}

    headers = {
        'User-Agent': "PostmanRuntime/7.18.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "e69aa853-7221-40a9-a1cb-d1161e3a747b,d374d8e1-965b-4f82-9997-4e5249461a18",
        'Host': "alerts.solutionsinfini.com",
        'Accept-Encoding': "gzip, deflate",
        'Cookie': "SID=srfhcn3bj043umekqq7rsdd147; redirect=https%3A%2F%2Falerts.solutionsinfini.com%2F%3Fapi_key%3DAd91a665b1870b2fe2bd8396d65dae3dd%26method%3Dsms%26message%3DRanters%26to%3D9618587902%26sender%3DHACKAT; AWSALB=3dM9eDh/9mggs23qCHdULpWQ2V49+kIMkiNX8EML9TjueKc37I0PuRmzNze72O+B/71LMzVJmG0FPw4j17map/2uDfbSnJwdnZS5kENcMszvjH9INdFPmouHnGcN",
        'Content-Length': "0",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

    response = requests.request("POST", url, headers=headers, params=querystring)

    print(response.text)
    return response.text

def do_stuff(threshold_val, phone_val):
    model = load_model('weights/my_model.h5')
    data = pd.read_csv('data.csv')
    data.dropna(inplace=True)
    data.isnull().sum()

    cl = data['High']

    scl = MinMaxScaler()
    cl = cl.values.reshape(cl.shape[0], 1)
    cl = scl.fit_transform(cl)

    #Create a function to process the data into 7 day look back slices
    def processData(data, lb):
        X,Y = [],[]
        for i in range(len(data)-lb-1):
            X.append(data[i:(i+lb),0])
            Y.append(data[(i+lb),0])
        return np.array(X),np.array(Y)

    X,y = processData(cl, 7)

    X_train,X_test = X[:int(X.shape[0]*0.80)],X[int(X.shape[0]*0.80):]
    y_train,y_test = y[:int(y.shape[0]*0.80)],y[int(y.shape[0]*0.80):]

    X_test = X_test.reshape((X_test.shape[0],X_test.shape[1],1))

    Xt = model.predict(X_test)    

    new_data = X_test[-1]
    pred = Xt[-1]

    threshold = threshold_val
    phone_no = phone_val

    date = datetime.datetime(2019, 10, 19).date()

    response = ''

    print('PREDICTING NOW.')
    for _ in range(10):
        new_data = np.append(new_data[1:], pred)
        new_datax = new_data.reshape(-1, 7, 1)
        pred = model.predict(new_datax)
        predx =  scl.inverse_transform(pred)[0][0]
        if predx > threshold:
            response += f"{date.day}/{date.month}/{date.year} : Higher than threshold \n"
        else:
            response += f"{date.day}/{date.month}/{date.year} : Lower than threshold\n"
        print(f"Predicted price on {date.day}/{date.month}/{date.year} : {predx}")
        date += datetime.timedelta(days=1)

    stuff = check_threshold(response, phone_no)
