import sqlite3
from flask import Flask, render_template
app = Flask(__name__)

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
  YearsExperience SMALLINT NOT NULL,
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

conn.commit()

#after pressing a button (add / delete / update / query) on the home page, these functions will take someone to the appropriate page to make their selections

#these pages don't exist yet, but I presume they'll include a 'submit' button to do the operation and send someone back to the home page

#@app.route('/updateEmployeeInfo/', methods=["GET", "POST"])
#def query():
#  return render_template('updateEmployeeInfo.html')

#@app.route('/delete/', methods=["GET", "POST"])
#def query():
#  return render_template('delete.html')

#@app.route('/addinsurance/', methods=["GET", "POST"])
#def query():
#  return render_template('addinsurance.html')

#@app.route('/addbenefit/', methods=["GET", "POST"])
#def query():
#  return render_template('addbenefit.html')

#@app.route('/addstatus/', methods=["GET", "POST"])
#def query():
#  return render_template('addstatus.html')

#@app.route('/addaddress/', methods=["GET", "POST"])
#def query():
#  return render_template('addaddress.html')

#@app.route('/addposition/', methods=["GET", "POST"])
#def query():
#  return render_template('addposition.html')

#@app.route('/adddepartment/', methods=["GET", "POST"])
#def query():
#  return render_template('adddepartment.html')

#@app.route('/addemployee/', methods=["GET", "POST"])
#def query():
#  return render_template('addemployee.html')

#@app.route('/addempbenefit/', methods=["GET", "POST"])
#def query():
#  return render_template('addempbenefit.html')

#@app.route('/addproject/', methods=["GET", "POST"])
#def query():
#  return render_template('addproject.html')

#@app.route('/addrole/', methods=["GET", "POST"])
#def query():
#  return render_template('addrole.html')

#@app.route('/addempproj/', methods=["GET", "POST"])
#def query():
#  return render_template('addempproj.html')

#@app.route('/addassignment/', methods=["GET", "POST"])
#def query():
#  return render_template('addassignment.html')
  
#to blend the html requests with the python, we'll need https://stackoverflow.com/questions/5615228/call-a-python-function-within-a-html-file

#the below will also need@app.route -- basically the above app routes took someone to the non-home pages; these take them back from the non-home pages

#this method deals with the initial state of the app
@app.route('/')
def home():
  return render_template('home.html')

