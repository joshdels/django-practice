from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Item
from .serializers import ItemSerializers


class ItemsView(APIView):
  def get(self, request):
    items = Item.objects.all()
    serializer = ItemSerializers(items, many=True)
    return Response(serializer.data)
  
  def post(self, request):
    serializer = ItemSerializers(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    return Response(serializer.erros, status=400)