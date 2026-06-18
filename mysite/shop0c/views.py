from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View
from shop0c.models import User, Item, Shopcart, Purchase, Detail, Admin, Category
from shop0c.forms import LoginForm, RegistUserForm ,UpdateUserForm, AdminLoginForm, ItemRegisterForm, ItemUpdateForm, PurchaseForm
#from django.contrib.auth import logout
from .forms import LoginForm, ItemRegisterForm, ItemUpdateForm, AdminPurchaseHistorySearchForm


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
            'recommended_items': Item.objects.filter(recommended=True),  
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
            '7':'帽子',
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
                
                    return redirect(reverse('shop0c:main'))

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
        user = User.objects.get(user_id=request.session.get('user_id'))
        carts = Shopcart.objects.filter(user=user)

        if not carts.exists():
            return redirect("shop0c:cart")

        details = []
        total = 0

        for cart in carts:
            total += cart.item.price * cart.amount
            details.append(cart)

        form = PurchaseForm(initial={
            "destination": user.address,
            "payment_mothod": "代引き"
        })

        context = {
            "details": details,
            "sum": total,
            "form": form,
        }
        return render(request, 'shop0c/purchase.html', context)

    def post(self, request):
        form = PurchaseForm(request.POST)

        if not form.is_valid():
            return redirect('shop0c:purchase')

        user = User.objects.get(user_id=request.session.get('user_id'))
        carts = Shopcart.objects.filter(user=user)

        if not carts.exists():
            return redirect("shop0c:cart")

        max_id_obj = Purchase.objects.order_by('-Purchase_id').first()
        if max_id_obj:
            max_purchase_id = int(max_id_obj.Purchase_id) + 1
        else:
            max_purchase_id = 1

        destination = form.cleaned_data["destination"]

        new_purchase = Purchase(
            Purchase_id=max_purchase_id,
            destination=destination,
            user=user
        )
        new_purchase.save()

        max_detail_obj = Detail.objects.order_by('-purchase_detail_id').first()

        if max_detail_obj:
            next_detail_id = int(max_detail_obj.purchase_detail_id) + 1
        else:
            next_detail_id = 1

        for cart in carts:
            new_detail = Detail(
                purchase_detail_id=next_detail_id,
                amount=cart.amount,
                Purchase=new_purchase,
                item=cart.item
            )
            new_detail.save()

            cart.delete()
            next_detail_id += 1

        return redirect('shop0c:purchase_commit')


class PurchaseCommit(View):
    def get(self, request):
        purchase = Purchase.objects.order_by('-Purchase_id').first()

        context = {
            "purchase": purchase,
        }
        return render(request, 'shop0c/purchaseCommit.html', context)


class PurchaseHistory(View):
    def get(self, request, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect("shop0c:login")

        user_id = request.session["user_id"]
        user = User.objects.get(user_id=user_id)

        purchases = Purchase.objects.filter(user=user).order_by("-booked_date")

        purchase_history_list = []

        for purchase in purchases:
            purchase_details = Detail.objects.filter(Purchase=purchase)

            detail_list = []
            total_price_all = 0

            for detail in purchase_details:
                total_price = detail.item.price * detail.amount
                total_price_all += total_price

                detail_list.append({
                    "detail": detail,
                    "item": detail.item,
                    "amount": detail.amount,
                    "total_price": total_price,
                })

            purchase_history_list.append({
                "purchase": purchase,
                "detail_list": detail_list,
                "total_price_all": total_price_all,
            })

        context = {
            "purchase_history_list": purchase_history_list,
            "login_user_id": request.session.get("user_id"),
            "login_name": request.session.get("name"),
        }
        return render(request, "shop0c/purchaseHistory.html", context)


###########################
# --- ここから管理機能 --- #
###########################

class AdminLogin(View):
    def get(self, request, *args, **kwargs):
        form = AdminLoginForm()

        context = {
            "form": form,
        }
        return render(request, "shop0c/adminLogin.html", context)

    def post(self, request, *args, **kwargs):
        form = AdminLoginForm(request.POST)

        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "shop0c/adminLogin.html", context)

        admin_id = form.cleaned_data["admin_id"]
        password = form.cleaned_data["password"]

        admin = Admin.objects.filter(admin_id=admin_id, password=password).first()

        if admin is None:
            context = {
                "form": form,
                "error": "管理者ID、またはパスワードが間違っています。",
            }
            return render(request, "shop0c/adminLogin.html", context)

        request.session["admin_id"] = admin.admin_id

        return redirect("shop0c:admin_main")


