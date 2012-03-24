import urllib, hashlib
from django import template

register = template.Library()

@register.inclusion_tag('templatetags/gravatar.html')
def show_gravatar(email, size=48):
	default = "http://www.gravatar.com/avatar/00000000000000000000000000000000?d=retro"
	user_id = hashlib.md5(email).hexdigest()

	url = "http://www.gravatar.com/avatar.php?"
	url += urllib.urlencode({
		'gravatar_id': user_id,
		'default': default,
		'size': str(size)
	})

	return {
		'gravatar': {
			'url': url,
			'size': size,
			'user_id': user_id
		}
	}