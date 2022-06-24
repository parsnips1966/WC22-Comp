from flask import Flask, render_template, request
import json
import info

details = info.details
countries = info.countries

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
    global username
    email = request.form['email']
    username = email[0: email.index('@')]
    password = request.form['password']
    if email not in details.keys():
        details[email] = password
        save = json.dumps(details)
        with open("details.json", "w") as file:
            file.write(save)
        return render_template("form.html", username=username, countries=countries)
    return render_template("home.html", error="That email is already in use, please login or use another one.")

@app.route("/formreturn", methods=['GET', 'POST'])
def formreturn():
    email = request.form['email']
    username = email[0: email.index('@')]
    password = request.form['password']
    if email in details.keys():
        if password == details[email]:
            return render_template("form.html", username=username, countries=countries)
        return render_template("home.html", error="That password is incorrect.")
    return render_template("home.html", error="That email is not registered.")

@app.route("/submitted", methods=['GET', 'POST'])
def submitted():
    items = []
    for i in request.form:
        items.append(request.form[i])
    return render_template("submitted.html", username=username, items=items)

if __name__ == "__main__":
    app.run()