from django.urls import path
from .views import (
    DesignListView,
    DesignDetailView,
    DesignCreateView,
    DesignUpdateDeleteView
)

urlpatterns = [
    path('', DesignListView.as_view(), name='design-list'),
    path('<int:pk>/', DesignDetailView.as_view(), name='design-detail'),
    path('create/', DesignCreateView.as_view(), name='design-create'),
    path('<int:pk>/update/', DesignUpdateDeleteView.as_view(), name='design-update-delete'),
]
