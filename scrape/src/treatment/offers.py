from os import listdir
from os.path import join
from bs4 import BeautifulSoup
from collections import defaultdict
import json

class_options = ['agrupador', 'linhaPar', 'linhaImpar']

padding = '\n\t\t\t\t\t\t\t\t\t\t\t\n\n\n\t\t\n\n\t\t\t\t\t\t\t\t\t\t\t'

def fetch_downloaded_files(path: str):
    return [join(path, file) for file in listdir(path) if file.endswith(".html")]

def apply_treatment_to_offer(html_doc: str):
    soup = BeautifulSoup(html_doc, 'html.parser').find('table', {'class': 'listagem'})

    if soup is None:
        return soup
    
    scrape = defaultdict(list)

    for element in soup.find('tbody').find_all('tr'):
        element_class = element.get('class')[0]

        if element_class not in class_options:
            continue

        if element_class == 'agrupador':
            last_course = element.find('span', {'class': 'tituloDisciplina'}).text.split(' - ')[0]
            continue

        (turma, _, docente, horario, _, _, _, place)  = [item.text for item in element.find_all('td')]

        turma, docente_info, place, horario = turma.strip(), docente.split(' '), place.strip(), horario.split(padding)

        professor, carga_horaria = ' '.join(docente_info[:-1]), int(docente_info[-1][1:-2])

        codigo_horario, objetos_horario = horario[0], horario[-1].strip()

        scrape[last_course].append([turma, professor, carga_horaria, codigo_horario, objetos_horario, place])
    return scrape

def get_all_offers(url: str = '../offers/'):
    paths, final = fetch_downloaded_files(url), defaultdict(list)

    for path in paths:
        with open(path, 'r') as file:
            html = file.read()

        result = apply_treatment_to_offer(html)

        if result is not None:
            final.update(result)
    return final

result = get_all_offers()

print(result)

with open('offers.json', 'w') as f:
    json.dump(result, f, ensure_ascii=False)
