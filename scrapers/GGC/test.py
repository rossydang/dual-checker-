 
import requests
import bs4
import re
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
url = "https://catalog.ggc.edu/preview_course_nopop.php?catoid=33&coid=5594"
#url = https://catalog.ggc.edu/preview_course.php?catoid=33&coid=5508&print

x = requests.get(url, verify=False).text

soup = bs4.BeautifulSoup(x, 'html.parser')
#print(soup.prettify())
p =soup.find_all("table")


#goal:
#find credit hours
#get course description
#get course prereqs

#get first result 

#TODO refine this method. It's quick hack
text = p[0]


for br in text.find_all("br"):
    br.replace_with("\n")
# replaces matches with the newline
#print(newtext)



#table_list = text.find_all("table")
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

if "Prerequisite" in lines_list[0]
    prereqs = lines_list.pop(0)

description = ""
for element in lines_list:
        description = description + element 

print(description)







#print(text.get_text().strip())
#print(text.prettify())
    
    
#print(table_list[1].prettify())

#for l in p:
    #if "BCHM" in l.get_text():
        
        
    
    

#the below code gets the prequisites, but without any of the special clauses
#p =soup.find_all("a")
#for l in p:
   # print(l.get_text())

#get preqs

