from django.urls import path

from . import views


urlpatterns = [
    path('login/',views.login, name='index'),
    path('',views.homePage, name='AdminHomePage'),
    path('logout',views.logout, name='logout'),
    path('truckInfo',views.truckInfo, name='TruckInfo'),
    path('truckInfoDetails/<truckname>',views.truckinfoDetails, name='TruckInfoDetails'),

]