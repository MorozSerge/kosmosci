from account.models import *
from ideas.models import UserNews
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from.models import *


# Create your views here.


@login_required
def source_list(request):
    sources = Source.objects.order_by('name')
    context = {'sources': sources}
    return render(request, 'news/newsList.html', context)


@login_required
def news_list(request, pk):
    news = New.objects.filter(source_id=pk).order_by('-published')
    source = Source.objects.get(pk=pk)
    paginator = Paginator(news, 20)
    page = request.GET.get('page')
    news = paginator.get_page(page)
    context = {'news': news,
               'source': source}
    return render(request, 'news/news.html', context=context)


def parse_news(query, content_type):
    feed = []
    for item in query:
        t = dict()
        t['id'] = item.id
        t['image'] = item.image
        t['published'] = item.published
        t['type'] = content_type
        if content_type == 0:
            t['link'] = None
            t['header'] = item.idea_source.username
            t['body'] = item.body
            t['src'] = item.idea_source
        else:
            t['link'] = item.link
            t['header'] = item.name
            t['body'] = item.description
            t['src'] = item.source

        feed.append(t)
    return feed


@login_required
def feed(request, pk):

    if pk == "1":
        idea_subs = UserFollow.objects.filter(follower=request.user)
        news_subs = NewsFollow.objects.filter(follower=request.user)
        idea_sources = [item.idea_source for item in idea_subs]
        news_src = [item.news_source for item in news_subs]
        ideas = UserNews.objects.filter(idea_source__in=idea_sources).order_by('-published')
        news = New.objects.filter(source__in=news_src).order_by('-published')
        feed = parse_news(ideas, 0) + parse_news(news, 1)
    else:
        if pk == "2":
            news = New.objects.all().order_by('-published')
            feed = parse_news(news, 1)
        else:
            if pk == "3":
                 news_src = Source.objects.filter(type_space=True)
                 news = New.objects.filter(source__in=news_src).order_by('-published')
                 feed = parse_news(news, 1)
            else:
                if pk == "4":
                    news_src = Source.objects.filter(type_space=False)
                    news = New.objects.filter(source__in=news_src).order_by('-published')

                    feed = parse_news(news, 1)
                else:
                    if pk == "5":
                        news_subs = NewsFollow.objects.filter(follower=request.user)
                        news_src = [item.news_source for item in news_subs]
                        news = New.objects.filter(source__in=news_src).order_by('-published')
                        feed = parse_news(news, 1)
                    else:
                        if pk == "6":
                            ideas = UserNews.objects.all().order_by('-published')
                            feed = parse_news(ideas, 0)
                        else:
                            if pk == "7":
                                idea_subs = UserFollow.objects.filter(follower=request.user)
                                idea_sources = [item.idea_source for item in idea_subs]
                                ideas = UserNews.objects.filter(idea_source__in=idea_sources).order_by(
                                    '-published')
                                feed = parse_news(ideas, 0)
                            else:
                                return redirect('news:feed', pk=1)

    feed = sorted(feed, key=lambda x: x['published'], reverse=True)
    paginator = Paginator(feed, 20)
    page = request.GET.get('page')
    feed = paginator.get_page(page)
    return render(request, 'news/feed.html', context={'feed': feed})
