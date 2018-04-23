from django.urls import path

from . import views


app_name = 'api-v1'

urlpatterns = [
    path('providers/', views.ProviderListCreateView.as_view(), name='provider-list-create'),
    path(
        'providers/<int:id>',
        views.ProviderRetrieveUpdateDestroyView.as_view(),
        name='provider-retrieve-update-destroy',
    ),
]
