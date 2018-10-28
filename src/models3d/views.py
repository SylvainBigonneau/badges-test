from django.contrib.auth.models import User
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .models import Model
from .forms import ModelCreateForm
from .processing import Processor


class ModelCreateView(CreateView):
    form_class = ModelCreateForm
    model = Model
    success_url = '/'

    def form_valid(self, form):
        model = form.save(commit=False)
        model.user = User.objects.get(pk=self.request.user.pk)
        model.save()

        processor = Processor()
        processor.configure(model.file.path)
        model.weight = processor.weigh()
        model.vertice_count = processor.count_vertices()
        model.save()

        return super(ModelCreateView, self).form_valid(form)


class ModelListView(ListView):
    queryset = Model.objects.all()


class ModelsView(View):
    def post(self, request, *args, **kwargs):
        return ModelCreateView.as_view()(request)

    def get(self, request, *args, **kwargs):
        return ModelListView.as_view()(request)


class ModelDetailView(DetailView):
    queryset = Model.objects.all()
    slug_field = 'name'
    slug_url_kwarg = 'name'

    def get_context_data(self, **kwargs):
        context = super(ModelDetailView, self).get_context_data(**kwargs)
        model = context['object']
        model.views += 1
        model.save(update_fields=['views'])

        return context