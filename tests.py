from django.test import TestCase

import datetime

# Create your tests here.
from . import models
from . import views
from .forms import CheckInOutForm

class CheckInTestCase(TestCase):
    def setUp(self):
        self.p_john_snow = models.Participant.objects.create(name="John", surname="Snow", uuid="abc123")
        self.e = models.Event.objects.create(title="Test event", description="A fake event", event_date = datetime.date(2001,1,14) )
        self.t_john_snow = models.Ticket.objects.create(event=self.e,participant=self.p_john_snow,has_checked_in=False,uuid="tkt123")

    def test_john_snow_can_check_in(self):
        views.event_do_check_in_out(self.e.id,self.p_john_snow.uuid,None,None,CheckInOutForm.CHECK_IN)
        tkt=models.Ticket.objects.get(participant__id=self.p_john_snow.id)
        self.assertEqual(tkt.has_checked_in,True)
        
