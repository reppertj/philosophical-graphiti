from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(
        r'^node-autocomplete/$',
        views.NodeAutocomplete.as_view(),
        name='node-autocomplete',
    ),
    re_path(
        r'^\?head=(?P<head>.*?)&tail=(?P<tail>.*)',
        views.index,
        name='results-graph',
    )
    #path("node/search", views.NodeSelectView.as_view(), name="node-select"),
]