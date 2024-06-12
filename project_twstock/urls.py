"""
URL configuration for project_twstock project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stock/', views.stock, name='stock'),
    path('stock_add/', views.stock_add, name='stock_add'),
    path('stock_delete/', views.stock_delete, name='stock_delete'),
    path('stock_search/', views.stock_search,),
    path('ETF/', views.ETF),   
    path('test/', views.test),
    path('popular/', views.popular),
    path('monthly/', views.monthly),

    path('index/', views.index),
    path('index_in/', views.index_in),
    path('login/', views.login),
    path('register/', views.register),  
    path('useradd/', views.useradd),
    path('page1/', views.page1),
    path('userlogout/', views.userlogout),

]


# path('update_table/', views.update_table),
# path('popular_stocks/', views.popular_stocks),
# path('update_stocks_data/', views.update_stocks_data),
# path('update_all_stocks_data/', views.update_all_stocks_data),
# path('last_trading_day/', views.last_trading_day),
# path('popular/', views.popular),
# path('get_top_30_stocks/', views.get_top_30_stocks),
# path('update_stocks_data/', views.update_stocks_data),
# path('get_last_trading_day/', views.get_last_trading_day),