"""
OTP utilities for email verification
"""
import random
import string
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import OTPVerification


def generate_otp(length=6):
    """Generate a random OTP code"""
    return ''.join(random.choices(string.digits, k=length))


def send_otp_email(email):
    """
    Generate OTP, save to database, and send via email.
    Returns the OTP object and True if successful, or (None, False) if failed.
    """
    try:
        # Delete any existing unverified OTPs for this email
        OTPVerification.objects.filter(email=email, is_verified=False).delete()
        
        # Generate OTP
        otp_code = generate_otp()
        
        # Set expiration time (10 minutes from now)
        expires_at = timezone.now() + timedelta(minutes=10)
        
        # Save OTP to database
        otp_obj = OTPVerification.objects.create(
            email=email,
            otp=otp_code,
            expires_at=expires_at
        )
        
        # Prepare email content
        subject = "Shanti Yuwa Club - Email Verification OTP"
        context = {
            'email': email,
            'otp': otp_code,
            'expires_in_minutes': 10,
            'site_name': 'Shanti Yuwa Club'
        }
        
        # Try to render HTML email, fallback to plain text
        try:
            html_message = render_to_string('emails/otp_verification.html', context)
        except:
            html_message = None
        
        plain_message = f"""
Hello,

Your OTP for email verification is: {otp_code}

This OTP will expire in 10 minutes.

If you didn't request this, please ignore this email.

Best regards,
Shanti Yuwa Club Team
        """
        
        # Send email
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )
        
        return otp_obj, True
        
    except Exception as e:
        print(f"Error sending OTP email: {str(e)}")
        return None, False


def verify_otp(email, otp_code):
    """
    Verify the OTP code for a given email.
    Returns (True, message) if successful, or (False, error_message) if failed.
    """
    try:
        # Get the latest OTP for this email
        otp_obj = OTPVerification.objects.filter(email=email).latest('created_at')
    except OTPVerification.DoesNotExist:
        return False, "No OTP found for this email. Please request a new one."
    
    # Check if OTP is expired
    if otp_obj.is_expired():
        return False, "OTP has expired. Please request a new one."
    
    # Check if OTP is already verified
    if otp_obj.is_verified:
        return False, "This OTP has already been used."
    
    # Increment attempts
    otp_obj.attempts += 1
    otp_obj.save()
    
    # Check if too many attempts
    if otp_obj.attempts > 5:
        return False, "Too many failed attempts. Please request a new OTP."
    
    # Check OTP code
    if otp_obj.otp != str(otp_code).strip():
        return False, f"Invalid OTP. Attempts remaining: {5 - otp_obj.attempts}"
    
    # Mark as verified
    otp_obj.is_verified = True
    otp_obj.save()
    
    return True, "Email verified successfully!"


def cleanup_expired_otps():
    """Delete expired OTPs older than 1 hour"""
    expiration_time = timezone.now() - timedelta(hours=1)
    OTPVerification.objects.filter(expires_at__lt=expiration_time).delete()
