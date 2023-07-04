from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
import json
from selenium import webdriver
from selenium.webdriver.common.by import By

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
@require_http_methods(["GET", "POST"])
def turmas(request, id):
    if request.method == 'GET':
        texto = [{"id": 4, "semestre": 1, "obrigatoria": True, "cargaHoraria": 30, "turma": "A",
                  "disciplina": {"codigo": "CIC025", "nome": "Software Básico"},
                  "professor": "Fulano de tal",
                  "datas": [
                      {
                          "diaSemana": 2,
                          "horario": "14:00 - 15:50"
                      },
                      {
                          "diaSemana": 4,
                          "horario": "14:00 - 15:50"
                      }
                  ],
                  "local": "bloco b - sala x - campus I",
                  "preRequisitos": ["CIC013", "CIC20"]
                  }]

        return JsonResponse(texto, safe=False)
        #return HttpResponse("GET para turmas" + str(id))
    elif request.method == 'POST':
        return HttpResponse("POST para turmas" + str(id))

@require_http_methods(["GET"])
def turmas_disponiveis(request, id):
    return HttpResponse("GET para turmas disponíveis" + str(id))


@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    driver = webdriver.Firefox()
    url = 'https://sigaa.unb.br/sigaa/logar.do?dispatch=logOn'
    received_json_data = json.loads(request.body.decode("utf-8"))
    driver.get(url)

    driver.find_element(By.XPATH, "//input[@name='user.login']").send_keys(received_json_data['user'])
    driver.find_element(By.XPATH, "//input[@name='user.senha']").send_keys(received_json_data['senha'])
    driver.find_element(By.XPATH, "//input[@value='Entrar']").click()
    profile = driver.page_source

    driver.find_element(By.XPATH, "//img[@src='/sigaa/img/icones/ensino_menu.gif']").click()
    driver.find_element(By.XPATH, "//td[text()='Consultar Minhas Notas']").click()

    source = driver.page_source
    driver.close()
    # return (profile, driver.page_source)

    return HttpResponse(source)
