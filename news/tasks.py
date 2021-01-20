from datetime import datetime, timezone, timedelta

from background_task import background
from .models import *
import feedparser
from bs4 import BeautifulSoup
from django.db import connection


@background(schedule=0)
def get_news():
    sources = Source.objects.all()
    for source in sources:
        channel = feedparser.parse(source.link)
        news = channel.entries
        queryset = New.objects.filter(source_id=source.id).order_by('-published')
        if len(queryset) > 0:
            last_date = queryset[0].published
        else:
            last_date = datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone(timedelta(hours=0)))
        for item in news:
            try:
                published_date = datetime(*item.published_parsed[:6],
                                          tzinfo=timezone(timedelta(hours=item.published_parsed[-1])))
            except:
                continue
            if last_date < published_date:
                try:
                    image = item.enclosures[0]['href']
                    if image[-3:] == 'mp4':
                        image = None
                except:
                    image = None
                try:
                    description = BeautifulSoup(item.description, "lxml").get_text(strip=True)
                except:
                    continue
                new_event = New(source=source, name=item.title, description=description, image=image, published=published_date, link=item.link)
                new_event.save()


@background(schedule=3600)
def clean_bg_tasks():
    c = connection.cursor()
    try:
        c.execute("DELETE FROM background_task_completedtask;")
        c.execute("DELETE FROM background_task;")
    finally:
        c.close()
    get_news(repeat=100, repeat_until=None)
