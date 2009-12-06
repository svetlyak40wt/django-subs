import md5

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class Subscription( models.Model ):
    subs_id = models.CharField( _('Subscription ID'), max_length = 40, db_index = True)
    email = models.CharField( _('Email'), max_length = 255)
    hash = models.CharField( _('Hash'), max_length = 32, db_index = True, editable = False)

    def __repr__(self):
        return 'Subscription(subs_id=%(subs_id)s, email=%(email)s, hash=%(hash)s' % self.__dict__

    def __unicode__(self):
        return '%s - %s' % (self.subs_id, self.email)

    def save(self):
        if not self.id:
            self.hash = md5.md5(self.subs_id + self.email + settings.SECRET_KEY).hexdigest()
        return super(Subscription, self).save()

    class Meta:
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')

