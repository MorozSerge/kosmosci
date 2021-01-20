from .models import *
from django import forms


class IdeaForm(forms.ModelForm):
	class Meta:
		model = UserNews
		fields = ('body', 'image')
		widgets = {
			'body': forms.Textarea(attrs={'autofocus': 'autofocus'})
		}
		labels = {
			'body': 'Your idea (350 symbols max):',
			'image': 'Attach an image'
		}