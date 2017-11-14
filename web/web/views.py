import sys

from django.conf import settings
from django.shortcuts import render
from django.views import View

sys.path.insert(0, settings.PROJECT_DIR)
from comments_remover import (
    Language, remove_comments_from_string, getListOfLangs,
    find_comments_from_string)

from web.forms import EditorForm


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

    def get_context(self, action='remove'):
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
                if action == 'highlight':
                    results_content = source_content
                    highlight_content = find_comments_from_string(
                        processed_source_content, lang)
                else:
                    results_content = (
                        remove_comments_from_string(
                            processed_source_content, lang)
                    )
            else:
                results_content = source_content

            self.form = EditorForm({
                'source_content': source_content,
                'results_content': results_content,
                'language' : language})

        context = {
            'form': self.form,
            'mode': self.get_code_mirror_mode(language),
            'results_content': results_content,
            'highlight_content': highlight_content
        }
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        action = None
        if 'highlight' in request.POST:
            action = 'highlight'
        else:
            action = 'remove'

        self.form = EditorForm(request.POST)
        context = self.get_context(action=action)
        response = render(request, self.template_name, context)
        response['X-XSS-Protection'] = 0 
        return response
