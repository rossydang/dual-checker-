 
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#url = "https://catalog.ggc.edu/preview_course_nopop.php?catoid=33&coid=5527"
url = "https://catalog.ggc.edu/preview_course_nopop.php?catoid=33&coid=5513"
x = requests.get(url, verify=False).text
#print(x)

#TODO don't hardcode year


#For now, I'm just going to list the course descriptions 


#ignore SAT scores and permission thing, will do later
#to simpliy for now, gonna ignore the extra MATH and ENG things
content = BeautifulSoup(x, 'html.parser')
#p = content.findAll('p')[3].find_all('a')

prereq_desc =  content.findAll('p')[3].get_text()
print(prereq_desc)


#final_course = set()
#for course in p:
#    course_prereq_title = course.string
    #print(course_prereq_title)
#    final_course.add(course_prereq_title)
#print(final_course)
#preview_course_nopop.php?catoid=33&coid=
#scrape title
