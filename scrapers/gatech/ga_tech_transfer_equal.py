import requests
import bs4 
import sqlite3
start = "https://oscar.gatech.edu/pls/bprod/wwsktrna.P_find_location" 
start2 = "https://oscar.gatech.edu/pls/bprod/wwsktrna.P_find_subj_levl_classes"

subjects = ['ACCT', "ANTH", "ARTS", "BCHM", "BIOL", "BUSA", "CHEM", "CHIN", 'STEC', 'COMM', 'EAP', 'ECON', 'ENGL', 'FILM', 'FINA',
'FREN', 'GEOG', 'GGC', 'GRMN', 'HIST', 'HNRS', 'ITEC', 'MATH', 'MGMT', 'MKTG', 'MSL', 'MUSC', 'PHED', 'PHIL', 'PHYS', 'POLS', 
'PSCI', 'PSYC', 'RELN', 'SOCI', 'SPAN']

data_format = {
    'state_in': 'GA',
    'nation_in': '',
    'sel_subj': "BIOL",
    'levl_in': 'US',
    "term_in": "202102",
    "sbgi_in": "004796",
    "school_in": ""
}

#    for br in text.find_all("br"):
#        br.replace_with("\n")


data2 = {

'sel_subj': 'RELN',
'sel_subj': 'SOCI',
'sel_subj': 'SPAN',
'levl_in' : 'US',
"term_in": "202102",
"sbgi_in": "004796",
"school_in": ""
}
#for some weird reason the scraping only happens with the last course...



#start2 = start2 + "state_in=GA&nation_in=&sel_subj=ACCT&sel_subj=ANTH&sel_subj=ARTS&sel_subj=BCHM&sel_subj=BIOL&sel_subj=BUSA&sel_subj=CHEM&sel_subj=CHIN&sel_subj=COMM&sel_subj=EAP&sel_subj=ECON&sel_subj=ENGL&sel_subj=FILM&sel_subj=FINA&sel_subj=FREN&sel_subj=GEOG&sel_subj=GGC&sel_subj=GRMN&sel_subj=HIST&sel_subj=HNRS&sel_subj=ITEC&sel_subj=MATH&sel_subj=MGMT&sel_subj=MKTG&sel_subj=MSL&sel_subj=MUSC&sel_subj=PHED&sel_subj=PHIL&sel_subj=PHYS&sel_subj=POLS&sel_subj=PSCI&sel_subj=PSYC&sel_subj=RELN&sel_subj=SOCI&sel_subj=SPAN&sel_subj=STEC&levl_in=US&term_in=202102&sbgi_in=004796&school_in="



#for elem in test_list:
 #   print(elem)
#print(test_list[19].get_text().split())

#['BIOL', '1101', 'Biological', 'Sciences', 'I', 'Undergraduate', 'C', '=>', 'ET', 'LAB', 'Credit', 'Awarded', 'w/BIOL', '1101L', '0.0']
#course listing starts at index 13
#if AND in index 1 of the list, then add it to the last thing 
#TODO don't hardcode this 
#print(soup.prettify())


#now to start scraping..

class TechCourse():
    #TODO implement gatech_courses regex
    def __init__(self, ggc_course, ggc_description, gatech_description):
        self.ggc_course = ggc_course
        #self.gatech_course = gatech_course
        self.ggc_description = ggc_description
        self. gatech_description = gatech_description


def scrape_course(subject):
    data_format["sel_subj"] = subject 
    x = requests.post(start2, data=data_format).text
    course_list = bs4.BeautifulSoup(x, 'html.parser').find_all("tr")
    scrape_list  = [] #filter out any empty courses

    for elem in course_list:
        processed = elem.get_text().split()

        if len(processed) > 3 and processed[0] in ("Or", "And", subject): #again cheap hack
            scrape_list.append(processed)

            if processed[0] == "All":
                return scrape_list#TODO confirm that last course has All in it

    #remove last course

    #list of bs4 tr items
    start = scrape_list 
    output_list = [] #related courses are grouped into lists in this list
    related_courses = []
    previous_course = ""
    for index, course_details in enumerate(start):   #start is now a list containing the lists of course material

        if index == 0:
            related_courses.append(course_details)
            continue
        
        if course_details[0] == subject:
            #the courses have no relationship
            output_list.append(related_courses)
            related_courses = []
            related_courses.append(course_details)

        elif course_details[0] == "Or" or course_details[0] == "And":
            #relationship exists
            related_courses.append(course_details)
    output_list.append(related_courses)
    related_courses = []
    return output_list



def process_class_list(class_list):
    #preprocess class list, remove the letter grade, merge everything with a space in
    full_transfer_list = []
    #length 1 only has => for classes
    for item in class_list:
        
        #length 1 = standalone, no relationships
        if len(item) == 1:
            title = item[0][0] + " " + item[0][1] 
            output = ' '.join(item[0])
            #print (title)
            full_transfer_list.append(output)

            #print(output)
        
        else: 
            #each index in a relationshipped list corresponds to an AND or OR clause
            first_transfer = ' '.join(item[0])
            #get rest of transfer courses
            for index, relationship in enumerate(item[1:]):
                gatech_class = item[index+ 1][1:]
                #output_tech_title = ' '.join(gatech_class) + ", "
                #first_transfer += ' '.join(gatech_class) + ", "
                
                #print(output_tech_title)
                relationship_formatted = ' '.join(item[index + 1 ] ) #this feels wrong but it works
                #print(relationship_formatted)
                first_transfer += " "  + relationship_formatted
                #print(first_transfer)
                
            full_transfer_list.append(first_transfer) #going to assume this all works fine...
    return full_transfer_list




def find_2nd(string, substring):
   return string.find(substring, string.find(substring) + 1)

def create_tech_courses(full_course_list):
    """go through the full_transfer_list and group them into something to place in a shelve module"""
    tech_course_list = []

    for element in full_course_list:
        #break up into 4 parts - ID, full title for everything
        arrow_location = element.index("=>")
        ggc_description = element[:arrow_location- 1]
        ggc_course = element[:find_2nd(element, " ")]
        gatech_description = element[arrow_location + 3:]
        #gatech_course = gatech_description[:find_2nd(gatech_description, " ")]
        tech_course_list.append( TechCourse(ggc_course, ggc_description, gatech_description)   )

        #print(ggc_course + " => " + gatech_description)

    return tech_course_list

    

import pprint
#pp = pprint.PrettyPrinter()   
#create_tech_courses(process_class_list(scrape_course("BIOL")))
#create_tech_courses(process_class_list(scrape_course("ITEC")))
#create_tech_courses(process_class_list(scrape_course("MATH")))


def create_database():
    # I'm going to hate doing this... but let's store them using a database
    con = sqlite3.connect("ggc_gatech_transfer.db")
    cur = con.cursor()
    #TODO store credit hours in these
    cur.execute(
    '''CREATE TABLE IF NOT EXISTS ggc_gatech_transfer
    (Ggc_course TEXT PRIMARY KEY, 
     Ggc_description TEXT,
     Gatech_description TEXT DEFAULT "") ''')
    for topic in subjects:
        topic_course_list =  create_tech_courses(process_class_list(scrape_course(topic)))
        for transfer_course in topic_course_list:
            t = (transfer_course.ggc_course, transfer_course.ggc_description,transfer_course.gatech_description)
            cur.execute( '''
                INSERT INTO ggc_gatech_transfer VALUES (?, ?, ?)''', t)

    con.commit()
    con.close()

   

create_database()
#each list is a grouping of related classes in a list
#for transfer_course in class_list:
 ###     transfer_course[0], #ggc course title
        
   #)
