from rest_framework.decorators import api_view
from rest_framework.response import Response
from main.models import Room
from .serializers import RoomSerializer

@api_view(['GET','POST'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]
    return Response(routes, )
@api_view(['GET','POST'])
def getRooms(request):
    rooms = Room.objects.all()
    serializers = RoomSerializer(rooms, many=True)
    print(serializers)
    return Response(serializers.data)

@api_view(['GET',]) 
def getRoom(request, pk):
    room = Room.objects.get(id = pk)
    serializers = RoomSerializer(room, many=False)
    print(serializers)
    return Response(serializers.data)