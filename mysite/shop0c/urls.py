from django.urls import path
from . import views

app_name = 'shop0c'

urlpatterns = [
    path('/', views.index, name='main'),
    path('result/', views.result, name='serchResult'),
    path('detail/', views.detail, name='itemDetail'),
    path('cart/', views.cart, name='cart'),
    path('login/', views.login, name='login'),
    path('registeruser/', views.register, name='registerUser'),
    #path('registerconfirm/', views.confirm, name='registerConfirm'),
]