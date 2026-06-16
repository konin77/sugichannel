from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from shop0c.models import User, Item, Shopcart, Purchase, Detail
from shop0c.forms import LoginForm, RegistUserForm ,UpdateUserForm
#from django.contrib.auth import logout

# Create your views here.

def index(request):
    return render(request,'shop0c/index.html')

class Top(View):
    def get(self,request):
        #form = Search()
        login_flag = request.session.get('is_login')
        name = request.session.get('name')
        context = {
            'login_flag':login_flag,
            'name':name,
            #'form':form
        }
        return render(request,'shop0c/main.html',context)
    def post(self,request):
        login_flag = request.session.get('is_login')
        context = {
            'login_flag':login_flag
        }
        return render(request,'shop0c/main.html',context)

class Search(View):
    def get(self, request):
        pass
    def post(self, request):
        category = request.POST['category']
        keyword = request.POST['keyword']
        category_map = {
            'all':'すべて',
            '1':'家電',
            '2':'パソコン・周辺機器',
            '3':'文房具',
            '4':'キッチン用品',
            '5':'スポーツ用品',
            '6':'鞄',
            '7':'帽子'
        }

        category_name = category_map[category]
        if category != 'all':
            if keyword:
                queryset = Item.objects.filter(category=int(category), name__icontains=keyword)
            else:
                queryset = Item.objects.filter(category=int(category))
        
        else:
            if keyword:
                queryset = Item.objects.filter(name__icontains=keyword)
            else:
                queryset = Item.objects.all()
        
        context = {
            'items':queryset,
            'category':category,
            'keyword':keyword,
            'category_name':category_name
        }

        return render(request,'shop0c/searchResult.html',context)
    
class Detailuesr(View):
    def get(self, request, pk):
        item = Item.objects.get(item_id=pk)
        is_login = request.session.get('is_login')
        context = {
            'item':item,
            'is_login':is_login
        }

        return render(request,'shop0c/itemDetail.html',context)

    def post(self, request):
        pass

class Cart(View):
    def get(self, request):

        user_id = request.session.get('user_id')
        items = Item.objects.all()
        user = User.objects.get(user_id=user_id)
        carts = Shopcart.objects.filter(user=user)

        sum = 0
        for cart in carts:
            sum += cart.amount*cart.item.price



        #carts = Shopcart.objects.get(user=user_id)
        context = {
            'carts':carts,
            'item':items,
            'sum':sum
        }

        return render(request,'shop0c/cart.html',context)


    def post(self, request):
        amount = request.POST['amount']
        item_id = request.POST['item_id']
        user_id = request.session.get('user_id')
        item = Item.objects.get(item_id=item_id)
        user = User.objects.get(user_id=user_id)

        if Shopcart.objects.filter(item=item, user=user):
            print('a')
            cart = Shopcart.objects.get(item=item, user=user)
            cart.amount += int(amount)
            cart.save()

        else:
            print('b')
            new_cart = Shopcart()
            new_cart.amount = amount
            new_cart.item = item
            new_cart.user = user
            new_cart.save()

        items = Item.objects.all()
        carts = Shopcart.objects.filter(user=user)

        sum = 0
        for cart in carts:
            sum += cart.amount*cart.item.price

        #carts = Shopcart.objects.get(user=user_id)
        context = {
            'carts':carts,
            'item':items,
            'sum':sum
        }

        return render(request,'shop0c/cart.html',context)

class Deletecart(View):
    def get(self, request):
        pass
    def post(self, request):
        id = request.POST['delete']
        cart = Shopcart.objects.get(id=id)
        cart.delete()

        return redirect(reverse('shop0c:cart'))
    
class Modifycart(View):
    def get(self, request):
        pass
        '''
        id = request.GET['id']
        amount = request.GET['amount']
        cart = Shopcart.objects.get(id=id)
        cart.amount = amount

        return redirect(reverse('shop0c:cart'))
        '''

    def post(self, request):
        id = request.POST['modify']
        cart = Shopcart.objects.get(id=id)
        context = {
            'cart':cart,
            'id':id
        }

        return render(request,'shop0c/modifycart.html',context)
        
class Updatecart(View): 
    def get(self, request):
        pass
    def post(self, request):
        id = request.POST['id']
        amount = request.POST['amount']
        cart = Shopcart.objects.get(id=id)
        cart.amount = amount
        cart.save()
        return redirect(reverse('shop0c:cart'))


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
                
                    return redirect(reverse('shop0c:'))

        s = '会員IDかパスワードが間違っています'
        form = LoginForm()
        context = {
            's':s,
            'form':form
        }
        return render(request, 'shop0c/login.html', context)

