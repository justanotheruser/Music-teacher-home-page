import datetime
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


MONTH_TO_RU_NAME = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь"
}

"""Returns photo published on specified month and year and links to previous and next month"""
def photos(request):
    def get_current_year_month():
        now = datetime.datetime.now()
        month = now.month
        return '{}-{:02d}'.format(now.year, now.month)

    def get_previous_month(year, month):
        month -= 1
        if month < 1:
            month = 12
            year -= 1
        return year, '{:02d}'.format(month)

    def get_next_month(year, month):
        month += 1
        if month > 12:
            month = 1
            year += 1
        return year, '{:02d}'.format(month)

    date = request.GET.get('date', get_current_year_month())
    splitted = date.split('-')
    if len(splitted) != 2:
        return HttpResponse(status=404)
    try:
        year, month = int(splitted[0]), int(splitted[1])
    except ValueError:
        return HttpResponse(status=404)

    photos = Photo.objects.filter(pub_date__year=year).filter(
        pub_date__month=month).order_by('-pub_date')
    render_data = {'photos': photos, 'year': year,
                   'month': MONTH_TO_RU_NAME[month]}

    render_data['prev_year'], render_data['prev_month'] = get_previous_month(
        year, month)
    now = datetime.datetime.now()
    if (year, month) != (now.year, now.month):
        render_data['next_year'], render_data['next_month'] = get_next_month(
            year, month)

    return render(request, 'musicTeacher/photos.html', render_data)


def latest_updates(request):
    papersUpdates = Paper.objects.order_by('-pub_date')[: 3]
    musicUpdates = Music.objects.order_by('-pub_date')[: 3]
    videoUpdates = Video.objects.order_by('-pub_date')[: 3]
    return render(request, 'musicTeacher/latest_updates.html',
                  {'paperUpdates': papersUpdates,
                   'musicUpdates': musicUpdates,
                   'videoUpdates': videoUpdates})
