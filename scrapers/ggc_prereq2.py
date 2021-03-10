import sqlite3
import bs4
import requests
from scrape_ga_futures import Course
import shelve
#use shelve module
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
class Course:
   
    def __init__(self, title, course_url, ID=False):
        self.title = title
        self.course_url = "https://catalog.ggc.edu/" +  course_url
        
        if ID:
            self.ID = ID
            
    
    def __str__(self):
        return self.title + " " +  self.course_url
    
    def __repr__(self):
        return self.__str__()

#again, another hack
class FinalCourse(Course):
    
    def __init__(self, title, course_url, credit_hours, prerequistes, description, ID):
        super.__init__(title, course_url)
        self. credit_hours = credit_hours
        self.prerequistes = prerequistes
        self.description = description
        self.ID = ID


g = "https://catalog.ggc.edu/"
#storing classes in database:
page_urls = ["https://catalog.ggc.edu/content.php?catoid=33&catoid=33&navoid=4229&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D=1#acalog_template_course_filter", "https://catalog.ggc.edu/content.php?catoid=33&catoid=33&navoid=4229&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D=2#acalog_template_course_filter", "https://catalog.ggc.edu/content.php?catoid=33&catoid=33&navoid=4229&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D=3#acalog_template_course_filter", "https://catalog.ggc.edu/content.php?catoid=33&catoid=33&navoid=4229&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D=4#acalog_template_course_filter", "https://catalog.ggc.edu/content.php?catoid=33&catoid=33&navoid=4229&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D=5#acalog_template_course_filter", "https://catalog.ggc.edu/content.php?catoid=33&catoid=33&navoid=4229&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D=6#acalog_template_course_filter", "https://catalog.ggc.edu/content.php?catoid=33&catoid=33&navoid=4229&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D=7#acalog_template_course_filter", "https://catalog.ggc.edu/content.php?catoid=33&catoid=33&navoid=4229&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D=8#acalog_template_course_filter", "https://catalog.ggc.edu/content.php?catoid=33&catoid=33&navoid=4229&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D=9#acalog_template_course_filter"] 

base_url = "preview_course_nopop.php?catoid=33&coid="
ggc_course_list = []

for url in page_urls:
    x = requests.get(url, verify=False).text
    soup = bs4.BeautifulSoup(x, 'html.parser')
    p = soup.find_all("a")

    for link in p:
        try:
            k = link['href']
            if base_url in k:
            #print(k) #got attribute that contains link
            #print(link['title'])
            #too lazy to use regex, hope this doesn't hurt in the future 
                title_index = link['title'].find("-") - 1
                course_title = link['title'][:title_index]   #ex. ACCT 2101
                course = Course(course_title, k)
                ggc_course_list.append(  course  )
        except:
            continue
#open shelve database
#for every url in ggc database,
    #for every page
        #if url in page:
            #break
        
def get_data(course_url):
    x = requests.get(course_url, verify=False).text
    soup = bs4.BeautifulSoup(x, 'html.parser')
    tables =soup.find_all("table")
    text = tables[0]
    #TODO refine this method cause it's a hack

    for br in text.find_all("br"):
        br.replace_with("\n")

    for script in text.find_all("script"):
        script.decompose()
    
    for script in text.find_all("span"):
        script.decompose()    
    
    for script in text.find_all("div"):
        script.decompose()    
#for script in text.find_all("a"): #use this for description
 #   script.decompose()    
    
    for script in text.find_all("h1"):
        script.decompose()    

    text = text.get_text().strip()
    lines_list = text. splitlines()
        
    #test for existance before popping
    #credit hours should always have an entry. if not that something's going on
    if "Credit Hours" in lines_list[0]: 
        credit_hours = lines_list.pop(0)

    if "Prerequisite" in lines_list[0]:
        prereqs = lines_list.pop(0)
        
    else:
        prereqs = "No prerequistes"

    description = ""
    for element in lines_list:
        description = description + element 
        
        
    #yeah it's another hack but whatever
    if "Global Search" in description:
        description = description.replace("Global Search", "" )

    #return description
    return (credit_hours, prereqs, description)
        

con = sqlite3.connect('GGC_dual_courses.db')
cur = con.cursor()
cur.execute('''   
    CREATE TABLE IF NOT EXISTS courses
    (ID TEXT PRIMARY KEY, 
     name TEXT NOT NULL,
     course_url TEXT DEFAULT "",
     credit_hours TINYINT,
     prereqs TEXT,
     description TEXT DEFAULT "",
     AP_equivalency TEXT DEFAULT ""
    )
    ''')


with shelve.open("Georgia_Gwinnett_college") as d:
    def getcourseIDs(course_name):
        
        #this is so messy and inefficient omg
        course_list = []
        for coursekey in d:
            course_list.append(d[coursekey])
        
        count = 0
        for course in course_list:
            if  course_name == course.ps_course:
                return course_list[count]
            count += 1 
                
        
    
    dual_course_list = []
    dual_course_ID = []
    for course_key in d:
        dual_course_list.append(d[course_key].ps_course)
    
    
    #compare the dual_course_list and ggc_course_list and find overlaps
    combined_courses = []
    combined_course_ID = []
    for course in ggc_course_list:
        if course.title in dual_course_list:
            combined_courses.append( course )
            course_id = getcourseIDs(course.title) #get course ID in same order as the combined_courses list
            
            #TODO CONFIRM THAT THE IDS ARE CORRECT
            combined_course_ID. append (course_id)
            
    
    
    
    combined_index = 0
    for elem in combined_courses: #TODO
        #add these courses to database 
        #print(elem.title + " " + elem.course_url   ) 
        
        x = get_data(elem.course_url)
        combined_url = combined_course_ID[combined_index]
        #print(x)
        
        #print ("")
        #print( "")
        
        #for now, print out their prequisites for me to view
        #yeah, not gonna be able to parse that
        #stored_course = FinalCourse(elem.title, elem.course_url, x(0), x(1), x(2), #elem.ID)
        
        t = (combined_url.ID, elem.title, elem.course_url, x[0], x[1], x[2], "" )
        cur. execute("INSERT INTO courses VALUES ( ?, ?, ?, ?, ?, ?,?)", t)
        combined_index += 1 
con.commit()

con.close()
        
        
        

    

