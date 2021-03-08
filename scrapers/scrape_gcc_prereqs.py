#temp file for testing 
 #create database of prereqs for classes
import requests
from scrape_ga_futures import Course
from selenium import webdriver
import shelve
import bs4
#used to click on all the links to get prereqs
#url = "https://catalog.ggc.edu/content.php?catoid=33&navoid=4229"
#url = "https://catalog.ggc.edu/content.php?catoid=33&catoid=33&navoid=4229&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D=9#acalog_template_course_filter"
#TODO use current data instead
driver = webdriver. Chrome("/home/ross/bin/chromedriver")
url_part = "https://catalog.ggc.edu/preview_course_nopop.php?catoid=33&coid="

page_urls = ["https://catalog.ggc.edu/content.php?catoid=33&catoid=33&navoid=4229&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D=1#acalog_template_course_filter", "https://catalog.ggc.edu/content.php?catoid=33&catoid=33&navoid=4229&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D=2#acalog_template_course_filter", "https://catalog.ggc.edu/content.php?catoid=33&catoid=33&navoid=4229&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D=3#acalog_template_course_filter", "https://catalog.ggc.edu/content.php?catoid=33&catoid=33&navoid=4229&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D=4#acalog_template_course_filter", "https://catalog.ggc.edu/content.php?catoid=33&catoid=33&navoid=4229&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D=5#acalog_template_course_filter", "https://catalog.ggc.edu/content.php?catoid=33&catoid=33&navoid=4229&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D=6#acalog_template_course_filter", "https://catalog.ggc.edu/content.php?catoid=33&catoid=33&navoid=4229&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D=7#acalog_template_course_filter", "https://catalog.ggc.edu/content.php?catoid=33&catoid=33&navoid=4229&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D=8#acalog_template_course_filter", "https://catalog.ggc.edu/content.php?catoid=33&catoid=33&navoid=4229&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D=9#acalog_template_course_filter"] 
#get all course preview links
#cheap hack I know, but TODO add a better method here

def get_course_urls():
    course_urls = []
    #get list of links for every course in ga course directory 
    #method: first go get link for every course in GGC course catalog
    for course_url in page_urls:
        driver.get(course_url)
        list_links = list_links = driver.find_elements_by_tag_name('a')
        for i in list_links:
            if ( url_part in str(i.get_attribute('href'))  ):
                course_urls.append(i.get_attribute('href'))
                course_urls.append(str(i.get_attribute('href')))
    return course_urls
    driver.quit()

def scrape_course(url_list):
    output = []
    for url in url_list:
        text = requests.get(url, verify=False).text
        soup = bs4.BeautifulSoup(text)
        course_ps_title = soup.find_all(class_="n1_header")[0]
        output.append(course_ps_title)
        
        

#scrape course info, mainly prereqs


#url = "https://catalog.ggc.edu/preview_course_nopop.php?catoid=33&coid=5484"


class GGCCourse():
    
    def __init__(self):
        self.prereq_clause = []
    
    def addPrequisite(self):
        """clauses will be represented by a seperate object placed into the prereq_clause list"""
        pass
    
    def checkPrereq(self):
        pass

#x = requests.get(url, verify=False).text
#print(x)


ggc_courses_list = scrape_course(get_course_urls())

with shelve.open("Georgia_Gwinnett_college") as d:
    dual_course_list = []
    for course_key in d:
        dual_course_list.append(d[course_key].ps_course)
    #compare the dual_course_list and ggc_course_list and find overlaps
    #probably could use some cool list comphrension jazz but nah
    combined_courses = [course for course in dual_couse_list if elem in ggc_course_list]
    for elem in combined_course:
        print(elem)



#nah, create database of courses



