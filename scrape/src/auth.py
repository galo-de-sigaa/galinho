from selenium import webdriver
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup
from collections import defaultdict
import json

url = 'https://sigaa.unb.br/sigaa/logar.do?dispatch=logOn'

def auth(login: str, password: str, url: str, driver: webdriver):
    driver.get(url)

    driver.find_element(By.XPATH, "//input[@name='user.login']").send_keys(login)
    driver.find_element(By.XPATH, "//input[@name='user.senha']").send_keys(password)

    driver.find_element(By.XPATH, "//input[@value='Entrar']").click()

    driver.find_element(By.XPATH, "//a[@id='j_id_jsp_340461267_264:detalharIndiceAcademico']").click()

    details = driver.page_source

    driver.find_element(By.XPATH, "//td[@class='voltar']").click()

    driver.find_element(By.XPATH, "//img[@src='/sigaa/img/icones/ensino_menu.gif']").click()
    driver.find_element(By.XPATH, "//td[text()='Consultar Minhas Notas']").click()

    return (details, driver.page_source)

def fetch_course(html_doc: str):
    soup = BeautifulSoup(html_doc, 'html.parser').find('table', {'id': 'identificacao'})

    course = None

    for element in soup.find_all('tr'):
        resolve = element.find('th', string='Curso:')

        if resolve is not None:
            course = element.find('td').text
    return course.strip()

def get_grades(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser').find('div', {'class': 'notas'})

    tables = soup.find_all('table', {'class': 'tabelaRelatorio'})

    scrape = defaultdict(str)

    for table in tables:
        for item in table.find_all('tr', {'class': ['linhaPar linha', 'linhaImpar linha']}):
            code = [i.text for i in item.find_all('td', {'nowrap': 'nowrap'})][0]

            situation = item.find('td', {'class': 'situacao'}).text

            if scrape[code] == 'APROVADO':
                continue
            scrape[code] = situation
    return scrape

def execute_auth(user, password):
    driver = webdriver.Firefox()

    details, grades = auth(user, password, driver=driver, url=url)

    driver.close()

    course, resulting_courses, approved = fetch_course(details), dict(get_grades(grades)), defaultdict(int)

    for key, value in resulting_courses.items():
        if value == 'APROVADO':
            approved[key] = 1

    with open('results/fluxos.json') as f:
        fluxos_data = json.load(f)

    incomplete_courses = defaultdict(list)

    for mode, values in fluxos_data[course].items():
        resolve = []
        for o in values:
            if approved[o[0]] != 1:
                resolve.append(o)
        incomplete_courses[mode] = resolve

    with open('results/offers.json') as f:
        offers_data = json.load(f)

    final_courses = dict()

    for key, value in incomplete_courses.items():
        temporary = dict()
        for o in value:
            if offers_data.get(o[0]) is not None:
                temporary.update({o[0]: offers_data.get(o[0])})
        if len(temporary) > 0:
            final_courses[key] = temporary
    return final_courses

def print_result(result):
    for key, value in result.items():
        print(key)
        for inner_key, inner_value in value.items():
            print('     ' + inner_key + ':')
            for o in inner_value:
                print('          ' + str(o))
    return None

print_result(execute_auth('200067184', 'Arroz1001farofa!'))

# execute_auth('200067184', 'Arroz1001farofa!')
