from rest_framework import serializers
from .models import OurNews, HNew, NewHNStories


class OurNewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = OurNews
        fields = ('__all__')


class HNewsSerializers(serializers.ModelSerializer):
    class Meta:
        model = HNew
        fields = ('__all__')
        
        
class NewHNStoriesSerializers(serializers.ModelSerializer):
    class Meta:
        model = NewHNStories
        fields = ('__all__')