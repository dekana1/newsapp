from django.shortcuts import render, get_object_or_404
from .models import OurNews, HNew, NewHNStories
from rest_framework import generics, viewsets
from .serializers import OurNewsSerializers, HNewsSerializers
import requests
import requests_cache


# Create Cache for latest stories

requests_cache.install_cache('latest_news_cache', backend='sqlite', expire_after=300)

# Get TOP Stories
# base_url = 'https://hacker-news.firebaseio.com/v0/'
# latest_story_url = f"{base_url}newstories.json"
# payload = "{}"
# response = requests.request("GET", latest_story_url, data=payload)

# story_ids = response.json()  # Top story IDS

# # Get LATEST STORY DETAILS
# story_dets = {}  
    
# for x in story_ids:
    
#     story_url = f"{base_url}item/{x}.json"
#     payload = "{}"
#     hn_response = requests.request("GET", story_url, data=payload)
    
#     story_dets[x] = hn_response.json()


class newsViewset(viewsets.ModelViewSet):
    
    serializer_class = HNewsSerializers
    
    def get_queryset(self):
        
        data = HNew.objects.all()
        
        return data
    
    
    def get_hnews(self):
        url = "https://hacker-news.firebaseio.com/v0/newstories.json"

        payload = "{}"
        api_response = requests.request("GET", url, data=payload)
        
        try:
            api_response.raise_for_status()
            return api_response.json()

        except:
            return None
        
    def save_hnews(self):
        
        new_hnews_id = self.get_hnews()
        
        print(new_hnews_id)
        
        if new_hnews_id is not None:
            try:
                
                print("Running For loop now")
                
                for x in new_hnews_id:
                    if NewHNStories.objects.filter(hn_id=x).exists():
                        pass
                    else:
                        new_hnews_id_object = NewHNStories.objects.create(hn_id=x)
                        new_hnews_id_object.save()
                
                print("End of loop")
            except:
                pass



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
    
    