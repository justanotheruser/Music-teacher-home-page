from django import forms
from .models import Paper


class PaperForm(forms.ModelForm):
    description = forms.CharField(required=False,
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}))

    class Meta:
        model = Paper
        fields = ('__all__')
