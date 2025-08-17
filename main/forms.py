from django import forms
from .models import ContactMessage, GalleryImage, GalleryCategory

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
