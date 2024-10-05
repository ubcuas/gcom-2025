from django.urls import path
from . import views

urlpatterns = [
    path("status", views.get_current_status, name="get_current_status"),
    path("status/history", views.get_status_history, name="get_status_history"),
    path("drone/takeoff", views.takeoff, name="takeoff"),
    path("drone/arm", views.arm, name="arm"),
    path("drone/land", views.land, name="land"),
    path("drone/rtl", views.get_rtl, name="rtl"),
    path("drone/rtl", views.post_rtl, name="rtl"),
    path("drone/lock", views.lock, name="lock"),
    path("drone/unlock", views.unlock, name="unlock"),
    path("drone/queue", views.get_queue, name="get_queue"),
    path("drone/queue", views.post_queue, name="post_queue"),
    path("drone/home", views.post_home, name="post_home"),
    path("drone/prepend", views.prepend, name="prepend"),
    path("drone/append", views.append, name="append"),
    path("drone/clear", views.clear, name="clear"),
    path("drone/diversion", views.diversion, name="diversion"),
    path(
        "drone/vtol/transition", views.get_vtol_transition, name="get_vtol_transition"
    ),
    path(
        "drone/vtol/transition", views.post_vtol_transition, name="post_vtol_transition"
    ),
    path("drone/flightmode", views.flightmode, name="flight_mode"),
]
