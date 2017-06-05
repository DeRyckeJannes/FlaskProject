from flask import Flask
from flask import request
from flask import render_template
from DbClass import DbClass
from Camera import PiCam
from sensorClasses import sensors
import os

mySensors = sensors()
humidityCompensationParameters = mySensors.ReadCompensationParametersHumidity()
temperatureCompensationParameters = mySensors.ReadCompensationParametersTemp()
camera = PiCam()
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
scheduler = BackgroundScheduler()
scheduler.start()
currentUser = []
app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def LogIn():
    DB_Layer = DbClass()
    error = ""
    users = DB_Layer.getUsersFromDatabase()
    if request.method == 'POST':
        InputEmail = request.form.get('email')
        InputPassword = request.form.get('password')
        for i in range(len(users)):
            userData = users[i]
            DBemail = userData[1]
            DBpassword = userData[2]
            if DBemail == InputEmail:
                if DBpassword == InputPassword:
                    print (userData) # hieruit nog ID halen om later op te slaan in database wanneer er gegevens worden ingegeven
                    return render_template("Home.html")
                else:
                    error = "Email or password is incorrect."
                return render_template("LogIn.html", error=error)
    if request.method == 'GET':
        return render_template("LogIn.html")


@app.route('/Home')
def Home():
    return render_template("Home.html")


@app.route('/Weather')
def TheWeather():
    DB_Layer = DbClass()
    SensorInfo = DB_Layer.getDataFromDatabase()
    SensorInfo=SensorInfo[0]
    print (SensorInfo)
    return render_template("Weather.html",SensorInfo=SensorInfo)


@app.route('/History')
def History():
    return render_template("History.html")


@app.route('/Contact', methods=['POST', 'GET'])
def Contact():
    error = ""
    succesful = "We have recieved your question, we will contact you by mail."
    DB_Layer = DbClass()
    if request.method == 'POST':
        Subject = request.form.get('Subject')
        Message = request.form.get('Message')
        print(Subject)
        print(Message)
        if Subject != "" and Message != "":
            DB_Layer.saveContactToDatabase(Subject, Message)
            return render_template("Contact.html", succesful=succesful)

        else:
            error = "Please fill in both fields."
            return render_template("Contact.html", error=error)
    if request.method == 'GET':
        return render_template("Contact.html")

def checkSensors():
    print ("checking sensors")
    DB_Layer = DbClass()
    t_fine, T = mySensors.CalculateTemperature(temperatureCompensationParameters)
    humidity = mySensors.CalculateHumidity(humidityCompensationParameters, t_fine)
    raindrop = mySensors.ReadRaindDrop()
    windspeed = mySensors.ReadWindspeed()
    values = [T, windspeed, humidity,raindrop]
    print ("temperatuur: " + str(values[0]))
    print ("windspeed: " + str(values[1]))
    print ("humidity: " + str(values[2]))
    print ("RainDrop: "+str(raindrop))
    DB_Layer.saveSensorValuesToDatabase(values)



scheduler.add_job(func=camera.checkForPicture, trigger=IntervalTrigger(minutes=1), id='CheckCamera',
                  name='check if camera has to take picture', replace_existing=True)

scheduler.add_job(func=checkSensors, trigger=IntervalTrigger(minutes=1), id='CheckSensors',
                  name='Saving sensor values', replace_existing=True)

if __name__ == '__main__':
    app.run(host='192.168.0.12', port=5000, debug=False)

    # address already in use ?
    # lsof -i:port
    # kill PID
