 
import requests
import bs4
x = requests.get("https://catalog.ggc.edu/preview_course.php?catoid=33&coid=5508&print", verify=False).text

soup = bs4.BeautifulSoup(x, 'html.parser')
#print(soup.prettify())
p =soup.find_all("table")

for l in p:
    print(l.get_text())

#the below code gets the prequisites, but without any of the special clauses
#p =soup.find_all("a")
#for l in p:
   # print(l.get_text())

#get preqs

