from django_ical.views import ICalFeed
from modeemintternet.models import Event


class EventFeed(ICalFeed):
    """
    Modeemi event iCal feed.
    """

    product_id = '-//Modeemi ry//Tapahtumat//FI'
    timezone = 'UTC'
    file_name = 'tapahtumat.ics'

    def items(self):
        return Event.objects.all().order_by('-starts')

    def item_title(self, event):
        return event.title

    def item_description(self, event):
        return event.description

    def item_location(self, event):
        return event.location

    def item_geolocation(self, event):
        return (event.lat, event.lon)

    def item_created(self, event):
        return event.posted

    def item_updated(self, event):
        return event.modified

    def item_start_datetime(self, event):
        return event.starts

    def item_end_datetime(self, event):
        return event.ends
