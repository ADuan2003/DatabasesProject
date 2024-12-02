from flask import Flask
from flask import render_template, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/add/", methods=["POST"])
def add():
    operation = None
    try:
        if request.form.get("addRow") == "Health Insurance":
            return render_template("addHealthInsurance.html")
        elif request.form.get("addRow") == "BenefitType":
            return render_template("home.html")
    except:
        return render_template("error.html")
    return render_template("home.html")

@app.route("/update/", methods=["POST"])
def update():
    return render_template("query.html", query = "update") #placeholder

@app.route("/delete/", methods=["POST"])
def delete():
    return render_template("query.html", query = "delete") #placeholder

@app.route("/query/")
def queryPage():
    return render_template("query.html")

@app.route("/showall/", methods=['POST'])
def showall():
    table = request.form.get("show")
    return render_template("query.html", query = table)

@app.route("/addHealthInsurance/", methods=['GET', 'POST'])
def insertIntoHealthInsurance():
    if request.method == 'POST':
        try:
            coverage = request.form.get('insertHI') #request.form['insertHI']
            added = insertIntoHealthInsurance(coverage)
            return render_template("addHealthInsurance.html", added = added)
        except:
            return render_template('error.html')
    else: 
        return render_template("addHealthInsurance.html")