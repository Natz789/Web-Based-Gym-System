from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Dashboard (role-based)
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Membership management
    path('plans/', views.membership_plans_view, name='membership_plans'),
    path('plans/subscribe/<int:plan_id>/', views.subscribe_plan, name='subscribe_plan'),
    
    # Walk-in management (staff/admin)
    path('walkin/', views.walkin_purchase, name='walkin_purchase'),
    
    # Reports & Analytics (admin)
    path('reports/', views.reports_view, name='reports'),
    
    # Member management (admin/staff)
    path('members/', views.members_list, name='members_list'),
    path('members/<int:user_id>/', views.member_detail, name='member_detail'),
]