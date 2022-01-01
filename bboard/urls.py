from django.urls import path

from .views import BbCreateView, BbByRubricView, BbView, BbDetailView, BbAddView, BbUpdateView, BbDeleteView

urlpatterns = [
    path("delete/<int:pk>/", BbDeleteView.as_view(), name='delete'),
    path("detail/<int:pk>/", BbDetailView.as_view(), name='detail'),
    path("update/<int:pk>/", BbUpdateView.as_view(), name='update'),
    path("add/", BbAddView.as_view(), name='add'),
    path("<int:rubric_id>/", BbByRubricView.as_view(), name='by_rubric'),
    path("", BbView.as_view(), name='index'),
]
