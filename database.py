import sqlite3

#Connect to sqlLite database (or create if it doesn't exist)
conn = sqlite3.connect('database.db')

#Create a cursor object
cursor = conn.cursor()

#Create a table
cursor.execute('''
--a list of commands for creating tables
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
--this is referring to the name of the health insurance, yeah?
--I feel like you could remove this table and just put this info in EmployeeBenefits 
--altho if you did that, that might cause redundant updating 

-- (having to update both employeeInfo and employeeBenefits when health insurance changes...)
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
  FOREIGN KEY (HiringPosition) REFERENCES Positions(position),
  FOREIGN KEY (CurrentPosition) REFERENCES Positions(position),
  FOREIGN KEY (Coverage) REFERENCES HealthInsurance(coverage),
  PRIMARY KEY (EmployeeID));
--how to verify that salary is within range?
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
  FOREIGN KEY (EmployeeID) REFERENCES EmployeeInfo(EmployeeID),
  FOREIGN KEY (Department) REFERENCES Departments(department),
  PRIMARY KEY (EmployeeID, Department, StartDate)); --EndDate nullable
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
  FOREIGN KEY (EmployeeID) REFERENCES EmployeeInfo(EmployeeID),
  FOREIGN KEY (Benefit) REFERENCES Benefits(benefit),
  PRIMARY KEY (EmployeeID, Benefit, StartDate)); --EndDate nullable
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
  FOREIGN KEY (Department) REFERENCES Department(department),
  FOREIGN KEY (ProjectLeader) REFERENCES EmployeeInfo(EmployeeID),
  FOREIGN KEY (Status) REFERENCES ProjectStatus(status),
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
  FOREIGN KEY (EmployeeID) REFERENCES EmployeeInfo(EmployeeID),
  FOREIGN KEY (Project) REFERENCES Projects(Project),
  FOREIGN KEY (Role) REFERENCES Roles(role),
  PRIMARY KEY (Employee, Project, Role)); --EndDate nullable
''')

conn.commit()

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

def updateTable(table, column, value, cond1, cond2):
    cursor.execute('UPDATE ? SET ? = ? WHERE ? = ?', (table, column, value, cond1, cond2))
    conn.commit()
#e.g. if it's like update table A set B = C where D = E
#then you would call updateTable('A', 'B', 'C', 'D', 'E')

def deleteFromTable(table, cond1, cond2):
    cursor.execute('DELETE FROM ? WHERE ? = ?', (table, cond1, cond2))
    conn.commit()

#these correspond to the queries we need to do in the instructions

def query1(emp):
    cursor.execute('SELECT * FROM EmployeeInfo WHERE EmployeeID = ?', (emp))
    conn.commit()

def query2(dept):
    cursor.execute('SELECT DISTINCT EmployeeID FROM EmployeeInfo WHERE (EndDate IS NULL OR EndDate >= GetDate()) && Department = ?', dept)
    conn.commit()

def query3(proj):
    cursor.execute('SELECT (EmployeeID, Name) FROM EmployeeProjects WHERE Project = ? AND (EndDate IS NULL OR EndDate >= GetDate())', proj)
    conn.commit()

def query4():
    #this will need some actual writing
    conn.commit()

def query5(proj):
    cursor.execute('SELECT * FROM Projects WHERE Project = ?;', proj)
    conn.commit()

def query6(proj, date):
    cursor.execute('SELECT COUNT (EmployeeID) FROM EmployeeProjects WHERE Project = ? AND (EndDate IS NULL OR EndDate >= ?) AND (StartDate <= ?)', proj, date, date)
    conn.commit()

def query7(ben):
    cursor.execute('SELECT COUNT (DISTINCT EmployeeID) FROM EmployeeBenefits WHERE (EndDate IS NULL OR EndDate >= GetDate()) AND Benefit = ?', ben)
    conn.commit()

def query8(proj, role):
    cursor.execute('SELECT EmployeeID FROM EmployeeProjects WHERE (EndDate IS NULL OR EndDate >= GetDate()) AND Project = ? AND Role = ?', proj, role)
    conn.commit()

def query9():
    cursor.execute('SELECT Project FROM Projects WHERE Status = \'in-progress\' OR Status = \'new\'')
    conn.commit()

def query10():
    cursor.execute('SELECT Department, EmployeeID, StartDate, EndDate FROM EmployeeAssignments GROUP BY Department')
    cursor.execute('SELECT Department, Project, ProjectLeader, Status FROM Projects GROUP BY DEPARTMENT')
    conn.commit()

def query11(emp):
    cursor.execute('SELECT Role FROM EmployeeProjects WHERE (EndDate IS NULL OR EndDate >= GetDate()) AND EmployeeID = ?', emp)
    conn.commit()

def query12(emp):
    cursor.execute('select role, startdate, enddate from EmployeeProjects where EmployeeID = ?', emp)
    conn.commit()

def query13(HealthPlan):
    cursor.execute('SELECT COUNT(EmployeeInfo) FROM EmployeeInfo WHERE Coverage = ?', HealthPlan)
    conn.commit()

def query14():
    cursor.execute('select count(distinct employeeid), coverage from employeeInfo group by coverage')
    conn.commit()

def query15():
    #this will need some actual writing
    conn.commit()

def query16(pos):
    cursor.execute('SELECT (minSalary, maxSalary) FROM Positions WHERE position = ?;', pos)
    conn.commit()

def query17():
    cursor.execute('select count(distinct project), status from projects group by status')
    conn.commit()

def query18(emp, dep):
    cursor.execute('SELECT (StartDate, EndDate) FROM EmployeeAssignments WHERE EmployeeID = ? AND Department = ?', emp, dep)
    conn.commit()

def query19():
    cursor.execute('SELECT (a.Project, b.Name) FROM Projects a, EmployeeID b, WHERE a.ProjectLeader == b.EmployeeID')
    conn.commit()

def query20():
    cursor.execute('SELECT (EmployeeID, Name) FROM EmployeeInfo WHERE 5*CurrentSalary >= 6*HiringSalary')
    conn.commit()

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
