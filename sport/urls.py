from django.urls import path
from sport import views
app_name = 'sport'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('basicdata/<slug:basicdata_name_slug>/', views.view_basicdata, name='view_basicdata'),
    path('complicatedData/<slug:complicatedData_name_slug>/', views.view_complicatedData, name='view_complicatedData'),
]