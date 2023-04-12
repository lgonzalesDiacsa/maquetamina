from rest_framework.serializers import ModelSerializer
from restapp.models import PostCardIDEvent

class restappSerializer(ModelSerializer):
    class Meta:
        model = PostCardIDEvent
        fields = ['id', 'cardid', 'f_evento', 'h_evento', 'evento']
        