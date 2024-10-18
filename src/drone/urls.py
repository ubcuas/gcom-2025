from django.urls import path
from . import views

urlpatterns = [
    path("status", views.get_current_status, name="get_current_status"),
    path("status/history", views.get_status_history, name="get_status_history"),
    path("takeoff", views.takeoff, name="takeoff"),
    path("arm", views.arm, name="arm"),
    path("land", views.land, name="land"),
    path("rtl", views.get_rtl, name="rtl"),
    path("rtl", views.post_rtl, name="rtl"),
    path("lock", views.lock, name="lock"),
    path("insert", views.insert, name="insert"),
    path("unlock", views.unlock, name="unlock"),
    path("queue", views.get_queue, name="get_queue"),
    path("queue", views.post_queue, name="post_queue"),
    path("home", views.post_home, name="post_home"),
    path("clear", views.clear, name="clear"),
    path("diversion", views.diversion, name="diversion"),
    path("flightmode", views.flightmode, name="flight_mode"),
]
