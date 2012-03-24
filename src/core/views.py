from django.shortcuts import render_to_response
from subscriptions.models import Subscription
from django import templatetags

def homepage(request):
	from django.conf import settings

	s = Subscription.objects.all()
	context = {
		'STATIC_URL': settings.STATIC_URL,
		'subscribers': s
	}

	return render_to_response('index.html', context)