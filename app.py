from flask import Flask, render_template , request, redirect, url_for ,session,flash
from models import db, Horse, Rider, Session


import os

app = Flask(__name__)

# Get DB connection string from environment variable
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://horsestabledb_user:5mqDX3DRyr1d6fOzcXf9seXOQ9Mp2u1i@dpg-d2cha33uibrs738gnpe0-a.oregon-postgres.render.com/horsestabledb' 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

db.init_app(app)

'''@app.route('/init-db')
def init_db():
    from models import db
    db.create_all()
    return "Database tables created."'''

@app.route("/add-horse", methods=["GET", "POST"])
def add_horse():
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        if name and age:
            horse = Horse(name=name, age=int(age))
            db.session.add(horse)
            db.session.commit()
            return redirect(url_for("home"))
    return render_template("add_horse.html")

@app.route("/add-rider", methods=["GET", "POST"])
def add_rider():
    if request.method == "POST":
        name = request.form.get("name")
        level = request.form.get("level")
        if name and level:
            rider = Rider(name=name, level=level)
            db.session.add(rider)
            db.session.commit()
            return redirect(url_for("home"))
    return render_template("add_rider.html")

@app.route("/app-login", methods=["GET", "POST"])
def app_login():
    return render_template("login.html")

@app.route("/testhorse")
def testhorse():
    return render_template("testHorse.html")

@app.route("/")
def home():
    """if 'user_id' not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for('app_login'))"""
    horses = Horse.query.all()
    riders = Rider.query.all()
    sessions = Session.query.all()
    return render_template("index.html", horses=horses, riders=riders, sessions=sessions)

if __name__ == "__main__":
    app.run#(debug=True)
