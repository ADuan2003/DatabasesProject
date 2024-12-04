from flask import Flask
from flask import render_template, request, redirect, url_for
import sqlite3

#Connect to sqlLite database (or create if it doesn't exist)
conn = sqlite3.connect('database.db')

#Create a cursor object
cursor = conn.cursor()

#Create a table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Addresses
  (address TEXT NOT NULL,
  zipCode TEXT NOT NULL,
  PRIMARY KEY (address));
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Positions 
(position TEXT NOT NULL,
  minSalary INT NOT NULL,
  maxSalary INT NOT NULL,
  PRIMARY KEY (position),
  CHECK (0 < minSalary),
  CHECK (minSalary <= maxSalary));
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS HealthInsurance
(coverage TEXT NOT NULL,
  PRIMARY KEY (coverage));
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS EmployeeInfo
(EmployeeID TEXT NOT NULL,
  SSN TEXT NOT NULL,
  Name TEXT NOT NULL,
  gender TEXT NOT NULL,
  DoB DATE NOT NULL,
  PrimaryAddress TEXT NOT NULL,
  PhoneNumber TEXT NOT NULL,
  HighestDegree TEXT NOT NULL,
  YearsExperience INT NOT NULL,
  HiringPosition TEXT NOT NULL,
  HiringSalary INT NOT NULL,
  CurrentPosition TEXT NOT NULL,
  CurrentSalary INT NOT NULL,
  Coverage TEXT NOT NULL,
  FOREIGN KEY (HiringPosition) REFERENCES Positions(position) ON DELETE CASCADE,
  FOREIGN KEY (CurrentPosition) REFERENCES Positions(position) ON DELETE CASCADE,
  FOREIGN KEY (Coverage) REFERENCES HealthInsurance(coverage) ON DELETE CASCADE,
  PRIMARY KEY (EmployeeID));
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Departments
(department TEXT NOT NULL,
  PRIMARY KEY (department));
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS EmployeeAssignments
(EmployeeID TEXT NOT NULL,
  Department TEXT NOT NULL,
  StartDate DATE NOT NULL,
  EndDate DATE, 
  FOREIGN KEY (EmployeeID) REFERENCES EmployeeInfo(EmployeeID) ON DELETE CASCADE,
  FOREIGN KEY (Department) REFERENCES Departments(department) ON DELETE CASCADE,
  PRIMARY KEY (EmployeeID, Department, StartDate)); 
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Benefits
(benefit TEXT NOT NULL,
  PRIMARY KEY (benefit));
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS EmployeeBenefits 
(EmployeeID TEXT NOT NULL,
  Benefit TEXT NOT NULL,
  StartDate DATE NOT NULL,
  EndDate DATE,
  FOREIGN KEY (EmployeeID) REFERENCES EmployeeInfo(EmployeeID) ON DELETE CASCADE,
  FOREIGN KEY (Benefit) REFERENCES Benefits(benefit) ON DELETE CASCADE,
  PRIMARY KEY (EmployeeID, Benefit, StartDate)); 
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS ProjectStatus
(status TEXT NOT NULL,
  PRIMARY KEY (status));
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Projects
(Project TEXT NOT NULL,
  Department TEXT NOT NULL,
  ProjectLeader TEXT NOT NULL,
  Status TEXT NOT NULL,
  FOREIGN KEY (Department) REFERENCES Department(department) ON DELETE CASCADE,
  FOREIGN KEY (ProjectLeader) REFERENCES EmployeeInfo(EmployeeID) ON DELETE CASCADE,
  FOREIGN KEY (Status) REFERENCES ProjectStatus(status) ON DELETE CASCADE,
  PRIMARY KEY (Project));
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Roles
(role TEXT NOT NULL,
  PRIMARY KEY (role));
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS EmployeeProjects
(EmployeeID TEXT NOT NULL,
  Project TEXT NOT NULL,
  Role TEXT NOT NULL,
  StartDate DATE NOT NULL,
  EndDate DATE, 
  FOREIGN KEY (EmployeeID) REFERENCES EmployeeInfo(EmployeeID) ON DELETE CASCADE,
  FOREIGN KEY (Project) REFERENCES Projects(Project) ON DELETE CASCADE,
  FOREIGN KEY (Role) REFERENCES Roles(role) ON DELETE CASCADE,
  PRIMARY KEY (EmployeeID, Project, Role)); 
