from os.path import join
from os import listdir
from bs4 import BeautifulSoup
from collections import defaultdict
import json

def fetch_downloaded_files(path: str):
    return [join(path, file) for file in listdir(path) if file.endswith(".html")]

def get_curriculum(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')

    for element in soup.find_all('tr'):
        info = element.find('th', string="Matriz Curricular: ")

        if info is not None:
            course_information = element.find('td').text.split(' - ')
            break

    try:
        course, degree, mode, when = (
            ' - '.join(course_information[:-3]),
            course_information[-3],
            course_information[-2],
            course_information[-1]
        )
    except:
        return None

    when = 'MT' if when == 'D' else 'N'

    if mode == 'Presencial':
        course_id = ' - '.join([course, degree, when])
    else:
        course_id = ' - '.join([course, degree, 'EAD', when])

    tags = soup.find_all('tr', {'class': ['tituloRelatorio', 'componentes']})

    scrape = defaultdict(list)

    for tag in tags:
        elements_in_tag = [item.text for item in tag.find_all('td')]

        if tag['class'] == ['tituloRelatorio']:
            last_title = elements_in_tag[0]
            continue

        if tag['class'] == ['componentes']:
            try:
                information, nature = elements_in_tag[0], elements_in_tag[1]

                information = information.split(' - ')

                code, name, hours = information[0], ' - '.join(information[1:-1]), int(information[-1][:-1])

                scrape[last_title].append([code, name, hours, nature])
            except:
                pass
    return {course_id: scrape}

def get_all_get_curriculums():
    paths, final = fetch_downloaded_files('../fluxo/'), defaultdict(list)

    for path in paths:
        print(path)
        with open(path, 'r') as f:
            html = f.read()

        result = get_curriculum(html)

        if result is not None:
            final.update(result)
    return final


result = get_all_get_curriculums()

with open('fluxos.json', 'w') as f:
    json.dump(result, f)
