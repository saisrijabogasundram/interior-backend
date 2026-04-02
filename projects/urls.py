from django.urls import path
from .views import ProjectListView, ProjectDetailView, CostEstimationView

urlpatterns = [
    path('', ProjectListView.as_view(), name='project-list'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),
    path('estimate/', CostEstimationView.as_view(), name='cost-estimate'),
]