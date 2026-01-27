"""
Views for OTP verification
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .otp_utils import send_otp_email, verify_otp
from .models import OTPVerification


@require_http_methods(["GET", "POST"])
def send_otp_view(request):
    """
    Send OTP to the provided email address
    POST: Send OTP
    GET: Display the send OTP form
    """
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        if not email:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Email is required'})
            messages.error(request, 'Email is required')
            return redirect(request.META.get('HTTP_REFERER', 'register'))
        
        # Send OTP
        otp_obj, success = send_otp_email(email)
        
        if success:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f'OTP sent to {email}. Check your email!'
                })
            messages.success(request, f'OTP sent to {email}. Check your email!')
            # Redirect to OTP verification page
            return redirect('verify-otp')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': 'Failed to send OTP. Please try again later.'
                })
            messages.error(request, 'Failed to send OTP. Please try again later.')
            return redirect(request.META.get('HTTP_REFERER', 'register'))
    
    return render(request, 'members/send_otp.html')


@require_http_methods(["GET", "POST"])
def verify_otp_view(request):
    """
    Verify OTP code
    POST: Verify the OTP
    GET: Display the verification form
    """
    email = request.session.get('otp_email') or request.POST.get('email', '')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        otp_code = request.POST.get('otp', '').strip()
        
        if not email or not otp_code:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Email and OTP are required'})
            messages.error(request, 'Email and OTP are required')
            return render(request, 'members/verify_otp.html', {'email': email})
        
        # Verify OTP
        success, message = verify_otp(email, otp_code)
        
        if success:
            # Store verified email in session
            request.session['verified_email'] = email
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': message
                })
            
            messages.success(request, message)
            # Redirect to registration form with verified email
            return redirect('register')
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': message
                })
            messages.error(request, message)
            return render(request, 'members/verify_otp.html', {'email': email})
    
    return render(request, 'members/verify_otp.html', {'email': email})


@require_http_methods(["POST"])
def resend_otp_view(request):
    """
    Resend OTP to the provided email
    AJAX endpoint
    """
    email = request.POST.get('email', '').strip()
    
    if not email:
        return JsonResponse({'success': False, 'error': 'Email is required'})
    
    # Check if there's a recent OTP
    try:
        otp_obj = OTPVerification.objects.filter(email=email).latest('created_at')
        # Allow resend only if more than 1 minute has passed since last OTP
        from django.utils import timezone
        from datetime import timedelta
        if (timezone.now() - otp_obj.created_at).total_seconds() < 60:
            return JsonResponse({
                'success': False,
                'error': 'Please wait before requesting a new OTP'
            })
    except OTPVerification.DoesNotExist:
        pass
    
    # Send new OTP
    otp_obj, success = send_otp_email(email)
    
    if success:
        return JsonResponse({
            'success': True,
            'message': 'OTP sent successfully!'
        })
    else:
        return JsonResponse({
            'success': False,
            'error': 'Failed to send OTP. Please try again later.'
        })
