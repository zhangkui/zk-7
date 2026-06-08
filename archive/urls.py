from django.urls import path
from . import views

app_name = 'archive'

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/<uuid:pk>/', views.project_detail, name='project_detail'),
    path('exhibitions/', views.exhibition_list, name='exhibition_list'),
    path('exhibitions/<uuid:pk>/', views.exhibition_detail, name='exhibition_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('tags/', views.tag_list, name='tag_list'),
    path('search/', views.search, name='search'),
    path('api/autocomplete/', views.autocomplete, name='autocomplete'),
]
