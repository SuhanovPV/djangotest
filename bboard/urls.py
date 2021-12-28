from django.urls import path
# from .views import index, by_rubric, BbCreateView
from .views import index, by_rubric, add_save

urlpatterns = [
    path("add/", add_save, name='add'),
    #path("add/", BbCreateView.as_view(), name='add'),
    path("<int:rubric_id>/", by_rubric, name='by_rubric'),
    path("", index, name='index'),
]
