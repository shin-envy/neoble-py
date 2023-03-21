from django.urls import path
from . import views
urlpatterns = [
    path("getuuid", views.getUUID, name="getUUID"),
    path("addplayer", views.addPlayer, name="addPlayer"),
    path("db", views.db, name="db"),
    path("test", views.test, name="test"),
]
