from flask import Flask, render_template , request, redirect, url_for ,session,flash ,jsonify
from models import db, Horse, Rider , Trining_class ,User ,RiderSub ,Paddock
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime



import os

app = Flask(__name__)

# Get DB connection string from environment variable

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

db.init_app(app)

@app.route('/init-db')
def init_db():
    from models import db
    db.create_all()
    return "Database tables created."

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
        phone = request.form.get("phone")
        email = request.form.get("email")
        if name and level:
            rider = Rider(name=name, level=level , mobile=phone, email=email)
            db.session.add(rider)
            db.session.commit()
            return redirect(url_for("home"))
    return render_template("add_rider.html")

@app.route("/app-login", methods=["GET", "POST"])
def app_login():
    if request.method == "POST":
        if request.form.get("do") == "register":
            email = request.form.get("email")
            fullName = request.form.get("fullName")
            Username = request.form.get("Username")
            hash_pass =  generate_password_hash(request.form.get("Password"), method='pbkdf2:sha256')
            mobile = request.form.get("mobile")
            new_user = User(username=Username, password=hash_pass ,email=email,mobile=mobile,fullname=fullName,role="Rider" )
            db.session.add(new_user)
            db.session.commit()
            flash("User registered successfully!", "success")
            return redirect(url_for('home'))
        else:
            user = User.query.filter_by(username=request.form['Username']).first()
            if user and check_password_hash(user.password, request.form['Password']):
                session['user_id'] = user.id
                session['username'] = user.username
                session['role'] = user.role
                if user.role == 'Rider':
                    rider = Rider.query.filter_by(user_id=user.id).first()
                    flash("Login successful!", "success")
                    session['rider_id'] = rider.id
                    return redirect(url_for('rider_detail' , rider_id=rider.id))
                elif user.role == 'admin':
                    flash("Login successful!", "success")
                    return redirect(url_for('home'))

            else:
                flash("Invalid username or password", "danger")

    return render_template("login.html")


@app.route("/testhorse")
def testhorse():
    return render_template("testHorse.html")

@app.route("/rider/<int:rider_id>")
def rider_detail(rider_id):
    # Get the rider and subscriptions in one go
    rider = Rider.query.get_or_404(rider_id)

    # subscriptions come from the relationship in the model
    subscriptions = rider.subscriptions  

    return render_template("rider_detail.html", rider=rider, subscriptions=subscriptions)


@app.route("/rider/<int:rider_id>/add_subscription_ajax", methods=["POST"])
def add_subscription_ajax(rider_id):
    try:
        start_date_str = request.form["start_date"]
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        active = "active" in request.form

        new_sub = RiderSub(
            start_date=start_date,
            rider_id=rider_id,
            active=active
        )
        db.session.add(new_sub)
        db.session.commit()

        return jsonify({
            "success": True,
            "data": {
                "start_date": start_date_str,
                "active": active
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route("/" , methods=["GET", "POST"] )
def home():
    if 'user_id' not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for('app_login'))
    elif session['role']=='admin':
        if request.method == "POST":
            date_str = request.form["date"]
            time_str = request.form["time"]
            datetime_str = f"{date_str} {time_str}"
            new_class = Trining_class(
                date=datetime.strptime(datetime_str, "%Y-%m-%d %H:%M"),
                horse_id=request.form["horse_id"],
                rider_id=request.form["rider_id"],
                paddock_id=request.form["paddock_id"]
            )
            db.session.add(new_class)
            db.session.commit()
            return redirect(url_for("home"))  # Redirect after insert
            
        horses = Horse.query.all()
        riders = Rider.query.all()
        paddocks = Paddock.query.all()
        #sessions = Session.query.all()
        return render_template("index.html", horses=horses, riders=riders , paddocks=paddocks) #, sessions=sessions)
    else:
        return redirect(url_for('rider_detail' , rider_id=session['rider_id']))

if __name__ == "__main__":
    app.run (debug=True)
