from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from shop0c.models import User
from shop0c.forms import LoginForm, RegistUserForm

# Create your views here.
class Top(View):
    def get(self,request):
        login_flag = request.session['is_login']
        name = request.session['name']
        context = {
            'login_flag':login_flag,
            'name':name
        }
        return render(request,'shop0c/main.html',context)
    def post(self,request):
        login_flag = request.session['is_login']
        context = {
            'login_flag':login_flag
        }
        return render(request,'shop0c/main.html',context)


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
                request.session['name'] = user.name
                request.session['address'] = user.address
                request.session['is_login'] = True
                
                return redirect(reverse('shop0c:main'))

            else:
                return redirect(reverse('shop0c:login'))

class Logout(View):
    def get(self, request):
        request.session['is_login'] = False
        return redirect(reverse('shop0c:main'))

class Register(View):
    def get(self, request):
        form = RegistUserForm()
        context = {
            "form":form,
        }
        return render(request, 'shop0c/registerUser.html', context)
        

    def post(self, request):
        form = RegistUserForm(request.POST)
        if not form.is_valid():
            context = {
                "form":form,
            }
            return render(request, 'shop0c/registerUser.html', context)
        
        else:
            context = {
                'id':request.POST['id'],
                'password':request.POST['password'],
                'name':request.POST['name'],
                'address':request.POST['address']
            }
            return render(request, 'shop0c/registerUserConfirm.html',context)

class Confirmregister(View):
    def get(self, request):
        form = RegistUserForm()
        context = {
            "form":form,
        }
        return render(request, 'shop0c/registerUser.html', context)
    def post(self, request):
        new_user = User()

        new_user.user_id = request.POST['id']
        new_user.password = request.POST['password']
        new_user.name = request.POST['name']
        new_user.address = request.POST['address']

        new_user.save()

        name = new_user.name
        context = {
            'name':name
        }
        return render(request, 'shop0c/registerUserCommit.html',context)
    
class UserInfo(View):
    def get(self,request):
        user_id = request.session['user_id']
        password = request.session['password']
        name = request.session['name']
        address = request.session['address']

        context = {
            'user_id':user_id,
            'password':password,
            'name':name,
            'address':address
        }

        return render(request,'shop0c/userInfo.html',context)

    def post(self,request):
        pass

class UpdateUser(View):
    def get(self, request):
        user_id = request.session['user_id']
        password = request.session['password']
        name = request.session['name']
        address = request.session['address']

        form = RegistUserForm()
        form.fields['id'].initial = user_id
        form.fields['name'].initial = name
        form.fields['address'].initial = address

        context = {
            'form':form
        }

        return render(request,'shop0c/updateUser.html',context)
    def post(self, request):
        pass

class UpdateUserConfirm(View):
    def get(self, request):
        pass
    def post(self, request):

        new_user = User()
        
        new_user.user_id = request.POST['id']
        new_user.password = request.POST['password']
        new_user.name = request.POST['name']
        new_user.address = request.POST['address']

        new_user.save()

class Delete(View):
    def get(self, request):
        name = request.session['name']
        context = {
            'name':name
        }
        return render(request,'shop0c/withdrawConfirm.html', context)

    def post(self, request):
        print(request.session['user_id'])
        user = User.objects.get(user_id=request.session['user_id'])
        name = user.name
        context = {
            'name':name
        }
        user.delete()
        request.session['is_login'] = False
        return render(request,'shop0c/withdrawCommit.html',context)



def update_confirm(request):
    pass
def update_commit(request):
    pass