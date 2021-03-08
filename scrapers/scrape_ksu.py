import bs4
import requests
from scrape_ga_futures import Course
import shelve
#probably could just import the course class thing from ggc_prereq2, but this is faster

class Course:
   
    def __init__(self, title, course_url):
        self.title = title
        self.course_url = course_url
    
    def __str__(self):
        return self.title + " " +  self.course_url
    
    def __repr__(self):
        return self.__str__()



page_urls = ["http://catalog.kennesaw.edu/content.php?catoid=51&catoid=51&navoid=3724&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D=1#acalog_template_course_filter", "http://catalog.kennesaw.edu/content.php?catoid=51&catoid=51&navoid=3724&filter%5Bitem_type%5D=3&filter%5Bonly_active%5D=1&filter%5B3%5D=1&filter%5Bcpage%5D=2#acalog_template_course_filter"]
base_url = "/content.php" #TODO don't hardcode this in
ksu_course_list = []
for url in page_urls:
    x = requests.get(url).text
    soup = bs4.BeautifulSoup(x, 'html.parser')
    p = soup.find_all("a")

    for link in p:
        try:
            k = link['href']
            if base_url in k:
                print(k)
            #print(k) #got attribute that contains link
            #print(link['title'])
            #too lazy to use regex, hope this doesn't hurt in the future 
                #title_index = link['title'].find("-") - 1
                #course_title = link['title'][:title_index]   #ex. ACCT 2101
                #course = Course(course_title, k)
                #ksu_course_list.append(  course  )
        except:
            continue
        
for course in ksu_course_list:
    print(course)
