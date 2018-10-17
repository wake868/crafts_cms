from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

from cms.models import Media


class MediaCreateView(CreateView):
    model = Media
    fields = ['upload', ]
    success_url = reverse_lazy('cms:media_index')
    template_name = 'cms/media_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        media = Media.objects.all()
        context['media'] = media
        return context
