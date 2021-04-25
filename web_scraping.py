import requests
import io
from PIL import Image,ImageOps
from bs4 import BeautifulSoup
import base64
import img_to_str


TRY = 5
URL = "https://coe1.annauniv.edu/home/"
URL_LOGIN = "https://coe1.annauniv.edu/home/students_corner.php"

REGISTER_NUMBER = '<YOUR NUMBER>'
DOB = '<YOUR DATE OF BIRTH>'

DATA = {
    'register_no':REGISTER_NUMBER,
    'dob':DOB,
    'gos':'Login'
}

DATA_FOR_RESULT = {
    'ExamResults':'',
    'univ_reg_no':''
}

def again_secret_code(after_login):
    login_html = BeautifulSoup(after_login.content,'html.parser')
    secret_code_form = login_html.find('form',id='formExamResults')
    secret_code = secret_code_form.find_all('input',type='hidden')
    secret_code = secret_code[0]['id']
    DATA_FOR_RESULT[secret_code] = secret_code

def captcha_solving(html):
    captcha = html.find('img',class_='small')
    src = captcha['src']
    decod = src.replace("data:image/png;base64","")
    #with open("temp.png","wb") as f:
    #    f.write(base64.urlsafe_b64decode(decod))
    f = io.BytesIO()
    f.write(base64.urlsafe_b64decode(decod))
    #security_code = str(input())
    security_code = img_to_str.clear_n_get_text(f)
    DATA['security_code_student'] = security_code

def saving_hidden_data(html):
    login_stu_form = html.find('form',id='login_stu')
    hidden = login_stu_form.find('input',type='hidden')
    hidden_name = hidden['id']
    DATA[hidden_name] = hidden_name

def extract_data(res):
    result = []
    tab4 = res.find('div',class_='tab4 tabsContent')
    tables = tab4.find_all('table',id='resulttable')
    for table in tables:
        all_tr = table.find_all('tr')[5:]
        for row in all_tr:
            row_data = []
            all_th = row.find_all('th')
            for th in all_th:
                row_data.append(th.text.strip())
            result.append(row_data)
    print(result)

if __name__=="__main__":
    RESULT = False
    i = 0
    while(i<TRY):
        with requests.Session() as rq:
            log = rq.get(URL)
            html = BeautifulSoup(log.content,'html.parser')
            saving_hidden_data(html)
            captcha_solving(html)
            after_login = rq.post(URL_LOGIN,data=DATA)
            try:
                again_secret_code(after_login)
                getting_result = rq.post(URL_LOGIN,data=DATA_FOR_RESULT)
                result_html = BeautifulSoup(getting_result.content,'html.parser')
                extract_data(result_html)
                RESULT = True
                break
            except:
                pass                
        i += 1
    if not RESULT:
        print("check your crendential")