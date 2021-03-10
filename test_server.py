from scrapers.scrape_ga_futures import Course
import flask
import os
import shelve
def getCourses(college): #replace this using each name as an identifer
    #returns a dict of all classes EX:
    courses_list = []
    if college == "Georgia Gwinnett College":
        d = shelve.open("scrapers/Georgia_Gwinnett_college")
        for course_entry in d:
            courses_list.append(d[course_entry]) #prob redundant
        d.close()
        return courses_list


x = getCourses("Georgia Gwinnett College")
for course in x:
    print(course)
