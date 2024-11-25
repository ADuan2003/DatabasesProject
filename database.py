import sqlite3

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
#semicolon optional? It only matters if there's multiple sql statements in one execute string

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
  FOREIGN KEY (HiringPosition) REFERENCES Positions(position),
  FOREIGN KEY (CurrentPosition) REFERENCES Positions(position),
  FOREIGN KEY (Coverage) REFERENCES HealthInsurance(coverage),
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
  FOREIGN KEY (EmployeeID) REFERENCES EmployeeInfo(EmployeeID),
  FOREIGN KEY (Department) REFERENCES Departments(department),
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
  FOREIGN KEY (EmployeeID) REFERENCES EmployeeInfo(EmployeeID),
  FOREIGN KEY (Benefit) REFERENCES Benefits(benefit),
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
  PRIMARY KEY (Employee, Project, Role)); 
''')

conn.commit()

#queries go here

#main method goes here

#insert format/syntax
#def funcName(args): 
# cursor.execute('insert into table (args) values (?)', (args))
# conn.commit()