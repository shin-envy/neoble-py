from django.urls import path
from . import views
import threading
urlpatterns = [
    path("getuuid", views.get_uuid, name="getUUID"),
    path("addplayer", views.add_player, name="addPlayer"),
    path("db", views.db, name="db"),
    path("test", views.test, name="test"),
    path("auctions", views.get_auctions, name="auctions")
]

views.refresh_auction()