from django.http import HttpResponse
from django.views import View
from core.tasks import add, generate_web_component
from django.shortcuts import render
import time

class MainView(View):
    def get(self, request, *args, **kwargs):
        html_content = "<html><body><h1>Hello, Crocodile 🐊</h1></body></html>"
        return HttpResponse(html_content, content_type="text/html; charset=utf-8")

class InferenceAI(View):
    def get(self, request, *args, **kwargs):
        try:
            metadata = {'Schema': ['country',
                                'description',
                                'designation',
                                'points',
                                'price',
                                'province',
                                'region_1',
                                'region_2',
                                'variety',
                                'winery'],
                                'Data Types': 'country         object\ndescription     object\ndesignation     object\npoints           int64\nprice          float64\nprovince        object\nregion_1        object\nregion_2        object\nvariety         object\nwinery          object\ndtype: object',
                                'Sample': [{'country': 'US',
                                'description': 'This tremendous 100% varietal wine hails from Oakville and was aged over three years in oak. Juicy red-cherry fruit and a compelling hint of caramel greet the palate, framed by elegant, fine tannins and a subtle minty tone in the background. Balanced and rewarding from start to finish, it has years ahead of it to develop further nuance. Enjoy 2022–2030.',
                                'designation': "Martha's Vineyard",
                                'points': 96,
                                'price': 235.0,
                                'province': 'California',
                                'region_1': 'Napa Valley',
                                'region_2': 'Napa',
                                'variety': 'Cabernet Sauvignon',
                                'winery': 'Heitz'}]
                        }
            time.sleep(1)
            task = generate_web_component.delay(metadata)  # start the data retrieval task 
            return HttpResponse({'data': 'initialising', 'task_id': task.id}, status=200)     
        except Exception as e:
            return HttpResponse({'error': str(e)}, status=401)    



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

