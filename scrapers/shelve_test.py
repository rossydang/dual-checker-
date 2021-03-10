 
 
from scrape_ga_futures import Course
import shelve

x = shelve.open("Georgia_Gwinnett_college")

for key in x:
    print(x[key].ps_course)

x.close()
