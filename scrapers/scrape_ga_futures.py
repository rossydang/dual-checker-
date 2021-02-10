
import shelve
import requests
import bs4
url = "https://www.gafutures.org/checs/DECourseDirectory/_DumpDataTable/?1607338557924&academic_yearinit=2021&partcollege_opeid=005601&categoryinit="



#print (requests.get(url).text)

#honestly I think using python's shelve module is fine enough 
class Course:
    
    
    def __init__(self, title, name, ID, academy):
        self.title = title #IE ECON 1010
        self.name = name #
        self.ID = ID
        self.academy = academy

             
        


class College:
    """Each college has their own unique ID and data payload"""
    
    def __init__(self, name, ID, url):
        self.college_name = name
        self.ID = ID
        self.url = url
       
   
        
    def getCourses(self):

        data = {"academic_yearinit" : "2021" , "partcollege_opeid": "001574" } #TODO don't hard code this in 
        
        text = requests.get(url).text
        courses = bs4.BeautifulSoup(text, 'html.parser')
        #TODO debug this for all colleges
        table = courses.find("table")
        table_body = table.find ("tbody")
        rows = table_body.find_all('tr') #list of every table rows
        
        
        coursesList = []
        #test_course = rows[0].contents
        #print(test_course)
        
        for course in rows:
            
           # print (course.contents[1]) #CTAE place
           # print  (course.contents[3]) #ID number
           # print  (course.contents[5]) #title
            print(course)
            course_Store = Course(course.contents[5].get_text(), course.contents[3].get_text(), course.contents[1].get_text()) #TODO check if this works for every course in ga 
            
            coursesList.append(course_Store)
            
            self.storeCourses(coursesList)
        
        
        
    def storeCourses(self, courses):
        #ID will be main key in storing courses
        savedCourses = shelve.open(self.college_name)
        
        for course in courses:
            if course.ID in savedCourses:
                pass
            
            else:
                #create entry 
                
        #BIG TODO figure out how to handle when the course directory deletes a course
                
            

def initalize():
    KSU = ""
    GGC = ""
    GaTech = ""
    




        
if __name__ == "__main__":
    c = College("DSD", "sadsa" ,url)
    c.getCourses()
        
        
        
        
    
