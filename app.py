from flask import Flask
from flask import render_template, request
from database import * 

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/query/", methods =['GET', 'POST'])
def queryPage():
    table = None
    if request.method == ['POST']:
        table = request.form.get('show') #for some reason this isn't getting set... 
    return render_template("query.html", query = table)