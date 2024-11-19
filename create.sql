#a list of commands for creating tables
CREATE TABLE Positions 
(position CHAR(40) NOT NULL,
  minSalary SMALLINT NOT NULL,
  maxSalary SMALLINT NOT NULL,
  PRIMARY KEY (position),
  CHECK (0 < minSalary),
  CHECK (minSalary <= maxSalary));

CREATE TABLE HealthInsurance
(coverage CHAR(40) NOT NULL,
  PRIMARY KEY (coverage));

CREATE TABLE EmployeeInfo
(EmployeeID SMALLINT NOT NULL,
  SSN SMALLINT NOT NULL,
  Name CHAR(30) NOT NULL,
  gender CHAR(20) NOT NULL,
  DoB DATE NOT NULL,
  PrimaryAddress CHAR(100) NOT NULL,
  PhoneNumber CHAR(20) NOT NULL,
  HighestDegree CHAR(20) NOT NULL,
  YearsExperience SMALLINT NOT NULL,
  HiringPosition CHAR(40) NOT NULL,
  HiringSalary SMALLINT NOT NULL,
  CurrentPosition CHAR(40) NOT NULL,
  CurrentSalary SMALLINT NOT NULL,
  Coverage CHAR(40) NOT NULL,
  FOREIGN KEY (HiringPosition) references Positions(position) ON DELETE CASCADE,
  FOREIGN KEY (CurrentPosition) references Positions(position) ON DELETE CASCADE,
  FOREIGN KEY (Coverage) references HealthInsurance(coverage) ON DELETE CASCADE,
  PRIMARY KEY (EmployeeID));
#how to verify that salary is within range?

CREATE TABLE Departments
(department CHAR(30) NOT NULL,
  PRIMARY KEY (department));

CREATE TABLE EmployeeAssignments
(EmployeeID SMALLINT NOT NULL,
  Department CHAR(30) NOT NULL,
  StartDate DATE NOT NULL,
  EndDate DATE NOT NULL,
  FOREIGN KEY (EmployeeID) references EmployeeInfo(EmployeeID) ON DELETE CASCADE,
  FOREIGN KEY (Department) references Departments(department) ON DELETE CASCADE,
  PRIMARY KEY (EmployeeID, Department, StartDate));

CREATE TABLE Benefits
(benefit CHAR(30) NOT NULL,
  PRIMARY KEY (benefit));

CREATE TABLE EmployeeBenefits 
(EmployeeID SMALLINT NOT NULL,
  Benefit CHAR(30) NOT NULL,
  StartDate DATE NOT NULL,
  EndDate DATE NOT NULL,
  FOREIGN KEY (EmployeeID) references EmployeeInfo(EmployeeID) ON DELETE CASCADE,
  FOREIGN KEY (Benefit) references Benefits(benefit) ON DELETE CASCADE,
  PRIMARY KEY (EmployeeID, Benefit, StartDate));

CREATE TABLE ProjectStatus
(status CHAR(20) NOT NULL,
  PRIMARY KEY (status));

CREATE TABLE Projects
(Project CHAR(40) NOT NULL,
  Department CHAR(30) NOT NULL,
  ProjectLeader SMALLINT NOT NULL,
  Status CHAR(20) NOT NULL,
  FOREIGN KEY (Department) references Department(department) ON DELETE CASCADE,
  FOREIGN KEY (ProjectLeader) references EmployeeInfo(EmployeeID) ON DELETE CASCADE,
  FOREIGN KEY (Status) references ProjectStatus(status) ON DELETE CASCADE,
  PRIMARY KEY (Project));

CREATE TABLE Roles
(role CHAR(30) NOT NULL,
  PRIMARY KEY (role));

CREATE TABLE EmployeeProjects
(EmployeeID SMALLINT NOT NULL,
  Project CHAR(40) NOT NULL,
  Role CHAR(30) NOT NULL,
  StartDate DATE NOT NULL,
  EndDate DATE NOT NULL, 
  FOREIGN KEY (EmployeeID) references EmployeeInfo(EmployeeID) ON DELETE CASCADE,
  FOREIGN KEY (Project) references Projects(Project) ON DELETE CASCADE,
  FOREIGN KEY (Role) references Roles(role) ON DELETE CASCADE,
  PRIMARY KEY (Employee, Project, Role));
