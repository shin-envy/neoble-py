from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
import requests


def get_username(uuid):
    res = requests.get("https://api.mojang.com/user/profile/" + uuid)
    if res.status_code == 200:
        if "errorMessage" not in res.json():
            return res.json()["name"]
        else:
            return "Invalid UUID"
    elif res.status_code == 404 or res.status_code == 400:
        if "errorMessage" in res.json():
            return res.json()["errorMessage"]
        else:
            return res.status_code


def get_uuid(username):
    res = requests.get(
        "https://api.mojang.com/users/profiles/minecraft/" + username)
    if res.status_code == 200:
        if "errorMessage" not in res.json():
            return res.json()["id"]
        else:
            return "Couldn't find any profile with that name"
    elif res.status_code == 404:
        if "errorMessage" in res.json():
            return res.json()["errorMessage"]
        else:
            return res.status_code


def getUUID(request):
    username = request.GET.get("username")
    if username is None or not username:
        return HttpResponseNotFound("No username provided")
    return HttpResponse(get_uuid(username=username))


def addPlayer(request):
    username = request.GET.get("username")
    if username is None or not username:
        return HttpResponseNotFound("No username provided")
    uuid = get_uuid(username)
    # check if given username is a valid player
    if uuid != "Couldn't find any profile with that name":
        _username = get_username(uuid)
        if not Player.objects.filter(player_name=username).exists() or not Player.objects.filter(player_uuid=uuid).exists():
            Player(player_name=username, player_uuid=uuid).save()
            return HttpResponse()
        else:
            if _username != username:
                Player.objects.get(player_uuid=uuid).player_name = _username
                return HttpResponse("Updated Database (Player Changed Username)")
            return HttpResponse("Database already has player data")
    else:
        return HttpResponseNotFound()


def test(request):
    print(get_username("0fa150a821cd419491ab4aa6fa1e52f4"))
    print(get_uuid("3nbi"))
    return HttpResponse()

# remove later


def db(request):
    print(Player.objects.all().values())
    return HttpResponse(Player.objects.all().values())
