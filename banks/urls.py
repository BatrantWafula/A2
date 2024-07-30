from django.urls import path
from . import views

urlpatterns = [
    path('', views.banks_list, name='banks_list'),
    path('add/', views.add_bank, name='add_bank'),
    path('<int:bank_id>/', views.bank_details, name='bank_details'),
    path('<int:bank_id>/add_branch/', views.add_branch, name='add_branch'),
    path('branch/<int:branch_id>/', views.branch_details, name='branch_details'),
    path('branch/<int:branch_id>/edit/', views.edit_branch, name='edit_branch'),
]
