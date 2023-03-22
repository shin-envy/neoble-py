from django.http import HttpResponse
from api.views import _get_uuid
# Create your views here.


async def index(request):
    uuid = _get_uuid("3nbi")
    return HttpResponse(uuid)
