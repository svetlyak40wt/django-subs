import logging

from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django_subs.models import Subscription

def subscribe(subs_id, email):
    if Subscription.objects.filter(
            subs_id = subs_id, email = email).count() == 0:
        sub = Subscription(subs_id = subs_id, email = email)
        sub.save()
        return sub.hash

def unsubscribe(hash):
    Subscription.objects.filter(hash = hash).delete()

def get_subs(subs_id):
    return list(Subscription.objects.filter(subs_id = subs_id))

def send_message(subs_id,
                 subject,
                 message,
                 from_email = '',
                 fail_silently = False,
                 template = 'subs/email.txt'):
    """Sends email to subscription list with given subs_id."""

    if not Site._meta.installed:
        site = {}
    else:
        site = Site._default_manager.get_current()

    for subscription in get_subs(subs_id):
        try:
            body = render_to_string(template, dict(
                message = message,
                site = site,
                subscription = subscription,
            ))
            send_mail(subject, body, from_email, [subscription.email], fail_silently = fail_silently)
        except Exception:
            logging.getLogger('django_subs').exception("Can't send email to %s" % email)
            if fail_silently == False:
                raise

