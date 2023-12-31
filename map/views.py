from map.models import Tract
from map.serializers import TractSerializer
from rest_framework import generics
from django.core.exceptions import ValidationError
from django.contrib.gis.geos import Point

class TractViewset(generics.ListAPIView):
    serializer_class = TractSerializer

    def get_queryset(self):
        try:
            lng = float(self.request.query_params.get('lng'))
            lat = float(self.request.query_params.get('lat'))
            pnt = Point(lng, lat)
        except:
            raise ValidationError(message='Failed to create point from lng/lat.')
       
        return Tract.objects.filter(geometry__intersects=pnt)