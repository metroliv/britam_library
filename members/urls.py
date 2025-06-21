from django.urls import path
from . import views

urlpatterns = [
    path('', views.member_dashboard, name='member_home'),  # 👈 new root for /members/
    path('dashboard/', views.member_dashboard, name='member_dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('register/', views.register_view, name='register'),
    path('profile/<int:user_id>/', views.member_profile_view, name='member_profile_view'),
    path('export/', views.export_members_csv, name='export_members_csv'),
    
    path('edit/<int:user_id>/', views.edit_member_profile, name='edit_member_profile'),

]
