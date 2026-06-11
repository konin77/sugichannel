from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from shop0c.models import User
from shop0c.forms import LoginForm

# Create your views here.
def index(request):
    pass
def result(request):
    pass
def detail(request):
    pass
def cart(request):
    pass

class Login(View):
    def get(self, request):
        form = LoginForm()
        context = {
            "form":form,
        }
        return render(request, 'shop0c/login.html', context)
        

    def post(self, request):
        form = LoginForm(request.POST)
        if not form.is_valid():
            context = {
                "form":form,
            }
            return render(request, 'shop0c/login.html', context)
        
        queryset = User.objects.all()
        for user in queryset:
            
            if user.user_id == request.POST['id'] and user.password == request.POST['password']:
                 
                request.session['user_id'] = user.user_id
                request.session['password'] = user.password

def register(request):
    pass
def confirm(request):
    pass
def commit(request):
    pass
def info(request):
    pass
def update_user(request):
    pass
def update_confirm(request):
    pass
def update_commit(request):
    pass