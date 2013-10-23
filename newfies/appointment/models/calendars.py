# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from appointment.models.users import Calendar_User
import datetime
import pytz


class Calendar(models.Model):
    '''
    This is for grouping events so that batch relations can be made to all
    events.  An example would be a project calendar.

    name: the name of the calendar
    events: all the events contained within the calendar.
    >>> calendar = Calendar(name = 'Test Calendar')
    >>> calendar.save()
    >>> data = {
    ...         'title': 'Recent Event',
    ...         'start': datetime.datetime(2008, 1, 5, 0, 0),
    ...         'end': datetime.datetime(2008, 1, 10, 0, 0)
    ...        }
    >>> event = Event(**data)
    >>> event.save()
    >>> calendar.events.add(event)
    >>> data = {
    ...         'title': 'Upcoming Event',
    ...         'start': datetime.datetime(2008, 1, 1, 0, 0),
    ...         'end': datetime.datetime(2008, 1, 4, 0, 0)
    ...        }
    >>> event = Event(**data)
    >>> event.save()
    >>> calendar.events.add(event)
    >>> data = {
    ...         'title': 'Current Event',
    ...         'start': datetime.datetime(2008, 1, 3),
    ...         'end': datetime.datetime(2008, 1, 6)
    ...        }
    >>> event = Event(**data)
    >>> event.save()
    >>> calendar.events.add(event)
    '''
    name = models.CharField(_("name"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=200)
    user = models.ForeignKey(Calendar_User, blank=True, null=True, verbose_name=_("user"),
                             help_text=_("select user"),
                             related_name="calendar user")
    max_concurrent = models.IntegerField(null=True, blank=True, default=0, help_text=_("Max concurrent is not implemented"))
    created_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name=_('date'))

    class Meta:
        verbose_name = _('calendar')
        verbose_name_plural = _('calendars')
        app_label = "appointment"

    def __unicode__(self):
        return self.name

    @property
    def events(self):
        return self.event_set

    def get_recent(self, amount=5, in_datetime=datetime.datetime.now, tzinfo=pytz.utc):
        """
        This shortcut function allows you to get events that have started
        recently.

        amount is the amount of events you want in the queryset. The default is
        5.

        in_datetime is the datetime you want to check against.  It defaults to
        datetime.datetime.now
        """
        return self.events.order_by('-start').filter(start__lt=timezone.now())[:amount]

    def get_absolute_url(self):
        return reverse('calendar_home', kwargs={'calendar_slug': self.slug})

    def add_event_url(self):
        return reverse('s_create_event_in_calendar', args=[self.slug])
