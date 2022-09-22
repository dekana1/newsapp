from django.shortcuts import render, get_object_or_404
from .models import OurNews
from rest_framework import generics
from .serializers import OurNewsSerializers
import requests

# Create your views here.

base_url = 'https://hacker-news.firebaseio.com/v0/'
top_story_url = f"{base_url}topstories.json"


payload = "{}"
response = requests.request("GET", top_story_url, data=payload)

story_ids = response.json() 

def news_list(request):
    
    context = {}
    news = OurNews.objects.all()
    
    context['story_ids'] = story_ids
    context['our_news'] = news
    
    return render(request, "newsapi/news_list.html", context)


def hacker_news_details(request, story_id):
    
    story_url = f"{base_url}item/{story_id}.json"
    
    payload = "{}"
    hn_response = requests.request("GET", story_url, data=payload)
    
    return render(request, 'newsapi/hn_news_details.html', {'news': hn_response})


def our_news_details(request, news_id):
    
    our_news = get_object_or_404(OurNews, id=news_id)
    
    return render(request, 'newsapi/our_news_details.html', {'news': our_news})


class NewsList(generics.ListCreateAPIView):
    serializer_class = OurNewsSerializers
    
    
    def get_queryset(self):
        
        queryset = OurNews.objects.all()
        type = self.request.query_params.get('type')
        
        if type is not None:
            queryset = OurNews.objects.filter(type=type)
            
        return queryset
    


class NewsDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OurNewsSerializers
    queryset = OurNews.objects.all()
    
    