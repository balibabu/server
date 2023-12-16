from django.urls import path
from . import views

urlpatterns = [
    path('',views.ExpenseListCreateView.as_view(),name='expense-list-create'),
    path('id/<int:pk>/',views.ExpenseDeleteView.as_view(),name='expense-delete'),
]
