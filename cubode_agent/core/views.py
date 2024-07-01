from django.views import View
from django.shortcuts import render


    
class MainView(View):
    def get(self,request):
            return render(request,"home.html")
