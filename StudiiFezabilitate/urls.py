from django.urls import path
from StudiiFezabilitate import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>', views.view_lucrare, name='view_lucrare'),
    path('add/', views.add, name='add_lucrare'),
    path('edit/<int:id>/', views.edit, name='edit_lucrare'),
    path('delete/<int:id>/', views.delete, name='delete_lucrare'),
    # CU
    path('lucrare/<int:id>/index_CU/', views.index_CU, name='index_CU'),
    path('lucrare/<int:id>/add_CU/', views.add_CU, name='add_CU'),
    path('lucrare/<int:id>/edit_CU/', views.edit_CU, name='edit_CU'),
    path('lucrare/<int:id>/index_CU/add_avize/',
         views.add_Avize, name='add_Avize'),
    path('lucrare/<int:lucrare_id>/index_CU/edit_aviz/<int:id>/',
         views.edit_Aviz, name='edit_aviz'),
    path('lucrare/<int:lucrare_id>/index_CU/delete_aviz/<int:id_aviz>/',
         views.delete_aviz, name='delete_aviz'),
]
