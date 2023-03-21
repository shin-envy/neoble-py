from django.db import models

# Create your models here.


class Item(models.Model):
    item_name = models.CharField(max_length=255)
    item_id = models.CharField(max_length=255)
    item_data = models.TextField()


class Player(models.Model):
    player_name = models.CharField(max_length=255)
    player_uuid = models.CharField(max_length=255)
