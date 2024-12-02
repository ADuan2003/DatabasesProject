from flask import Flask
from flask import render_template, request
from database import * 

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route("/query/")
def queryPage():
    return render_template("query.html")

@app.route("/showall/", methods=['POST'])
def showall():
    table = request.form.get("show")
    return render_template("query.html", query = table)