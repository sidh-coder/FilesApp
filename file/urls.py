from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='file_list'),
    path('<str:folder_name>/',views.folder_view,name='folder_view'),
]