class AdminMain(View):
    def get(self, request, *args, **kwargs):
        if "admin_id" not in request.session:
            return redirect("shop0c:admin_login")

        context = {
            "admin_id": request.session["admin_id"],
        }
        return render(request, "shop0c/adminMain.html", context)
    

class AdminLogout(View):
    def get(self, request, *args, **kwargs):
        if "admin_id" in request.session:
            del request.session["admin_id"]

        return redirect("shop0c:admin_login")


class ItemList(View):
    def get(self, request, *args, **kwargs):
        if "admin_id" not in request.session:
            return redirect("shop0c:admin_login")

        keyword = request.GET.get("keyword", "")
        category_id = request.GET.get("category_id", "all")

        items = Item.objects.all()

        if keyword != "":
            items = items.filter(name__contains=keyword)

        if category_id != "all":
            items = items.filter(category_id=category_id)

        items = items.order_by("item_id")
        categories = Category.objects.all().order_by("category_id")

        context = {
            "items": items,
            "categories": categories,
            "keyword": keyword,
            "selected_category_id": category_id,
        }
        return render(request, "shop0c/adminItemList.html", context)

# ============================================================
# views.py の ItemRegister クラスを以下に丸ごと置き換えてください
# ============================================================

class ItemRegister(View):
    def get(self, request, *args, **kwargs):
        if "admin_id" not in request.session:
            return redirect("shop0c:admin_login")

        form = ItemRegisterForm()

        context = {
            "form": form,
        }
        return render(request, "shop0c/adminItemRegister.html", context)

    def post(self, request, *args, **kwargs):
        if "admin_id" not in request.session:
            return redirect("shop0c:admin_login")

        # ★ ファイルアップロードのため request.FILES も渡す
        form = ItemRegisterForm(request.POST, request.FILES)

        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "shop0c/adminItemRegister.html", context)

        item_id = form.cleaned_data["item_id"]
        name = form.cleaned_data["name"]
        category = form.cleaned_data["category"]
        manufacturer = form.cleaned_data["manufacturer"]
        color = form.cleaned_data["color"]
        price = form.cleaned_data["price"]
        stock = form.cleaned_data["stock"]
        recommended = form.cleaned_data["recommended"]
        image = form.cleaned_data.get("image")  # ★ 追加

        if Item.objects.filter(item_id=item_id).exists():
            context = {
                "form": form,
                "error": "この商品IDはすでに使われています。",
            }
            return render(request, "shop0c/adminItemRegister.html", context)

        item = Item(
            item_id=item_id,
            name=name,
            category=category,
            manufacturer=manufacturer,
            color=color,
            price=price,
            stock=stock,
            recommended=recommended,
        )

        # ★ 画像が選択されていれば保存
        if image:
            item.image = image

        item.save()

        return redirect("shop0c:item_list")


# ============================================================
# views.py の ItemUpdate クラスを以下に丸ごと置き換えてください
# ============================================================

