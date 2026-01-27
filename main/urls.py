from django.urls import path
from . import views
from . import otp_views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('programs/', views.programs, name='programs'),
    path('programs/<slug:slug>/', views.program_detail, name='program_detail'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('set-language/', views.set_language, name='set_language'),
    
    # OTP Verification
    path('send-otp/', otp_views.send_otp_view, name='send-otp'),
    path('verify-otp/', otp_views.verify_otp_view, name='verify-otp'),
    path('resend-otp/', otp_views.resend_otp_view, name='resend-otp'),
    
    # Member Portal
    path('member/register/', views.member_register, name='member_register'),
    path('register/', views.member_register, name='register'),  # Alternative URL
    path('member/login/', views.member_login, name='member_login'),
    path('member/logout/', views.member_logout, name='member_logout'),
    path('member/dashboard/', views.member_dashboard, name='member_dashboard'),
    path('member/profile/', views.member_profile, name='member_profile'),
    path('member/events/', views.member_events, name='member_events'),
    path('member/events/register/<int:event_id>/', views.register_for_event, name='register_for_event'),
    path('member/events/cancel/<int:event_id>/', views.cancel_event_registration, name='cancel_event_registration'),
    path('member/programs/', views.member_programs, name='member_programs'),
    path('member/programs/enroll/<int:program_id>/', views.enroll_in_program, name='enroll_in_program'),
]
