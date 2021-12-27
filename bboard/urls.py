from django.urls import path
# from .views import index, by_rubric, BbCreateView
from .views import index, by_rubric, add, add_save

urlpatterns = [
    path("add/save/", add_save, name='add_save'),
    path("add/", add, name='add'),
    #path("add/", BbCreateView.as_view(), name='add'),
    path("<int:rubric_id>/", by_rubric, name='by_rubric'),
    path("", index, name='index'),
]
