from flask import Flask
from flask import request
from flask import render_template
from DbClass import DbClass
from CreateCharts import History
mycharts = History()
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import datetime
from Camera import PiCam
from lcdClass import LCD
from sensorClasses import sensors
LabelHours = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
LabelDays = [1, 2, 3, 4, 5, 6, 7]
myLCD = LCD(21, 0, 20, 0, 0, 0, 0, 16, 12, 25, 24)
myLCD.startDisplay()
myLCD.ShowText("Temp: ")
myLCD.ShowText("hum: ")
mySensors = sensors()
humidityCompensationParameters = mySensors.ReadCompensationParametersHumidity()
temperatureCompensationParameters = mySensors.ReadCompensationParametersTemp()
# camera = PiCam()
scheduler = BackgroundScheduler()
scheduler.start()
currentUser = []
app = Flask(__name__)
myLCD.ShowText("...")
myLCD.ShowText("...")

def checkSensors():
    global myLCD
    print ("checking sensors")
    today = datetime.datetime.today()
    moment = today.strftime("%y/%m/%d %H:%M")
    DB_Layer = DbClass()
    t_fine, T = mySensors.CalculateTemperature(temperatureCompensationParameters)
    humidity = mySensors.CalculateHumidity(humidityCompensationParameters, t_fine)
    raindrop = mySensors.ReadRaindDrop()
    windspeed = mySensors.ReadWindspeed()
    values = [T, windspeed, humidity, raindrop]
    myLCD.ShowText(str(T) + "C")
    myLCD.ShowText(str(humidity) + "%")
    DB_Layer.saveSensorValuesToDatabase(1, values, moment)
    print ("temperatuur: " + str(values[0]))
    print ("windspeed: " + str(values[1]))
    print ("humidity: " + str(values[2]))
    print ("RainDrop: " + str(raindrop))

@app.route('/', methods=['POST', 'GET'])
def LogIn():
    DB_Layer = DbClass()
    error = ""
    global WeerstationID
    global currentUser
    users = DB_Layer.getUsersFromDatabase()
    if request.method == 'POST':
        InputEmail = request.form.get('email')
        InputPassword = request.form.get('password')
        for i in range(len(users)):
            userData = users[i]
            currentUser=userData
            DBemail = userData[1]
            DBpassword = userData[2]
            if DBemail == InputEmail:
                if DBpassword == InputPassword:
                    WeerstationID = DB_Layer.getWeerstationIDFromUser(userData[0])
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
    SensorInfo = DB_Layer.getLatestDataFromDatabase()
    SensorInfo = SensorInfo[0]
    return render_template("Weather.html", SensorInfo=SensorInfo)

@app.route('/History', methods=['POST', 'GET'])
def History():
    if request.method == 'POST':
        if request.form['submit'] == "Day by Day":
            DailyTemp, DailyHum, DailyWindSpeed = mycharts.Daily()
            LabelDays2 = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            return render_template("History.html", Temp=DailyTemp, Hum=DailyHum, WindSpeed=DailyWindSpeed,
                                   labels=LabelDays)
        if request.form['submit'] == "Hour by Hour":
            HourlyTemp, HourlyHum, HourlyWindSpeed = mycharts.Hourly()
            return render_template("History.html", Temp=HourlyTemp, Hum=HourlyHum, WindSpeed=HourlyWindSpeed,
                                   labels=LabelHours)
    elif request.method == 'GET':
        return render_template("History.html")

# @app.route('/HistoryDaily')
# def HistoryDaily():

@app.route('/Contact', methods=['POST', 'GET'])
def Contact():
    error = ""
    succesful = "We have recieved your question, we will contact you by mail."
    DB_Layer = DbClass()
    if request.method == 'POST':
        Subject = request.form.get('Subject')
        Message = request.form.get('Message')
        print Message
        if Subject != "" and Message != "":
            DB_Layer.saveContactToDatabase(currentUser[0],Subject, Message)
            return render_template("Contact.html", succesful=succesful)
        else:
            error = "Please fill in both fields."
            return render_template("Contact.html", error=error)
    if request.method == 'GET':
        return render_template("Contact.html")

# scheduler.add_job(func=camera.checkForPicture, trigger=IntervalTrigger(minutes=1), id='CheckCamera',
#                   name='check if camera has to take picture', replace_existing=True)

scheduler.add_job(func=checkSensors, trigger=IntervalTrigger(seconds=10), id='CheckSensors',
                  name='Saving sensor values', replace_existing=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)