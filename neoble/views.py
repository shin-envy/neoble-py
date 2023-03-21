from django.http import HttpResponse
from api.views import get_uuid
# Create your views here.


async def index(request):
    uuid = get_uuid("3nbi")
    return HttpResponse(uuid)
