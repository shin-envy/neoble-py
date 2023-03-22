from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from .models import *
import requests
import nbt
import base64
import io
import time
import threading

timer_running = False
last_refresh = 1

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


def _get_uuid(username):
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


def get_uuid(request):
    username = request.GET.get("username")
    if username is None or not username:
        return HttpResponseNotFound("No username provided")
    return HttpResponse(_get_uuid(username=username))


def add_player(request):
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

#def test(request):
#    print(parse_item_data("H4sIAAAAAAAAAHVUXW/TMBS93Qa05WMT7IUXMIiJlW1d0jRtMvFSuq0rsA6tmxBCKHITr7Xm2FXibPSR/wHPlfgZ/Sn8EMR1W9hAIg+OfX3O9T3HuSkCFCDHiwCQW4AFHuVu5+BGU2VS54qwqGm/AEtMhgMwTw5un8pewug57QmWW4TCAY/YvqD9FHd/FuFWxNOhoCMkvVUJy2N0FR5PxvUWownphhjbIZNx5Dk+vrz1StV2S1BCwC6NaX+6GW64noVvtr7hWKUpbMPerHtW2SvBS4R2dcJkXw9mYNv2r4P99Y26ayYRsqpzuuP7Za9agk1kNxOuyV+nWWszHk5+H1fz1krwyIQ/YqYf377g7NM/S9T2EFeTsZiNR5KRfZWQhhCkjZsvJuNao8cF16Md0uJU6ucp6Qoam3IRf9xuHZyQ5tt28w08NbLM1khlCUkvVRIRLrUiesBIP8HriOAZYiJGBZd9U7dd8zctr1426uvRVA/RCu7jSqLZvRFhksWcpWVYRVGHVFLSVKk2oh3bsuABRptKiUhdShOkjmVucRm17ZvrjcgrJbMUnsxN4yEVZMB1Sgb0ghFKwgGV4fTQtXlpJBvi0uSyXWNqnX3WCSWz6sqY3P9t2DmdjBNy3b7DDycH7SbZPe209o46pPv+6HiXXMHzsNShMYMahubl/fF0ahe6/ePr9/+NUITlPVNMQ+uE9zLN0kVYTijqGgXZsJ/QiBn1+E2vDJQOhkpTrYLQNIIxpQhLfRaneci/bnTf7R0HFizttzt7VwF7FijAvUwKFZ6zKEiF0qnpgYVrtCs8cmMV8TPOErh5NtW0CHfnxQSCXTCB3Bt505Zwp9VudE66wdSXItwxPYnyYyY1KlnNhOYx1SxQkgVnKgmoENOGRd+yDPnPeq7jeJHrb9lnobNVjSxryw9r7hazmMMqvku9sJ6HAqZhqabxEFYq25XqdsUhdmXHtUjj0Oi4Oesc8zP4BRPUC8I7BAAA"))
#    refresh_auction()
#    return HttpResponse()

#def db(request):
#    print(Player.objects.all().values())
#    return HttpResponse(Auction.objects.all().values())

def _get_auctions():
    try:
        re = requests.get("https://api.hypixel.net/skyblock/auctions")
    except:
        raise Exception("Unable to send request to Hypixel API")
    if re.status_code == 200:
        if re.json()["success"] == True:
            if not Auction.objects.filter(last_updated=re.json()["lastUpdated"]).exists():
                Auction(last_updated=re.json()["lastUpdated"], auctions=re.json()["auctions"]).save()
                # crawl auctions and find for flips
                print("Added Auction " + str(re.json()["lastUpdated"]))
            else:
                print("Auction " + str(re.json()["lastUpdated"]) + " already exists")
            return re.json()

def refresh_auction():
    threading.Thread(target=start_refresh,args=(_get_auctions()["lastUpdated"], last_refresh)).start()

def get_auctions(request):
   return _get_auctions()

#TODO
def find_flips(auctions):
    raise NotImplementedError()
        
def parse_item_data(item_bytes):
    nbt_file = nbt.nbt.NBTFile(fileobj=io.BytesIO(base64.b64decode(item_bytes)))
    print(nbt_file[0][0]["tag"]["ExtraAttributes"])
    # nbt_file[0][0]["tag"]["ExtraAttributes"]["rarity_upgrades"] 1 = recombed 0 = not recombed
    # nbt_file[0][0]["tag"]["ExtraAttributes"]["uuid"]
    # nbt_file[0][0]["tag"]["ExtraAttributes"]["hot_potato_cound"]
    # nbt_file[0][0]["tag"]["ExtraAttributes"]["gems"]
    # nbt_file[0][0]["tag"]["ExtraAttributes"]["modfier"] reforge
    # nbt_file[0][0]["tag"]["ExtraAttributes"]["id"]
    # nbt_file[0][0]["tag"]["ExtraAttributes"]["count"]
    # nbt_file[0][0]["tag"]["ExtraAttributes"]["enchantments"] tag compound
    return nbt_file[0][0]

def start_refresh(last_updated, _last_refresh):
    if _last_refresh == last_updated :
        return
    print("starting refresh")
    last_refresh = last_updated
    next_update = last_updated / 1000 + 62
    timer_running = True
    while timer_running:
        if time.time() > next_update:
            refresh_auction()
            timer_running = False
