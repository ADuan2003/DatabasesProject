#1 -- Finding employee’s data for a given employee
# emp is the given EmployeeID
SELECT *
  FROM EmployeeInfo
  WHERE (EmployeeID = emp);

#2 -- Finding who are employees of a given department
# dept is the given Department
# look into how to do the comparison -- maybe make dates yyyy-mm-dd?
SELECT DISTINCT EmployeeID
  FROM EmployeeInfo
  WHERE (EndDate >= GetDate() && Department = dept)
  
#3 -- Finding who are employees working on a given project


#4 -- Finding the zip code that most employees live in

#5 -- Finding the project info of any given project

#6 -- Finding the number of employees working on a given project at any given time

#7 -- Finding the number of employees who have a certain benefit

#8 -- Finding the employee who has a given role in a given project

#9 -- Finding all active projects

#10 -- Finding any information of each department.

#11 -- Finding the current role of an employee

#12 -- Finding all roles of an employees along with the date
# I presume this meant 'employee'

#13 -- Finding the number of employees who have certain health plan

#14 -- Finding the number of employees for each and all the types of health plan

#15 -- Finding if the salary of underpaid female employees (namely, those who for the same role and level as their male counter-part were paid less) is improved?
