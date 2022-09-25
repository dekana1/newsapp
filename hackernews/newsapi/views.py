from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import OurNews, HNew, NewHNStories, Comments
from django.contrib.auth.decorators import login_required
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
        
        # print(new_hnews_id)
        
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
    
         
    def save_hnews_dets(self, pk_id):
        
        if HNew.objects.filter(pk_id=pk_id).exists():
            pass
            
        else:
            
            hnews_data = self.get_hnews_details(pk_id)
            
            if hnews_data is not None:
                
                try:

                    print("In hnews data")
                    
                    print(hnews_data)
                    
                    new_hnews_object = HNew.objects.create(pk_id=hnews_data['id'], by=hnews_data['by'], score=hnews_data['score'], time_created=hnews_data['time'],
                                                            title=hnews_data['title'], type=hnews_data['type'], url=hnews_data['url'])
                    new_hnews_object.save()
                    print("Saved HNews data")
                    
                except:
                    pass
                      
@login_required                  
def home(request):
    
    context = {}
    
    our_news = OurNews.objects.all().order_by('time_created')
    our_news_paginator = Paginator(our_news, 5)
    page = request.GET.get('page')
    
    
    o_news = our_news_paginator.get_page(page)
    
    

    return render(request, 'newsapi/news_list.html', {'our_news': o_news})


@login_required
def other_news(request):
    
    context = {}
    
    hnews = HNew.objects.all().order_by('time_created')
    hnews_paginator = Paginator(hnews, 2)
    page = request.GET.get('page')
    
    h_news = hnews_paginator.get_page(page)
    

    return render(request, 'newsapi/hnews.html', {'h_news': h_news})


@login_required
def our_news_details(request, news_id):
    
    our_news = get_object_or_404(OurNews, id=news_id)
    comments = Comments.objects.filter(parent=our_news).order_by('time')
    
    return render(request, 'newsapi/our_news_details.html', {'news': our_news, "comments": comments})


@login_required
def search(request):
    
    if request.method == 'POST':
        
        search_bar = request.POST['search-bar']
        
        our_news  = OurNews.objects.filter(title__contains=search_bar)
        h_news = HNew.objects.filter(title__contains=search_bar)
        
        return render(request, 'newsapi/search_result.html', {'search_bar': search_bar, "Our_new_results": our_news, "Hnew_results": h_news})
    
    else:
        return render(request, 'newsapi/search_result.html')


@login_required
def catergory(request, cats):
    
    catergory_our_news = OurNews.objects.filter(type=cats)
    catergory_h_news = HNew.objects.filter(type=cats)
    
    return render(request, 'newsapi/catergories.html', {'cats': cats, 'our_news_results': catergory_our_news, 'h_news_results': catergory_h_news})
    
    
@login_required  
def write_comment(request):
    
    if request.method == 'POST':
        
        text = request.POST['text']
        parent = request.POST['parent']
        
        article = OurNews.objects.get(id=parent)
        
        new_comment = Comments(type='comment', by=request.user, parent=article, text=text)
        new_comment.save()
    
    return HttpResponse("thanks")
    
    

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
    
    