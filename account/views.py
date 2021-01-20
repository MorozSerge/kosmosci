import time

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.views import View

from .forms import *


# Create your views here.


class Registration(View):

	def get(self, request):
		context = {'reg_stat': 1}
		return render(request, 'account/registration.html', context)

	def post(self, request):
		try:
			user = Enlightened.objects.create_user(username=request.POST['username'], email=request.POST['email'],
												   password=request.POST['password1'])
		except IntegrityError:
			context = {'reg_stat': 0}
			return render(request, 'account/registration.html', context)
		request.session['reg_stat'] = 1
		return HttpResponseRedirect(reverse('account:login'))


class Login(View):
	def get(self, request):
		reg_status = request.session.get('reg_stat', 0)
		log_status = request.session.get('log_stat', 2)
		request.session['reg_stat'] = 0
		request.session['log_stat'] = 2
		context = {'reg_stat': reg_status, 'log_stat': log_status}
		return render(request, 'account/login.html', context)

	def post(self, request):
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			request.session['log_stat'] = 1
			return HttpResponseRedirect(reverse('home'))
		else:
			request.session['log_stat'] = 0
			return HttpResponseRedirect(reverse('account:login'))


@login_required
def sign_out(request):
	logout(request)
	return HttpResponseRedirect(reverse('account:login'))


@login_required
def home(request):
	return render(request, 'account/base.html')


@login_required
def profile(request):
	user = request.user
	new_source = Source.objects.all()
	idea_source = list(Enlightened.objects.all())
	news_subs = NewsFollow.objects.filter(follower=user)
	idea_subs = UserFollow.objects.filter(follower=user)

	idea_source.remove(user)
	labels = [item.news_source.name for item in news_subs]
	usernames = [item.idea_source.username for item in idea_subs]
	success = request.session.get('success', False)
	request.session['success'] = False
	form = EnlightenedForm(instance=user, prefix="form")
	pass_form = PasswordChangeForm(user, prefix="pass")
	if request.method == "POST":
		pass_form = PasswordChangeForm(user, request.POST, prefix="pass")
		form = EnlightenedForm(request.POST, request.FILES, instance=user, prefix="form")
		if form.is_valid():
			form.save()
		if pass_form.is_valid():
			user = pass_form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Your password was successfully updated!')
			time.sleep(2)

			return redirect('home')
		else:
			if not form.is_valid():
				messages.error(request, 'Please correct the error below.')

	context = {'form': form,
			   'pass_form': pass_form,
			   'new_source': new_source,
			   'news_subs': labels,
			   'idea_source': idea_source,
			   'idea_subs': usernames,
			   'success': success
			   }
	return render(request, 'account/profile.html', context)


@login_required
def updateNewsSources(request):
	source_labels = dict(request.POST)
	source_labels = list(source_labels.keys())
	source_labels.remove('csrfmiddlewaretoken')
	try:
		newsSubs = NewsFollow.objects.filter(follower=request.user)
		for subs in newsSubs:
			subs.delete()
	finally:
		for label in source_labels:
			news_source = Source.objects.get(name=label)
			NewsFollow.objects.create(follower=request.user, news_source=news_source)
	request.session['success'] = True
	return HttpResponseRedirect(reverse('account:profile'))


@login_required
def updateIdeaSources(request):
	source_labels = dict(request.POST)
	source_labels = list(source_labels.keys())
	source_labels.remove('csrfmiddlewaretoken')
	try:
		usersnews = UserFollow.objects.filter(follower=request.user)
		for subs in usersnews:
			subs.delete()
	finally:
		for name in source_labels:
			source_user = Enlightened.objects.get(username=name)
			UserFollow.objects.create(follower=request.user, idea_source=source_user)
	request.session['success'] = True
	return HttpResponseRedirect(reverse('account:profile'))
