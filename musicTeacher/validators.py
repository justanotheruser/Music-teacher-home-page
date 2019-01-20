import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


youtubeURL = re.compile(
    '^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$')


def validate_youtube_url(url):
    if not youtubeURL.match(url):
        raise ValidationError(
            _('%(value)s is not a YouTube video'),
            params={'url': url},
        )
