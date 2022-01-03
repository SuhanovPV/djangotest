from django.urls import path

from .views import BbCreateView, BbByRubricView, BbView, BbDetailView, BbAddView, BbUpdateView, BbDeleteView, \
    BbIndexView, BbByYear, BbByMonth, BbByDay

urlpatterns = [
    path("<int:year>/<int:month>/<int:day>", BbByDay.as_view(), name='by_day'),
    path("<int:year>/<int:month>", BbByMonth.as_view(), name='by_month'),
    path("<int:year>/<int:month>", BbByMonth.as_view(), name='by_month'),
    path("<int:year>/", BbByYear.as_view(), name='by_year'),
    path("delete/<int:pk>/", BbDeleteView.as_view(), name='delete'),
    path("detail/<int:pk>/", BbDetailView.as_view(), name='detail'),
    path("update/<int:pk>/", BbUpdateView.as_view(), name='update'),
    path("add/", BbAddView.as_view(), name='add'),
    path("rubric/<int:rubric_id>/", BbByRubricView.as_view(), name='by_rubric'),
    path("", BbIndexView.as_view(), name='index'),
]
