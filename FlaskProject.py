from flask import Flask
from flask import request
from flask import render_template
import os
app = Flask(__name__)
import time

@app.route('/', methods=['POST', 'GET'])
def LogIn():
    error = ""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(email)
        print(password)
        if email == "jannes.derycke@hotmail.com" and password == "jannes":
            return render_template("Home.html")
        else:
            error = "Email or password are incorrect."
            return render_template("LogIn.html", error=error)
    if request.method == 'GET':
        return render_template("LogIn.html")


@app.route('/Home')
def Home():
    return render_template("Home.html")


@app.route('/Weather')
def TheWeather():
    return render_template("Weather.html")


@app.route('/History')
def History():
    return render_template("History.html")


@app.route('/Contact')
def Contact():
    return render_template("Contact.html")


if __name__ == '__main__':
    app.run(host='172.30.252.30', port=5000, debug=True)