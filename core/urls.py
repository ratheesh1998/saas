from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    # Project management
    path('project/create/', views.create_project, name='create_project'),
    path('project/<int:project_id>/', views.project_view, name='project_view'),
    # Project service API
    path('project/service/create/', views.create_project_service, name='create_project_service'),
    path('project/<int:project_id>/services/', views.get_project_services, name='get_project_services'),
    path('project/<int:project_id>/service/<str:service_id>/delete/', views.delete_project_service, name='delete_project_service'),
]

