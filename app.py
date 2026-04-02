from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect("database.db")

def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS songs(id INTEGER PRIMARY KEY, song_name TEXT, mood TEXT)")
    db.commit()

init_db()

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user,pwd))
        data = cursor.fetchone()
        if data:
            session['user'] = user
            return redirect('/dashboard')
        else:
            return "Invalid Login"
    return render_template("login.html")

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO users(username,password) VALUES(?,?)",(user,pwd))
        db.commit()
        return redirect('/')
    return render_template("register.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route('/mood')
def mood():
    return render_template("mood.html")

@app.route('/songs', methods=['POST'])
def songs():
    mood = request.form['mood']
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM songs WHERE mood=?", (mood,))
    data = cursor.fetchall()
    return render_template("songs.html", songs=data)

@app.route('/add_song', methods=['GET','POST'])
def add_song():
    if request.method == 'POST':
        name = request.form['song']
        mood = request.form['mood']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO songs(song_name,mood) VALUES(?,?)",(name,mood))
        db.commit()
        return "Song Added Successfully"
    return render_template("add_song.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
