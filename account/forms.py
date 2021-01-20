from .models import *
from django.forms import ModelForm


class EnlightenedForm(ModelForm):
	class Meta:
		model = Enlightened
		fields = ('portrait', 'about')

		labels = {
			'about': 'Tell us about yourself',
			'portrait': 'Attach new profile image'
		}
