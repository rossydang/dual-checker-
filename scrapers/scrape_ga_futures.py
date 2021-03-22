
import shelve
import requests
import bs4
#url = "https://www.gafutures.org/checs/DECourseDirectory/_DumpDataTable/?1607338557924&academic_yearinit=2021&partcollege_opeid=005601&categoryinit="



#print (requests.get(url).text)

#honestly I think using python's shelve module is fine enough 
class Course:
    
    
    def __init__(self, title, ID, name, ps_course, college_course_name, academy=None):
        self.title = title #IE ECON 1010
        self.name = name #
        self.ID = ID
        self.academy = academy
        self. college_course_name = college_course_name
        self.ps_course = ps_course #whitespace is removed here to make things... slightly easier? 
        
        self.ap_credit = {
            #list of minimum AP scores to get credit
            }
             
        


class College:
    """Each college has their own unique ID and data payload"""
    
    def __init__(self, name, ID, url):
        self.college_name = name
        self.ID = ID
        self.url = url
        self.getCourses()
       
   
        
    def getCourses(self):

        #data = {"academic_yearinit" : "2021" , "partcollege_opeid": "001574" } #TODO don't hard code this in 
        
        text = requests.get(self.url).text
        courses = bs4.BeautifulSoup(text, 'html.parser')
        #TODO debug this for all colleges
        table = courses.find("table")
        table_body = table.find ("tbody")
        rows = table_body.find_all('tr') #list of every table rows
        
        
        coursesList = []
        #test_course = rows[0].contents
        #print(test_course)
        
        for course in rows:
            
            #print (course.contents[1]) #CTAE place
            #print  (course.contents[3]) #ID number
            #print  (course.contents[5]) #title
            print  (course.contents[9]) # college course name
            #print(course)
            #print(course.contents[7]) #PS course title - name in college 
            #there's a better method that fully remove all whitespace, but this should work for now 
            course_Store = Course(course.contents[5].get_text(), str( course.contents[3].get_text()), course.contents[1].get_text(), course.contents[7].get_text(), course.contents[9].get_text()) #TODO check if this works for every course in ga 
            
            #print(course.contents[4])
            coursesList.append(course_Store)
            
        self.storeCourses(coursesList)
        
        
        
    def storeCourses(self, coursesList):
        #ID will be main key in storing courses
        with shelve.open(self.college_name) as savedCourses:
        
            for course in coursesList:
                if course.ID in savedCourses:
                    pass
            
                else:
                    savedCourses[ course.ID ] = course
                    
            
                    
                    #create entry 
                    
            #print( list(savedCourses.keys()))
                
        #BIG TODO figure out how to handle when the course directory deletes a course
                
            

def initalize():
    KSU = ""
    GGC = "https://www.gafutures.org/checs/DECourseDirectory/_DumpDataTable/?1612967601471&academic_yearinit=2021&partcollege_opeid=041429&categoryinit="
    GaTech = ""
    




        
if __name__ == "__main__":
    GGC = "https://www.gafutures.org/checs/DECourseDirectory/_DumpDataTable/?1612967601471&academic_yearinit=2021&partcollege_opeid=041429&categoryinit="
    c = College("Georgia_Gwinnett_college", "sadsa" ,GGC)
    c.getCourses()
        
        
        
        
    
