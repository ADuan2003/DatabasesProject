from flask import Flask
from flask import render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

###remove later? 
@app.route("/query/")
def queryPage():
    return render_template("query.html")

@app.route("/showall/", methods=['POST'])
def showall():
    table = request.form.get("show")
    return render_template("query.html", query = table)
###

@app.route("/add/", methods=["POST"])
def add():
    try:
        if request.form.get("addRow") == "Health Insurance":
            return redirect(url_for("insertIntoHealthInsurance"))
        elif request.form.get("addRow") == "BenefitType":
            return render_template("add.html")
    except:
        return render_template("error.html")
    return render_template("add.html")

@app.route("/update/", methods=["GET", "POST"])
def update():
    return render_template("query.html", query = "update") #placeholder

@app.route("/delete/", methods=["POST"])
def delete():
    return render_template("query.html", query = "delete") #placeholder

@app.route("/addHealthInsurance/", methods=['GET', 'POST'])
def insertIntoHealthInsurance():
    if request.method == 'POST':
        try:
            coverage = request.form.get('insertHI') #request.form['insertHI']
            #added = insertIntoHealthInsurance(coverage)
            return render_template("addHealthInsurance.html", added = coverage)
        except:
            return render_template('error.html')
    else: 
        return render_template("addHealthInsurance.html")
    
@app.route("/addBenefit/", methods=['GET', 'POST'])
def insertIntoBenefits():
    if request.method == 'POST':
        try:
            benefit = request.form.get('i1') 
            return render_template("addBenefits.html", added = benefit)
        except:
            return render_template('error.html')
    else: 
        return render_template("addBenefits.html")
    
@app.route("/addDepartment/", methods=['GET', 'POST'])
def insertIntoDepartments():
    if request.method == 'POST':
        try:
            dep = request.form.get('i1') 
            return render_template("addDepartments.html", added = dep)
        except:
            return render_template('error.html')
    else: 
        return render_template("addDepartments.html")
    
@app.route("/addPosition/", methods=['GET', 'POST'])
def insertIntoPositions():
    if request.method == 'POST':
        try:
            position = request.form.get('i1') 
            return render_template("addPositions.html", added = position)
        except:
            return render_template('error.html')
    else: 
        return render_template("addPosition.html")

@app.route("/addProjects/", methods=['GET', 'POST'])
def insertIntoDepartments():
    if request.method == 'POST':
        try:
            project = request.form.get('projectName') 
            dep = request.form.get('department')
            leader = request.form.get('leader')
            status = request.form.get('status')
            return render_template("addProjects.html", added = project)
        except:
            return render_template('error.html')
    else: 
        return render_template("addProjects.html")
    
@app.route("/addRoles/", methods=['GET', 'POST'])
def insertIntoRoles():
    if request.method == 'POST':
        try:
            role = request.form.get('i1') 
            return render_template("addRoles.html", added = role)
        except:
            return render_template('error.html')
    else: 
        return render_template("addRoles.html")

@app.route("/addProjectStatus/", methods=['GET', 'POST'])
def insertIntoProjectStatus():
    if request.method == 'POST':
        try:
            status = request.form.get('i1') 
            return render_template("addProjectStatus.html", added = status)
        except:
            return render_template('error.html')
    else: 
        return render_template("addProjectStatus.html")
    
@app.route("/addEmployeeProjects/", methods=['GET', 'POST'])
def insertIntoEmployeeProjects():
    if request.method == 'POST':
        try:
            employee = request.form.get('employee') 
            project = request.form.get('project')
            role = request.form.get('role')
            start = request.form.get('start')
            end = request.form.get('end')
            return render_template("addEmployeeProjects.html", added = employee)
        except:
            return render_template('error.html')
    else: 
        return render_template("addEmployeeProjects.html")