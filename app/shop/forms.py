from django import forms

from shop.models import Rewiew


class RewiewForm(forms.ModelForm):

    class Meta:
        model = Rewiew
        fields = ('name', 'email', 'comment')
