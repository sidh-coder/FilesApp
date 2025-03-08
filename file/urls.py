from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='file_list'),
    path('<path:folder_path>/', views.folder_view, name='folder_view'),
]
