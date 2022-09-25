from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import OurNews, HNew, NewHNStories, Comments
from rest_framework import generics, viewsets
from rest_framework.pagination import LimitOffsetPagination
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
    
         
    def save_hnews_dets(self):
        
        story_ids = NewHNStories.objects.values_list('hn_id', flat=True)
        new_hnews_id = {*story_ids}
        
        
        if new_hnews_id is not None:
            print(news_hnews_id)
            
            existing = {ids.pk_id for ids in HNew.objects.all()}
            print(existing)
            try:
                print("Running hnews dets ...")
                
                news_hnews_id = new_hnews_id.remove(existing)
                batch_number = len(new_hnews_id)
                
                print(batch_number)
                
                for x in range(batch_number):
                
                    new_hnews_details = self.get_hnews_details(new_hnews_id[x])
                    print("dets", new_hnews_details)
                    
                    details_object = HNew.objects.create(pk_id=new_hnews_id[x], by=new_hnews_details['by'], score=new_hnews_details['score'], time_created=new_hnews_details['time'],
                                        title=new_hnews_details['title'], type=new_hnews_details['type'], url=new_hnews_details['url'])
                    details_object.save()
                    
                    print("saved...")
                    
                    
            except:
                pass
                    
                    
def home(request):
    
    context = {}
    
    our_news = OurNews.objects.all()
    # our_news_paginator = Paginator(our_news, 5)
    
    # page = request.GET.get('page')
    
    # try:
    #     o_news = our_news_paginator.page(page)
        
    # except PageNotAnInteger:
    #     o_news = our_news_paginator.page(1)
    
    # except EmptyPage:
    #     o_news = our_news_paginator.page(paginator.num_pages)
        
    hnews = HNew.objects.all()
    # hnews_paginator = Paginator(hnews, 5)
    
    # try:
    #     h_news = hnews_paginator.page(page)
        
    # except PageNotAnInteger:
    #     h_news = hnews_paginator.page(1)
    
    # except EmptyPage:
    #     h_news = hnews_paginator.page(paginator.num_pages)

    return render(request, 'newsapi/news_list.html', {'our_news': our_news, 'HNews': hnews})


def our_news_details(request, news_id):
    
    our_news = get_object_or_404(OurNews, id=news_id)
    comments = Comments.objects.filter(parent=our_news).order_by('time')
    
    return render(request, 'newsapi/our_news_details.html', {'news': our_news, "comments": comments})


def search(request):
    
    if request.method == 'POST':
        
        search_bar = request.POST['search-bar']
        
        our_news  = OurNews.objects.filter(title__contains=search_bar)
        
        
        return render(request, 'newsapi/search_result.html', {'search_bar': search_bar, "results": our_news})
    
    else:
        return render(request, 'newsapi/search_result.html')
    
    
class NewsList(generics.ListCreateAPIView):
    serializer_class = OurNewsSerializers
    pagination_class = LimitOffsetPagination
    
    def get_queryset(self):
        
        queryset = OurNews.objects.all()
        type = self.request.query_params.get('type')
        
        if type is not None:
            queryset = OurNews.objects.filter(type=type)
            
        return queryset
    

class NewsDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OurNewsSerializers
    queryset = OurNews.objects.all()
    
    