import requests
from bs4 import BeautifulSoup
import re
base_url = "https://ggc.gabest.usg.edu/pls/B400/bwckschd.p_disp_dyn_sched"
import sqlite3

base_url2 = "https://ggc.gabest.usg.edu/pls/B400/bwckschd.p_get_crse_unsec?"

#TODO don't hardcode this in

#data = "term_in=202102&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj=BIOL
#&sel_crse=&sel_title=&sel_schd=%25&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&sel_levl=%25&sel_ptrm=%25&sel_instr=%25&sel_attr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a"

subjects = [
	"dummy",
	"ACCT",
	"AFAM",
	"ANTH",
	"ARTS",
	"BCHM",
	"BIOL",
	"BUSA",
	"CHEM",
	"CHIN",
	"CMAP",
	"COMM",
	"CSCI",
	"CJCR",
	"ECON",
	"EDUC",
	"ELED",
	"ENGL",
	"ELAN",
	"ESNS",
	"ESSS",
	"EXSC",
	"FILM",
	"FINA",
	"FREN",
	"GNDR",
	"GEOG",
	"GFA",
	"GGC",
	"HSCI",
	"HIST",
	"HNRS",
	"HDAS",
	"ITEC",
	"ISCI",
	"LEAD",
	"MGMT",
	"MKTG",
	"MATH",
	"MSL",
	"MUSC",
	"NURS",
	"PHIL",
	"PHED",
	"PSCI",
	"PHYS",
	"POLS",
	"PSYC",
	"READ",
	"RELN",
	"STEC",
	"SOCI",
	"SPAN",
	"SCM", 
	"THEA" ]
#the entire thing is just a bunch of tr's. Find tr that contains the course, and then move down to find 1 tr for class information

def verifyA_tags(tags):
    #TODO find a better way of doing this
    
    #This is such a hack omg
    count = 0
    
    #iterate through all of the tags, but skip the first 4 lines
    #since those aren't classes
    output = []
    for tag in tags:
        string = tag.get_text()
        if count != 6:
            count += 1
            continue
        
        if "View Catalog Entry" not in string and "Return to Previous" not in string and "Skip to top of page" not in string and "Go to Main Content" not in string and string != "":
            
            output.append(tag)
            
    return output
            
    
   # for element in output:
    #    print(element)
        
    #print(len(output[310]))
        
    
class CourseSchedule():
    #TODO ignore labs for now. Add later
    #easy place to parse course availibility
    #tag is the tr immediately after the the title a tag
    def __init__(self, course_name, tag):
        self.course_name = course_name.get_text() #a long title that has more info than something like BIOL 2000
        x = tag.find_all('tr')
        
        print("-----" + course_name.get_text() + "----------")
        
        
        def _get_name(): #used for identifying in database
            regex = re.compile("[a-zA-Z]+\s[0-9]+\S+",re.IGNORECASE)
            self.course_title = regex.findall(self.course_name)[0]
            
        def _store_database():
            
            t = (self.course_title, self.course_name, self.class_type)
            cur.execute('''
                INSERT INTO Semester VALUES (?, ?, ?) ''', t)
            
     
            
        
        
        def _parse(text):
            #find line that contains class
            #Sometimes a class can only have a Lab part, or have both a Lab and Class Part. Get Class part if able, and prefer it. Otherwise, get lab data
            #TODO check if this is correct
        
            #-Biological Sciences I w/Lab - Online - 20286 - BIOL 1101K - 0
            
            text = text.split("\n")
            #print (text)
            
            #get starting position of class, online, or lab and then get next 4 lines from it 
            index = 0 
            for line in text:
                if line == "Class":
                    #session represents in person or online
                    self.session = "In-Person"
                    break
                
                if line == "Online":
                    self.session = "Online"
                    break
                
                if line == "Lab":
                    self.session = "In-person"
                    break
                
                if line == "Online Lab":
                    self.session = "Online"
                    break
                index += 1
                
            
            #get whether class is asynch or not
            
            #for some reason the EDUC classes fail on this, so TODO bug fix that l8ter
            try:
                self.class_type = str(text[index + 5])
            except:
                self.class_type = str(text)
            #for x in range (0, 7):
             #   print(text[index + x])
             
             
             #use regex to get course title
             
             
                
            
        
        #stupid hack to run this only the 2nd time    
        run_once = True
        p = ""
        for tr in x:
            
            if run_once:
                run_once = False
            else:
                p = (tr.get_text())
                p = p + p 
            
        _parse(p)
        _get_name()
        _store_database()
        
        
            #print(p)
            
    
            

        
        
        
        
        
con = sqlite3.connect('next_semester_courses.db')
cur = con.cursor()
cur.execute(''' 
    CREATE TABLE IF NOT EXISTS Semester (title TEXT, 
    name TEXT  PRIMARY KEY, 
    class_type TEXT DEFAULT "")
    ''')

    





def test(topic):
    data = "term_in=202102&sel_subj=dummy&sel_day=dummy&sel_schd=dummy&sel_insm=dummy&sel_camp=dummy&sel_levl=dummy&sel_sess=dummy&sel_instr=dummy&sel_ptrm=dummy&sel_attr=dummy&sel_subj=" +topic+ "&sel_crse=&sel_title=&sel_schd=%25&sel_insm=%25&sel_from_cred=&sel_to_cred=&sel_camp=%25&sel_levl=%25&sel_ptrm=%25&sel_instr=%25&sel_attr=%25&begin_hh=0&begin_mi=0&begin_ap=a&end_hh=0&end_mi=0&end_ap=a"
    
    
    x = requests.post(base_url2 + data).text
    soup = BeautifulSoup(x, "html.parser")
    soup = soup.find_all('a')
    for tag in verifyA_tags(soup):
        #title of class
        #print(tag.get_text())
        
        #This gets the info of the course
        #print(tag.parent.parent.next_sibling.next_sibling.prettify())
        CourseSchedule(tag, tag.parent.parent.next_sibling.next_sibling)
    
    
    
    #print(soup.prettify())
    
for subject in subjects:
    test(subject)
    

con.commit()
con.close()
