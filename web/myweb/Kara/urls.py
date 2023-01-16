from django.urls import path

from .views import ( seaching_view, waiting_view,result_view)


app_name='Kara'

urlpatterns = [
    path('search/',seaching_view.as_view(),name='search'),
    path('waiting/',waiting_view.as_view(),name='waiting'),
    path('result/',result_view.as_view(),name='result'),
]