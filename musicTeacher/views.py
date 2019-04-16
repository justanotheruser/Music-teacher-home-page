import random

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader

from .models import MainPageInfo, Music, Video, Paper, Photo


def index(request):
    mainPageInfos = MainPageInfo.objects.all()[:1]
    if len(mainPageInfos) == 0:
        mainPageInfo = MainPageInfo()
    else:
        mainPageInfo = mainPageInfos[0]
    achievements = Photo.objects.filter(
        is_achievement__exact=True).order_by('-pub_date')

    params = {'achievements': achievements, 'main': mainPageInfo}
    citations = mainPageInfo.citation_set.all()
    if len(citations) > 0:
        params['citation'] = random.choice(citations)

    return render(request, 'musicTeacher/index.html', params)


def sheets(request):
    originals = Music.objects.filter(is_original__exact=True).order_by('-name')
    remakes = Music.objects.filter(is_original__exact=False).order_by('-name')
    context = {
        'originals': originals,
        'remakes': remakes
    }
    template = loader.get_template('musicTeacher/sheets.html')
    return HttpResponse(template.render(context, request))


def video(request):
    video = Video.objects.order_by('-pub_date')
    context = {'videos': video}
    template = loader.get_template('musicTeacher/video.html')
    return HttpResponse(template.render(context, request))


def papers(request):
    papers = Paper.objects.order_by('-pub_date')
    context = {'papers': papers}
    template = loader.get_template('musicTeacher/papers.html')
    return HttpResponse(template.render(context, request))


def paper(request, paper_id):
    paper = get_object_or_404(Paper, pk=paper_id)
    return render(request, 'musicTeacher/paper.html', {'paper': paper})


def photos(request):
    photos = Photo.objects.order_by('-pub_date')
    return render(request, 'musicTeacher/photos.html', {'photos': photos})


def latest_updates(request):
    papersUpdates = Paper.objects.order_by('-pub_date')[:3]
    musicUpdates = Music.objects.order_by('-pub_date')[:3]
    videoUpdates = Video.objects.order_by('-pub_date')[:3]
    return render(request, 'musicTeacher/latest_updates.html',
                  {'paperUpdates': papersUpdates,
                   'musicUpdates': musicUpdates,
                   'videoUpdates': videoUpdates})
