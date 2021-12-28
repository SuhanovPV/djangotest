from django.urls import path

from .views import index, by_rubric, add_save, BbCreateView, BbByRubricView, BbView

urlpatterns = [
    #path("add/", add_save, name='add'),
    path("add/", BbCreateView.as_view(), name='add'),
    path("<int:rubric_id>/", BbByRubricView.as_view(), name='by_rubric'),
    path("", BbView.as_view(), name='index'),
]
