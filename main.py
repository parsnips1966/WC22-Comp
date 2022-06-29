from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from sqlalchemy.dialects.sqlite.json import JSON
from info import details

# SETUP
app = Flask(__name__)
app.config["SECRET_KEY"] = "abcxyz"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["UPLOAD_FOLDER"] = "static/files"
app.debug = True

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    predictions = db.Column(JSON)
    username = db.Column(db.String(20), unique=True)

# db.create_all()  # This is required on first-time ONLY


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        username = email[0: email.index('@')]
        password = request.form['password']

        user_obj = User.query.filter_by(email=email).first()

        if user_obj is None:
            return render_template("home.html", error="That email is not registered.")

        elif check_password_hash(user_obj.password, password):
            login_user(user_obj)
            return redirect(url_for("submitted"))

        else:
            return render_template("home.html", error="That password is incorrect.")

    return render_template("login.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    global user
    if request.method == "POST":
        email = request.form['email']
        username = email[0: email.index('@')]
        password = request.form['password']

        if User.query.filter_by(email=email).first() is not None:
            return render_template("home.html", error="That email is already in use, please login or use another one.")

        user = User(
            email=email, predictions={}, username=username,
            password=generate_password_hash(password, salt_length=8, method="pbkdf2:sha256")
        )

        db.session.add(user)  # Add user temporarily
        db.session.commit()  # Add user permanently

        login_user(user)
        return redirect(url_for("submitted"))

    return render_template("signup.html")


@app.route("/submitted", methods=['GET', 'POST'])
@login_required
def submitted():
    email = current_user.email
    username = current_user.username

    if request.method == "POST":
        for i in range(len(request.form)):
            save = user.predictions

        print(details[email]["predictions"])
        return render_template("submitted.html", username=username, predictions=user.predictions)

    return render_template("form.html", username=username)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run()
