from django.views import View
from core.tasks import generate_web_component #add
from django.shortcuts import render
import time
import json
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
class MainView(View):
  def get(self,request):
      return render(request,"home.html")

@method_decorator(csrf_exempt, name='dispatch')
class InferenceAI(View):
    def get(self, request, *args, **kwargs):
        try:
            metadata = {
                'Schema': ['country', 'description', 'designation', 'points', 'price', 'province', 'region_1', 'region_2', 'variety', 'winery'],
                'Data Types': 'country         object\ndescription     object\ndesignation     object\npoints           int64\nprice          float64\nprovince        object\nregion_1        object\nregion_2        object\nvariety         object\nwinery          object\ndtype: object',
                'Sample': [{
                    'country': 'US',
                    'description': 'This tremendous 100% varietal wine hails from Oakville and was aged over three years in oak. Juicy red-cherry fruit and a compelling hint of caramel greet the palate, framed by elegant, fine tannins and a subtle minty tone in the background. Balanced and rewarding from start to finish, it has years ahead of it to develop further nuance. Enjoy 2022–2030.',
                    'designation': "Martha's Vineyard",
                    'points': 96,
                    'price': 235.0,
                    'province': 'California',
                    'region_1': 'Napa Valley',
                    'region_2': 'Napa',
                    'variety': 'Cabernet Sauvignon',
                    'winery': 'Heitz'
                }]
            }
            time.sleep(1)
            task = generate_web_component.delay(metadata, "X", "Y   ")  # start the data retrieval task 
            response = JsonResponse({'data': 'initialising', 'task_id': task.id}, status=200)
            return self.add_cors_headers(response)
        except Exception as e:
            response = JsonResponse({'error': str(e)}, status=500)
            return self.add_cors_headers(response)
    
    def post(self, request, *args, **kwargs):
        try:
            # Parse the JSON payload
            data = json.loads(request.body)
            hash_value = data.get('hash')
            filename_value = data.get('fileName')

            if not hash_value:
                response = JsonResponse({'error': 'Hash value is required'}, status=400)
                return self.add_cors_headers(response)
            
            # response_data = {'message': f'Hash {hash_value} received and processed for file {filename_value}. Running AI Inference on this data file.'}

            # response = JsonResponse(response_data, status=200)
            return self.create_webcomponent(hash_value, filename_value)
        except json.JSONDecodeError:
            response = JsonResponse({'error': 'Invalid JSON payload'}, status=400)
            return self.add_cors_headers(response)
        except Exception as e:
            response = JsonResponse({'error': str(e)}, status=500)
            return self.add_cors_headers(response)

    def create_webcomponent(self, hash, fileName):
        try:
            metadata = {
                'Schema': ['country', 'description', 'designation', 'points', 'price', 'province', 'region_1', 'region_2', 'variety', 'winery'],
                'Data Types': 'country         object\ndescription     object\ndesignation     object\npoints           int64\nprice          float64\nprovince        object\nregion_1        object\nregion_2        object\nvariety         object\nwinery          object\ndtype: object',
                'Sample': [{
                    'country': 'US',
                    'description': 'This tremendous 100% varietal wine hails from Oakville and was aged over three years in oak. Juicy red-cherry fruit and a compelling hint of caramel greet the palate, framed by elegant, fine tannins and a subtle minty tone in the background. Balanced and rewarding from start to finish, it has years ahead of it to develop further nuance. Enjoy 2022–2030.',
                    'designation': "Martha's Vineyard",
                    'points': 96,
                    'price': 235.0,
                    'province': 'California',
                    'region_1': 'Napa Valley',
                    'region_2': 'Napa',
                    'variety': 'Cabernet Sauvignon',
                    'winery': 'Heitz'
                }]
            }
            time.sleep(1)
            task = generate_web_component.delay(metadata, hash, fileName)  # start the data retrieval task 
            response = JsonResponse({'data': 'initialising', 'task_id': task.id}, status=200)
            return self.add_cors_headers(response)
        except Exception as e:
            response = JsonResponse({'error': str(e)}, status=500)
            return self.add_cors_headers(response)
    
    def add_cors_headers(self, response):
        response["Access-Control-Allow-Origin"] = "http://localhost:9000"
        response["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
        return response
    

class WebSocketTest(View):
    def get(self, request, *args, **kwargs):
      try:
          return render(request, "websockettest.html")
      except Exception as e:
          print(str(e))
          return HttpResponse({'error': str(e)}, status=401)

        

# class TestTask(View):
#   def get(self, request, *args, **kwargs):
#      try:
#          params = { #EXAMPLE ARGS
#              'x':10,
#              'y':5
#          }
#          task = add.delay(params)  # RUN THE TASK 
#          return JsonResponse({'data': 'initialising', 'task_id': task.id}, status=200)     
#      except Exception as e:
#          return JsonResponse({'error': str(e)}, status=401)

# def websocket_test(request):
#     try:
#         return render(request, "websockettest.html")
#     except Exception as e:
#         print(str(e))
#         return HttpResponse({'error': str(e)}, status=401)    

class HtmxTest(View):
  def get(self,request):
      return render(request,"echarts_example.html")

# class ButtonClicked(View):
#     @csrf_exempt

#     def get(self, request):
#         import random

#         colors = [
#         "#FF5733",  # Red-Orange
#         "#33FF57",  # Lime Green
#         "#3357FF",  # Blue
#         "#F1C40F",  # Yellow
#         "#9B59B6",  # Purple
#         ]

#         random_color = random.choice(colors)

#         html_template = f"<div style='color: {random_color};'> HTMX working </div>"

#         return HttpResponse(html_template)

# # # class HtmxWebSocket(View):
# # def index(request):
# #     return render(request,"htmx_websocket_test.html")


