from django.urls import path
from django.views.static import serve 
from django.conf.urls import url
from django.conf import settings
from django.conf.urls import *

from . import views

app_name = "supermarkets"

urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
    path("receivedata/", view=views.ReceiveSupermarketsFromQuery.as_view(), name="get"),
    path('warn/<str:pk>/', view=views.WarningCreateView.as_view(), name="post")
    
]