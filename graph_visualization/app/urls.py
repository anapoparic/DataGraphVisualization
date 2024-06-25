from django.urls import path

from . import views

urlpatterns = [
    path('', views.load_index_page, name='index'),
    path('load_workspace/<int:wsc_id>/', views.load_workspace, name='workspace'),
    path('generated_graph/', views.render_graph, name='graph_visualize'),
    path('search-filter/', views.search_filter_graph, name='search_filter_graph'),
    path('clear-filter/', views.clear_search_filter_input, name='clear_search_filter_input'),
]