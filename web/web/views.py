from django.shortcuts import render
from django.views import View

from web.forms import EditorForm

from web.comments_remover import (
    Language, remove_comments_from_string)


class WebView(View):
    template_name = "base.html"

    context = {}

    def get(self, request, *args, **kwargs):
        form = EditorForm()
        self.context['form'] = form
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        source_content= request.POST['source_content']
        language = Language.get_from_string('HTML')
        results_content = remove_comments_from_string(
            source_content, language)
        form = EditorForm({
            'source_content': source_content,
            'results_content': results_content
        })
        self.context['form'] = form
        response = render(request, self.template_name, self.context)
        response['X-XSS-Protection'] = 0 
        return response