#this method is called when a selection is made on home.html; it directs to one of the operation .html (add / delete / update / query) pages
@app.route('/selection', methods=["GET", "POST"])
def selection():
  if request.method == 'POST':
    try:
      selec = request.form['operation']
      if selec == 'Ainsurance':
        return render_template('addHealthInsurance.html')
      elif selec == 'Abenefit':
        return render_template('addBenefits.html')
      elif selec == 'Astatus':
        return render_template('addProjectStatus.html')
      elif selec == 'Aaddress':
        return render_template('addAddresses.html')
      elif selec == 'Aposition':
        return render_template('addPositions.html')
      elif selec == 'Adepartment':
        return render_template('addDepartments.html')
      elif selec == 'Aemployee':
        return render_template('addEmployeeInfo.html')
      elif selec == 'AempBenefit':
        return render_template('addEmployeeBenefits.html')
      elif selec == 'Aproject':
        return render_template('addProjects.html')
      elif selec == 'Arole':
        return render_template('addRoles.html')
      elif selec == 'AempProject':
        return render_template('addEmployeeProjects.html')
      elif selec == 'AempDep':
        return render_template('addEmployeeAssignments.html')
      elif selec == 'Uinsurance':
        return render_template('updateHealthInsurance.html')
      elif selec == 'Ubenefit':
        return render_template('updateBenefits.html')
      elif selec == 'Ustatus':
        return render_template('updateProjectStatus.html')
      elif selec == 'Uaddress':
        return render_template('updateAddresses.html')
      elif selec == 'Uposition':
        return render_template('updatePositions.html')
      elif selec == 'Udepartment':
        return render_template('updateDepartments.html')
      elif selec == 'Uemployee':
        return render_template('updateEmployeeInfo.html')
      elif selec == 'UempBenefit':
        return render_template('updateEmployeeBenefits.html')
      elif selec == 'Uproject':
        return render_template('updateProjects.html')
      elif selec == 'Urole':
        return render_template('updateRoles.html')
      elif selec == 'UempProject':
        return render_template('updateEmployeeProjects.html')
      elif selec == 'UempDep':
        return render_template('updateEmployeeAssignments.html')
      elif selec == 'Dinsurance':
        return render_template('deleteHealthInsurance.html')
      elif selec == 'Dbenefit':
        return render_template('deleteBenefits.html')
      elif selec == 'Dstatus':
        return render_template('deleteProjectStatus.html')
      elif selec == 'Daddress':
        return render_template('deleteAddresses.html')
      elif selec == 'Dposition':
        return render_template('deletePositions.html')
      elif selec == 'Ddepartment':
        return render_template('deleteDepartments.html')
      elif selec == 'Demployee':
        return render_template('deleteEmployeeInfo.html')
      elif selec == 'DempBenefit':
        return render_template('deleteEmployeeBenefits.html')
      elif selec == 'Dproject':
        return render_template('deleteProjects.html')
      elif selec == 'Drole':
        return render_template('deleteRoles.html')
      elif selec == 'DempProject':
        return render_template('deleteEmployeeProjects.html')
      elif selec == 'DempDep':
        return render_template('deleteEmployeeAssignments.html')
      elif selec == 'query1':
        return render_template('query1.html')
      elif selec == 'query2':
        return render_template('query2.html')
      elif selec == 'query3':
        return render_template('query3.html')
      elif selec == 'query4':
        return render_template('query4.html')
      elif selec == 'query5':
        return render_template('query5.html')
      elif selec == 'query6':
        return render_template('query6.html')
      elif selec == 'query7':
        return render_template('query7.html')
      elif selec == 'query8':
        return render_template('query8.html')
      elif selec == 'query9':
        return render_template('query9.html')
      elif selec == 'query10':
        return render_template('query10.html')
      elif selec == 'query11':
        return render_template('query11.html')
      elif selec == 'query12':
        return render_template('query12.html')
      elif selec == 'query13':
        return render_template('query13.html')
      elif selec == 'query14':
        return render_template('query14.html')
      elif selec == 'query15':
        return render_template('query15.html')
      elif selec == 'query16':
        return render_template('query16.html')
      elif selec == 'query17':
        return render_template('query17.html')
      elif selec == 'query18':
        return render_template('query18.html')
      elif selec == 'query19':
        return render_template('query19.html')
      elif selec == 'query20':
        return render_template('query20.html')
      elif selec == 'query21':
        return render_template('query21.html')
      return render_template('error.html') #if somehow isn't something in list
    except:
      return render_template('error.html') #I'll try to expand these blocks to other functions Saturday
  return render_template('error.html')

#if an error is found, this method takes the user back to the home page after notifying them of the error
@app.route('/error', methods=["GET", "POST"]) 
def error():
  return render_template('home.html')

#these insertion methods come from add .html files; they take the user back to the home page after doing their operation
@app.route('/insertIntoHealthInsurance', methods=["GET", "POST"])
def insertIntoHealthInsurance():
  if request.method == 'POST':
    try:
      coverage = request.form['i1']
      cursor.execute('INSERT INTO HealthInsurance (coverage) VALUES (?)', (coverage))
      conn.commit()
      return render_template('home.html')
    except:
      return render_template('error.html')
  return render_template('error.html')

