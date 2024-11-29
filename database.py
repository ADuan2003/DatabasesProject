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
  zipCode SMALLINT NOT NULL,
  PRIMARY KEY (address));
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Positions 
(position TEXT NOT NULL,
  minSalary SMALLINT NOT NULL,
  maxSalary SMALLINT NOT NULL,
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
(EmployeeID SMALLINT NOT NULL,
  SSN SMALLINT NOT NULL,
  Name TEXT NOT NULL,
  gender TEXT NOT NULL,
  DoB DATE NOT NULL,
  PrimaryAddress TEXT NOT NULL,
  PhoneNumber TEXT NOT NULL,
  HighestDegree TEXT NOT NULL,
  YearsExperience SMALLINT NOT NULL,
  HiringPosition TEXT NOT NULL,
  HiringSalary SMALLINT NOT NULL,
  CurrentPosition TEXT NOT NULL,
  CurrentSalary SMALLINT NOT NULL,
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
(EmployeeID SMALLINT NOT NULL,
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
(EmployeeID SMALLINT NOT NULL,
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
  ProjectLeader SMALLINT NOT NULL,
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
(EmployeeID SMALLINT NOT NULL,
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

#@app.route('/updateEmployeeInfo/', methods=['POST'])
#def query():
#  return render_template('updateEmployeeInfo.html')

#@app.route('/delete/', methods=['POST'])
#def query():
#  return render_template('delete.html')

#@app.route('/addinsurance/', methods=['POST'])
#def query():
#  return render_template('addinsurance.html')

#@app.route('/addbenefit/', methods=['POST'])
#def query():
#  return render_template('addbenefit.html')

#@app.route('/addstatus/', methods=['POST'])
#def query():
#  return render_template('addstatus.html')

#@app.route('/addaddress/', methods=['POST'])
#def query():
#  return render_template('addaddress.html')

#@app.route('/addposition/', methods=['POST'])
#def query():
#  return render_template('addposition.html')

#@app.route('/adddepartment/', methods=['POST'])
#def query():
#  return render_template('adddepartment.html')

#@app.route('/addemployee/', methods=['POST'])
#def query():
#  return render_template('addemployee.html')

#@app.route('/addempbenefit/', methods=['POST'])
#def query():
#  return render_template('addempbenefit.html')

#@app.route('/addproject/', methods=['POST'])
#def query():
#  return render_template('addproject.html')

#@app.route('/addrole/', methods=['POST'])
#def query():
#  return render_template('addrole.html')

#@app.route('/addempproj/', methods=['POST'])
#def query():
#  return render_template('addempproj.html')

#@app.route('/addassignment/', methods=['POST'])
#def query():
#  return render_template('addassignment.html')
  
#to blend the html requests with the python, we'll need https://stackoverflow.com/questions/5615228/call-a-python-function-within-a-html-file

#the below will also need@app.route -- basically the above app routes took someone to the non-home pages; these take them back from the non-home pages

def insertIntoHealthInsurance(coverage):
    cursor.execute('INSERT INTO HealthInsurance (coverage) VALUES (?)', (coverage))
    conn.commit()

def insertIntoBenefits(benefit):
    cursor.execute('INSERT INTO Benefits (benefit) VALUES (?)', (benefit))
    conn.commit()

def insertIntoProjectStatus(status):
    cursor.execute('INSERT INTO ProjectStatus (status) VALUES (?)', (status))
    conn.commit()

def insertIntoAddresses(address, zipcode):
    cursor.execute('INSERT INTO Addresses (address, zipCode) VALUES (?, ?)', (address, zipcode))
    conn.commit()

def insertIntoPositions(position, minSalary, maxSalary):
    cursor.execute('INSERT INTO Positions (position, minSalary, maxSalary) VALUES (?, ?, ?)', (position, minSalary, maxSalary))
    conn.commit()

def insertIntoDepartments(department):
    cursor.execute('INSERT INTO Departments (department) VALUES (?)', (department))
    conn.commit()

def insertIntoEmployeeInfo(employeeID, ssn, name, gender, DoB, address, phone, degree, years, hiringPosition, hiringSalary, currentPosition, currentSalary, coverage):
    cursor.execute('INSERT INTO EmployeeInfo (EmployeeID, SSN, Name, gender, DoB, PrimaryAddress, PhoneNumber, HighestDegree, YearsExperience, HiringPosition, HiringSalary, CurrentPosition, CurrentSalary, Coverage) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (employeeID, ssn, name, gender, DoB, address, phone, degree, years, hiringPosition, hiringSalary, currentPosition, currentSalary, coverage))
    conn.commit()

def insertIntoEmployeeAssignments(employeeID, department, startDate, endDate):
    cursor.execute('INSERT INTO EmployeeAssignments (EmployeeID, Department, StartDate, EndDate) VALUES (?, ?, ?, ?)', (employeeID, department, startDate, endDate))
    conn.commit()

def insertIntoEmployeeBenefits(employeeID, benefit, startDate, endDate):
    cursor.execute('INSERT INTO EmployeeBenefits (EmployeeID, Benefit, StartDate, EndDate) VALUES (?, ?, ?, ?)', (employeeID, benefit, startDate, endDate))
    conn.commit()

def insertIntoProjects(project, department, projectLeader, status):
    cursor.execute('INSERT INTO Projects (Project, Department, ProjectLeader, Status) VALUES (?, ?, ?, ?)', (project, department, projectLeader, status))
    conn.commit()

def insertIntoRoles(role):
    cursor.execute('INSERT INTO Roles (role) VALUES (?)', (role))
    conn.commit()

def insertIntoEmployeeProjects(employeeID, project, role, startDate, endDate):
    cursor.execute('INSERT INTO EmployeeProjects (EmployeeID, Project, Role, StartDate, EndDate) VALUES (?, ?, ?, ?, ?)', (employeeID, project, role, startDate, endDate))
    conn.commit()

#the drop-down menu will definitely come in handy down below

#@app.route('/update-<table>-<column>-<value>-<cond1>-<cond2>/', methods=['POST'])
def updateTable(table, column, value, cond1, cond2):
    cursor.execute('UPDATE ? SET ? = ? WHERE ? = ?', (table, column, value, cond1, cond2))
    conn.commit()
#e.g. if it's like update table A set B = C where D = E
#then you would call updateTable('A', 'B', 'C', 'D', 'E')

#@app.route('/delete-<table>-<cond1>-<cond2>/', methods=['POST'])
def deleteFromTable(table, cond1, cond2):
    cursor.execute('DELETE FROM ? WHERE ? = ?', (table, cond1, cond2))
    conn.commit()

#these correspond to the queries we need to do in the instructions

#@app.route('/query1-<emp>/', methods=['POST'])
def query1(emp):
    cursor.execute('SELECT * FROM EmployeeInfo WHERE EmployeeID = ?', (emp))
    conn.commit()

#@app.route('/query2-<dept>/', methods=['POST'])
def query2(dept):
    cursor.execute('SELECT DISTINCT EmployeeID FROM EmployeeInfo WHERE (EndDate IS NULL OR EndDate >= GetDate()) && Department = ?', dept)
    conn.commit()

#@app.route('/query3-<proj>/', methods=['POST'])
def query3(proj):
    cursor.execute('SELECT (EmployeeID, Name) FROM EmployeeProjects WHERE Project = ? AND (EndDate IS NULL OR EndDate >= GetDate())', proj)
    conn.commit()

#@app.route('/query4/', methods=['POST'])
def query4():
    cursor.execute('SELECT distinct(zipCode) FROM Addresses GROUP BY zipCode HAVING count(zipCode) >= ALL (SELECT count(zipCode) FROM Addresses GROUP BY zipCode)')
    conn.commit()

#@app.route('/query5-<proj>/', methods=['POST'])
def query5(proj):
    cursor.execute('SELECT * FROM Projects WHERE Project = ?;', proj)
    conn.commit()

#@app.route('/query6-<proj>-<date>/', methods=['POST'])
def query6(proj, date):
    cursor.execute('SELECT COUNT (EmployeeID) FROM EmployeeProjects WHERE Project = ? AND (EndDate IS NULL OR EndDate >= ?) AND (StartDate <= ?)', proj, date, date)
    conn.commit()

#@app.route('/query7-<ben>/', methods=['POST'])
def query7(ben):
    cursor.execute('SELECT COUNT (DISTINCT EmployeeID) FROM EmployeeBenefits WHERE (EndDate IS NULL OR EndDate >= GetDate()) AND Benefit = ?', ben)
    conn.commit()

#@app.route('/query8-<proj>-<role>/', methods=['POST'])
def query8(proj, role):
    cursor.execute('SELECT EmployeeID FROM EmployeeProjects WHERE (EndDate IS NULL OR EndDate >= GetDate()) AND Project = ? AND Role = ?', proj, role)
    conn.commit()

#@app.route('/query9/', methods=['POST'])
def query9():
    cursor.execute('SELECT Project FROM Projects WHERE Status = \'in-progress\' OR Status = \'new\'')
    conn.commit()

#@app.route('/query10/', methods=['POST'])
def query10():
    cursor.execute('SELECT Department, EmployeeID, StartDate, EndDate FROM EmployeeAssignments GROUP BY Department')
    cursor.execute('SELECT Department, Project, ProjectLeader, Status FROM Projects GROUP BY DEPARTMENT')
    conn.commit()

#@app.route('/query11-<emp>/', methods=['POST'])
def query11(emp):
    cursor.execute('SELECT Role FROM EmployeeProjects WHERE (EndDate IS NULL OR EndDate >= GetDate()) AND EmployeeID = ?', emp)
    conn.commit()

#@app.route('/query12-<emp>/', methods=['POST'])
def query12(emp):
    cursor.execute('select role, startdate, enddate from EmployeeProjects where EmployeeID = ?', emp)
    conn.commit()

#@app.route('/query13-<HealthPlan>/', methods=['POST'])
def query13(HealthPlan):
    cursor.execute('SELECT COUNT(EmployeeInfo) FROM EmployeeInfo WHERE Coverage = ?', HealthPlan)
    conn.commit()

#@app.route('/query14/', methods=['POST'])
def query14():
    cursor.execute('select count(distinct employeeid), coverage from employeeInfo group by coverage')
    conn.commit()

#@app.route('/query15-<role>-<lev>/', methods=['POST'])
def query15(role, lev):
  #not sure if this is how you'd solve the issue
    cursor.execute('SELECT AVG(CurrentSalary) FROM EmployeeInfo WHERE Gender = \'Female\' AND CurrentPosition = ? AND YearsExperience = ?', role, lev)
    #this was giving me errors regarding the '' with female and male -- yeah needed the \' oops
    cursor.execute('SELECT AVG(CurrentSalary) FROM EmployeeInfo WHERE Gender = \'Male\' AND CurrentPosition = ? AND YearsExperience = ?', role, lev)
    conn.commit()

#@app.route('/query16-<pos>/', methods=['POST'])
def query16(pos):
    cursor.execute('SELECT (minSalary, maxSalary) FROM Positions WHERE position = ?;', pos)
    conn.commit()

#@app.route('/query17/', methods=['POST'])
def query17():
    cursor.execute('select count(distinct project), status from projects group by status')
    conn.commit()

#@app.route('/query15-<emp>-<dep>/', methods=['POST'])
def query18(emp, dep):
    cursor.execute('SELECT (StartDate, EndDate) FROM EmployeeAssignments WHERE EmployeeID = ? AND Department = ?', emp, dep)
    conn.commit()

#@app.route('/query19/', methods=['POST'])
def query19():
    cursor.execute('SELECT (a.Project, b.Name) FROM Projects a, EmployeeID b, WHERE a.ProjectLeader == b.EmployeeID')
    conn.commit()

#@app.route('/query20/', methods=['POST'])
def query20():
    cursor.execute('SELECT (EmployeeID, Name) FROM EmployeeInfo WHERE 5*CurrentSalary >= 6*HiringSalary')
    conn.commit()

#@app.route('/query21/', methods=['POST'])
def query21():
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
