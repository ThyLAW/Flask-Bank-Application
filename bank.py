from flask import Flask
from flask import render_template
from flask import url_for
from flask import request
from flask import redirect
from flask import session
from flask_bootstrap import Bootstrap

import sqlite3 as sql

app = Flask(__name__)

# Creates the secret key, should be more secure in production.


app.secret_key = 'secretkey'

# static routs, some not used
    
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

# Creates the database. Delete old database and then uncomment the following script and then run to create
# the database. Cretes the users and transactions tables.

# def create_database():
#     conn = sql.connect("bank.db")
#     conn.execute("CREATE TABLE users (userid INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, fname TEXT, lname TEXT, phonenumber INTEGER, email TEXT, balance INT)")
#     conn.execute("CREATE TABLE transactions (transactionid INTEGER PRIMARY KEY AUTOINCREMENT, userid INTEGER, type TEXT, amount INTEGER, CONSTRAINT fk_users FOREIGN KEY (userid) REFERENCES users(userid))")
#     conn.close()

# create_database()

# Code for the test page. Simply displays all of the information from the database on this page for both tables.

@app.route("/testpage")
def list_data():
    con = sql.connect("bank.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    
    rows = cur.fetchall()
    con.commit()

    con = sql.connect("bank.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("SELECT * FROM transactions")
    rowstransactions = cur.fetchall()

    rows2 = cur.fetchall()
    return render_template("testpage.html", rows = rows, rows2 = rowstransactions)

# Used in createaccount.html form. Extracts information from form and inserts it into the database.
# Then sends back to login page if completed succesfully.
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

# Takes information from login.html. Gets the form.values and inserts them as session variables. If not done
# this way, the app will crash when navigating away from the main page. AFter storing values, the page redirects
# to create main method.

@app.route('/form_login', methods=['POST', 'GET'])
def login():
    
    session['loginusername'] = request.form['username']
    session['loginpassword'] = request.form['password']

    return redirect(url_for('createmain'))

#Populates the main.html file with information. 

@app.route('/newmain')
def createmain():

    #Takes values from sessions and makes them local variables

    loginusername = session['loginusername']
    loginpassword = session['loginpassword']

    # Gets all of the inforamtion for a user where username = loginusername. Stores it in testquery variable.
    con = sql.connect("bank.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username=? AND password=?", [loginusername, loginpassword])
    testquery = cur.fetchone()
    con.commit()

    #Used to get the userid. Data originates as a tuple, this makes it into a single text variable.
    con = sql.connect("bank.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    query = cur.execute("SELECT userid FROM users WHERE username = ? ", [loginusername])

    # checks if row[0] exists first. if not, makes user id = 0. this is so that the application does not crash.
    row = cur.fetchone()
    if row:
        session['userid'] = row[0]
    else:
        session['userid'] = 0

    # Gets all of the transactions when equal to session stored user id.
    con = sql.connect("bank.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM transactions WHERE userid = ?", [session['userid']])
    rowstransactions2 = cur.fetchall()
    rows3 = cur.fetchall()
    con.commit()
    
    # if testquery finds a match of username and password, displays main.html with populated data. Else, returns to login page
    if testquery:
        return render_template('main.html', row = testquery, rows3 = rowstransactions2)
    else:
        return redirect(url_for('login_page'))

    
    #   Adds a transaction to the transactions table from the main.html form
        
@app.route('/addtransaction', methods=['POST', 'GET'])
def addtransaction():

    #receives information from the form, determines what radio button was picked

    formamount = request.form['amount']
    button = request.form['flexRadioDefault']
    transactiontype = "Deposit"
    if button == 'Deposit':
        transactiontype = 'Deposit'
    else:
        transactiontype = 'Withdrawal'
  
    # inserts into table, and then updates the balance for the user id depending on choice of deposit or withdrawal
    with sql.connect("bank.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO transactions (userid, type, amount) VALUES (?, ?, ?)" , [session['userid'], transactiontype, formamount])
        if transactiontype == 'Deposit':
            cur.execute("UPDATE users SET balance = (balance + ?) WHERE username = ?", [formamount, session['loginusername']])
        elif transactiontype == 'Withdrawal':
            cur.execute("UPDATE users SET balance = (balance - ?) WHERE username = ?", [formamount, session['loginusername']])
        con.commit()
    return redirect(url_for('createmain'))
    
if __name__ == '__main__':
    app.run(debug=True)
