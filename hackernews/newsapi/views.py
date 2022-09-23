from django.shortcuts import render, get_object_or_404
from .models import OurNews, HNew, NewHNStories
from rest_framework import generics, viewsets
from .serializers import OurNewsSerializers, HNewsSerializers, NewHNStoriesSerializers
import requests
import requests_cache


# Create Cache for latest stories


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
        
    
    def get_hnews_details(self, id):
        
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{id}.json"
        payload = "{}"
        hn_details_response = requests.request("GET", story_url, data=payload)
        
        try:
            hn_details_response.raise_for_status()
            return hn_details_response.json()

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
    
    
    
    
    
    # print("hey", new_hnews_id)         
    
         
    def save_hnews_dets(self):
        
        story_ids = NewHNStories.objects.values_list('hn_id', flat=True)
        new_hnews_id = [*story_ids]
        
        if new_hnews_id is not None:
            
            try:
                print("Running hnews dets ...")
                batch_number = len(new_hnews_id) // 50
                
                for x in range(batch_number):
                
                    new_hnews_details = self.get_hnews_details(new_hnews_id[x])
                    
                    print("dets", new_hnews_details)
                    
                    s_obj = NewHNStories.objects.filter(hn_id=new_hnews_id[x])
                    
                    pk = HNew.objects.filter(pk_id=s_obj)
                    print(pk)
                    
                    if pk.exists():
                        pass
                    else:
                        details_object = HNew.objects.create(pk_id=pk, by=new_hnews_details['by'], score=new_hnews_details['score'], time_created=new_hnews_details['time'],
                                            title=new_hnews_details['title'], type=new_hnews_details['type'], url=new_hnews_details['url'])
                        details_object.save()
                        
                        print("saved...")
                    
                    # new_hnews_id.remove(new_hnews_id[x])
                    
            except:
                pass
                    
                    
def home(request):
    
    context = {}
    
    our_news = OurNews.objects.all()
    hnews = HNew.objects.all()

    return render(request, 'newsapi/news_list.html', {'our_news': our_news, 'HNews': hnews})


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
    
    