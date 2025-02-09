from django.urls import path
from StudiiFezabilitate import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>', views.view_lucrare, name='view_lucrare'),
    path('add/', views.add, name='add_lucrare'),
    path('edit/<int:id>/', views.edit, name='edit_lucrare'),
    path('delete/<int:id>/', views.delete, name='delete_lucrare'),
]
