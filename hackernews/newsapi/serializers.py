from rest_framework import serializers
from .models import OurNews


class OurNewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = OurNews
        fields = ('__all__')
