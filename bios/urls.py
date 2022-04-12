# paths to different pages
from django.urls import path

from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    path('<str:name>', views.index, name='index'),
    path('<str:name>/edit/', views.edit, name='edit'),
    path('', views.home, name='home'),
    path('create/', views.create, name='create'),
    path('test/', views.test, name='test'),
    path('upload_img/', views.upload_img, name='upload_img'),
    path('talent_dashboard/', views.dashboard, name='dashboard'),
]

# handler404 = 'bios.views.error_404'

