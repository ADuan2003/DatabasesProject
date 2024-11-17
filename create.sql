#a list of commands for creating tables
CREATE TABLE Positions 
(position CHAR(20) NOT NULL,
  minSalary SMALLINT NOT NULL,
  maxSalary SMALLINT NOT NULL,
  PRIMARY KEY (position));
