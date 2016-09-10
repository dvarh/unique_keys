from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from models import Keys
import json


class IssuedKey(APITestCase):
    def test_issued(self):
        key_1 = Keys(key='aaaa')
        key_1.save()
        self.assertEqual(Keys.objects.all().count(), 1)
        url = reverse('issue_key')
        response = self.client.get(url)
        self.assertEqual(Keys.objects.all().count(), 2)
        db_key_1 = Keys.objects.all().last()
        self.assertEqual(db_key_1.key, json.loads(response.content))
        self.assertEqual(db_key_1.key_type, Keys.KEY_TYPE_ISSUED)


class UseKey(APITestCase):
    def test_use(self):
        key_1 = Keys(key='1234')
        key_1.save()
        key_2 = Keys(key='5678', key_type=Keys.KEY_TYPE_ISSUED)
        key_2.save()
        key_3 = Keys(key='aa33', key_type=Keys.KEY_TYPE_USED)
        key_3.save()
        url = reverse('use_key', kwargs={'key': key_1.key})
        response = self.client.get(url)
        key_1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(key_1.key_type, Keys.KEY_TYPE_NOT_ISSUED)
        url = reverse('use_key', kwargs={'key': key_2.key})
        response = self.client.get(url)
        key_2.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(key_2.key_type, Keys.KEY_TYPE_USED)
        url = reverse('use_key', kwargs={'key': key_3.key})
        response = self.client.get(url)
        key_3.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(key_3.key_type, Keys.KEY_TYPE_USED)


class KeyInfo(APITestCase):
    def test_info(self):
        key_1 = Keys(key='1234')
        key_1.save()
        key_2 = Keys(key='5678', key_type=Keys.KEY_TYPE_ISSUED)
        key_2.save()
        key_3 = Keys(key='aa33', key_type=Keys.KEY_TYPE_USED)
        key_3.save()
        url = reverse('key_info', kwargs={'key': key_1.key})
        response = self.client.get(url)
        self.assertEqual(json.loads(response.content), 'Not Issued')
        url = reverse('key_info', kwargs={'key': key_2.key})
        response = self.client.get(url)
        self.assertEqual(json.loads(response.content), 'Issued')
        url = reverse('key_info', kwargs={'key': key_3.key})
        response = self.client.get(url)
        self.assertEqual(json.loads(response.content), 'Used')
        url = reverse('key_info', kwargs={'key': 'aaaa'})
        response = self.client.get(url)
        self.assertEqual(json.loads(response.content), 'Not Issued')


class KeyCount(APITestCase):
    def test_count(self):
        key_1 = Keys(key='1234')
        key_1.save()
        key_2 = Keys(key='5678', key_type=Keys.KEY_TYPE_ISSUED)
        key_2.save()
        key_3 = Keys(key='aa33', key_type=Keys.KEY_TYPE_USED)
        key_3.save()
        url = reverse('key_counts')
        response = self.client.get(url)
        self.assertEqual(json.loads(response.content), (26+26+10)**4 - 2)
