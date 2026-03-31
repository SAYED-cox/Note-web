from package import module flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Change this to a secure key

# Database setup (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20))
    class_no = db.Column(db.String(50))
    topic = db.Column(db.String(200))

# Create tables
with app.app_context():
    db.create_all()

# Simple username/password
USERNAME = "admin"
PASSWORD = "1234"

# Login page
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            return redirect("/notes")
        else:
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")

# Notes page
@app.route("/notes", methods=["GET", "POST"])
def notes_page():
    if not session.get("logged_in"):
        return redirect("/")
    if request.method == "POST":
        date = request.form["date"]
        class_no = request.form["class_no"]
        topic = request.form["topic"]
        new_note = Note(date=date, class_no=class_no, topic=topic)
        db.session.add(new_note)
        db.session.commit()
        return redirect("/notes")
    all_notes = Note.query.order_by(Note.id.desc()).all()
    return render_template("notes.html", notes=all_notes, today=datetime.today().strftime('%Y-%m-%d'))

# Logout
@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
    