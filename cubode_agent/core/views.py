from django.views import View
from django.shortcuts import render


class MainView(View):
    def get(self, request):
        return render(request, "index.html", {})


class Registration(View):
    def get(self, request):
        return render(request, "register.html", {})


class Login(View):
    def get(self, request):
        return render(request, "login.html", {})


class RecoverPassword(View):
    def get(self, request):
        return render(request, "reset_password.html", {})
