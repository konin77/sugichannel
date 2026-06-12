from django.urls import path
from . import views

app_name = 'shop0c'

urlpatterns = [
    path('', views.Top.as_view(), name='main'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout',views.Logout.as_view(), name='logout'),
    path('registeruser/', views.Register.as_view(), name='registerUser'),
    path('registerconfirm/', views.Confirmregister.as_view(), name='confirmregister'),
    path('commit', views.commit, name='registerCommit'),
    path('info', views.info, name='userInfo'),
    path('updateuser', views.update_user,name='updateUser'),
    path('updateconfirm',views.update_confirm,name='updateConfirm'),
    path('updatecommit',views.update_commit,name='updateCommit'),
]