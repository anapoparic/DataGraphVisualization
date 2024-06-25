from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('config/', views.config, name='generated_graph'),
    path('generated_graph/', views.generate, name='generated_graph'),
    path('search/', views.search, name='search_graph'),
    path('clear/', views.clear_filters, name='clear_filters'),
    path('set_workspace/<int:number>/', views.set_workspace, name='workspace')
]