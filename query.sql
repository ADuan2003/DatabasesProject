-- I googled and apparently comments in sql are actually with "--"

#stuff to fix -- I asked Amro
  #Priority 1 --> finish queries

#1 -- Finding employee’s data for a given employee
# emp is the given EmployeeID
SELECT *
  FROM EmployeeInfo
  WHERE EmployeeID = emp;

#2 -- Finding who are employees of a given department
# dept is the given Department
# look into how to do the comparison -- maybe make dates yyyy-mm-dd?
-- What is the usual format for Date in SQL again? Just put it in that format and the operators should probably just work? 
SELECT DISTINCT EmployeeID
  FROM EmployeeInfo
  WHERE (EndDate IS NULL OR EndDate >= GetDate()) && Department = dept
  
#3 -- Finding who are employees working on a given project
#proj is the given project
#should name be included?
-- if you want name you're gonna need a join with EmployeeInfo -E
SELECT (EmployeeID, Name)
  FROM EmployeeProjects
  WHERE Project = proj AND (EndDate IS NULL OR EndDate >= GetDate());

#4 -- Finding the zip code that most employees live in
# how does address relate to ZIP code?
--I'm thinking we're gonna split address into multiple sections (street, city, state, zip, etc.), and then have a table for address??
--  Not entirely sure how the foreign keys are gonna work tho (unless we just dump everything into EmployeeInfo, but will that still maintain 3NF and losslessness?) -E

#5 -- Finding the project info of any given project
#proj is the given project
SELECT *
  FROM Projects
  WHERE Project = proj;

#6 -- Finding the number of employees working on a given project at any given time
#proj is the given project
#date is the given date
# does this 'given time' possibly refer to a past time???
-- Probably -E 
--Do we wanna add "distinct"? Ex. select distinct count(employeeid) -E
SELECT COUNT (EmployeeID)
  FROM EmployeeProjects
  WHERE Project = proj AND (EndDate IS NULL OR EndDate >= date) AND (StartDate <= date);

#7 -- Finding the number of employees who have a certain benefit
# ben is the given benefit
# look into how to do the comparison -- maybe make dates yyyy-mm-dd?
SELECT COUNT (DISTINCT EmployeeID)
  FROM EmployeeBenefits
  WHERE (EndDate IS NULL OR EndDate >= GetDate()) AND Benefit = ben;

#8 -- Finding the employee who has a given role in a given project
# role is the given role, and proj is the given project
SELECT EmployeeID
  FROM EmployeeProjects
  WHERE (EndDate IS NULL OR EndDate >= GetDate()) AND Project = Proj AND Role = role;

#9 -- Finding all active projects
SELECT Project
  FROM Projects
  WHERE Status = 'in-progress' OR Status = 'new';

#10 -- Finding any information of each department.
# probably requires a join
--I'm sensing a chain of ifs... -E
select --wanted attributes
  from --projects or employeeassigments depending on the wanted info 
  where --insert operators

#11 -- Finding the current role of an employee
# emp is the employee
SELECT Role
  FROM EmployeeProjects
  WHERE (EndDate IS NULL OR EndDate >= GetDate()) AND EmployeeID = emp;
  

#12 -- Finding all roles of an employees along with the date
# I presume this meant 'employee'
--depending on how info is entered, we might need a join to find the id associated with an employee's name 
select role, startdate, enddate
  from EmployeeProjects
  where --find emp

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
--how would you find the improvement of something...? Especially since we're (presumably) not storing former salaries of people... 
--something something data warehouse? 

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
select max(avg(CurrentSalary))
  from (
    select avg(CurrentSalary) 
    from EmployeeInfo
    group by CurrentPosition)

#22 -- In addition to above queries, you may come up with other queries.

