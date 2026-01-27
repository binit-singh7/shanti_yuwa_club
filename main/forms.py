from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ContactMessage, GalleryImage, GalleryCategory, MemberProfile

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your Message', 'rows': 6}),
        }

class MultipleImageUploadForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=GalleryCategory.objects.all(),
        required=True,
        label="Gallery Category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    title_prefix = forms.CharField(
        max_length=100,
        required=True,
        help_text="A prefix for all uploaded images. Each image will be named: prefix_1, prefix_2, etc.",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        required=False,
        help_text="Optional description to apply to all uploaded images"
    )


# ========================
# MEMBER PORTAL FORMS
# ========================

class MemberRegistrationForm(UserCreationForm):
    """Comprehensive registration/joining form for new members"""
    email = forms.EmailField(
        required=True,
        help_text="We'll use this to keep you updated about club activities"
    )
    first_name = forms.CharField(max_length=30, required=True, label="First Name")
    last_name = forms.CharField(max_length=30, required=True, label="Last Name")
    phone = forms.CharField(
        max_length=20,
        required=True,
        help_text="Your contact number for club communications"
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2}),
        required=False,
        help_text="Your current address (Optional)"
    )
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Your date of birth",
        label="Date of Birth"
    )
    
    BLOOD_GROUP_CHOICES = [
        ('', 'Select Blood Group'),
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
    ]
    blood_group = forms.ChoiceField(
        choices=BLOOD_GROUP_CHOICES,
        required=True,
        help_text="Your blood group",
        label="Blood Group"
    )
    
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        help_text="Tell us a bit about yourself and why you want to join (Optional)"
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Create or update member profile with additional fields
            profile, created = MemberProfile.objects.get_or_create(user=user)
            profile.phone = self.cleaned_data.get('phone', '')
            profile.address = self.cleaned_data.get('address', '')
            profile.date_of_birth = self.cleaned_data.get('date_of_birth')
            profile.blood_group = self.cleaned_data.get('blood_group', '')
            profile.bio = self.cleaned_data.get('bio', '')
            profile.save()
        return user


class MemberProfileForm(forms.ModelForm):
    """Form for updating member profile"""
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = MemberProfile
        fields = ['phone', 'address', 'date_of_birth', 'profile_picture', 'bio']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            # Update user fields
            profile.user.first_name = self.cleaned_data['first_name']
            profile.user.last_name = self.cleaned_data['last_name']
            profile.user.email = self.cleaned_data['email']
            profile.user.save()
            profile.save()
        return profile

