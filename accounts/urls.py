from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('logout/', auth_views.LogoutView.as_view(
        http_method_names=['get', 'post'],
        next_page='/login/'
    ), name='logout'),
]
