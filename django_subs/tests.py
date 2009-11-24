from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from django_subs.models import Subscription
from django_subs.utils import subscribe, unsubscribe

class SimpleTests(TestCase):
    urls = 'django_subs.testurls'

    def testSubscribeTwiceViaFunction(self):
        self.assertEqual(0, Subscription.objects.count())
        subscribe('blah-minor', 'art@example.com')
        subscribe('blah-minor', 'art@example.com')
        self.assertEqual(1, Subscription.objects.count())


    def testSubscribeViaView(self):
        c = Client()

        self.assertEqual(0, Subscription.objects.count())

        response = c.post(
            reverse('subscribe'),
            dict(
                subs_id = 'blah-minor',
                email = 'art@example.com',
                next = '/'
            )
        )
        self.assertRedirects(response, '/')
        self.assertEqual(1, Subscription.objects.count())


    def testUnSubscribeTwiceViaFunction(self):
        hash = subscribe('blah-minor', 'art@example.com')
        self.assertEqual(1, Subscription.objects.count())
        unsubscribe(hash)
        self.assertEqual(0, Subscription.objects.count())


    def testUnSubscribeViaView(self):
        c = Client()

        hash = subscribe('blah-minor', 'art@example.com')
        self.assertEqual(1, Subscription.objects.count())

        response = c.post(
            reverse('unsubscribe'),
            dict(
                hash = hash,
                next = '/'
            )
        )
        self.assertRedirects(response, '/')
        self.assertEqual(0, Subscription.objects.count())

