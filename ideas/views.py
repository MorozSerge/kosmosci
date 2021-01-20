from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from .forms import IdeaForm
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required


from .models import *

# Create your views here.


@login_required
def ideas(request):
    user = request.user
    user_news = UserNews.objects.filter(idea_source=user).order_by('-published')
    paginator = Paginator(user_news, 10)
    page = request.GET.get('page')
    user_news = paginator.get_page(page)
    form = IdeaForm()
    if request.method == "POST":
        new_idea = UserNews(idea_source=user, body='', published=now())
        form = IdeaForm(request.POST, request.FILES, instance=new_idea)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('ideas:ideas'))
    context = {'idea_source': user,
               'user_news': user_news,
               'form': form}
    return render(request, 'ideas/ideas.html', context)


@login_required()
def others_ideas(request, pk):
    user = Enlightened.objects.get(pk=pk)
    if request.user == user:
        return redirect('ideas:ideas')
    user_news = UserNews.objects.filter(idea_source=user).order_by('-published')
    paginator = Paginator(user_news, 10)
    page = request.GET.get('page')
    user_news = paginator.get_page(page)
    context = {'idea_source': user,
               'user_news': user_news}
    return render(request, 'ideas/ideas_of_others.html', context)


@login_required()
def edit_idea(request, pk):
    idea = UserNews.objects.get(pk=pk)
    if idea.idea_source.id == request.user.id:
        form = IdeaForm(instance=idea)
        if request.method == "POST":
            form = IdeaForm(request.POST, request.FILES, instance=idea)
            if form.is_valid():
                form.save()
                return redirect('ideas:ideas')
        context = {'idea': idea, 'user': request.user, 'form': form}
        return render(request, 'ideas/edit.html', context)
    else:
        return redirect('ideas:ideas')


@login_required()
def delete_idea(request, pk):
    idea = UserNews.objects.get(pk=pk)
    if idea.idea_source.id == request.user.id:
        idea.delete()
    return redirect('ideas:ideas')

