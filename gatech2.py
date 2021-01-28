#scrapes the georgia tech course directory  
import requests
import sqlite3

def createSession(subject): #pass in subject string 
    s = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0'}

    url = "https://oscar.gatech.edu/bprod/bwckctlg.p_disp_cat_term_date"
    data = {
        "call_proc_in": "bwckctlg.p_disp_dyn_ctlg",
        "cat_term_in": "202102"
        }
    r = s.post(url,  headers=headers, data=data)

    url = "https://oscar.gatech.edu/bprod/bwckctlg.p_display_courses"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "DNT": "1",
        "Origin": "https://oscar.gatech.edu",
        "Referer": "https://oscar.gatech.edu/bprod/bwckctlg.p_disp_cat_term_date",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    
    datas = {
        "term_in": "202008",
        "call_proc_in": "bwckctlg.p_disp_dyn_ctlg",
        "sel_levl": "dummy",
        "sel_schd": "dummy",
        "sel_coll": "dummy",
        "sel_divs": "dummy",
        "sel_dept": "dummy",
        "sel_attr": "dummy",
        "sel_subj": subject,
        "sel_crse_strt":"", 
        "sel_crse_end": "",
        "sel_title": "",
        "sel_from_cred":"" ,
        "sel_to_cred": ""
        }
    datas2 =    "term_in=202008&call_proc_in=bwckctlg.p_disp_dyn_ctlg&sel_subj=dummy&sel_levl=dummy&sel_schd=dummy&sel_coll=dummy&sel_divs=dummy&sel_dept=dummy&sel_attr=dummy&sel_subj=AE&sel_crse_strt=&sel_crse_end=&sel_title=&sel_levl=%25&sel_schd=%25&sel_coll= %25&sel_divs=%25&sel_dept=%25&sel_from_cred=&sel_to_cred=&sel_attr=%25"

    r = s.post(url, headers=headers, data=datas2)
    print(r.text)


class Course: #A single course

     #only 1 instance of a class's name should exist. TODO: implement this. 
    def __init__(self, full_title):
        self.prerequisites = []
        #self.name = name #I.E MATH 1553
        #self.title = title #Intro to Linear Algebra

        x = full_title.split(" - ")
        self.title = x[0]
        self.course_ID = x[1]
        self.name = x[2]
        #What do I do with the G01 G02? It's probably a way to designate multiple classes at diff times

    def getPrereqs(self):
        link = "https://oscar.gatech.edu/pls/bprod/bwckschd.p_disp_detail_sched?term_in=" + TERM + "&crn_in=" + self.course_ID #TODO: Make TERM not a global var and make it change to reflect semester
        print(link)
        r = requests.get(link)
        print(r.text)


    def parseTable(): #Each course page is split into multiple tables. Parsing each table and breaking it up into different sections helps me get stuff like credit hours, prereqs, and restrictions
        pass

    def __str__(self):
        return  self.name
    
    def storeTable(self):
        """Store course, along with its prerequisites in database"""
        pass
    

#This will probably become it's own script sometimes 

def initScript():
    """Got to start somewhere. This will initalize the original database"""
    connection = sqlite3.connect("courses.db")
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE courses (name TEXT)  )" ) #subject to change
    cursor.execute("CREATE TABLE courses (name TEXT)  )" ) #subject to change
    
    
if __name__ == "__main__":
    initScript()




