from django.contrib.syndication.views import Feed

from django_ical.views import ICalFeed

from modeemintternet.models import News


class NewsRSSFeed(Feed):
    title = "Modeemi ryn uutiset"
    link = "/uutiset/"

    def items(self):
        return News.objects.order_by('-posted')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.text


class NewsICalFeed(ICalFeed):
    """
    Modeemi news iCal feed.
    """

    product_id = '-//Modeemi ry//Uutiset//FI'
    timezone = 'UTC'
    file_name = 'uutiset.ics'

    def items(self):
        return News.objects.all().order_by('-starts')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.text

    def item_location(self, item):
        return item.location

    def item_geolocation(self, item):
        return (item.lat, item.lon)

    def item_created(self, item):
        return item.posted

    def item_updated(self, item):
        return item.modified

    def item_start_datetime(self, item):
        return item.starts

    def item_end_datetime(self, item):
        return item.ends
