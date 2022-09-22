from django.urls import path
from . import views
from .views import NewsList, NewsDetails

urlpatterns = [
    path("", views.news_list, name="news_list"),
    path("<int:news_id>", views.news_details, name="news_details"),
    path("<int:story_id>", views.hacker_news_details, name="hacker_news_details"),
     
    path("News/", NewsList.as_view()),
    path("News/<int:pk>/", NewsDetails.as_view()),
     
]
