from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import redirect
from flask import session
from flask_bootstrap import Bootstrap

import sqlite3 as sql

app = Flask(__name__)
app.static_folder = 'static'

app.secret_key = 'secretkey'

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

# @app.route("/main/<userid>")

#http get route
#app.route
#create database and then pass in id and id extract information from that id


# def create_database():
#     conn = sql.connect("bank.db")
#     conn.execute("CREATE TABLE users (userid INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, fname TEXT, lname TEXT, phonenumber INTEGER, email TEXT, balance INT)")
#     conn.execute("CREATE TABLE transactions (transactionid INTEGER PRIMARY KEY AUTOINCREMENT, userid INTEGER, type TEXT, amount INTEGER, CONSTRAINT fk_users FOREIGN KEY (userid) REFERENCES users(userid))")
#     conn.close()

# create_database()

def add_transaction():
    with sql.connect("bank.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO transactions (userid, type, amount) VALUES (1, DEPOSIT, 1000)")
    con.commit()

@app.route("/testpage")
def list_data():
    con = sql.connect("bank.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM users")

    rows = cur.fetchall()

    cur.execute("SELECT * FROM transactions")
    rowstransactions = cur.fetchall()

    rows2 = cur.fetchall()
    return render_template("testpage.html", rows = rows, rows2 = rowstransactions)

@app.route("/addrec", methods=["POST"])
def addrec():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        fname = request.form["firstname"]
        lname = request.form["lastname"]
        phone = request.form["phonenumber"]
        email = request.form["email"]

        with sql.connect("bank.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO users (username, password, fname, lname, phonenumber, email, balance) VALUES (?, ?, ?, ?, ?, ?, 0)"
            , [username, password, fname, lname, phone, email])
        con.commit()

        return redirect(url_for('login_page'))

@app.route('/form_login', methods=['POST', 'GET'])
def login():
    
    session['loginusername'] = request.form['username']
    session['loginpassword'] = request.form['password']

    return redirect(url_for('createmain'))

    
@app.route('/newmain')
def createmain():
    loginusername = session['loginusername']
    loginpassword = session['loginpassword']

    con = sql.connect("bank.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", [loginusername, loginpassword])
    testquery = cur.fetchone()
    
    if testquery:
        return render_template('main.html', row = testquery)
    else:
        return redirect(url_for('login_page'))
        
    
    


        
# @app.route('/sendtocreateaccount', methods=['GET', 'POST'])
# def sendtocreateaccount():
#     if request.method == 'POST':
#         return render_template('createaccount.html')

# @app.route('/sendtologinpage', methods=['GET', 'POST'])
# def sendtologinpage():
#     if request.method == 'POST':
#         return render_template('login.html')

# @app.route('/mainlink', methods=['GET', 'POST'])
# def sendtomain():
#     if request.method == 'POST':
#         return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)
