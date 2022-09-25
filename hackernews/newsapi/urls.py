from django.urls import path, include
from . import views
from .views import NewsList, NewsDetails, newsViewset

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('data', newsViewset, basename='HNews-data')

urlpatterns = [
    path("", views.home, name="home"),
    path("search", views.search, name="search"),
    path("api/", include(router.urls)),
    path("<int:news_id>", views.our_news_details, name="our_news_details"),
    path("News/", NewsList.as_view(), name='create'),
    path("News/<int:pk>/", NewsDetails.as_view()),
     
]
