import sys

from django.conf import settings
from django.shortcuts import render
from django.views import View

from web.forms import EditorForm, LANGUAGE_CHOICES

sys.path.insert(0, settings.PROJECT_DIR)
from comments_remover import (
    Language, remove_comments_from_string,
    find_comments_from_string)  # noqa


class WebView(View):
    template_name = "base.html"
    form = EditorForm()
    default_mode = 'htmlmixed'
    default_language = 'JavaScript'

    def processed_language_choices(self, choices=None):
        choices = choices or LANGUAGE_CHOICES
        choices_dict = dict((k, v) for k, v in choices)
        renamed = {
            'assembly': 'z80',
            'c': 'clike',
            'html': 'htmlmixed',
            'actionscript': 'javascript',
            'applescript': 'shell',
            'bash': 'shell',
            'csharp': 'clike'
        }
        choices_dict.update(renamed)
        return choices_dict

    def get_code_mirror_mode(self, language):
        mode = language.lower()
        modes = self.processed_language_choices()
        return modes[mode] if mode in modes.keys() else mode

    def get_context(self):
        language = self.default_language
        results_content = ''
        highlight_content = []

        if self.form.is_valid():
            language = self.form.cleaned_data.get('language')
            lang = Language.get_from_string(language)

            source_content = self.form.cleaned_data.get('source_content')

            processed_source_content = (
                source_content.replace('\r\n', '\n')
                if source_content else source_content
            )

            if processed_source_content:
                highlight_content = find_comments_from_string(
                    processed_source_content, lang)
                results_content = (
                    remove_comments_from_string(
                        processed_source_content, lang)
                )
            else:
                results_content = source_content

            self.form = EditorForm({
                'source_content': source_content,
                'results_content': results_content,
                'language': language})

        context = {
            'form': self.form,
            'mode': self.get_code_mirror_mode(language),
            'results_content': results_content,
            'highlight_content': highlight_content,
            'language_choices':  self.processed_language_choices(LANGUAGE_CHOICES)
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
