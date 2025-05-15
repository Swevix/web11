from django.urls import path
from .views import (
    HomeView, AboutView, CarDetailView,
    AddCarCustomView, CarCreateView,
    CarUpdateView, CarDeleteView, UploadFileView
)

app_name = 'cars'

urlpatterns = [
    path('',               HomeView.as_view(),      name='home'),
    path('about/',         AboutView.as_view(),     name='about'),
    path('<slug:car_slug>/', CarDetailView.as_view(), name='car_detail'),
    path('add-custom/',    AddCarCustomView.as_view(), name='add_car_custom'),
    path('add-model/',     CarCreateView.as_view(), name='add_car_model'),
    path('edit/<slug:car_slug>/',   CarUpdateView.as_view(), name='edit_car'),
    path('delete/<slug:car_slug>/', CarDeleteView.as_view(), name='delete_car'),
    path('upload/',        UploadFileView.as_view(), name='upload_file'),
]
