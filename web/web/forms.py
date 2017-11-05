from django import forms


class EditorForm(forms.Form):
    source_content = forms.CharField(
        required=False,
        widget=forms.Textarea())
    results_content = forms.CharField(
        required=False,
        widget=forms.Textarea())
