#a list of commands for creating tables
CREATE TABLE Positions 
(position CHAR(20) NOT NULL,
  minSalary SMALLINT NOT NULL,
  maxSalary SMALLINT NOT NULL,
  PRIMARY KEY (position),
  CHECK (0 < minSalary),
  CHECK (minSalary <= maxSalary));

CREATE TABLE HealthInsurance
(coverage CHAR(20) NOT NULL,
  PRIMARY KEY (coverage));

CREATE TABLE EmployeeInfo
(EmployeeID SMALLINT NOT NULL,
  SSN SMALLINT NOT NULL,
  Name CHAR(20) NOT NULL,
  gender CHAR(20) NOT NULL,
  DoB DATE NOT NULL,
  PrimaryAddress CHAR(80) NOT NULL,
  PhoneNumber CHAR(20) NOT NULL,
  HighestDegree CHAR(20) NOT NULL,
  YearsExperience SMALLINT NOT NULL,
  HiringPosition CHAR(20) NOT NULL,
  HiringSalary SMALLINT NOT NULL,
  CurrentPosition CHAR(20) NOT NULL,
  CurrentSalary SMALLINT NOT NULL,
  Coverage CHAR(20) NOT NULL,
  FOREIGN KEY K1 (HiringPosition) references Positions(position) ON DELETE CASCADE,
  FOREIGN KEY K2 (CurrentPosition) references Positions(position) ON DELETE CASCADE,
  FOREIGN KEY K3 (Coverage) references HealthInsurance(coverage) ON DELETE CASCADE,
  PRIMARY KEY (EmployeeID));
#how to verify that salary is within range?

CREATE TABLE Departments
(department CHAR(20) NOT NULL,
  PRIMARY KEY (department));

CREATE TABLE EmployeeAssignments
(EmployeeID SMALLINT NOT NULL,
  Department CHAR(20) NOT NULL,
  StartDate DATE NOT NULL,
  EndDate DATE NOT NULL,
  FOREIGN KEY K4 (EmployeeID) references EmployeeInfo(EmployeeID) ON DELETE CASCADE,
  FOREIGN KEY K5 (Department) references Departments(department) ON DELETE CASCADE,
  PRIMARY KEY (EmployeeID, Department, StartDate));

CREATE TABLE Benefits
(benefit CHAR(20) NOT NULL,
  PRIMARY KEY (benefit));

CREATE TABLE EmployeeBenefits 
(EmployeeID SMALLINT NOT NULL,
  Benefit CHAR(20) NOT NULL,
  StartDate DATE NOT NULL,
  EndDate DATE NOT NULL,
  FOREIGN KEY K6 (EmployeeID) references EmployeeInfo(EmployeeID) ON DELETE CASCADE,
  FOREIGN KEY K7 (Benefit) references Benefits(benefit) ON DELETE CASCADE,
  PRIMARY KEY (EmployeeID, Department, StartDate));

CREATE TABLE ProjectStatus
(status CHAR(20) NOT NULL,
  PRIMARY KEY (status));

CREATE TABLE Projects
(Project CHAR(20) NOT NULL,
  Department CHAR(20) NOT NULL,
  ProjectLeader SMALLINT NOT NULL,
  Status CHAR(20) NOT NULL,
  FOREIGN KEY K8 (Department) references Department(department) ON DELETE CASCADE,
  FOREIGN KEY K9 (ProjectLeader) references EmployeeInfo(EmployeeID) ON DELETE CASCADE,
  FOREIGN KEY KA (Status) references ProjectStatus(status) ON DELETE CASCADE,
  PRIMARY KEY (Project));