class ItemUpdate(View):
    def get(self, request, item_id, *args, **kwargs):
        if "admin_id" not in request.session:
            return redirect("shop0c:admin_login")

        item = Item.objects.filter(item_id=item_id).first()

        if item is None:
            return redirect("shop0c:item_list")

        form = ItemUpdateForm(initial={
            "item_id": item.item_id,
            "name": item.name,
            "category": item.category,
            "manufacturer": item.manufacturer,
            "color": item.color,
            "price": item.price,
            "stock": item.stock,
            "recommended": item.recommended,
        })

        context = {
            "form": form,
            "item": item,
        }
        return render(request, "shop0c/adminItemUpdate.html", context)

    def post(self, request, item_id, *args, **kwargs):
        if "admin_id" not in request.session:
            return redirect("shop0c:admin_login")

        old_item = Item.objects.filter(item_id=item_id).first()

        if old_item is None:
            return redirect("shop0c:item_list")

        # ★ ファイルアップロードのため request.FILES も渡す
        form = ItemUpdateForm(request.POST, request.FILES)

        if not form.is_valid():
            context = {
                "form": form,
                "item": old_item,
            }
            return render(request, "shop0c/adminItemUpdate.html", context)

        new_item_id = form.cleaned_data["item_id"]
        image = form.cleaned_data.get("image")  # ★ 追加

        # 商品IDに変更があったときの処理
        if new_item_id != old_item.item_id:
            if Item.objects.filter(item_id=new_item_id).exists():
                context = {
                    "form": form,
                    "item": old_item,
                    "error": "この商品IDはすでに使われています。",
                }
                return render(request, "shop0c/adminItemUpdate.html", context)

            new_item = Item(
                item_id=new_item_id,
                name=form.cleaned_data["name"],
                category=form.cleaned_data["category"],
                manufacturer=form.cleaned_data["manufacturer"],
                color=form.cleaned_data["color"],
                price=form.cleaned_data["price"],
                stock=form.cleaned_data["stock"],
                recommended=form.cleaned_data["recommended"],
                # ★ 画像：新しく選択されていれば新画像、なければ旧画像を引き継ぐ
                image=image if image else old_item.image,
            )

            new_item.save()

            Shopcart.objects.filter(item=old_item).update(item=new_item)
            Purchase.objects.filter(item=old_item).update(item=new_item)

            old_item.delete()

        # 商品IDに変更がなければそのままのものを使う
        else:
            old_item.name = form.cleaned_data["name"]
            old_item.category = form.cleaned_data["category"]
            old_item.manufacturer = form.cleaned_data["manufacturer"]
            old_item.color = form.cleaned_data["color"]
            old_item.price = form.cleaned_data["price"]
            old_item.stock = form.cleaned_data["stock"]
            old_item.recommended = form.cleaned_data["recommended"]
            # ★ 画像：新しく選択されていれば上書き、未選択なら現在の画像を維持
            if image:
                old_item.image = image

            old_item.save()

        return redirect("shop0c:item_list")

class ItemDelete(View):
    def get(self, request, item_id, *args, **kwargs):
        if "admin_id" not in request.session:
            return redirect("shop0c:admin_login")

        item = Item.objects.filter(item_id=item_id).first()

        if item is None:
            return redirect("shop0c:item_list")

        context = {
            "item": item,
        }

        return render(request, "shop0c/adminItemDelete.html", context)

    def post(self, request, item_id, *args, **kwargs):
        if "admin_id" not in request.session:
            return redirect("shop0c:admin_login")

        item = Item.objects.filter(item_id=item_id).first()

        if item is None:
            return redirect("shop0c:item_list")

        # 購入履歴が存在する商品は削除できないようにしておく（いらんかも）
        # if PurchaseModel.objects.filter(item=item).exists():
        #     context = {
        #         "item": item,
        #         "error": "この商品は購入履歴に存在するため、削除できません。",
        #     }

        #     return render(request, "adminItemDelete.html", context)

        Shopcart.objects.filter(item=item).delete()
        item.delete()

        return redirect("shop0c:item_list")
    

