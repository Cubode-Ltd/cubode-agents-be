from django.views import View
from django.shortcuts import render


    
class MainView(View):
    def get(self,request):
            return render(request,"home.html",{'is_logged':True,'upload':False})
    

class Registration(View):
    def get(self,request):
            return render(request,"signUp.html",{'is_signup':True})

class Login(View):
    def get(self,request):
            return render(request,"signUp.html",{'is_signup':False})