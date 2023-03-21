from django.test import TestCase

from api.models import *
from api.views import *


class APITestCase(TestCase):
    def setUp(self):
        Player.objects.create(
            player_name="3nbi",
            player_uuid=get_uuid("3nbi")
        )
        print("Added 3nbi to DB")

    def test(self):
        enbi = Player.objects.get(player_name="3nbi")
        if enbi.player_uuid == "0fa150a821cd419491ab4aa6fa1e52f4":
            print("UUID found in DB")
            self.assertTrue
        else:
            print("UUID Not found in DB")
            self.assertFalse
