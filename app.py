from flask import Flask, request, render_template, session
import mysql.connector
import random
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask apps
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Database connection
mydb = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME')
)

# Email server setup
server = smtplib.SMTP('smtp.office365.com', 587)
server.starttls()
server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASSWORD'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails['name']
        password = userDetails['pass']
        email = userDetails['email']

        # Generate a unique ID for the user
        rid = random.randint(10000, 99999)

        # Email content
        email_content = f"This is your unique ID which you will require to log in to the ParkoBuddy app.\nUNIQUE ID: {rid}"
        msg = EmailMessage()
        msg['subject'] = "Unique ID"
        msg['from'] = os.getenv('EMAIL_USER')
        msg['to'] = email
        msg.set_content(email_content)

        # Send email
        server.send_message(msg)

        # Insert user details into the database
        cur = mydb.cursor()
        cur.execute(
            "INSERT INTO users (u_id, username, password) VALUES (%s, %s, %s)",
            (rid, name, password)
        )
        mydb.commit()
        cur.close()

        return render_template('login.html')
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get("nm")
        password = request.form.get('pass')
        uid = int(request.form.get("uid"))

        # Check user credentials
        cur = mydb.cursor(dictionary=True)
        cur.execute(
            "SELECT * FROM users WHERE u_id = %s AND username = %s AND password = %s",
            (uid, name, password)
        )
        user = cur.fetchone()
        cur.close()

        if user:
            session['user_id'] = user['u_id']
            return render_template("user.html", d=user['username'], uid=uid)
        else:
            return "Invalid credentials"
    return render_template('login.html')


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        userDetails = request.form
        region = userDetails['reg']

        # Map region to query
        query_map = {
            "centd": ("Central Delhi", "SELECT Location, total, inuse FROM centd"),
            "od": ("Old Delhi", "SELECT Location, total, inuse FROM od"),
            "sd": ("South Delhi", "SELECT Location, total, inuse FROM sd")
        }

        if region in query_map:
            area, query = query_map[region]
            cur = mydb.cursor(dictionary=True)
            cur.execute(query)
            data = cur.fetchall()
            cur.close()

            headings = ("Address", "Total Space", "Occupied")
            return render_template("data.html", headings=headings, data=data, ar=area)
    return render_template('index.html')


@app.route('/user', methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        userDetails = request.form
        region = userDetails['reg']
        usid = userDetails['uid']

        # Map region to query
        query_map = {
            "centd": ("Central Delhi", "SELECT Location, total, inuse, total-inuse AS Vacant, p_id FROM centd WHERE own_id = %s"),
            "od": ("Old Delhi", "SELECT Location, total, inuse, total-inuse AS Vacant, p_id FROM od WHERE own_id = %s"),
            "sd": ("South Delhi", "SELECT Location, total, inuse, total-inuse AS Vacant, p_id FROM sd WHERE own_id = %s")
        }

        if region in query_map:
            area, query = query_map[region]
            cur = mydb.cursor(dictionary=True)
            cur.execute(query, (usid,))
            data = cur.fetchall()
            cur.close()

            headings = ("Address", "Total Space", "Occupied", "Vacant", "Parking ID")
            return render_template("data2.html", headings=headings, data=data, ar=area)
    return render_template('user.html')


@app.route('/new', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        form = request.form
        uid = form.get('ud')
        loc = form.get('loc')
        tc = form.get('tc')
        region = form.get('reg')
        inu = 0
        pid = random.randint(1000, 9999)

        # Map region to table
        table_map = {
            "centd": "centd",
            "od": "od",
            "sd": "sd"
        }

        if region in table_map:
            table = table_map[region]
            cur = mydb.cursor()
            cur.execute(
                f"INSERT INTO {table} (Location, total, inuse, own_id, p_id) VALUES (%s, %s, %s, %s, %s)",
                (loc, tc, inu, uid, pid)
            )
            mydb.commit()
            cur.close()
            return render_template('success.html')
    return render_template("add-new.html")


@app.route('/remove', methods=['GET', 'POST'])
def remove():
    if request.method == 'POST':
        form = request.form
        pid = form.get('pic')
        region = form.get('reg')

        # Map region to table
        table_map = {
            "centd": "centd",
            "od": "od",
            "sd": "sd"
        }

        if region in table_map:
            table = table_map[region]
            cur = mydb.cursor()
            cur.execute(f"DELETE FROM {table} WHERE p_id = %s", (pid,))
            mydb.commit()
            cur.close()
            return render_template('success1.html')
    return render_template("remove.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
