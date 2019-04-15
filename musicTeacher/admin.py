from django.contrib import admin
from django import forms

from .forms import PaperForm
from .models import Music, Video, Paper, Photo, MainPageInfo


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    exclude = ('pub_date', 'upd_date')


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    exclude = ('pub_date', 'upd_date')


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    exclude = ('pub_date', 'upd_date')


@admin.register(MainPageInfo)
class MainPageInfoAdmin(admin.ModelAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(MainPageInfoAdmin, self).formfield_for_dbfield(
            db_field, **kwargs)
        if db_field.name == 'greeting':
            formfield.widget = forms.Textarea(attrs={'cols': '80', 'rows': '10'})
        return formfield


class PaperVideoMembershipInline(admin.TabularInline):
    model = Paper.videos.through


class PaperPhotoMembershipInline(admin.TabularInline):
    model = Paper.photos.through


class Video(admin.ModelAdmin):
    inlines = [
        PaperVideoMembershipInline,
    ]


class Photo(admin.ModelAdmin):
    inlines = [
        PaperPhotoMembershipInline,
    ]


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    inlines = [
        PaperVideoMembershipInline,
        PaperPhotoMembershipInline,
    ]
    exclude = ('pub_date', 'upd_date', 'videos', 'photos')
    form = PaperForm

