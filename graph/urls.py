from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('random', views.get_random, name='get_random'),
    path('more', views.more, name='more'),
    re_path(
        r'^node-autocomplete/$',
        views.NodeAutocomplete.as_view(),
        name='node-autocomplete',
    ),
    re_path(
        r'^.*generate/(?P<source>.*)_sub(?P<directed_value>dg|g)data_(?P<target>.*).json',
        views.vega_spec,
        name='vega_spec'
    ),
    re_path(
        r'^paths/(?P<source>.*)_sub(?P<directed_value>dg|g)data_(?P<target>.*).json',
        views.subgraph_json,
        name='subgraph_json'
    ),
    re_path(
        r'^paths/',
        views.result,
        name='result',
    ),
    re_path(
        r'^(?P<source>.*)_sub(?P<directed_value>dg|g)data_(?P<target>.*).json',
        views.subgraph_json,
        name='subgraph_json'
    ),
    re_path(
        r'^neighbors/',
        views.neighbors,
        name='neighbors',
    ),
]
