from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings

import string

User = settings.AUTH_USER_MODEL


class Keys(models.Model):
    key = models.CharField('Key', blank=False, unique=True, max_length=4, help_text=_('Unique key'))
    KEY_TYPE_NOT_ISSUED = 'not_issued'
    KEY_TYPE_ISSUED = 'issued'
    KEY_TYPE_USED = 'used'
    KEY_TYPE_CHOICES = (
        (KEY_TYPE_NOT_ISSUED, 'Not Issued'),
        (KEY_TYPE_ISSUED, 'Issued'),
        (KEY_TYPE_USED, 'Used'),
    )

    key_type = models.CharField('Key type', default=KEY_TYPE_NOT_ISSUED, max_length=100, choices=KEY_TYPE_CHOICES)

    @staticmethod
    def count_not_ussued():
        chars = string.letters +  string.digits
        total_count = len(chars) ** 4
        return total_count - Keys.objects.exclude(key_type=Keys.KEY_TYPE_NOT_ISSUED).count()