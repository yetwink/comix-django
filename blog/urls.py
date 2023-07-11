from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('genre/<int:pk>/', genre_page, name='genre'),
    path('comic/<int:pk>/', comic_detail, name='comic'),
    path('add_comics/', add_comics, name='add_comics'),
    path('comic/<int:pk>/volumes/add/', add_volume, name='add_volume'),
    path('comic/<int:pk>/volumes/', volumes_view, name='volume'),
    path('comic/<int:pk>/volumes/<int:id>/chapters/', chapters_view, name='chapters'),
    path('comic/<int:pk>/volumes/<int:id>/chapters/add/', add_chapter, name='add_chapter'),
    path('comic/<int:comics_id>/volumes/<int:volume_id>/chapters/<int:pk>/pictures/', pictures_view, name='pictures'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('comics/<int:pk>/update/', UpdateComics.as_view(), name='update'),
    path('comics/<int:pk>/delete/', DeleteComics.as_view(), name='delete'),
    path('save_comment/<int:pk>/', save_comment, name='save_comment'),
    path('chapter/<int:pk>/', show_volume_pictures, name='chapter'),
    path('profile/<int:pk>/', profile_view, name='profile'),
    path('search/', search_results, name='search'),
    path('edit_profile/<int:pk>/', EditProfileView.as_view(), name='edit')
]
