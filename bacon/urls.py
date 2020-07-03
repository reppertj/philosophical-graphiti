"""bacon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    path('', include('graph.urls')),
#    path('bacon/', include('graph.urls')),
    path('admin/', admin.site.urls),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),
    re_path('djga/', include('google_analytics.urls')),
    re_path(r'^loaderio-a6835b730a78a1b0817b48d09474984e.txt', TemplateView.as_view(template_name="graph/loaderio-a6835b730a78a1b0817b48d09474984e.txt", content_type="text/plain")),
]
