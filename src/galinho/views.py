from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
import json

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
@require_http_methods(["GET", "POST"])
def turmas(request, id):
    if request.method == 'GET':
        return HttpResponse("GET para turmas" + str(id))
    elif request.method == 'POST':
        return HttpResponse("POST para turmas" + str(id))

@require_http_methods(["GET"])
def turmas_disponiveis(request, id):
    return HttpResponse("GET para turmas disponíveis" + str(id))

@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    received_json_data = json.loads(request.body.decode("utf-8"))
    return HttpResponse("Egg. (POST para login)" + received_json_data['nome'])