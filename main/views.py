from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Program, GalleryImage, GalleryCategory, TeamMember, Event, ContactMessage
from .forms import ContactForm

# Create your views here.
def home(request):
    """View for homepage"""
    programs = Program.objects.filter(is_active=True)[:3]
    team_members = TeamMember.objects.filter(is_active=True)[:4]
    events = Event.objects.filter(is_active=True)[:3]
    gallery_images = GalleryImage.objects.all()[:6]
    
    context = {
        'programs': programs,
        'team_members': team_members,
        'events': events,
        'gallery_images': gallery_images,
    }
    return render(request, 'main/home.html', context)

def about(request):
    """View for about page"""
    team_members = TeamMember.objects.filter(is_active=True)
    
    context = {
        'team_members': team_members,
    }
    return render(request, 'main/about.html', context)

def programs(request):
    """View for programs listing page"""
    all_programs = Program.objects.filter(is_active=True)
    paginator = Paginator(all_programs, 6)  # Show 6 programs per page
    
    page_number = request.GET.get('page')
    programs = paginator.get_page(page_number)
    
    context = {
        'programs': programs,
    }
    return render(request, 'main/programs.html', context)

def program_detail(request, slug):
    """View for individual program details"""
    program = get_object_or_404(Program, slug=slug, is_active=True)
    related_programs = Program.objects.filter(is_active=True).exclude(id=program.id)[:3]
    
    context = {
        'program': program,
        'related_programs': related_programs,
    }
    return render(request, 'main/program_detail.html', context)

def gallery(request):
    """View for gallery page"""
    categories = GalleryCategory.objects.all()
    selected_category = request.GET.get('category')
    
    if selected_category:
        images = GalleryImage.objects.filter(category__name=selected_category)
    else:
        images = GalleryImage.objects.all()
        
    paginator = Paginator(images, 12)  # Show 12 images per page
    page_number = request.GET.get('page')
    gallery_images = paginator.get_page(page_number)
    
    context = {
        'categories': categories,
        'gallery_images': gallery_images,
        'selected_category': selected_category,
    }
    return render(request, 'main/gallery.html', context)

def contact(request):
    """View for contact page"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent. Thank you for contacting us!')
            return redirect('contact')
    else:
        form = ContactForm()
        
    context = {
        'form': form,
    }
    return render(request, 'main/contact.html', context)

def set_language(request):
    """
    View for setting the language - now always redirects to homepage
    as language switching is no longer supported
    """
    return HttpResponseRedirect(reverse('home'))
