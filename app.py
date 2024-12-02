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
        if request.form.get("addRow") == "insurance":
            return redirect(url_for("insertIntoHealthInsurance"))
        elif request.form.get("addRow") == "benefit":
            return redirect(url_for("insertIntoBenefits"))
        elif request.form.get("addRow") == "status":
            return redirect(url_for("insertIntoProjectStatus"))
        elif request.form.get("addRow") == "address":
            return redirect(url_for("insertIntoAddresses"))
        elif request.form.get("addRow") == "position":
            return redirect(url_for("insertIntoPositions"))
        elif request.form.get("addRow") == "department":
            return redirect(url_for("insertIntoDepartments"))
        elif request.form.get("addRow") == "employee":
            return redirect(url_for("insertIntoEmployeeInfo"))
        elif request.form.get("addRow") == "empBenefit":
            return redirect(url_for("insertIntoEmployeeBenefits"))
        elif request.form.get("addRow") == "project":
            return redirect(url_for("insertIntoProjects"))
        elif request.form.get("addRow") == "role":
            return redirect(url_for("insertIntoRoles"))
        elif request.form.get("addRow") == "empProject":
            return redirect(url_for("insertIntoEmployeeProjects"))
        elif request.form.get("addRow") == "empDep":
            return redirect(url_for("insertIntoEmployeeAssignments"))
    except:
        return render_template("error.html")
    return render_template("add.html")

@app.route("/update/", methods=["GET", "POST"])
def update():
    return render_template("query.html", query = "update") #placeholder

@app.route("/delete/", methods=["POST"])
def delete():
    return render_template("query.html", query = "delete") #placeholder

#Add pages
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
            min = request.form.get('i2')
            max = request.form.get('i3')
            return render_template("addPositions.html", added = position)
        except:
            return render_template('error.html')
    else: 
        return render_template("addPositions.html")

@app.route("/addProjects/", methods=['GET', 'POST'])
def insertIntoProjects():
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
    
@app.route("/addAddress/", methods=['GET', 'POST'])
def insertIntoAddresses():
    if request.method == 'POST':
        try:
            address = request.form.get('i1') 
            zip = request.form.get('i2')
            return render_template("addAddresses.html", added = address)
        except:
            return render_template('error.html')
    else: 
        return render_template("addAddresses.html")
    
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
    
@app.route("/addEmployeeInfo/", methods=['GET', 'POST'])
def insertIntoEmployeeInfo():
    if request.method == 'POST':
        try:
            id = request.form.get('id') 
            ssn = request.form.get('ssn')
            name = request.form.get('name')
            gender = request.form.get('gender')
            birth = request.form.get('birth')
            address = request.form.get('address')
            phone = request.form.get('phone')
            degree = request.form.get('degree')
            hPosition = request.form.get('hPosition')
            hSalary = request.form.get('hSalary')
            experience = request.form.get('experience')
            position = request.form.get('position')
            salary = request.form.get('salary')
            insurance = request.form.get('insurance')
            return render_template("addEmployeeInfo.html", added = name)
        except:
            return render_template('error.html')
    else: 
        return render_template("addEmployeeInfo.html")
    
@app.route("/addEmployeeBenefits/", methods=['GET', 'POST'])
def insertIntoEmployeeBenefits():
    if request.method == 'POST':
        try:
            emp = request.form.get('employee') 
            ben = request.form.get('benefit')
            start = request.form.get('start')
            end = request.form.get('end')
            return render_template("addEmployeeBenefits.html", added = emp)
        except:
            return render_template('error.html')
    else: 
        return render_template("addEmployeeBenefits.html")
    
@app.route("/addEmpAssignment/", methods=['GET', 'POST'])
def insertIntoEmployeeAssignments():
    if request.method == 'POST':
        try:
            emp = request.form.get('emp') 
            dep = request.form.get('dep')
            start = request.form.get('start')
            end = request.form.get('end')
            return render_template("addEmployeeAssignment.html", added = emp)
        except:
            return render_template('error.html')
    else: 
        return render_template("addEmployeeAssignments.html")