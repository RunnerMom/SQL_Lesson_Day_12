import sqlite3

DB = None
CONN = None

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    if row == None:
        print "Student does not exist."
    else:
        print """\
    Student: %s %s
    Github account: %s"""%(row[0], row[1], row[2])

def get_grade(title):
    query = """SELECT * FROM Projects where title=?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    if row ==None:
        print "Project does not exist. format grade <title>"
    else:
        print """\
    Project: %s 
    Description: %s
    """%(row[0], row[1], row[2])

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" %(first_name, last_name)


def add_project(title, description, max_grade):
    query = """INSERT into Projects values (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added Project: %s %s %s" %(title, description, max_grade)

def get_project_title(title):
    query = """SELECT * FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    if row == None:
        print "Title doesn't exist."
    else:
        print """\
    Title: %s
    Description: %s
    Max Grade: %s """ %(row[0], row[1], row[2])


def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            if len(args)==1:
                get_student_by_github(*args) 
            else:
                print "incorrect arguments, correct format is: student <github>. "
        elif command == "new_student":
            if len(args)==3:
                make_new_student(*args)
            else:
                print "incorrect arguments, correct format is: new_student <fname> <lname> <github>"
        elif command == "projects":
            if len(args)== 1:
                get_project_title(*args)
            else:
                print "Incorrect argument, correct format is: projects <title>"
        elif command == "project+":             #checks for string arg
            if len(args) > 3:
                title= tokens[1]
                description = " ".join(tokens[2:-1]) #everything in between is the string
                max_grade = tokens[-1]
                add_project(title, description, max_grade)
            else:
                print """Incorrect number of arguments, correct format is: 
                project+ <title> <description> <max_grade>"""
        else:
            print "That was not a valid command."

    CONN.close()

if __name__ == "__main__":
    main()
