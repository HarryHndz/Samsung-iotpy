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


db, cur = None, None
db = pymysql.connect(host = 'localhost', user = 'root', password = '1234', db = 'Datos', charset = 'utf8')
cur = db.cursor()

def aguaTierra(channel):
    
    if GPIO.input(channel):
        a = "Water Not Detected!"
        return a
    else:
        a = "Water Detected!"
        return a


#sensor de lluvia
def leer_nivel_lluvia(pin_analogico):
	valor_analogico = GPIO.input(pin_analogico)
	if valor_analogico == 0:
		valor_analogico = "No hay inundación por el momento"
	else:
		valor_analogico = "Cuidado posible inundación"
	
	return valor_analogico

def humedadTemperaura(sensor, pin):
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    
    if humidity is not None and temperature is not None:
        return humidity, temperature
    else:
        return "Todo mal"
    

def ingresarDatos(estatus, humedad1, humedad2, dia, hora):
	
	sql = "INSERT INTO sensor (nombre, temperatura, humedad, fecha, hora) VALUES (%s,%s,%s,%s,%s)"
	cur.execute(sql, (estatus, humedad1, humedad2, dia, hora))
	db.commit()
