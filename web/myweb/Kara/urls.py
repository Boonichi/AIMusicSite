from django.urls import path

from .views import ( seaching_view, waiting_view,result_view,API_JSON)


app_name='Kara'

urlpatterns = [
    path('',seaching_view.as_view(),name='search'),
    path('waiting/',waiting_view.as_view(),name='waiting'),
    path('result/',result_view.as_view(),name='result'),
    path('api/getjson/',API_JSON.as_view())
]