@app.route('/insertIntoBenefits', methods=["GET", "POST"])
def insertIntoBenefits():
  if request.method == 'POST':
    try:
      benefit = request.form['i1']
      cursor.execute('INSERT INTO Benefits (benefit) VALUES (?)', (benefit))
      conn.commit()
      return render_template('home.html')
    except:
      return render_template('error.html')
  return render_template('error.html')

@app.route('/insertIntoProjectStatus', methods=["GET", "POST"])
def insertIntoProjectStatus():
  if request.method == 'POST':
    try:
      status = request.form['i1']
      cursor.execute('INSERT INTO ProjectStatus (status) VALUES (?)', (status))
      conn.commit()
      return render_template('home.html')
    except:
      return render_template('error.html')
  return render_template('error.html')

@app.route('/insertIntoAddresses', methods=["GET", "POST"])
def insertIntoAddresses():
  if request.method == 'POST':
    try:
      address = request.form['i1']
      zipcode = request.form['i2']
      cursor.execute('INSERT INTO Addresses (address, zipCode) VALUES (?, ?)', (address, zipcode))
      conn.commit()
      return render_template('home.html')
    except:
      return render_template('error.html')
  return render_template('error.html')

@app.route('/insertIntoPositions', methods=["GET", "POST"])
def insertIntoPositions():
  if request.method == 'POST':
    try:
      position = request.form['i1']
      minSalary = request.form['i2']
      maxSalary = request.form['i3']
      cursor.execute('INSERT INTO Positions (position, minSalary, maxSalary) VALUES (?, ?, ?)', (position, int(minSalary), int(maxSalary)))
      conn.commit()
      return render_template('home.html')
    except:
      return render_template('error.html')
  return render_template('error.html')

@app.route('/insertIntoDepartments', methods=["GET", "POST"])
def insertIntoDepartments():
  if request.method == 'POST':
    try:
      department = request.form['i1']
      cursor.execute('INSERT INTO Departments (department) VALUES (?)', (department))
      conn.commit()
      return render_template('home.html')
    except:
      return render_template('error.html')
  return render_template('error.html')

