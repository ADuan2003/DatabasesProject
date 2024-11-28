from flask import Flask
from flask import render_template
from database import * 

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/query/")
def queryPage():
    return render_template("query.html")