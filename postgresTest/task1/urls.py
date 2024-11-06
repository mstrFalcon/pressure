from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("statistics/", views.statistics, name="statistics"),
    #path('statistics/', views.statistics, nam),
    path('api/', views.ChartData.as_view()),
]