from django import forms

from web.comments_remover import getListOfLangs

LANGUAGE_CHOICES = [
    (each, each) for each in getListOfLangs()]


class EditorForm(forms.Form):
    source_content = forms.CharField(
        required=False,
        widget=forms.Textarea())
    results_content = forms.CharField(
        required=False,
        widget=forms.Textarea())
    language = forms.ChoiceField(
        required=False,
        initial="HTML",
        choices=LANGUAGE_CHOICES)
