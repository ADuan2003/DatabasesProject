// Online Java Compiler
// Use this editor to write, compile and run your Java code online

class Main {
    public static void main(String[] args) {
        //open up scanner from keyboard
        //while (true) I think???
        //and take something in and see what to do with it
    }
    public static void add (String table, String[] info) {
        //link to table and run add command on info
    }
    public static void update (String table, String[] colsToChange, String[] newColValues, String onCol, Object onValue) {
        //colsToChange represents columns in the tuple that will get new values
        //newColValues are the new values they will get
        //onCol and onValue represent that these changes will occur where onCol == onValue
    }
    public static void delete (String table, String onCol, Object onValue) {
        //link to table and look for info to delete
    }
    public String[] findEmployeeData (String employeeID) {
        //looks into employee table; #1
    }
    public String[] findEmployeesDepartment (String department) {
        //#2
    }
    public String[] findEmployeesProject (String project) {
        //#3
    }
    public String findMostCommonZIPCode () {
        //#4
    }
    public String findProjectInfo () {
        //#5
    }
    // I imagine we'll just set up one function for each numbered thing we'll need to do in the project
}
