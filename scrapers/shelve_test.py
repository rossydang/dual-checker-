 
 
from scrape_ga_futures import Course
import shelve

x = shelve.open("Georgia_Gwinnett_college")

p = x["46.0A924"]

print (p.title)
x.close()
