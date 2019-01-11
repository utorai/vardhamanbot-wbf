import requests
from bs4 import BeautifulSoup
import roman

class Scraper:
    def __init__(self):
        self.session = requests.Session()
        self.authenticated = False

    def authenticate(self, rollno, wak):
        if not self.authenticated:
            data = {
                'rollno' : rollno,
                'wak' : wak,
                'ok' : 'SignIn'
            }
            response = self.session.post('http://studentscorner.vardhaman.org', data)
            print()
            if not 'Content-Length' in response.headers:
                #print(response.headers)
                self.authenticated = True
    
    def getPeriods(self):
        if self.authenticated:
            conducted = 0
            attended = 0
            response = self.session.get('http://studentscorner.vardhaman.org/student_attendance.php')
            soup = BeautifulSoup(response.text, 'html.parser')
            for element in soup.find_all('th'):
                #print(element.decode_contents().strip())
                if(element.decode_contents().strip()== "Conducted"):
                    tr = element.parent
                    for td in tr.find_all("th")[1:]:
                        conducted += int(td.decode_contents().strip())
                if(element.decode_contents().strip()== "Attended"):
                    tr = element.parent
                    for td in tr.find_all("th")[1:]:
                            attended += int(td.decode_contents().strip())
            return (conducted,attended)
        
    def get_gpa(self, semester):
        if self.authenticated:
            semester_text = "Semester - " + roman.toRoman(semester)
            response = self.session.get('http://studentscorner.vardhaman.org/src_programs/students_corner/CreditRegister/credit_register.php')
            soup = BeautifulSoup(response.text, 'html.parser')
            for element in soup.find_all('th'):
                if element.decode_contents().strip() == semester_text:
                    for gpa_element in element.find_parent('tr').find_all_next():
                        if "Semester Grade Point Average" in gpa_element.decode_contents().strip():
                            gpa = float(gpa_element.contents[0].findChildren()[0].decode_contents().split("Semester Grade Point Average :")[1].strip())
                            break
            return gpa
        else:
            raise Exception("User authentication required for this feature.")
    
    def get_cgpa(self):
        if self.authenticated:
            response = self.session.get('http://studentscorner.vardhaman.org/src_programs/students_corner/CreditRegister/credit_register.php')
            soup = BeautifulSoup(response.text, 'html.parser')
            for element in soup.find_all('th'):
                if "Cumulative Grade Point Average" in element.decode_contents().strip():
                    cgpa = float(element.contents[0].decode_contents().split("Cumulative Grade Point Average :")[1].strip())
                    break
            return cgpa
        else:
            raise Exception("User authentication required for this feature.")

    def get_attendance(self):
        if self.authenticated:
            response = self.session.get('http://studentscorner.vardhaman.org/student_attendance.php')
            soup = BeautifulSoup(response.text, 'html.parser')
            for element in soup.find_all('th'):
                if element.decode_contents().strip() == 'Attendance Percentage':
                    attendance = element.findNext('th').contents[0].findChildren()[0].decode_contents()
                    return float(attendance)
        else:
            raise Exception("User authentication required for this feature.")

    def get_studentdata(self):
        if self.authenticated:
            studentdata = {}
            response = self.session.get("http://studentscorner.vardhaman.org/student_information.php")
            soup = BeautifulSoup(response.text,"html.parser")
            table = soup.find_all("table")[2]
            for tr in table.find_all('tr'):
                if len(tr.find_all('th'))==1 and len(tr.find_all('td')) == 1:
                    key = tr.find_all('th')[0].text.strip().replace(' ','').replace('-','').replace('/','').replace('(','').replace(')','')
                    value = tr.find_all('td')[0].text.strip()
                    studentdata[key] = value
            return studentdata
        else:
            raise Exception("User authentication required for this feature.")    
    
    def getResults(self,rollno,wak,exam_code="BT4R15MAY18"):
        data = {
                'rollno' : rollno,
                'wak': wak,
                'exam_code': exam_code,
                'go': 'GO',
            }
        #BT5R15DEC18
        response = self.session.post("http://results.vardhaman.org/all_exam_results_report_vcer15.php",data)
        #print(response.text)
        soup = BeautifulSoup(response.text,"html.parser")
        table = soup.find_all("table")[1].find_all("tbody")[0]
        trs = table.find_all("tr")
        subjects  = trs[0:len(trs)-2]
        res = []
        #print("-----------------")
        for tr in subjects:
            tds = tr.find_all("td")[1:]
            code = tds[0].text.strip()
            name = tds[1].text.strip()
            grade = tds[2].text.strip()
            credit = tds[3].text.strip()
            result = tds[4].text.strip()
            res.append([code,name,grade,credit,result])
            #add this subject into the subjects array
        summary = trs[-2:]
        totalcred = summary[0].find_all('td')[1].text.strip()
        gpa = summary[1].find_all('td')[1].text.strip()
        return (res,int(totalcred), float(gpa))
        #print(table.decode_contents())