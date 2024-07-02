from django.http import HttpResponse
from django.views import View
from core.tasks import add
from django.shortcuts import render
import time

class MainView(View):
    def get(self, request, *args, **kwargs):
        html_content = "<html><body><h1>Hello, Crocodile 🐊</h1></body></html>"
        return HttpResponse(html_content, content_type="text/html; charset=utf-8")

def test_task(request):
    try:
        params = {
            'x':10,
            'y':5
        }
        time.sleep(5)
        task = add.delay(params)  # start the data retrieval task 
        return HttpResponse({'data': 'initialising', 'task_id': task.id}, status=200)     
    except Exception as e:
        return HttpResponse({'error': str(e)}, status=401)     

def websocket_test(request):
    try:
        return render(request, "websockettest.html")
    except Exception as e:
        print(str(e))
        return HttpResponse({'error': str(e)}, status=401)    

