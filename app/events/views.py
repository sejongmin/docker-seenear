from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Event
from .serializers import EventSerializer

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_event(request):
    serializer = EventSerializer(data=request.data)
    
    if serializer.is_valid():
        event = serializer.create(request.user.family_id)
        response_data = serializer.data
        response_data['id'] = event.id
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    response_data = {'error': serializer.errors}
    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_events(request, date):
    try:
        queryset = Event.objects.filter(
            Q(family_id=request.user.family_id) &
            Q(datetime__date=date)
        )
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    serializer = EventSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]