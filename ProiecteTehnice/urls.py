from django.urls import path
from ProiecteTehnice import views

app_name = 'PTH'

urlpatterns = [
    path('', views.index_PTH, name='index'),
]
