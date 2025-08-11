from flask import Flask, render_template
from models import db, Horse, Rider, Session
import os

app = Flask(__name__)

# Get DB connection string from environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/init-db')
def init_db():
    from models import db
    db.create_all()
    return "Database tables created."


@app.route("/")
def home():
    horses = Horse.query.all()
    riders = Rider.query.all()
    sessions = Session.query.all()
    return render_template("index.html", horses=horses, riders=riders, sessions=sessions)

if __name__ == "__main__":
    app.run
