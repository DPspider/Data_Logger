from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    #Student portal - Student Login URL
    path('company_login/', views.company_login, name='company_login'),
    path('company_logout/', views.company_logout, name='company_logout'),
    path('company_register/', views.company_register, name='company_register'),

    path('company_dashboard/', views.company_dashboard, name='company_dashboard'),

    path('device_report/<int:pk>',views.device_report, name='device_report'),



    #Student portal - Student Forget password URLs
    path('company_forgot_password/', views.company_forgot_password, name='company_forgot_password'),

    path('password_reset/', views.password_reset, name='password_reset'),

    path('password_reset_done/', views.password_reset_done, name='password_reset_done'),

    # 
    path('password_reset_test/<token>', views.password_reset_test, name='password_reset_test'),

    #Student portal - Student Reset password URLs
    path('password_change/', views.passwordchange, name='password_change'),

    path('password_reset_confirm/', views.password_reset_confirm, name='password_reset_confirm'),


]