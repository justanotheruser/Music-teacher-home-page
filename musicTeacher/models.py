from django.db import models
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.utils.functional import cached_property
from django.utils import timezone
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from .validators import youtubeURL, validate_youtube_url


class SingletonModel(models.Model):

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class MainPageInfo(SingletonModel):
    photo = models.FileField(upload_to='photos', null=True,
                             validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    surname = models.CharField(max_length=128, default='<фамилия>')
    name = models.CharField(max_length=128, default='<имя>')
    patronymic = models.CharField(max_length=128, default='<отчество>')
    position = models.CharField(max_length=255, default='<должность>')
    greeting = models.CharField(max_length=2000, default='<приветствие>')

    def __str__(self):
        return u"Информация на главной странице"


class Music(models.Model):
    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', editable=False)
    upd_date = models.DateTimeField('date updated', editable=False)
    is_original = models.BooleanField(default=True)
    sheets = models.FileField(upload_to='sheets/sheets', blank=True, null=True,
                              validators=[FileExtensionValidator(allowed_extensions=['pdf', 'rar', 'zip', '7z'])])
    audio = models.FileField(upload_to='sheets/audio', blank=True, null=True,
                             validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'mid', 'midi'])])
    difficulty = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(4)],
                                     blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.pub_date = timezone.now()
        self.upd_date = timezone.now()
        super(Music, self).save(*args, **kwargs)


class Video(models.Model):
    name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    url = models.URLField(max_length=200, validators=[validate_youtube_url])

    def save(self, *args, **kwargs):
        if youtubeURL.match(self.url):
            self.url = self.url.replace('watch?v=', 'embed/', 1)
        else:
            return
        if not self.id:
            self.pub_date = timezone.now()
        self.upd_date = timezone.now()
        super(Video, self).save(*args, **kwargs)

    @cached_property
    def pub_date_only(self):
        return self.pub_date.date()

    def __str__(self):
        return self.name


class Photo(models.Model):
    title = models.CharField(max_length=100)
    photo = models.FileField(upload_to='photos',
                             validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])])
    photo_thumbnail = ImageSpecField(source='photo',
                                     processors=[ResizeToFill(324, 240)],
                                     format='JPEG',
                                     options={'quality': 70})
    pub_date = models.DateTimeField('date published', editable=False)
    upd_date = models.DateTimeField('date updated', editable=False)
    is_achievement = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.pub_date = timezone.now()
        self.upd_date = timezone.now()
        return super(Photo, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Paper(models.Model):
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    document = models.FileField(upload_to='papers',
                                validators=[FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx'])])
    pub_date = models.DateTimeField('date published', editable=False)
    upd_date = models.DateTimeField('date updated', editable=False)
    videos = models.ManyToManyField(Video)
    photos = models.ManyToManyField(Photo)

    def save(self, *args, **kwargs):
        if not self.id:
            self.pub_date = timezone.now()
        self.upd_date = timezone.now()
        return super(Paper, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
