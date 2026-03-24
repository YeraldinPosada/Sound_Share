from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import SongCreateView, SongListView, SongDetailView
router = DefaultRouter()

urlpatterns = [
    path('songs', SongCreateView.as_view(), name='create_song'),
    path('songs/', SongListView.as_view(), name='list_songs'),
    path('songs/<int:pk>', SongDetailView.as_view(), name='song_detail'),
]