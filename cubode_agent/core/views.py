from django.views import View
from core.tasks import add
from django.shortcuts import render


    
class MainView(View):
  def get(self,request):
      return render(request,"home.html")

# def test_task(request):
#     try:
#         params = {
#             'x':10,
#             'y':5
#         }
#         task = add.delay(params)  # start the data retrieval task 
#         return HttpResponse({'data': 'initialising', 'task_id': task.id}, status=200)     
#     except Exception as e:
#         return HttpResponse({'error': str(e)}, status=401)     

