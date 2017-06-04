from flask import Flask
from flask import request
from flask import render_template
from DbClass import DbClass
from Camera import PiCam
from BME280class import sensors

BME = sensors()
humidityCompensationParameters = BME.ReadCompensationParametersHumidity()
temperatureCompensationParameters = BME.ReadCompensationParametersTemp()
# camera=PiCam()
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

scheduler = BackgroundScheduler()
scheduler.start()


def PrintTime():
    print("this runs every 5 seconds")


def CheckCamera():
    print ("we checken of het tijd is om een foto te nemen")


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
            DBemail = userData[0]
            DBpassword = userData[1]
            if DBemail == InputEmail:
                if DBpassword == InputPassword:
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
    print (SensorInfo)
    return render_template("Weather.html")


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


# scheduler.add_job(func=camera.checkForPicture, trigger=IntervalTrigger(minutes=10), id='CheckCamera',
#                   name='check if camera has to take picture', replace_existing=True)

# def checkBME():
#     t_fine, T = BME.calculateTemperature(temperatureCompensationParameters)
#     print T
#     print t_fine
#     humidity = BME.calculateHumidity(humidityCompensationParameters, t_fine)
#     print humidity
#     BMEvalues = [humidity, T]
#
#
# scheduler.add_job(func=BME.calculateTemperature, trigger=IntervalTrigger(minutes=1), id='CheckTemp',
#                   name='Updating temperature', replace_existing=True)

if __name__ == '__main__':
    app.run(host='192.168.0.12', port=5000, debug=False)

    # address already in use ?
    # lsof -i:port
    # kill PID
