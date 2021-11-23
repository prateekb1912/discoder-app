from django.db.models.base import Model
from base.models import Room
from rest_framework.serializers import ModelSerializer

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
