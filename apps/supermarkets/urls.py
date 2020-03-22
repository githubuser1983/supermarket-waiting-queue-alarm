from django.urls import path

from . import views

app_name = "supermarkets"

urlpatterns = [
    path("receivedata/", view=views.ReceiveSupermarketsFromQuery.as_view(), name="get"),
    path('warn/<str:pk>/', view=views.WarningCreateView.as_view(), name="post"),
]
