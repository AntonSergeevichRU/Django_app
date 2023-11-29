from django.test import TestCase
from django.urls import reverse

import json
from .views import get_cookie_view



class GetCookieViewTestCase(TestCase):
    def test_get_cookie_view(self):
        response = self.client.get(reverse('my_auth:cookie_get'))
        self.assertContains(response, 'Куки значение')


class FooBarViewTestCase(TestCase):
    def test_foo_bar_view(self):
        response = self.client.get(reverse('my_auth:foo_bar'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        expected_data = {"spam": "eggs", "foo": "bar", }

        self.assertJSONEqual(response.content, expected_data)