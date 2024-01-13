from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
# from .views import Home

urlpatterns = [
    
    path('', views.index, name="home"),
    path('login/', auth_views.LoginView.as_view(template_name='home/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page = "/"), name="logout"),
    path('register/', views.register, name="register"),
    path('home/', views.home, name="home"),
    path('chat/<id>', views.chat, name="chat"),
    path('send_message/', views.send_message, name="send_message"),
    path('get_latest_messages/<id>/', views.get_latest_messages, name="get_latest_messages"),
    

]