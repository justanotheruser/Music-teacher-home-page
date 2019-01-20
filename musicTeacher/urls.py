from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('sheets', views.sheets, name='sheets'),
    path('video', views.video, name='video'),
    path('papers', views.papers, name='papers'),
    path('papers/<int:paper_id>', views.paper, name='paper'),
    path('photos', views.photos, name='photos'),
    path('latest_updates', views.latest_updates, name='latest_updates')
]
