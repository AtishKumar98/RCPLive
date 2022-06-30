from django.urls import path
from django.contrib.auth import views as auth_views
# from django.conf.urls import url
from . import views 
import uuid

urlpatterns = [
    path('', views.index,name='home'),
    path('login/',views.loginpage,name='login'),
    path('main/', views.home,name='Bile'),
    path('logout/',views.logoutUser, name='logout'),
    path('dashboard/', views.dashboard,name='dashboard'),
    path('cart/', views.cart,name='cart'),
    path('pay/', views.initiate_payment, name='pay'),
    path('analytics/', views.analytics, name = 'analytics'),
    path('profile/<str:user>/',views.user_profile,name="user_profile"),
    path('callback/', views.callback, name='callback'),
    path('order_status/', views.order_status, name='order_status'),
    path('update_item/',views.update_item,name='update_item'),
    path('profile/',views.userProfile,name="profile_main"),
    path('SM_profile/',views.profile,name="profile_sm"),
    path('room/<str:room>/',views.room, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('posts/', views.posts, name='posts'),
    path('like/', views.LikeView, name='like_products'),


    ##Regarding ForgetPassword
    path('reset_password/',auth_views.PasswordResetView.as_view(),name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset_password_complete /',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]