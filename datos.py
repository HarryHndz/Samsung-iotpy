import requests
from flask import Flask,request,render_template, send_file
import RPi.GPIO as GPIO
import time
import Adafruit_DHT
import sys
import pymysql
import pandas as pd
import matplotlib.pyplot as plt                                                                                                                                                            
import datetime
from funciones import *
from prueba import *

pin_analogico = 3
channel = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_analogico, GPIO.IN)
GPIO.setup(channel, GPIO.IN)

sensor = Adafruit_DHT.DHT11
pin = 20

app = Flask(__name__)

@app.route('/')
def page_inicio() :
    ciudadClima = "Tabasco"
    url = "https://api.openweathermap.org/data/2.5/weather?q="+ciudadClima+"&appid=83177a230ed6391b46520af268ae01df"
    response = requests.get(url)
    if response.status_code == 200:
        info = response.json()
        infoFinal = round(info['main']['temp']-272.15,2)
        imgClima="http://openweathermap.org/img/wn/"+info['weather'][0]['icon']+"@4x.png"
        
        agua = aguaTierra(channel)
        print(agua)
        
        nivel_lluvia = leer_nivel_lluvia(pin_analogico)
        print(nivel_lluvia)
        
        humedad = humedadTemperaura(sensor, pin)
        print(humedad)
            
        ahora = datetime.datetime.now()
        dia = ahora.date()
        hora = ahora.time()
        
        ingresarDatos('normal',humedad[1],humedad[0],dia, hora)

        return render_template('datos.html', info=infoFinal,img=imgClima, agua=agua, nivel_lluvia=nivel_lluvia, humedad = humedad)
    else :
        return render_template('datos.html', error ="nada que mostrar")
    
    
db, cur = None, None
db = pymysql.connect(host = 'localhost', user = 'root', password = '1234', db = 'Datos', charset = 'utf8')
cur = db.cursor()

@app.route('/obtener reporte')
def page_ini_pdf():

    cur.execute("SELECT temperatura,humedad FROM sensor LIMIT 100")
    listaTemperatura = []
    listaHumedad = []

    for  temperatura,humedad in cur.fetchall():
        listaTemperatura.append(temperatura)
        listaHumedad.append(humedad)
        

    data = {
        "sensor de humedad": listaHumedad,
        "sensor de temperatura":listaTemperatura
    }

    DataSetSensor = pd.DataFrame(data)

    media_temperatura = DataSetSensor["sensor de temperatura"].mean()
    media_humedad=DataSetSensor["sensor de humedad"].mean()
    labels = ['Temperatura', 'Humedad']

    medias = [media_temperatura, media_humedad]


    DataSetSensor["sensor de temperatura"].plot(kind='line', figsize=(4, 2), title="Sensor de temperatura")
    plt.gca().spines[['top', 'right']].set_visible(False)
    plt.gca().set_facecolor("#CACACA")
    plt.savefig("graficaTemperatura.png")

    plt.figure()

    DataSetSensor["sensor de humedad"].plot(kind="line", figsize=(4, 2), title='Sensor de humedad',color="red")
    plt.gca().spines[['top', 'right']].set_visible(False)
    plt.gca().set_facecolor("#CACACA")
    plt.savefig("graficaHumedad.png")

    plt.figure()

    plt.figure(figsize=(4,2))
    plt.bar(labels,medias)
    plt.title("Media de la temperatura y humedad")
    plt.xlabel('Sensor')
    plt.ylabel('Media')
    plt.savefig("graficaMedia.png")
    
    generar_pdf('Reporte.pdf','graficaTemperatura.png','graficaHumedad.png','graficaMedia.png')
    
    ruta_pdf = "Reporte.pdf"
    return send_file(ruta_pdf,as_attachment=True)

if __name__ == '__main__' :
    app.run(debug=True,port=80,host='0.0.0.0')


