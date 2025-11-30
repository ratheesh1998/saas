from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/', views.profile_view, name='profile'),
    path('settings/', views.settings_view, name='settings'),
    path('template/quick-create/', views.quick_create_template, name='quick_create_template'),
    path('template/<int:template_id>/view/', views.view_template, name='view_template'),
    path('template/<int:template_id>/delete/', views.delete_template, name='delete_template'),
    path('service/create/', views.create_service, name='create_service'),
    path('service/update/', views.update_service, name='update_service'),
    path('service/validate-image/', views.validate_docker_image, name='validate_docker_image'),
    path('template/<int:template_id>/services/', views.get_services, name='get_services'),
]

