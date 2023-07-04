from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

url = 'https://sigaa.unb.br/sigaa/public/turmas/listar.jsf'

def set_payload(department: str) -> dict:
    return {
        'formTurma:inputDepto': department,
        'formTurma:inputNivel': 'G',
        'formTurma:inputAno': '2023',
        'formTurma:inputPeriodo': '2'
    }

def get_available_departments(html_doc: str):

    soup = BeautifulSoup(html_doc, 'html.parser')

    select = soup.find('select', {'id': 'formTurma:inputDepto', 'name': 'formTurma:inputDepto'})

    return [element['value'] for element in select.findAll('option') if element['value'] != '0']


def fetch_depatment_offer(payload: dict, driver: webdriver):

    level, depto, year, period = (
        payload['formTurma:inputNivel'],
        payload['formTurma:inputDepto'],
        payload['formTurma:inputAno'],
        payload['formTurma:inputPeriodo']
    )

    driver.get(url)

    driver.find_element(By.XPATH, f"//select[@name='formTurma:inputNivel']/option[@value='{level}']").click()
    driver.find_element(By.XPATH, f"//select[@name='formTurma:inputDepto']/option[@value='{depto}']").click()

    driver.find_element(By.XPATH, f"//input[@name='formTurma:inputAno']").send_keys(year)

    driver.find_element(By.XPATH, f"//select[@name='formTurma:inputPeriodo']/option[@value='{period}']").click()
    driver.find_element(By.XPATH, f"//input[@value='Buscar']").click()

    return driver.page_source


def fetch_all_offers(html_doc: str):
    departments = get_available_departments(html_doc)

    driver, scrape = webdriver.Firefox(), []

    for element in departments:
        payload = set_payload(department=element)

        print(f'processing ID {element}...\n')

        source_code = fetch_depatment_offer(payload=payload, driver=driver)

        try:
            with open(f'../offers/{element}.html', 'w') as file:
                file.write(source_code)
        except:
            source_code = ''

            with open(f'../log_error_offers.txt', 'a') as file:
                file.write(element + '\n')

        scrape.append(source_code)
    driver.close()

    return scrape

with open('../oferta.html', 'r') as file:
    bia = fetch_all_offers(file.read())
