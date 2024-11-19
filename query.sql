#stuff to fix -- I asked Amro
  #1 --> EndDates can be NULL; queries should see if they are 1) NULL or 2) in the future
  #2 --> address table should be created with address and ZIP code
  #3 --> StartDate, EndDate used for query on EmployeeProjects
  #4 --> 'a date' can refer to a past date
  #5 --> query no. 15 is about making comparison from current data

#1 -- Finding employee’s data for a given employee
# emp is the given EmployeeID
SELECT *
  FROM EmployeeInfo
  WHERE EmployeeID = emp;

#2 -- Finding who are employees of a given department
# dept is the given Department
# look into how to do the comparison -- maybe make dates yyyy-mm-dd?
SELECT DISTINCT EmployeeID
  FROM EmployeeInfo
  WHERE EndDate >= GetDate() && Department = dept
  
#3 -- Finding who are employees working on a given project
#proj is the given project
#should name be included?
SELECT (EmployeeID, Name)
  FROM EmployeeProjects
  WHERE Project = proj AND Current = TRUE;

#4 -- Finding the zip code that most employees live in
# how does address relate to ZIP code?
  

#5 -- Finding the project info of any given project
#proj is the given project
SELECT *
  FROM Projects
  WHERE Project = proj;

#6 -- Finding the number of employees working on a given project at any given time
#proj is the given project
# does this 'given time' possibly refer to a past time???
SELECT COUNT (EmployeeID)
  FROM EmployeeProjects
  WHERE Project = proj AND Current = True;

#7 -- Finding the number of employees who have a certain benefit
# ben is the given benefit
# look into how to do the comparison -- maybe make dates yyyy-mm-dd?
SELECT COUNT (DISTINCT EmployeeID)
  FROM EmployeeBenefits
  WHERE EndDate >= GetDate() && Benefit = ben;

#8 -- Finding the employee who has a given role in a given project
# role is the given role, and proj is the given project
SELECT EmployeeID
  FROM EmployeeProjects
  WHERE Current = TRUE AND Project = Proj AND Role = role;

#9 -- Finding all active projects
SELECT Project
  FROM Projects
  WHERE Status = 'in-progress' OR Status = 'new';

#10 -- Finding any information of each department.
# probably requires a join

#11 -- Finding the current role of an employee
# emp is the employee
SELECT Role
  FROM EmployeeProjects
  WHERE Current = TRUE AND EmployeeID = emp;
  

#12 -- Finding all roles of an employees along with the date
# I presume this meant 'employee'

#13 -- Finding the number of employees who have certain health plan
# HealthPlan is our variable
SELECT COUNT(EmployeeInfo)
  FROM EmployeeInfo
  WHERE Coverage = HealthPlan;

#14 -- Finding the number of employees for each and all the types of health plan
#very uncertain about this one
SELECT DISTINCT (COUNT(Coverage), Coverage)
  FROM EmployeeInfo
  GROUP BY Coverage;

#15 -- Finding if the salary of underpaid female employees (namely, those who for the same role and level as their male counter-part were paid less) is improved?

#16 -- Finding min & max salary for a given position
#pos is position
SELECT (minSalary, maxSalary)
  FROM Positions
  WHERE position = pos;

#17 -- Finding the number of projects per project status
#very uncertain about this one
SELECT DISTINCT (COUNT(Status), Status)
  FROM Projects
  GROUP BY Status;

#18 -- Finding the start & end date of a given employee for any of the employee’s department(s)
#emp is employee and dep is department
SELECT (StartDate, EndDate)
  FROM EmployeeAssignments
  WHERE EmployeeID = emp AND Department = dep;

#19 -- Finding the name of all project leaders along with the name of project
SELECT (a.Project, b.Name)
  FROM Projects a, EmployeeID b,
  WHERE a.ProjectLeader == b.EmployeeID;

#20 -- Finding whose salaries are increased by 20% since their hiring in the company
#does this include more than 20%?
SELECT (EmployeeID, Name)
  FROM EmployeeInfo
  WHERE 4*CurrentSalary >= 5*HiringSalary;

#21 -- Finding which position type has the highest average salary


#22 -- In addition to above queries, you may come up with other queries.