@app.route('/insertIntoEmployeeInfo', methods=["GET", "POST"])
def insertIntoEmployeeInfo():
  if request.method == 'POST':
    try:
      employeeID = request.form['i1']
      ssn = request.form['i2']
      name = request.form['i3']
      gender = request.form['i4']
      DoB = request.form['i5']
      address = request.form['i6']
      phone = request.form['i7']
      degree = request.form['i8']
      years = request.form['i9']
      hiringPosition = request.form['i10']
      hiringSalary = request.form['i11']
      currentPosition = request.form['i12']
      currentSalary = request.form['i13']
      coverage = request.form['i14']
      cursor.execute('INSERT INTO EmployeeInfo (EmployeeID, SSN, Name, gender, DoB, PrimaryAddress, PhoneNumber, HighestDegree, YearsExperience, HiringPosition, HiringSalary, CurrentPosition, CurrentSalary, Coverage) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (employeeID, ssn, name, gender, DoB, address, phone, degree, int(years), hiringPosition, int(hiringSalary), currentPosition, int(currentSalary), coverage))
      conn.commit()
      return render_template('home.html')
    except:
      return render_template('error.html')
  return render_template('error.html')

@app.route('/insertIntoEmployeeAssignments', methods=["GET", "POST"])
def insertIntoEmployeeAssignments():
  if request.method == 'POST':
    try:
      employeeID = request.form['i1']
      department = request.form['i2']
      startDate = request.form['i3']
      endDate = request.form['i4']
      cursor.execute('INSERT INTO EmployeeAssignments (EmployeeID, Department, StartDate, EndDate) VALUES (?, ?, ?, ?)', (employeeID, department, startDate, endDate))
      conn.commit()
      return render_template('home.html')
    except:
      return render_template('error.html')
  return render_template('error.html')

@app.route('/insertIntoEmployeeBenefits', methods=["GET", "POST"])
def insertIntoEmployeeBenefits():
  if request.method == 'POST':
    try:
      employeeID = request.form['i1']
      benefit = request.form['i2']
      startDate = request.form['i3']
      endDate = request.form['i4']
      cursor.execute('INSERT INTO EmployeeBenefits (EmployeeID, Benefit, StartDate, EndDate) VALUES (?, ?, ?, ?)', (employeeID, benefit, startDate, endDate))
      conn.commit()
      return render_template('home.html')
    except:
      return render_template('error.html')
  return render_template('error.html')

@app.route('/insertIntoProjects', methods=["GET", "POST"])
def insertIntoProjects():
  if request.method == 'POST':
    try:
      project = request.form['i1']
      department = request.form['i2']
      projectLeader = request.form['i3']
      status = request.form['i4']
      cursor.execute('INSERT INTO Projects (Project, Department, ProjectLeader, Status) VALUES (?, ?, ?, ?)', (project, department, projectLeader, status))
      conn.commit()
      return render_template('home.html')
    except:
      return render_template('error.html')
  return render_template('error.html')

@app.route('/insertIntoRoles', methods=["GET", "POST"])
def insertIntoRoles():
  if request.method == 'POST':
    try:
      role = request.form['i1']
      cursor.execute('INSERT INTO Roles (role) VALUES (?)', (role))
      conn.commit()
      return render_template('home.html')
    except:
      return render_template('error.html')
  return render_template('error.html')

@app.route('/insertIntoEmployeeProjects', methods=["GET", "POST"])
def insertIntoEmployeeProjects():
  if request.method == 'POST':
    try:
      employeeID = request.form['i1']
      project = request.form['i2']
      role = request.form['i3']
      startDate = request.form['i4']
      endDate = request.form['i5']
      cursor.execute('INSERT INTO EmployeeProjects (EmployeeID, Project, Role, StartDate, EndDate) VALUES (?, ?, ?, ?, ?)', (employeeID, project, role, startDate, endDate))
      conn.commit()
      return render_template('home.html')
    except:
      return render_template('error.html')
  return render_template('error.html')

#coming from the update html pages, this method sends the user back to the home page after doing the operation
@app.route('/update', methods=["GET", "POST"])
def update():
  if request.method == 'POST':
    try:
      table = request.form['i1']
      column = request.form['i2']
      value = request.form['i3']
      cond1 = request.form['i4']
      cond2 = request.form['i5']
      if column == 'CurrentSalary' or column == 'HiringSalary' or column == 'YearsExperience' or column == 'minSalary' or column == 'maxSalary':
        value = int(value)
      if cond1 == 'CurrentSalary' or cond1 == 'HiringSalary' or cond1 == 'YearsExperience' or cond1 == 'minSalary' or cond1 == 'maxSalary':
        cond2 = int(cond2)
       #proper int formatting
      cursor.execute('UPDATE ? SET ? = ? WHERE ? = ?', (table, column, value, cond1, cond2))
      conn.commit()
      return render_template('home.html')
    except:
      return render_template('error.html')
  return render_template('error.html')
#e.g. if it's like update table A set B = C where D = E
#then you would call updateTable('A', 'B', 'C', 'D', 'E')

#coming from the delete html pages, this method sends the user back to the home page after doing the operation
@app.route('/delete', methods=["GET", "POST"])
def delete():
  if request.method == 'POST':
    try:
      table = request.form['i1']
      column = request.form['i2']
      value = request.form['i3']
      if cond1 == 'CurrentSalary' or cond1 == 'HiringSalary' or cond1 == 'YearsExperience' or cond1 == 'minSalary' or cond1 == 'maxSalary':
        cond2 = int(cond2)
        #proper int formatting
      cursor.execute('DELETE FROM ? WHERE ? = ?', (table, cond1, cond2))
      conn.commit()
      return render_template('home.html')
    except:
      return render_template('error.html')
  return render_template('error.html')

#these correspond to the queries we need to do in the instructions
#after the appropriate query .html page has its button clicked, these send the user to a query page to view their query
#that page DOES NOT EXIST yet as of the morning of 12/1, but it will link the user back home

@app.route('/query1', methods=["GET", "POST"])
def query1():
  if request.method == 'POST':
    emp = request.form['i1']
    cursor.execute('SELECT * FROM EmployeeInfo WHERE EmployeeID = ?', (emp))
    conn.commit()
  #return render_template('home.html')

@app.route('/query2', methods=["GET", "POST"])
def query2():
  if request.method == 'POST':
    dept = request.form['i1']
    cursor.execute('SELECT DISTINCT EmployeeID FROM EmployeeInfo WHERE (EndDate IS NULL OR EndDate >= GetDate()) && Department = ?', dept)
    conn.commit()

@app.route('/query3', methods=["GET", "POST"])
def query3():
  if request.method == 'POST':
    proj = request.form['i1']
    cursor.execute('SELECT (EmployeeID, Name) FROM EmployeeProjects WHERE Project = ? AND (EndDate IS NULL OR EndDate >= GetDate())', proj)
    conn.commit()

@app.route('/query4', methods=["GET", "POST"])
def query4():
  if request.method == 'POST':
    cursor.execute('SELECT distinct(zipCode) FROM Addresses GROUP BY zipCode HAVING count(zipCode) >= ALL (SELECT count(zipCode) FROM Addresses GROUP BY zipCode)')
    conn.commit()

@app.route('/query5', methods=["GET", "POST"])
def query5():
  if request.method == 'POST':
    proj = request.form['i1']
    cursor.execute('SELECT * FROM Projects WHERE Project = ?;', proj)
    conn.commit()

@app.route('/query6', methods=["GET", "POST"])
def query6():
  if request.method == 'POST':
    proj = request.form['i1']
    date = request.form['i2']
    cursor.execute('SELECT COUNT (EmployeeID) FROM EmployeeProjects WHERE Project = ? AND (EndDate IS NULL OR EndDate >= ?) AND (StartDate <= ?)', proj, date, date)
    conn.commit()

@app.route('/query7', methods=["GET", "POST"])
def query7():
  if request.method == 'POST':
    ben = request.form['i1']
    cursor.execute('SELECT COUNT (DISTINCT EmployeeID) FROM EmployeeBenefits WHERE (EndDate IS NULL OR EndDate >= GetDate()) AND Benefit = ?', ben)
    conn.commit()

@app.route('/query8', methods=["GET", "POST"])
def query8():
  if request.method == 'POST':
    proj = request.form['i1']
    role = request.form['i2']
    cursor.execute('SELECT EmployeeID FROM EmployeeProjects WHERE (EndDate IS NULL OR EndDate >= GetDate()) AND Project = ? AND Role = ?', proj, role)
    conn.commit()

@app.route('/query9', methods=["GET", "POST"])
def query9():
  if request.method == 'POST':
    cursor.execute('SELECT Project FROM Projects WHERE Status = \'in-progress\' OR Status = \'new\'')
    conn.commit()

@app.route('/query10', methods=["GET", "POST"])
def query10():
  if request.method == 'POST':
    cursor.execute('SELECT Department, EmployeeID, StartDate, EndDate FROM EmployeeAssignments GROUP BY Department')
    cursor.execute('SELECT Department, Project, ProjectLeader, Status FROM Projects GROUP BY DEPARTMENT')
    conn.commit()

@app.route('/query11', methods=["GET", "POST"])
def query11():
  if request.method == 'POST':
    emp = request.form['i1']
    cursor.execute('SELECT Role FROM EmployeeProjects WHERE (EndDate IS NULL OR EndDate >= GetDate()) AND EmployeeID = ?', emp)
    conn.commit()

@app.route('/query12', methods=["GET", "POST"])
def query12():
  if request.method == 'POST':
    emp = request.form['i1']
    cursor.execute('select role, startdate, enddate from EmployeeProjects where EmployeeID = ?', emp)
    conn.commit()

@app.route('/query13', methods=["GET", "POST"])
def query13():
  if request.method == 'POST':
    HealthPlan = request.form['i1']
    cursor.execute('SELECT COUNT(EmployeeInfo) FROM EmployeeInfo WHERE Coverage = ?', HealthPlan)
    conn.commit()

@app.route('/query14', methods=["GET", "POST"])
def query14():
  if request.method == 'POST':
    cursor.execute('select count(distinct employeeid), coverage from employeeInfo group by coverage')
    conn.commit()

@app.route('/query15', methods=["GET", "POST"])
def query15():
  if request.method == 'POST':
    role = request.form['i1']
    lev = request.form['i2']
  #not sure if this is how you'd solve the issue
    cursor.execute('SELECT AVG(CurrentSalary) FROM EmployeeInfo WHERE Gender = \'Female\' AND CurrentPosition = ? AND YearsExperience = ?', role, lev)
    #this was giving me errors regarding the '' with female and male -- yeah needed the \' oops
    cursor.execute('SELECT AVG(CurrentSalary) FROM EmployeeInfo WHERE Gender = \'Male\' AND CurrentPosition = ? AND YearsExperience = ?', role, lev)
    conn.commit()

@app.route('/query16', methods=["GET", "POST"])
def query16():
  if request.method == 'POST':
    pos = request.form['i1']
    cursor.execute('SELECT (minSalary, maxSalary) FROM Positions WHERE position = ?;', pos)
    conn.commit()

@app.route('/query17', methods=["GET", "POST"])
def query17():
  if request.method == 'POST':
    cursor.execute('select count(distinct project), status from projects group by status')
    conn.commit()

@app.route('/query18', methods=["GET", "POST"])
def query18():
  if request.method == 'POST':
    emp = request.form['i1']
    dep = request.form['i2']
    cursor.execute('SELECT (StartDate, EndDate) FROM EmployeeAssignments WHERE EmployeeID = ? AND Department = ?', emp, dep)
    conn.commit()

@app.route('/query19', methods=["GET", "POST"])
def query19():
  if request.method == 'POST':
    cursor.execute('SELECT (a.Project, b.Name) FROM Projects a, EmployeeID b, WHERE a.ProjectLeader == b.EmployeeID')
    conn.commit()

@app.route('/query20', methods=["GET", "POST"])
def query20():
  if request.method == 'POST':
    cursor.execute('SELECT (EmployeeID, Name) FROM EmployeeInfo WHERE 5*CurrentSalary >= 6*HiringSalary')
    conn.commit()

@app.route('/query21', methods=["GET", "POST"])
def query21():
  if request.method == 'POST':
    cursor.execute('select max(avg(CurrentSalary)) from ( select avg(CurrentSalary)  from EmployeeInfo group by CurrentPosition)')
    conn.commit()

def main ():
    insertIntoPositions('Research Scientist', 50000, 100000)
    #numerical values are arbitrary for now
    insertIntoPositions('Applied Scientist', 50000, 75000)
    insertIntoPositions('Engineer / Programmer', 80000, 150000)
    insertIntoPositions('Senior Programmer', 120000, 200000)
    insertIntoPositions('Director', 100000, 200000)
    insertIntoBenefits('health')
    insertIntoBenefits('dental')
    insertIntoBenefits('life insurance')
    insertIntoBenefits('short/long term disability')
    insertIntoProjectStatus('in progress')
    insertIntoProjectStatus('completed')
    insertIntoProjectStatus('new')
    insertIntoProjectStatus('on-hold')
    insertIntoHealthInsurance('Affordable Care Act')
    insertIntoHealthInsurance('Medicare')
    insertIntoHealthInsurance('family')
    insertIntoHealthInsurance('company')
