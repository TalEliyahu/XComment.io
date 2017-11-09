from django.shortcuts import render
from django.views import View

from web.forms import EditorForm

from web.comments_remover import (
    Language, remove_comments_from_string, getListOfLangs)


class WebView(View):
    template_name = "base.html"
    form = EditorForm()
    default_mode = 'htmlmixed'
    default_language = 'JavaScript'

    def get_code_mirror_mode(self, language):
        renamed = {
            'c': 'clike',
            'html': 'javascript',
            'actionscript': self.default_mode,
            'applescript': self.default_mode,
            'bash': self.default_mode,
            'csharp': self.default_mode
        }
        mode = language.lower()
        return renamed[mode] if mode in renamed.keys() else mode

    def get_context(self):
        language = self.default_language
        results_content = ''
        if self.form.is_valid():
            language = self.form.cleaned_data.get('language')
            lang = Language.get_from_string(language)

            source_content = self.form.cleaned_data.get('source_content')
            results_content = (
                remove_comments_from_string(
                    source_content.replace('\r\n', '\n'),
                    lang) if source_content else source_content)

            self.form = EditorForm({
                'source_content': source_content,
                'results_content': results_content,
                'language' : language})

        context = {
            'form': self.form,
            'mode': self.get_code_mirror_mode(language)
        }
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        self.form = EditorForm(request.POST)
        context = self.get_context()
        response = render(request, self.template_name, context)
        response['X-XSS-Protection'] = 0 
        return response
