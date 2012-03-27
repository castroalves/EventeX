# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

from subscriptions.models import Subscription
from subscriptions.validators import CpfValidator

class PhoneWidget(forms.MultiWidget):

	def __init__(self, attrs=None):
		widgets = (
			forms.TextInput(attrs=attrs),
			forms.TextInput(attrs=attrs))
		super(PhoneWidget, self).__init__(widgets, attrs)

	def decompress(self, value):
		if not value:
			return [None, None]
		return value.split('-')

class PhoneField(forms.MultiValueField):
	widget = PhoneWidget

	def __init__(self, *args, **kwargs):
		fields = (
			forms.IntegerField(),
			forms.IntegerField())
		super(PhoneField, self).__init__(fields, *args, **kwargs)

	def compress(self, data_list):
		if not data_list:
			return None
		if data_list[0] in EMPTY_VALUES:
			raise forms.ValidationError(u'DDD inválido')
		if data_list[1] in EMPTY_VALUES:
			raise forms.ValidationError(u'Número inválido')
		return '%s-%s' % tuple(data_list)

class SubscriptionForm(forms.ModelForm):

	name = forms.CharField(label=_('Nome'), max_length=100)
	cpf = forms.CharField(label=_('CPF'), max_length=11, min_length=11, validators=[CpfValidator])
	email = forms.EmailField(label=_('E-mail'))
	phone = PhoneField(label=_('Telefone'), required=False)

	class Meta:
		model = Subscription
		exclude = ('created_at', 'paid',)

	def _unique_check(self, fieldname, error_message):
		param = {fieldname: self.cleaned_data.get(fieldname)}
		try:
			s = Subscription.objects.get(**param)
		except Subscription.DoesNotExist:
			return self.cleaned_data.get(fieldname)
		raise forms.ValidationError(error_message)

	def clean_cpf(self):
		return self._unique_check('cpf', _(u'Este CPF já está inscrito.'))

	def clean_email(self):
		return self._unique_check('email', _(u'Este e-mail já está inscrito.'))

	def clean(self):
		super(SubscriptionForm, self).clean()

		if not self.cleaned_data.get('email') and not self.cleaned_data.get('phone'):
			raise forms.ValidationError(_(u'Você precisa informar seu e-mail ou seu telefone.'))
		return self.cleaned_data