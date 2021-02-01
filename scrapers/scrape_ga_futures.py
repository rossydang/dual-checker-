"""Scrapes the dual enrollment course directory"""

import requests
import bs4
url = "https://www.gafutures.org/checs/DECourseDirectory/_DumpDataTable/?1607338557924&academic_yearinit=2021&partcollege_opeid=005601&categoryinit="



#print (requests.get(url).text)

#honestly I think using python's shelve module is fine enough 
class College:
    """Each college has their own unique ID and data payload"""
    
    def __init__(self, name, ID, url):
        self.name = name
        self.ID = ID
        self.url = url
        
        
    def getCourses(self):

        data = {"academic_yearinit" : "2021" , "partcollege_opeid": "001574" } #TODO don't hard code this in 
        
        text = requests.get(url).text
        courses = bs4.BeautifulSoup(text, 'html.parser')
        #TODO debug this for all colleges
        table = courses.find("table")
        table_body = table.find ("tbody")
        rows = table_body.find_all('tr')
        
        print(rows)
        
    def storeCourses():
        pass                        
        
if __name__ == "__main__":
    c = College("DSD", "sadsa" ,url)
    c.getCourses()
        
        
        
        
    
