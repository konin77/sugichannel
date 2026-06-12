from django.urls import path
from . import views

app_name = 'shop0c'

urlpatterns = [
    path('', views.Top.as_view(), name='main'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout',views.Logout.as_view(), name='logout'),
    path('registeruser/', views.Register.as_view(), name='registerUser'),
    path('registerconfirm/', views.Confirmregister.as_view(), name='confirmregister'),
    path('info/ ', views.UserInfo.as_view(), name='userInfo'),
    path('updateuser/', views.UpdateUser.as_view(),name='updateUser'),
    path('updateconfirm/',views.UpdateUserConfirm.as_view(),name='updateConfirm'),
    path('delete/',views.Delete.as_view(),name='delete'),
]