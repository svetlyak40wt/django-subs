from django_subs.models import Subscription

def subscribe(subs_id, email):
    if Subscription.objects.filter(
            subs_id = subs_id, email = email).count() == 0:
        sub = Subscription(subs_id = subs_id, email = email)
        sub.save()
        return sub.hash

def unsubscribe(hash):
    Subscription.objects.filter(hash = hash).delete()