class AdminPurchaseHistory(View):
    def get(self, request, *args, **kwargs):
        if "admin_id" not in request.session:
            return redirect("shop0c:admin_login")
        
        form = AdminPurchaseHistorySearchForm(request.GET)

        purchases = Purchase.objects.all().order_by("-booked_date")

        if form.is_valid():
            purchase_id = form.cleaned_data["purchase_id"]
            user_id = form.cleaned_data["user_id"]
            item_name = form.cleaned_data["item_name"]
            cancel = form.cleaned_data["cancel"]

            if purchase_id is not None:
                purchases = purchases.filter(Purchase_id=purchase_id)

            if user_id != "":
                purchases = purchases.filter(user__user_id__contains=user_id)

            if item_name != "":
                purchase_ids = Detail.objects.filter(
                    item__name__icontains=item_name
                ).values_list("Purchase_id", flat=True).distinct()
                purchases = purchases.filter(Purchase_id__in=purchase_ids)

            # if item_name != "":
            #     purchase_ids = Detail.objects.filter(item__name__icontains=item_name).values_list("purchase_detail_id", flat=True)
            #     purchases = purchases.filter(Purchase_id__in=purchase_ids)

            if cancel == "not_cancel":
                purchases = purchases.filter(cancel=False)

            if cancel == "cancel":
                purchases = purchases.filter(cancel=True)

        purchase_history_list = []

        for purchase in purchases:
            purchase_details = Detail.objects.filter(Purchase=purchase)

            detail_list = []
            total_price_all = 0

            for detail in purchase_details:
                total_price = detail.item.price * detail.amount #カート内の商品ごとの合計金額
                total_price_all += total_price

                detail_list.append({
                    "detail": detail,
                    "item": detail.item,
                    "amount": detail.amount,
                    "total_price": total_price,
                })

            purchase_history_list.append({
                "purchase": purchase,
                "detail_list": detail_list,
                "total_price_all": total_price_all,
            })

        context = {
            "form": form,
            "purchase_history_list": purchase_history_list,
        }
        return render(request, "shop0c/adminPurchaseHistory.html", context)
    

class AdminPurchaseCancel(View):
    def get(self, request, purchase_id, *args, **kwargs):
        if "admin_id" not in request.session:
            return redirect("shop0c:admin_login")

        purchase = Purchase.objects.filter(Purchase_id=purchase_id).first()

        if purchase is None:
            return redirect("shop0c:admin_purchase_history")

        # すでにキャンセル済みの場合はエラーを表示
        if purchase.cancel:
            purchase_details = Detail.objects.filter(Purchase=purchase)
            detail_list = []
            total_price_all = 0
            for detail in purchase_details:
                total_price = detail.item.price * detail.amount
                total_price_all += total_price
                detail_list.append({
                    "detail": detail,
                    "item": detail.item,
                    "amount": detail.amount,
                    "total_price": total_price,
                })
            context = {
                "purchase": purchase,
                "detail_list": detail_list,
                "total_price_all": total_price_all,
                "error": "この注文はすでにキャンセル済みです。",
            }
            return render(request, "shop0c/adminPurchaseCancel.html", context)

        purchase_details = Detail.objects.filter(Purchase=purchase)

        detail_list = []
        total_price_all = 0

        for detail in purchase_details:
            total_price = detail.item.price * detail.amount
            total_price_all += total_price
            detail_list.append({
                "detail": detail,
                "item": detail.item,
                "amount": detail.amount,
                "total_price": total_price,
            })

        context = {
            "purchase": purchase,
            "detail_list": detail_list,
            "total_price_all": total_price_all,
        }
        return render(request, "shop0c/adminPurchaseCancel.html", context)

    def post(self, request, purchase_id, *args, **kwargs):
        if "admin_id" not in request.session:
            return redirect("shop0c:admin_login")

        purchase = Purchase.objects.filter(Purchase_id=purchase_id).first()

        if purchase is None:
            return redirect("shop0c:admin_purchase_history")

        purchase.cancel = True
        purchase.save()

        return redirect("shop0c:admin_purchase_history")
