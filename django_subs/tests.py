from pdb import set_trace

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.core import mail

from django_subs.models import Subscription
from django_subs.utils import subscribe, unsubscribe, send_message

def clear():
    mail.outbox = []

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


    def testSendMessageUsesSimpleTemplate(self):
        clear()
        hash = subscribe('blah',  'art@example.com')
        subscribe('blah',  'sasha@example.com')
        subscribe('minor', 'peter@example.com')

        send_message('blah', 'subject', 'Test message')

        self.assertEqual(2, len(mail.outbox))
        self.assertEqual(['art@example.com'], mail.outbox[0].to)
        self.assertEqual(['sasha@example.com'], mail.outbox[1].to)

        body = mail.outbox[0].body

        self.assert_('Test message' in body)
        self.assert_(hash in body)