''')

#default values
cursor.execute('insert into Benefits values (\'health\')')
cursor.execute('insert into Benefits values (\'dental\')')
cursor.execute('insert into Benefits values (\'life insurance\')')
cursor.execute('insert into Benefits values (\'short/long term disability\')')
cursor.execute('insert into HealthInsurance values (\'kaiser\')')
cursor.execute('insert into HealthInsurance values (\'Affordable Care Act\')')
cursor.execute('insert into HealthInsurance values (\'family member\')')
cursor.execute('insert into HealthInsurance values (\'company\')')
cursor.execute('insert into HealthInsurance values (\'Medicare\')')
cursor.execute('insert into Departments values (\'cs\')')
cursor.execute('insert into Departments values (\'eng\')')
cursor.execute('insert into Positions values (\'scientist\', 100, 1000)')
cursor.execute('insert into Positions values (\'temp\', 10, 20)')
cursor.execute('insert into Positions values (\'research scientist\', 200, 1000)')
cursor.execute('insert into Positions values (\'applied scientist\', 100, 800)')
cursor.execute('insert into Positions values (\'engineer / programmer\', 500, 1000)')
cursor.execute('insert into Positions values (\'senior programmer\', 750, 1250)')
cursor.execute('insert into Positions values (\'director\', 1000, 2000)')
cursor.execute('insert into ProjectStatus values (\'in progress\')')
cursor.execute('insert into ProjectStatus values (\'completed\')')
cursor.execute('insert into ProjectStatus values (\'hold\')')
cursor.execute('insert into ProjectStatus values (\'new\')')
cursor.execute('insert into Addresses values (\'test\', \'90\')')
cursor.execute('insert into Roles values (\'role\')')

conn.commit()
conn.close()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

###query page 
@app.route("/query/")
def queryPage():
    return render_template("query.html")

@app.route("/showall/", methods=['POST'])
def showall():
    table = request.form.get("show")
    if request.method == "POST":
        try:
            conn = sqlite3.connect("database.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            #cursor.execute('insert into HealthInsurance values (\'test\');') #test
            cursor.execute('select * from ' + table) #test
            query = cursor.fetchall()
            cursor.close()
        except Exception as e:
            return render_template("error.html", e = e)
    return render_template("query.html", query = query) #test; edit this

@app.route("/query/search/", methods = ["GET", "POST"])
def genQuery():
    query = None
    if request.method == "POST":
        try:
            att = request.form.get("attribute")
            cond = request.form.get("cond")
            op = request.form.get("operation")
            input = request.form.get("input")
            if op == "like":
                input = "\'" + input + "\'"
            conn = sqlite3.connect("database.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            if att == "emp":
                if cond == "benefit":
                    cursor.execute('select * from EmployeeInfo e, EmployeeBenefits b where e.EmployeeID = b.EmployeeID and b.Benefit ' +op+ '?', (input,))
                elif cond == "department":
                    cursor.execute('select * from EmployeeInfo e, EmployeeAssignments d where e.EmployeeID = d.EmployeeID and d.Department' +op+ '?', (input,))
                else:
                    cursor.execute('select * from EmployeeInfo where ' +cond+ ' ' +op+ ' ?', (input,))
            query = cursor.fetchall()
            cursor.close()
        except Exception as e:
            return render_template("error.html", e=e)
    return render_template("query.html")

@app.route("/query/menu/", methods=["POST"])
def queryMenu():
    if request.form.get("q") == "1":
        return redirect(url_for("query1"))
    elif request.form.get("q") == "2":
        return redirect(url_for("query2"))
    elif request.form.get("q") == "3":
        return redirect(url_for("query3"))
    elif request.form.get("q") == "4":
        return redirect(url_for("query4"))
    elif request.form.get("q") == "5":
        return redirect(url_for("query5"))
    elif request.form.get("q") == "6":
        return redirect(url_for("query6"))
    elif request.form.get("q") == "7":
        return redirect(url_for("query7"))
    elif request.form.get("q") == "8":
        return redirect(url_for("query8"))
    elif request.form.get("q") == "9":
        return redirect(url_for("query9"))
    elif request.form.get("q") == "10":
        return redirect(url_for("query10"))
    elif request.form.get("q") == "11":
        return redirect(url_for("query11"))
    elif request.form.get("q") == "12":
        return redirect(url_for("query12"))
    elif request.form.get("q") == "13":
        return redirect(url_for("query13"))
    elif request.form.get("q") == "14":
        return redirect(url_for("query14"))
    elif request.form.get("q") == "15":
        return redirect(url_for("query15"))
    elif request.form.get("q") == "16":
        return redirect(url_for("query16"))
    elif request.form.get("q") == "17":
        return redirect(url_for("query17"))
    elif request.form.get("q") == "18":
        return redirect(url_for("query18"))
    elif request.form.get("q") == "19":
        return redirect(url_for("query19"))
    elif request.form.get("q") == "20":
        return redirect(url_for("query20"))
    elif request.form.get("q") == "21":
        return redirect(url_for("query21"))
    else:
        return render_template("query.html")

@app.route("/query/sql/", methods=['POST'])
def sql():
    input = request.form.get("input")
    if request.method == "POST":
        try:
            conn = sqlite3.connect("database.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(input) #test
            query = cursor.fetchall()
            cursor.close()
        except Exception as e:
            return render_template("error.html", e)
    return render_template("query.html", query = query)
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
    return render_template("home.html")

@app.route("/update/", methods=["POST"])
def update():
    try:
        if request.form.get("updateRow") == "insurance":
            return redirect(url_for("updateHealth"))
        elif request.form.get("updateRow") == "benefit":
            return redirect(url_for("updateBen"))
        elif request.form.get("updateRow") == "status":
            return redirect(url_for("updateStatus"))
        elif request.form.get("updateRow") == "address":
            return redirect(url_for("updateAddress"))
        elif request.form.get("updateRow") == "position":
            return redirect(url_for("updatePos"))
        elif request.form.get("updateRow") == "department":
            return redirect(url_for("updateDep"))
        elif request.form.get("updateRow") == "employee":
            return redirect(url_for("updateEmp"))
        elif request.form.get("updateRow") == "empBenefit":
            return redirect(url_for("updateEmpBen"))
        elif request.form.get("updateRow") == "project":
            return redirect(url_for("updateProj"))
        elif request.form.get("updateRow") == "role":
            return redirect(url_for("updateRole"))
        elif request.form.get("updateRow") == "empProject":
            return redirect(url_for("updateEmpProj"))
        elif request.form.get("updateRow") == "empDep":
            return redirect(url_for("updateEmpDep"))
    except:
        return render_template("error.html")
    return render_template("home.html")

@app.route("/delete/", methods=["POST"])
def delete():
    if request.form.get("deleteRow") == "insurance":
        return redirect(url_for("deleteHealth"))
    elif request.form.get("deleteRow") == "benefit":
        return redirect(url_for("deleteBen"))
    elif request.form.get("deleteRow") == "department":
        return redirect(url_for("deleteDep"))
    elif request.form.get("deleteRow") == "status":
        return redirect(url_for("deleteStatus"))
    elif request.form.get("deleteRow") == "role":
        return redirect(url_for("deleteRole"))
    elif request.form.get("deleteRow") == "position":
        return redirect(url_for("deletePos"))
    elif request.form.get("deleteRow") == "empDep":
        return redirect(url_for("deleteEmpDep"))
    elif request.form.get("deleteRow") == "empBenefit":
        return redirect(url_for("deleteEmpBen"))
    elif request.form.get("deleteRow") == "employee":
        return redirect(url_for("deleteEmpInfo"))
    elif request.form.get("deleteRow") == "empProject":
        return redirect(url_for("deleteEmpProj"))
    return render_template("home.html") 

#Add pages
@app.route("/addHealthInsurance/", methods=['GET', 'POST'])
def insertIntoHealthInsurance():
    if request.method == 'POST':
        try:
            coverage = request.form.get('insertHI') #request.form['insertHI']
            conn = sqlite3.connect("database.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('insert into HealthInsurance values (?)', (coverage,)) 
            conn.commit()
            cursor.close()
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
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('insert into Benefits values (?)', (benefit,)) 
            conn.commit()
            cursor.close()
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
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('insert into Benefits values (?)', (dep,)) 
            conn.commit()
            cursor.close()
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
            conn = sqlite3.connect("database.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('insert into Positions values (?, ?, ?)', (position, min, max,)) 
            conn.commit()
            cursor.close()
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
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('insert into Projects values (?, ?, ?, ?)', (project, dep, leader, status,)) 
            conn.commit()
            cursor.close()
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
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('insert into Roles values (?)', (role,)) 
            conn.commit()
            cursor.close()
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
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('insert into ProjectStatus values (?)', (status,)) 
            conn.commit()
            cursor.close()
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
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('insert into Addresses values (?, ?)', (address, zip,)) 
            conn.commit()
            cursor.close()
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
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('insert into EmployeeProjects values (?, ?, ?, ?, ?)', (employee, project, role, start, end,)) 
            conn.commit()
            cursor.close()
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
            experience = request.form.get('experience')
            hPosition = request.form.get('hPosition')
            hSalary = request.form.get('hSalary')
            position = request.form.get('position')
            salary = request.form.get('salary')
            insurance = request.form.get('insurance')
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('insert into EmployeeInfo values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (id, ssn, name, gender, birth, address, phone, degree, experience, hPosition, hSalary, position, salary, insurance,)) 
            conn.commit()
            cursor.close()
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
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('insert into EmployeeBenefits values (?, ?, ?, ?)', (emp, ben, start, end,)) 
            conn.commit()
            cursor.close()
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
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('insert into EmployeeAssignments values (?, ?, ?, ?)', (emp, dep, start, end,)) 
            conn.commit()
            cursor.close()
            return render_template("addEmployeeAssignment.html", added = emp)
        except:
            return render_template('error.html')
    else: 
        return render_template("addEmployeeAssignments.html")
    
#update pages
@app.route("/updateHealthInsurance/", methods=['GET', 'POST'])
def updateHealth():
    if request.method == 'POST':
        try:
            attribute = request.form.get('i2')
            value = request.form.get('i3')
            where = request.form.get('i4')
            whereVal = request.form.get('i5')
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('UPDATE HealthInsurance SET ' +attribute+ '= ? WHERE ' +where+ '= ?', (value, whereVal,))
            conn.commit()
            cursor.close()
        except:
            render_template("error.html")
    return render_template("updateHealthInsurance.html")

@app.route("/updateAddresses/", methods=['GET', 'POST'])
def updateAddress():
    if request.method == "POST":
        try:
            att = request.form.get('attribute')
            value = request.form.get('input')
            #if(att == "zipCode"):
            #    value = int(value)
            whereAtt = request.form.get('position')
            whereVal = request.form.get('input2')
            #if(whereAtt == "zipCode"):
            #    whereVal = int(whereVal)
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('UPDATE Addresses SET ' +att+  '=? WHERE ' +whereAtt+ '=?;', (value, whereVal,))
            conn.commit()
            cursor.close()
        except:
            return render_template("error.html")
    return render_template("updateAddresses.html")

@app.route("/updateBenefits/", methods=['GET', 'POST'])
def updateBen():
    if request.method == 'POST':
        try:
            new = request.form.get('new')
            old = request.form.get('old')
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('update Benefits set benefit = ? where benefit = ?', (new, old,))
            conn.commit()
            cursor.close()
        except:
            return render_template("error.html")
    return render_template("updateBenefits.html")

@app.route("/updateDepartments/", methods=['GET', 'POST'])
def updateDep():
    if request.method == 'POST':
        try:
            new = request.form.get('new')
            old = request.form.get('old')
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('update Departments set department = ? where department = ?', (new, old,))
            conn.commit()
            cursor.close()
        except:
            return render_template("error.html")
    return render_template("updateDepartments.html")

@app.route("/updateEmployeeAssignments/", methods=['GET', 'POST'])
def updateEmpDep():
    if request.method == 'POST':
        try:
            att = request.form.get('i2')
            where = request.form.get('i4')
            new = request.form.get('new')
            if(att == "EmployeeID"): #might not need this due to sqlite's flexible typing
                new = int(new)
            old = request.form.get('old')
            if(where == "EmployeeID"):
                old = int(old)
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('update EmployeeAssignments set ' +att+ ' = ? where '+where+' = ?', (new, old,))
            conn.commit()
            cursor.close()
        except:
            return render_template("error.html")
    return render_template("updateEmployeeAssignments.html")

@app.route("/updateEmployeeBenefits/", methods=['GET', 'POST'])
def updateEmpBen():
    if request.method == 'POST':
        try:
            new = request.form.get('new')
            old = request.form.get('old')
            att = request.form.get('i2')
            where = request.form.get('i4')
            if(att == "EmployeeID"):
                new = int(new)
            if(where == "EmployeeID"):
                old = int(old)
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('update EmployeeBenefits set ' +att+ ' = ? where '+where+' = ?', (new, old,))
            conn.commit()
            cursor.close()
        except:
            return render_template("error.html")
    return render_template("updateEmployeeBenefits.html")

@app.route("/updateEmployeeInfo/", methods=['GET', 'POST'])
def updateEmp():
    if request.method == 'POST':
        try:
            new = request.form.get('new')
            old = request.form.get('old')
            att = request.form.get('i2')
            where = request.form.get('i4')
            if(att == "YearsExperience" or att == "HiringSalary" or att == "CurrentSalary"):
                new = int(new)
            if(where == "YearsExperience" or where == "HiringSalary" or where == "CurrentSalary"):
                old = int(old)
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('update EmployeeInfo set ' +att+ ' = ? where '+where+' = ?', (new, old,))
            conn.commit()
            cursor.close()
        except:
            return render_template("error.html")
    return render_template("updateEmployeeInfo.html")

@app.route("/updateEmployeeProjects/", methods=['GET', 'POST'])
def updateEmpProj():
    if request.method == 'POST':
        try:
            new = request.form.get('new')
            old = request.form.get('old')
            att = request.form.get('i2')
            where = request.form.get('i4')
            if(att == "EmployeeID"):
                new = int(new)
            if(where == "EmployeeID"):
                old = int(old)
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('update EmployeeProjects set ' +att+ ' = ? where '+where+' = ?', (new, old,))
            conn.commit()
            cursor.close()
        except:
            return render_template("error.html")
    return render_template("updateEmployeeProjects.html")

@app.route("/updatePositions/", methods=['GET', 'POST'])
def updatePos():
    if request.method == 'POST':
        try:
            new = request.form.get('new')
            old = request.form.get('old')
            att = request.form.get('i2')
            where = request.form.get('i4')
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('update Positions set ' +att+ ' = ? where '+where+' = ?', (new, old,))
            conn.commit()
            cursor.close()
        except:
            return render_template("error.html")
    return render_template("updatePositions.html")

@app.route("/updateProjects/", methods=['GET', 'POST'])
def updateProj():
    if request.method == 'POST':
        try:
            new = request.form.get('new')
            old = request.form.get('old')
            att = request.form.get('i2')
            where = request.form.get('i4')
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('update Projects set ' +att+ ' = ? where '+where+' = ?', (new, old,))
            conn.commit()
            cursor.close()
        except:
            return render_template("error.html")
    return render_template("updateProjects.html")

@app.route("/updateProjectStatus/", methods=['GET', 'POST'])
def updateStatus():
    if request.method == 'POST':
        try:
            new = request.form.get('new')
            old = request.form.get('old')
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('update ProjectStatus set status = ? where status = ?', (new, old,))
            conn.commit()
            cursor.close()
        except:
            return render_template("error.html")
    return render_template("updateProjectStatus.html")

@app.route("/updateRoles/", methods=['GET', 'POST'])
def updateRole():
    if request.method == 'POST':
        try:
            new = request.form.get('new')
            old = request.form.get('old')
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('update Roles set role = ? where role = ?', (new, old,))
            conn.commit()
            cursor.close()
        except:
            return render_template("error.html")
    return render_template("updateRoles.html")

#delete pages
@app.route("/deleteHealthInsurance", methods=['GET', 'POST'])
def deleteHealth():
    if request.method == 'POST':
        try:
            delete = request.form.get('input')
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('delete from HealthInsurance where coverage = ?', (delete,))
            conn.commit()
            cursor.close()
        except:
            return render_template("error.html")
    return render_template("deleteHealthInsurance.html")

@app.route("/deleteBenefits/", methods=['GET', 'POST'])
def deleteBen():
    if request.method == 'POST':
        try:
            delete = request.form.get('input')
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('delete from Benefits where benefit = ?', (delete,))
            conn.commit()
            cursor.close()
        except:
            return render_template("error.html")
    return render_template("deleteBenefits.html")

@app.route("/deleteDepartments/", methods=['GET', 'POST'])
def deleteDep():
    if request.method == 'POST':
        try:
            delete = request.form.get('input')
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('delete from Departments where department = ?', (delete,))
            conn.commit()
            cursor.close()
        except:
            return render_template("error.html")
    return render_template("deleteDepartments.html")

@app.route("/deleteStatus/", methods=['GET','POST'])
def deleteStatus():
    if request.method == 'POST':
        try:
            delete = request.form.get('input')
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('delete from ProjectStatus where status = ?', (delete,))
            conn.commit()
            cursor.close()
        except:
            return render_template("error.html")
    return render_template("deleteProjectStatus.html")

@app.route("/deleteRoles/", methods=['GET','POST'])
def deleteRole():
    if request.method == 'POST':
        try:
            delete = request.form.get('input')
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('delete from Roles where role = ?', (delete,))
            conn.commit()
            cursor.close()
        except:
            return render_template("error.html")
    return render_template("deleteRoles.html")

@app.route("/deletePositions/", methods=['GET','POST'])
def deletePos():
    if request.method == 'POST':
        try:
            delete = request.form.get('input')
            att = request.form.get('att')
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('delete from Positions where ' +att+ ' = ?', (delete,))
        except:
            return render_template("error.html")
    return render_template("deletePositions.html")

@app.route("/deleteEmployeeAssignments/", methods=['GET','POST'])
def deleteEmpDep():
    if request.method == 'POST':
        try:
            delete = request.form.get('old')
            att = request.form.get('att')
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('delete from EmployeeAssignments where ' + att + ' = ?', (delete,))
            conn.commit()
            cursor.close()
        except:
            return render_template("error.html")
    return render_template("deleteEmployeeAssignments.html")

@app.route("/deleteEmployeeBenefits/", methods=['GET','POST'])
def deleteEmpBen():
    if request.method == 'POST':
        try:
            delete = request.form.get('old')
            att = request.form.get('att')
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('delete from EmployeeBenefits where ' + att + ' = ?', (delete,))
            conn.commit()
            cursor.close()
        except:
            return render_template("error.html")
    return render_template("deleteEmployeeBenefits.html")

@app.route("/deleteEmployeeInfo/", methods=['GET','POST'])
def deleteEmpInfo():
    if request.method == 'POST':
        try:
            delete = request.form.get('old')
            att = request.form.get('att')
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('delete from EmployeeInfo where ' + att + ' = ?', (delete,))
            conn.commit()
            cursor.close()
        except:
            return render_template("error.html")
    return render_template("deleteEmployeeInfo.html")

@app.route("/deleteEmployeeProjects/", methods=['GET','POST'])
def deleteEmpProj():
    if request.method == 'POST':
        try:
            delete = request.form.get('old')
            att = request.form.get('att')
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('delete from EmployeeProjects where ' + att + ' = ?', (delete,))
            conn.commit()
            cursor.close()
        except:
            return render_template("error.html")
    return render_template("deleteEmployeeProjects.html")

@app.route("/deleteProjects/", methods=['GET','POST'])
def deleteProj():
    if request.method == 'POST':
        try:
            delete = request.form.get('old')
            att = request.form.get('att')
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('delete from Projects where ' + att + ' = ?', (delete,))
            conn.commit()
            cursor.close()
        except:
            return render_template("error.html")
    return render_template("deleteProjects.html")

@app.route("/deleteAddresses/", methods=['GET','POST'])
def deleteAddress():
    if request.method == 'POST':
        try:
            delete = request.form.get('old')
            att = request.form.get('att')
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            cursor.execute('delete from Projects where ' + att + ' = ?', (delete,))
            conn.commit()
            cursor.close()
        except:
            return render_template("error.html")
    return render_template("deleteAddresses.html")

@app.route('/query1', methods=["GET", "POST"])
def query1():
  info = None
  if request.method == 'POST':
    try:
      emp = request.form['i1']
      con = sqlite3.connect("database.db")
      con.row_factory = sqlite3.Row
      cursor = con.cursor()
      cursor.execute('SELECT * FROM EmployeeInfo WHERE EmployeeID = ?', (emp))
      info = cursor.fetchall()
      cursor.close()
    except:
      return render_template('error.html')
  return render_template('query1.html', query=info)

@app.route('/query2', methods=["GET", "POST"])
def query2():
  info = None
  if request.method == 'POST':
    try:
      dept = request.form['i1']
      con = sqlite3.connect("database.db")
      con.row_factory = sqlite3.Row
      cursor = con.cursor()
      cursor.execute('SELECT DISTINCT EmployeeID FROM EmployeeInfo e, EmployeeAssignments d WHERE e.employeeID = d.employeeID and (d.EndDate IS NULL OR d.EndDate >= GetDate()) and d.Department = ?', dept)
      info = cursor.fetchall()
      cursor.close()
    except Exception as e:
      return render_template('error.html', e=e)
  return render_template('query2.html', query=info)

@app.route('/query3', methods=["GET", "POST"])
def query3():
  info = None
  if request.method == 'POST':
    try:
      proj = request.form['i1']
      con = sqlite3.connect("database.db")
      con.row_factory = sqlite3.Row
      cursor = con.cursor()
      cursor.execute('SELECT (EmployeeID, Name) FROM EmployeeProjects WHERE Project = ? AND (EndDate IS NULL OR EndDate >= GetDate())', proj)
      info = cursor.fetchall()
      cursor.close()
    except Exception as e:
      return render_template('error.html', e=e)
  return render_template('query3.html', query=info)

@app.route('/query4', methods=["GET", "POST"])
def query4():
  info = None
  if request.method == 'POST':
    try:
      con = sqlite3.connect("database.db")
      con.row_factory = sqlite3.Row
      cursor = con.cursor()
      cursor.execute('SELECT distinct(zipCode) FROM Addresses GROUP BY zipCode HAVING count(zipCode) >= ALL (SELECT count(zipCode) FROM Addresses GROUP BY zipCode)')
      info = cursor.fetchall()
      cursor.close()
    except:
      return render_template('error.html')
  return render_template('query4.html', query=info)

@app.route('/query5', methods=["GET", "POST"])
def query5():
  info = None
  if request.method == 'POST':
    try:
      proj = request.form['i1']
      con = sqlite3.connect("database.db")
      con.row_factory = sqlite3.Row
      cursor = con.cursor()
      cursor.execute('SELECT * FROM Projects WHERE Project = ?;', proj)
      info = cursor.fetchall()
      cursor.close()
    except:
      return render_template('error.html')
  return render_template('query5.html', query=info)

@app.route('/query6', methods=["GET", "POST"])
def query6():
  info = None
  if request.method == 'POST':
    try:
      proj = request.form['i1']
      date = request.form['i2']
      con = sqlite3.connect("database.db")
      con.row_factory = sqlite3.Row
      cursor = con.cursor()
      cursor.execute('SELECT COUNT (EmployeeID) FROM EmployeeProjects WHERE Project = ? AND (EndDate IS NULL OR EndDate >= ?) AND (StartDate <= ?)', proj, date, date)
      info = cursor.fetchall()
      cursor.close()
    except:
      return render_template('error.html')
  return render_template('query6.html', query=info)

@app.route('/query7', methods=["GET", "POST"])
def query7():
  info = None
  if request.method == 'POST':
    try:
      ben = request.form['i1']
      con = sqlite3.connect("database.db")
      con.row_factory = sqlite3.Row
      cursor = con.cursor()
      cursor.execute('SELECT COUNT (DISTINCT EmployeeID) FROM EmployeeBenefits WHERE (EndDate IS NULL OR EndDate >= GetDate()) AND Benefit = ?', ben)
      info = cursor.fetchall()
      cursor.close()
    except:
      return render_template('error.html')
  return render_template('query7.html', query=info)

@app.route('/query8', methods=["GET", "POST"])
def query8():
  info = None
  if request.method == 'POST':
    try:
      proj = request.form['i1']
      role = request.form['i2']
      con = sqlite3.connect("database.db")
      con.row_factory = sqlite3.Row
      cursor = con.cursor()
      cursor.execute('SELECT EmployeeID FROM EmployeeProjects WHERE (EndDate IS NULL OR EndDate >= GetDate()) AND Project = ? AND Role = ?', proj, role)
      info = cursor.fetchall()
      cursor.close()
    except:
      return render_template('error.html')
  return render_template('query8.html', query=info)

@app.route('/query9', methods=["GET", "POST"])
def query9():
  info = None
  if request.method == 'POST':
    try:
      con = sqlite3.connect("database.db")
      con.row_factory = sqlite3.Row
      cursor = con.cursor()
      cursor.execute('SELECT Project FROM Projects WHERE Status = \'in-progress\' OR Status = \'new\'')
      info = cursor.fetchall()
      cursor.close()
    except:
      return render_template('error.html')
  return render_template('query9.html', query=info)

@app.route('/query10', methods=["GET", "POST"])
def query10():
  query = None
  if request.method == 'POST':
    try:
      con = sqlite3.connect("database.db")
      con.row_factory = sqlite3.Row
      cursor = con.cursor()
      cursor.execute('SELECT Department, EmployeeID, StartDate, EndDate FROM EmployeeAssignments GROUP BY Department; SELECT Department, Project, ProjectLeader, Status FROM Projects GROUP BY DEPARTMENT')
      query = cursor.fetchall()
      cursor.close()
    except:
      return render_template('error.html')
  return render_template('query10.html', query=query)

@app.route('/query11', methods=["GET", "POST"])
def query11():
  query = None
  if request.method == 'POST':
    try:
      emp = request.form['i1']
      con = sqlite3.connect("database.db")
      con.row_factory = sqlite3.Row
      cursor = con.cursor()
      cursor.execute('SELECT Role FROM EmployeeProjects WHERE (EndDate IS NULL OR EndDate >= GetDate()) AND EmployeeID = ?', emp)
      query = cursor.fetchall()
      cursor.close()
    except:
      return render_template('error.html')
  return render_template('query11.html', query=query)

@app.route('/query12', methods=["GET", "POST"])
def query12():
  query = None
  if request.method == 'POST':
    try:
      emp = request.form['i1']
      con = sqlite3.connect("database.db")
      con.row_factory = sqlite3.Row
      cursor = con.cursor()
      cursor.execute('select role, startdate, enddate from EmployeeProjects where EmployeeID = ?', emp)
      query = cursor.fetchall()
      cursor.close()
    except:
      return render_template('error.html')
  return render_template('query12.html', query=query)

@app.route('/query13', methods=["GET", "POST"])
def query13():
  query = None
  if request.method == 'POST':
    try:
      HealthPlan = request.form['i1']
      con = sqlite3.connect("database.db")
      con.row_factory = sqlite3.Row
      cursor = con.cursor()
      cursor.execute('SELECT COUNT(EmployeeInfo) FROM EmployeeInfo WHERE Coverage = ?', HealthPlan)
      query = cursor.fetchall()
      cursor.close()
    except:
      return render_template('error.html')
  return render_template('query13.html', query=query)

@app.route('/query14', methods=["GET", "POST"])
def query14():
  query = None
  if request.method == 'POST':
    try:
      con = sqlite3.connect("database.db")
      con.row_factory = sqlite3.Row
      cursor = con.cursor()
      cursor.execute('select count(distinct employeeid), coverage from employeeInfo group by coverage')
      query = cursor.fetchall()
      cursor.close()
    except:
      return render_template('error.html')
  return render_template('query14.html', query=query)

@app.route('/query15', methods=["GET", "POST"])
def query15():
  query = None
  if request.method == 'POST':
    try:
      role = request.form['i1']
      lev = request.form['i2']
      con = sqlite3.connect("database.db")
      con.row_factory = sqlite3.Row
      cursor = con.cursor()
      #not sure if this is how you'd solve the issue
      cursor.execute('SELECT AVG(CurrentSalary) FROM EmployeeInfo WHERE Gender = \'Female\' AND CurrentPosition = ? AND YearsExperience = ?; SELECT AVG(CurrentSalary) FROM EmployeeInfo WHERE Gender = \'Male\' AND CurrentPosition = ? AND YearsExperience = ?', role, lev, role, lev)
      query = cursor.fetchall()
      cursor.close()
    except:
      return render_template('error.html')
  return render_template('query15.html', query=query)

@app.route('/query16', methods=["GET", "POST"])
def query16():
  query = None
  if request.method == 'POST':
    try:
      pos = request.form['i1']
      con = sqlite3.connect("database.db")
      con.row_factory = sqlite3.Row
      cursor = con.cursor()
      cursor.execute('SELECT (minSalary, maxSalary) FROM Positions WHERE position = ?;', pos)
      query = cursor.fetchall()
      cursor.close()
    except:
      return render_template('error.html')
  return render_template('query16.html', query=query)

@app.route('/query17', methods=["GET", "POST"])
def query17():
  query = None
  if request.method == 'POST':
    try:
      con = sqlite3.connect("database.db")
      con.row_factory = sqlite3.Row
      cursor = con.cursor()
      cursor.execute('select count(distinct project), status from projects group by status')
      query = cursor.fetchall()
      cursor.close()
    except:
      return render_template('error.html')
  return render_template('query17.html', query=query)

@app.route('/query18', methods=["GET", "POST"])
def query18():
  query = None
  if request.method == 'POST':
    try:
      emp = request.form['i1']
      dep = request.form['i2']
      con = sqlite3.connect("database.db")
      con.row_factory = sqlite3.Row
      cursor = con.cursor()
      cursor.execute('SELECT (StartDate, EndDate) FROM EmployeeAssignments WHERE EmployeeID = ? AND Department = ?', emp, dep)
      query = cursor.fetchall()
      cursor.close()
    except:
      return render_template('error.html')
  return render_template('query18.html', query=query)

@app.route('/query19', methods=["GET", "POST"])
def query19():
  query = None
  if request.method == 'POST':
    try:
      con = sqlite3.connect("database.db")
      con.row_factory = sqlite3.Row
      cursor = con.cursor()
      cursor.execute('SELECT (a.Project, b.Name) FROM Projects a, EmployeeID b, WHERE a.ProjectLeader == b.EmployeeID')
      query = cursor.fetchall()
      cursor.close()
    except:
      return render_template('error.html')
  return render_template('query19.html', query=query)

@app.route('/query20', methods=["GET", "POST"])
def query20():
  query = None
  if request.method == 'POST':
    try:
      con = sqlite3.connect("database.db")
      con.row_factory = sqlite3.Row
      cursor = con.cursor()
      cursor.execute('SELECT (EmployeeID, Name) FROM EmployeeInfo WHERE 5*CurrentSalary >= 6*HiringSalary')
      query = cursor.fetchall()
      cursor.close()
    except:
      return render_template('error.html')
  return render_template('query20.html', query=query)

@app.route('/query21', methods=["GET", "POST"])
def query21():
  query = None
  if request.method == 'POST':
    try:
      con = sqlite3.connect("database.db")
      con.row_factory = sqlite3.Row
      cursor = con.cursor()
      cursor.execute('select max(avg(CurrentSalary)) from ( select avg(CurrentSalary)  from EmployeeInfo group by CurrentPosition)')
      query = cursor.fetchall()
      cursor.close()
    except:
      return render_template('error.html')
  return render_template('query21.html', query=query)
