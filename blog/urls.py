from django.urls import path
from . import views

app_name='blog'

urlpatterns = [
    path("",views.index, name="index"),
    path("post/<str:slug>",views.detail,name="detail"),
    path("new__something_url",views.new_url,name="new_page_url"),
    path("old_url",views.old_url_redirect,name="old_url"),
    path("contact",views.contact,name="contact"),
    path("about",views.about,name="contact"),
    path("register",views.register,name="register"),
    path("login",views.login,name="login"),
    path("dashboard",views.dashboard,name="dashboard")

]