from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
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


class BbByRubricView(TemplateView):
    template_name = 'bboard/by_rubric.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bbs'] = Bb.objects.filter(rubric=context['rubric_id'])
        context['rubrics'] = Rubric.objects.annotate(Count('bb'))
        context['current_rubric'] = Rubric.objects.get(pk=context['rubric_id'])
        return context


class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
