from django.urls import path

from .views import BbCreateView, BbByRubricView, BbView, BbDetailView, BbAddView

urlpatterns = [
    path("detail/<int:pk>/", BbCreateView.as_view(), name='detail'),
    path("add/", BbAddView.as_view(), name='add'),
    path("<int:rubric_id>/", BbByRubricView.as_view(), name='by_rubric'),
    path("", BbView.as_view(), name='index'),
]
