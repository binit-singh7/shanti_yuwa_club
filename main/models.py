from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Program(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    short_description = models.CharField(max_length=300)
    content = RichTextField()
    image = models.ImageField(upload_to='programs/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            # Handle slug collision
            while Program.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class GalleryCategory(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Gallery Categories"

class GalleryImage(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery/')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    image = models.ImageField(upload_to='team/')
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['display_order']

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    description = RichTextField()
    image = models.ImageField(upload_to='events/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-date']

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    class Meta:
        ordering = ['-created_at']


# ========================
# MEMBER PORTAL MODELS
# ========================

class MemberProfile(models.Model):
    """Extended profile for club members"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='member_profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True, help_text="Your blood group")
    
    profile_picture = models.ImageField(upload_to='members/', blank=True, null=True)
    bio = models.TextField(blank=True, help_text="Short bio about yourself")
    joined_date = models.DateField(auto_now_add=True)
    is_verified = models.BooleanField(default=False, help_text="Verified by admin")
    
    MEMBERSHIP_CHOICES = [
        ('regular', 'Regular Member'),
        ('active', 'Active Member'),
        ('executive', 'Executive Member'),
    ]
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_CHOICES, default='regular')
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}'s Profile"
    
    @property
    def total_events_attended(self):
        return self.event_attendances.filter(status='attended').count()
    
    @property
    def total_programs_participated(self):
        return self.program_participations.count()


class EventAttendance(models.Model):
    """Track member attendance at events"""
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name='event_attendances')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='attendances')
    registered_at = models.DateTimeField(auto_now_add=True)
    
    STATUS_CHOICES = [
        ('registered', 'Registered'),
        ('attended', 'Attended'),
        ('absent', 'Absent'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registered')
    notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['member', 'event']
        ordering = ['-registered_at']
    
    def __str__(self):
        return f"{self.member.user.username} - {self.event.title}"


class ProgramParticipation(models.Model):
    """Track member participation in programs"""
    member = models.ForeignKey(MemberProfile, on_delete=models.CASCADE, related_name='program_participations')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='participations')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
    ROLE_CHOICES = [
        ('participant', 'Participant'),
        ('volunteer', 'Volunteer'),
        ('coordinator', 'Coordinator'),
        ('lead', 'Program Lead'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='participant')
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('dropped', 'Dropped'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    certificate_issued = models.BooleanField(default=False)
    feedback = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['member', 'program']
        ordering = ['-enrolled_at']
    
    def __str__(self):
        return f"{self.member.user.username} - {self.program.title}"


# Signal to create MemberProfile when a new User is created
@receiver(post_save, sender=User)
def create_member_profile(sender, instance, created, **kwargs):
    """Create a MemberProfile for new users (non-staff only)"""
    if created and not instance.is_staff:
        MemberProfile.objects.create(user=instance)


# ========================
# OTP VERIFICATION MODEL
# ========================

class OTPVerification(models.Model):
    """Model to store OTP for email verification"""
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0, help_text="Number of failed verification attempts")
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email', 'is_verified']),
            models.Index(fields=['expires_at']),
        ]
    
    def __str__(self):
        return f"OTP for {self.email}"
    
    def is_expired(self):
        """Check if OTP has expired"""
        from django.utils import timezone
        return timezone.now() > self.expires_at
    
    def is_valid(self):
        """Check if OTP is still valid (not expired and not verified)"""
        return not self.is_expired() and not self.is_verified


