import requests
from bs4 import BeautifulSoup

pattern = (
    '<th width="50%">Componente Curricular</th>\n<th style="text-align:left">Local</th>\n<th width="15%">Horário</th>'
)

def get_current_courses(login: str, password: str):
    url = 'https://sigaa.unb.br/sigaa/logar.do?dispatch=logOn'

    logon = requests.post(url, data={'user.login': login, 'user.senha': password})

    soup = BeautifulSoup(logon.text, 'html.parser')

    for element in soup.findAll('table', {'style': 'margin-top: 1%;'}):
        if pattern in str(element):
            table = element
            break
        return Exception('ERROR: Wrong credentials!')

    courses = [element.text.strip().split('\n\n\n') for element in table.findAll('tr')]

    for index in range(len(courses)):
        courses[index] = [element.strip().split('\n') for element in courses[index]]

    courses, result = [element for element in courses if element != [['']]], []

    for element in courses:
        row = []
        for inner in element:
            row += inner
        result.append(row)

    return result[2:] if len(result) > 1 else Exception('ERROR: No courses found!')
