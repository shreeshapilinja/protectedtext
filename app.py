import os
import sqlite3 as s
from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.config['SECRET_KEY'] = '9353917389'

# Function to create the user database and user_info table
def create_user_database(username):
    user_db_path = os.path.join('databases', f'{username}.db')
    # Check if the user's database exists
    if not os.path.exists(user_db_path):
        conn = s.connect(user_db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_info (
                id INTEGER PRIMARY KEY,
                user_id TEXT,
                text TEXT,
                FOREIGN KEY (user_id) REFERENCES users (username)
            )
        ''')
        conn.commit()
        conn.close()

def check_user_and_auth(username, password):
    conn = s.connect('user_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, password FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()

    if user is None:
        flash('User not found. Creating a new user.')
        conn = s.connect('user_database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        create_user_database(username)
        session['username'] = username
        return True
    elif user[1] == password:
        session['username'] = username
        return True
    else:
        return False


# Home page
@app.route('/')
def home():
    auth_param = request.args.get('')
    if auth_param:
        username, password = auth_param.split('@')
        if check_user_and_auth(username, password):
            return redirect(url_for('dashboard', username=username))
        else:
            return render_template('home.html',error="Incorrect Password or User Already Exits")
    return render_template('home.html',error='')

# Login route
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_user_and_auth(username, password):
            return redirect(url_for('dashboard', username=username))
        else:
            return render_template('home.html', error="Incorrect Password or User Already Exists")
    return redirect(url_for('home', error="Invalid request"))


# Dashboard page
@app.route('/dashboard/<username>', methods=['GET', 'POST'])
def dashboard(username):
    if 'username' in session and session['username'] == username:
        user_db_path = os.path.join('databases', f'{username}.db')
        if request.method == 'POST':
            text = request.form['text']
            conn = s.connect(user_db_path)
            cursor = conn.cursor()
            
            # Check if a row exists for this user
            cursor.execute('SELECT * FROM user_info WHERE user_id = ?', (username,))
            existing_row = cursor.fetchone()
            
            if existing_row:
                # Update the existing row
                cursor.execute('UPDATE user_info SET text = ? WHERE user_id = ?', (text, username))
            else:
                # Insert a new row
                cursor.execute('INSERT INTO user_info (user_id, text) VALUES (?, ?)', (username, text))
                
            conn.commit()
            conn.close()

        conn = s.connect(user_db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT text FROM user_info WHERE user_id = ?', (username,))
        result = cursor.fetchone()
        text = result[0] if result else ""
        conn.close()

        return render_template('dashboard.html', username=username, text=text)
    else:
        return render_template('home.html', error="Unauthorized")


@app.route('/logout')
def logout():
    # Clear the session to log out the user
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
