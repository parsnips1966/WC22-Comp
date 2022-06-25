from flask import Flask, render_template, request
import json

with open("info.json", "r") as file:
    info = json.load(file)

app = Flask(__name__)
app.debug = True

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/formnew", methods=['GET', 'POST'])
def formnew():
    global email, username
    email = request.form['email']
    username = email[0: email.index('@')]
    input_password = request.form['password']
    #if email not in details.keys():
    #    details[email].password = input_password
    #    save = json.dumps(details)
    #    with open("details.json", "w") as file:
    #        file.write(save)
    return render_template("form.html", username=username)
    #return render_template("home.html", error="That email is already in use, please login or use another one.")

@app.route("/formreturn", methods=['GET', 'POST'])
def formreturn():
    global email, username
    email = request.form['email']
    username = email[0: email.index('@')]
    input_password = request.form['password']
    #if email in info():
    #    if input_password == info[email].password:
    return render_template("form.html", username=username)
    #    return render_template("home.html", error="That password is incorrect.")
    #return render_template("home.html", error="That email is not registered.")

@app.route("/submitted", methods=['GET', 'POST'])
def submitted():
    #for i in request.form:
    #    info[email].predictions.insert(i, request.form[i])
    #print(info[email].predictions)
    return render_template("submitted.html", username=username)
    #, predictions=info[email].predictions goes on previous line

if __name__ == "__main__":
    app.run()