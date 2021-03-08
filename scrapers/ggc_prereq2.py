
import bs4
import requests
from scrape_ga_futures import Course
import shelve
#use shelve module

class Course:
   
    def __init__(self, title, course_url):
        self.title = title
        self.course_url = course_url
    
    def __str__(self):
        return self.title + " " +  self.course_url
    
    def __repr__(self):
        return self.__str__()



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
        
def get_prerequisites(course_url):
    x = requests.get(course_url, verify=False).text
    soup = BeautifulSoup(x, 'html.parser')
    
        
        

with shelve.open("Georgia_Gwinnett_college") as d:
    dual_course_list = []
    for course_key in d:
        dual_course_list.append(d[course_key].ps_course)
    #compare the dual_course_list and ggc_course_list and find overlaps
    combined_courses = []
    for course in ggc_course_list:
        if course.title in dual_course_list:
            combined_courses.append(course)
    
    for elem in combined_courses: #TODO
        #add these courses to database 
        
        #for now, print out their prequisites for me to view

    

