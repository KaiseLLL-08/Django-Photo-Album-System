from django.urls import path
from . import views

urlpatterns = [
    # Albums
    path('', views.AlbumListView.as_view(), name='album-list'),
    path('create/', views.AlbumCreateView.as_view(), name='album-create'),
    path('<int:pk>/', views.AlbumDetailView.as_view(), name='album-detail'),
    path('<int:pk>/edit/', views.AlbumUpdateView.as_view(), name='album-edit'),
    path('<int:pk>/delete/', views.AlbumDeleteView.as_view(), name='album-delete'),

    # Photos
    path('photos/upload/', views.PhotoCreateView.as_view(), name='photo-create'),
    path('photos/<int:pk>/', views.PhotoDetailView.as_view(), name='photo-detail'),
    path('photos/<int:pk>/edit/', views.PhotoUpdateView.as_view(), name='photo-edit'),
    path('photos/<int:pk>/delete/', views.PhotoDeleteView.as_view(), name='photo-delete'),
]