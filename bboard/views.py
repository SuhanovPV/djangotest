from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView, DayArchiveView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy, reverse, resolve
from django.db.models import Count
from django.http import HttpResponseRedirect

from .models import Bb, Rubric
from .forms import BbForm


class BbView(TemplateView):
    template_name = 'bboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['bbs'] = Bb.objects.all()
        context['rubrics'] = Rubric.objects.annotate(Count('bb'))
        return context


class BbIndexView(ArchiveIndexView):
    model = Bb
    date_field = 'published'
    date_list_period = 'year'
    template_name = 'bboard/index_by_archive.html'
    context_object_name = 'bbs'
    allow_empty = True

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.annotate(Count('bb'))
        return context


class BbByYear(YearArchiveView):
    model = Bb
    date_field = 'published'
    template_name = 'bboard/by_year.html'
    context_object_name = 'bbs'
    make_object_list = True
    allow_empty = True

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.annotate(Count('bb'))
        return context


class BbByMonth(MonthArchiveView):
    model = Bb
    date_field = 'published'
    template_name = 'bboard/by_month.html'
    context_object_name = 'bbs'
    allow_empty = True
    month_format = '%m'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.annotate(Count('bb'))
        return context


class BbByDay(DayArchiveView):
    model = Bb
    date_field = 'published'
    template_name = 'bboard/by_day.html'
    context_object_name = 'bbs'
    allow_empty = True
    month_format = '%m'
    day_format = '%d'

    def get_context_data(self, *args, object_list=None, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.annotate(Count('bb'))
        return context


class BbByRubricView(ListView):
    template_name = 'bboard/by_rubric.html'
    context_object_name = 'bbs'

    def get_queryset(self):
        return Bb.objects.filter(rubric=self.kwargs['rubric_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.annotate(Count('bb'))
        context['current_rubric'] = Rubric.objects.get(pk=self.kwargs['rubric_id'])
        return context


class BbDetailView(DetailView):
    model = Bb

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['rubrics'] = Rubric.objects.annotate(Count('bb'))
        return context


class BbAddView(FormView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    initial = {'price': 0.0}

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.annotate(Count('bb'))
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        self.object = super().get_form(form_class)
        return self.object

    def get_success_url(self):
        return reverse('by_rubric',
                       kwargs={'rubric_id': self.object.cleaned_data['rubric'].pk})


class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rubrics'] = Rubric.objects.annotate(Count('bb'))
        return context


class BbUpdateView(UpdateView):
    template_name = 'bboard/update.html'
    model = Bb
    form_class = BbForm
    success_url = '/bboard/detail/{id}'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.annotate(Count('bb'))
        return context


class BbDeleteView(DeleteView):
    template_name = 'bboard/delete.html'
    model = Bb
    success_url = '/bboard/{rubric_id}'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['rubrics'] = Rubric.objects.annotate(Count('bb'))
        return context


def index(request):
    bbs = Bb.objects.all()
    rubrics = Rubric.objects.annotate(Count('bb'))
    context = {'bbs': bbs, 'rubrics': rubrics}
    return render(request, 'bboard/index.html', context)


def by_rubric(request, rubric_id):
    bbs = Bb.objects.filter(rubric=rubric_id)
    rubrics = Rubric.objects.annotate(Count('bb'))
    current_rubric = Rubric.objects.get(pk=rubric_id)
    context = {'bbs': bbs, 'rubrics': rubrics, 'current_rubric': current_rubric}
    return render(request, 'bboard/by_rubric.html', context)


def add_save(request):
    rubrics = Rubric.objects.annotate(Count('bb'))
    if request.method == 'POST':
        bbf = BbForm(request.POST)
        if bbf.is_valid():
            bbf.save()
            return HttpResponseRedirect(reverse('by_rubric', kwargs={'rubric_id': bbf.cleaned_data['rubric'].pk}))
        else:
            context = {'form': bbf, 'rubrics': rubrics}
            return render(request, 'bboard/create.html', context)
    else:
        bbf = BbForm()
        context = {'form': bbf, 'rubrics': rubrics}
        return render(request, 'bboard/create.html', context)