class Logout(View):
    def get(self, request):
        request.session['is_login'] = False
        request.session['user_id'] = ''
        request.session['password'] = ''
        request.session['name'] = ''
        request.session['address'] = ''
        return redirect(reverse('shop0c:login'))

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
                "errors":form.errors
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
        user_id = request.session.get('user_id')
        password = request.session.get('password')
        name = request.session.get('name')
        address = request.session.get('address')

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
        user_id = request.session.get('user_id')
        password = request.session.get('password')
        name = request.session.get('name')
        address = request.session.get('address')

        form = UpdateUserForm()
        #form.fields['id'].initial = user_id
        form.fields['name'].initial = name
        form.fields['address'].initial = address

        context = {
            'form':form,
            'user_id':user_id
        }

        return render(request, 'shop0c/updateUser.html', context)

    def post(self, request):
        pass

class UpdateConfirm(View):
    def get(self, request):
        pass
    def post(self, request):

        form = UpdateUserForm(request.POST)
        if not form.is_valid():

            user_id = request.session.get('user_id')
            context = {
                "form":form,
                "errors":form.errors,
                "user_id":user_id
            }
            return render(request, 'shop0c/updateUser.html', context)

        user_id = request.session.get('user_id')
        password = request.POST['password']
        name = request.POST['name']
        address = request.POST['address']

        context = {
            'user_id':user_id,
            'password':password,
            'name':name,
            'address':address
        }

        return render(request,'shop0c/updateUserConfirm.html',context)

class UpdateUserConfirm(View):
    def get(self, request):
        pass
    def post(self, request):

        old_user = User.objects.get(user_id=request.session['user_id'])
        old_user.delete()


        new_user = User()
        
        new_user.user_id = request.session.get('user_id')
        new_user.password = request.POST['password']
        new_user.name = request.POST['name']
        new_user.address = request.POST['address']

        new_user.save()

        request.session['user_id'] = new_user.user_id
        request.session['password'] = new_user.password
        request.session['name'] = new_user.name
        request.session['address'] = new_user.address
        request.session['is_login'] = True

        context = {
            'user_id':request.session.get('user_id'),
            'name':request.session.get('name'),
            'address':request.session.get('address')
        }

        return render(request,'shop0c/updateUserCommit.html',context)



class Delete(View):
    def get(self, request):
        name = request.session.get('name')
        context = {
            'name':name
        }
        return render(request,'shop0c/withdrawConfirm.html', context)

    def post(self, request):
        print(request.session.get('user_id'))
        user = User.objects.get(user_id=request.session.get('user_id'))
        name = user.name
        context = {
            'name':name
        }
        user.delete()
        request.session['is_login'] = False
        return render(request,'shop0c/withdrawCommit.html',context)


class Purchase_cart(View):
    def get(self, request):
        pass
    def post(self, request):
        sum = request.POST['sum']
        new_purchase = Purchase()
        user = User.objects.get(user_id=request.session.get('user_id'))
        max_id_o = Purchase.objects.order_by('-Purchase_id').first()
        max_id = int(max_id_o.Purchase_id)+1
        new_purchase.Purchase_id = max_id
        new_purchase.destination = user.address
        new_purchase.user = user
        new_purchase.save()

        carts = Shopcart.objects.filter(user=user)
        details = []
        print(carts)
        for cart in carts:

            new_detail = Detail()
            max_id_o = Detail.objects.order_by('-purchase_detail_id').first()
            max_id = int(max_id_o.purchase_detail_id)+10
            new_detail.purchase_detail_id = max_id
            new_detail.amount = cart.amount
            new_detail.Purchase = new_purchase
            new_detail.item = cart.item
            cart.delete()
            new_detail.save()
            details.append(new_detail)
        

        print(details)
        context = {
            'new_purchase':new_purchase,
            'details':details,
            'sum':sum,
            #'item':item,
        }

        details = []
        return render(request,'shop0c/purchase.html',context)
    
class Updatedestination(View):
    def get(self, request):
        pass
    def post(self, request):
        destination = request.POST['destination']
        purchase_id = request.POST['purchase_id']
        purchase = Purchase.objects.get(Purchase_id=purchase_id)
        purchase.destination = destination
        purchase.save()
        context = {
            'destination':destination
        }

        return render(request,'shop0c/updatedestination.html',context)

a = 'テスト'
