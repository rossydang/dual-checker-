
from scrapers.scrape_ga_futures import Course
import flask
from flask import Flask, request, render_template
app = Flask("dual")
import os
import shelve
avalible_courses = {
    "Georgia Gwinnet College": "Georgia_Gwinnett_college"
    }

@app.route('/', methods=["POST", "GET"])
def start():
    #greet user, ask to start
    #ask for ap classes 
    if request.method == 'POST':
        tests_taken = request.form #AP scores
        print(tests_taken)
        return flask.redirect("/college")

        
    return render_template("start.html")
#optionally ask for major

def getCourses(college): #replace this using each name as an identifer
    #returns a dict of all classes EX:
    courses_list = []
    if college == "Georgia Gwinnett College":
        d = shelve.open("scrapers/Georgia_Gwinnett_college")
        for course_entry in d:
            courses_list.append(d[course_entry]) #prob redundant
        d.close()
        return courses_list
    
    
    #find database to open
    #print out each course


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
