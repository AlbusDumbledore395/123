from flask import Flask, render_template, request, redirect, url_for, g, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)

DATABASE = 'users.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        cursor = db.cursor()

        # Check if the username and password match an entry in the database
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            return redirect(url_for('success'))  # Redirect to the success page or main dashboard
        else:
            return "Invalid username or password. Please try again."

    return render_template('index.html')  # Show the login page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the password meets complexity requirements

        db = get_db()
        cursor = db.cursor()

        # Check if the username already exists
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user:
            return render_template('signup.html', error='Username already exists. Please choose another username.')

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        db.commit()

        return redirect(url_for('success'))

    return render_template('index.html') # Show the signup page

@app.route('/logout')
def logout():
    return render_template('index.html')
@app.route('/success')
def success():
    return render_template('Qrater.html')
@app.route('/failure')
def failure():
    return render_template('signup.html')
@app.route('/portfolio')
def portfolio():
    return render_template('home.html')
@app.route('/insta')
def insta():
    return redirect('https://www.instagram.com/itz_coolest_ravana_21/')
@app.route('/data_structure')
def data_structure():
    return render_template('python.html')
@app.route('/OS')
def OS():
    return render_template('OS.html')
@app.route('/exists')
def exists():
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
