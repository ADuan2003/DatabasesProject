from flask import Flask
from flask import render_template, request
from database import * 

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/add/", methods=["POST"])
def add():
    return render_template("query.html", query = "add")

@app.route("/update/", methods=["POST"])
def update():
    return render_template("query.html", query = "update")

@app.route("/delete/", methods=["POST"])
def delete():
    return render_template("query.html", query = "delete")

@app.route("/query/")
def queryPage():
    return render_template("query.html")

@app.route("/showall/", methods=['POST'])
def showall():
    table = request.form.get("show")
    return render_template("query.html", query = table)