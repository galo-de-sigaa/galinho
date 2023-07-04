import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By

url, prefix = (
    'https://sigaa.unb.br/sigaa/public/curso/lista.jsf?nivel=G&aba=p-ensino',
    'https://sigaa.unb.br/sigaa/public/curso/curriculo.jsf?lc=pt_BR&id='
)

def get_course_hyper_links() -> list[str]:
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')
    table = soup.find("table", {"class":"listagem"})

    hrefs = [row['href'] for row in table.findAll("a", {"title": "Visualizar Página do Curso"})]

    hrefs = [link.split("?")[-1].split("&")[0].split("=")[-1] for link in hrefs]

    return (hrefs, [prefix + element for element in hrefs])

def access_course_curriculum(url: str, driver: webdriver):
    driver.get(url)
    try:
        driver.find_element(By.XPATH, "//a[@title='Relatório da Estrutura Curricular']").click()

        return driver.page_source
    except:
        return ''

def access_all_curriculums():
    id, hyper_links = get_course_hyper_links()

    information, scrape = dict(zip(id, hyper_links)), []

    driver = webdriver.Firefox()

    for identification, hyper_link in information.items():
        page_source = access_course_curriculum(hyper_link, driver)

        print(f'getting link of ID {identification}...\n')

        try:
            with open(f'../fluxo/{identification}.html', 'w') as f:
                f.write(page_source)
        except:
            page_source = ''

            with open(f'../fluxo/{identification}.html', 'w') as f:
                f.write(page_source)

            with open(f'../log_error_fluxos.txt', 'a') as log:
                log.write(str(identification) + '\n')

        scrape.append(page_source)
    driver.close()

    return scrape

print(access_all_curriculums())