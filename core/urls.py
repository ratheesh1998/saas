from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('project/create/', views.create_project, name='create_project'),
    path('project/<int:project_id>/', views.project_view, name='project_view'),
]

