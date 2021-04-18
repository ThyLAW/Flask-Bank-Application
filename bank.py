from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask_bootstrap import Bootstrap

import sqlite3 as sql

app = Flask(__name__)
app.static_folder = 'static'


@app.route("/")
def default_page():
    return render_template("login.html")
    
@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/createaccount")
def createaccount_page():
    return render_template("createaccount.html")

@app.route("/main")
def main_page():
    return render_template("main.html")

@app.route("/about")
def about_page():
    return render_template("about.html")

    
@app.route('/sendtocreateaccount', methods=['GET', 'POST'])
def sendtocreateaccount():
    if request.method == 'POST':
        return render_template('createaccount.html')

@app.route('/sendtologinpage', methods=['GET', 'POST'])
def sendtologinpage():
    if request.method == 'POST':
        return render_template('login.html')

@app.route('/mainlink', methods=['GET', 'POST'])
def sendtomain():
    if request.method == 'POST':
        return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)
