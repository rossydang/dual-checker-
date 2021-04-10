
from scrapers.scrape_ga_futures import Course
import flask
from flask import Flask, request, render_template, session
app = Flask("dual")
import os
import shelve
import sqlite3
#database format is Course - MIN_SCORE, Course - MIN_SCORE
app.secret_key = b'_5#y2L"Fdkjhaw8z\n\xec]/'

avalible_courses = {
    "Georgia Gwinnet College": "Georgia_Gwinnett_college"
    }
transfer_courses = {
    "Georgia Tech": "Georgia_tech_courses"
} #unused for now 
AP_names = {
    "English Literature": "ENG L",
    "English Composition": "ENG C",
    "Calculus AB": "MATH AB",
    "Calculus BC": "MATH BC"
}
databases = {"Georgia Gwinnett College": "GGC_dual_courses.db"}

def parseStart(data):
    for key in data: #you're printing out each key
        #store them in session object
        session[key] = data[key]

@app.route('/', methods=["POST", "GET"])
def start():
    #greet user, ask to start
    #ask for ap classes 
    if request.method == 'POST': #store session data
        parseStart(request.form)
        session["course_id"] = 0 #internally used to keep track of checkboxes
        return flask.redirect("courses") #consider using the name thing 
    return render_template("start.html")
#optionally ask for major

@app.route('/js/<path:path>')
def send_js(path):
    return flask.send_from_directory('templates/js', path)

def AP_credit():
    #returns list of courses that user has  gotten credit through exams
    college_selected = session['college']
    course_con = sqlite3.connect("scrapers/" + databases[college_selected])
    cur = course_con.cursor()
    course_credits_granted = []
    ap_tests = []
    for test in session:
        if test == "college" or test =="transfer_college":
            pass 

        elif int(session[test]) > 0: 
        #TODO optimize later
            #create dict with the ap names, and place users score in them
            #loop through dict and find the transferable courses 
            #list of (test name, scores)
           # ap_tests.append( (key, session[key]))
            t =(  "%" + str(test) + "%" , ) #double the protection
            x = cur.execute("SELECT name, AP_equivalency FROM courses WHERE AP_equivalency LIKE ?", t)
            for row in x:
                #each row is a tuple of (credit, AP TEST - SCORE). credits can repeat multiple times
                #course_credits_granted.append(row)

                #I changed this to only include the credit 
                course_credits_granted.append(row[0])

            
    #get course credit
    course_con.close()
    return course_credits_granted


def parseCourses(data):
        #hack
        selection = list(data.keys())[0]
        template = ""
        #courses, major, or schedule
        if selection == "courses":
            template = "course_table.html"
        elif selection == "major":
            template = "placeholder" #TODO this 

        elif selection == "schedule":
            template = "placeholder" #TODO this
        else:
            return ("Something's gone wrong, I can feel it")

        return template 





@app.route('/courses', methods=["POST", "GET"])
def list_courses():
    selected_college = session["college"]
    transferring = session["transfer_college"]
    template = "course_table.html" #default
   
    if request.method == "POST":
        template = parseCourses(request.values)
        render_template(template, college =selected_college, items=getCourses(selected_college, transferring) )

    courses_list = []
    #college_selected = avalible_courses[request.form.get("college")] 
    #college_transfer = request.form.get("transfer_college")  




    return render_template("course_table.html", college= selected_college, items=getCourses(selected_college, transferring))


def getCourses(college, transferring): #replace this using each name as an identifer
    #returns a dict of all classes EX:
    courses_list = []
    if college == "Georgia Gwinnett College":
        d = shelve.open("scrapers/Georgia_Gwinnett_college", "r")
        for course_entry in d:
            #courses_list.append(d[course_entry]) #prob redundant
            college_table_info = WrapperClassCourse( d[course_entry] , transferring  )
            courses_list.append(college_table_info)
        d.close()

    return courses_list

    

    
    
    
    #find database to open
    #print out each course

#wrapper class for combining everything together... TODO unify all parts of my program into one universal class object and database...

class WrapperClassCourse(Course):

    def __init__(self, dual_college_course, transferring_college):
        super().__init__(dual_college_course.title, dual_college_course.ID, dual_college_course.name, dual_college_course.ps_course, dual_college_course.college_course_name)
        #this will have the AP equivalency, course equalency, and prerequistes and description in addition to all of this
        self.AP_equals = ""
        #self. description = description
        self.checkboxID = session["course_id"]
        session["course_id"] += 1


        #for credit in AP_credit():
            #self.AP_equals += credit
        ap_credits_gained = AP_credit()
        if self.ps_course in ap_credits_gained:
            #self.AP_equals = ap_credits_gained[ap_credits_gained.index(self.ps_course)]
            self.AP_equals = "Yes"

        #get prereqs
        self. dual_course_prereq = "" 

        college_selected = session['college']
        course_con = sqlite3.connect("scrapers/" + databases[college_selected])
        cur = course_con.cursor()

        t = ( self.ps_course,)
        for prereq_desc in cur.execute(''' SELECT prereqs FROM courses WHERE name LIKE ? ''', t):
            self.dual_course_prereq = prereq_desc[0]
        course_con.close()
            
        #set course equal
        self.course_equal = ""

        #TODO make this better
        if transferring_college == "Georgia Tech":
            p = sqlite3.connect("scrapers/ggc_gatech_transfer.db")
            l = p.cursor()
            j = (self.ps_course,)
            for transfer_credit in l.execute('''SELECT Gatech_description FROM ggc_gatech_transfer WHERE Ggc_course LIKE  ?''', j):
                self.course_equal = transfer_credit[0]
    
            p.close()

           

        
        



    
    




def getTransferred(selected_college, transferring_college):
    """returns a dict of all courses that are transferable between the selected institution and transferring instiution"""

    #a more efficient way probably exists but whatever I'll just merge them into the same database
     



@app.route('/college', methods=["POST", "GET"])
def pickCollege():
     if request.method == 'POST':
        college_selected = request.form.get("college")
        return render_template("course_table.html", items=getCourses(college_selected))
        
        #data =  flask.jsonify( {"college": getCourses(college_selected)  })
        
        
        
        
     return render_template("college.html")

    #use ajax request
    #handles picking a college 
    #then display the courses they can take and the prerequistes behind each course
    #display whether they have AP credit 
    #Color the prereq course in diff color if AP credit satisfied 
    #right now, do ksu and gatech
    
    
#once college is picked, ask them to select which college they want to transfer credits to
#see which credits transgers

@app.route('/dasd', methods=["POST", "GET"])
def showCouses():
    #show what courses are avalible at a college and its prerequistes
    pass

if __name__ == '__main__':
  
    app.run(debug=True)
