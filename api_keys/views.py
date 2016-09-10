from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from models import Keys
from django.conf import settings
import string
import itertools

User = settings.AUTH_USER_MODEL
chars = string.letters + string.digits
raw_generate_keys = (p for p in itertools.product(chars, repeat=4))

class IssuedKey(APIView):
    def get(self, request, format=None):
        key = next(generate_key())
        key.key_type = Keys.KEY_TYPE_ISSUED
        key.save()
        return Response(key.key)


class UseKey(APIView):
    def get(self, request, key, format=None):
        try:
            db_key = Keys.objects.get(key=key, key_type=Keys.KEY_TYPE_ISSUED)
        except Keys.DoesNotExist:
            return Response(data="Coudn't use this key", status=status.HTTP_403_FORBIDDEN)
        db_key.key_type = Keys.KEY_TYPE_USED
        db_key.save()
        return Response('ok')


class KeyInfo(APIView):
    def get(self, request, key, format=None):
        try:
            key = Keys.objects.get(key=key)
        except Keys.DoesNotExist:
            return Response(data="Not Issued")
        return Response(data=key.get_key_type_display())


class KeyCount(APIView):
    def get(self, request, format=None):
        return Response(data=Keys.count_not_ussued())


def generate_key():
    for k in raw_generate_keys:
        k = ''.join(k)
        if Keys.objects.filter(key=k).exists():
            continue
        key = Keys(key=k)
        key.save()
        yield key
