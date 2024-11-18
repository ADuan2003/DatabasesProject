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
