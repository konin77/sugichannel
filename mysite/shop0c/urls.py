from django.urls import path
from . import views

app_name = 'shop0c'

urlpatterns = [
    path('',views.index),
    path('main/', views.Top.as_view(), name='main'),
    path('search/', views.Search.as_view(), name='search'),
    path('detail/<int:pk>/', views.Detailuesr.as_view(), name='detail'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout',views.Logout.as_view(), name='logout'),
    path('registeruser/', views.Register.as_view(), name='registerUser'),
    path('registerconfirm/', views.Confirmregister.as_view(), name='confirmregister'),
    path('info/ ', views.UserInfo.as_view(), name='userInfo'),
    path('updateuser/', views.UpdateUser.as_view(),name='updateUser'),
    path('updateconf',views.UpdateConfirm.as_view(),name='updateconf'),
    path('updateconfirm/',views.UpdateUserConfirm.as_view(),name='updateConfirm'),
    path('delete/',views.Delete.as_view(),name='delete'),
    path('cart/',views.Cart.as_view(),name='cart'),
    path('deletecart/',views.Deletecart.as_view(),name='deletecart'),
    path('modifycart',views.Modifycart.as_view(),name='modifycart'),
    path('updatecart',views.Updatecart.as_view(),name='updatecart'),
    path('purchase/',views.Purchase_cart.as_view(),name='purchase'),
    path('updatedestination',views.Updatedestination.as_view(),name='updatedestination'),

    # --- 管理機能　--- #
    path("admin/", views.AdminLogin.as_view(), name="admin_login"),
    path("adminMain/", views.AdminMain.as_view(), name="admin_main"),
    path("adminLogout/", views.AdminLogout.as_view(), name="admin_logout"),

    path("adminItemList/", views.ItemList.as_view(), name="item_list"),
    path("adminItemRegister/", views.ItemRegister.as_view(), name="item_register"),
    path("adminItemUpdate/<int:item_id>/", views.ItemUpdate.as_view(), name="item_update"),
    path("adminItemDelete/<int:item_id>/", views.ItemDelete.as_view(), name="item_delete"),
]