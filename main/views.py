from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from .models import Program, GalleryImage, GalleryCategory, TeamMember, Event, ContactMessage, MemberProfile, EventAttendance, ProgramParticipation
from .forms import ContactForm, MemberRegistrationForm, MemberProfileForm

# Create your views here.
def home(request):
    """View for homepage"""
    programs = Program.objects.filter(is_active=True)[:3]
    team_members = TeamMember.objects.filter(is_active=True)[:4]
    # Order events by date to show upcoming events first
    events = Event.objects.filter(is_active=True).order_by('date')[:3]
    gallery_images = GalleryImage.objects.select_related('category').all()[:6]
    
    # Get enrolled program IDs if user is logged in
    enrolled_program_ids = []
    if request.user.is_authenticated:
        try:
            profile = MemberProfile.objects.get(user=request.user)
            enrolled_program_ids = list(ProgramParticipation.objects.filter(member=profile).values_list('program_id', flat=True))
        except MemberProfile.DoesNotExist:
            pass
    
    context = {
        'programs': programs,
        'team_members': team_members,
        'events': events,
        'gallery_images': gallery_images,
        'enrolled_program_ids': enrolled_program_ids,
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
    
    # Get enrolled program IDs if user is logged in
    enrolled_program_ids = []
    if request.user.is_authenticated:
        try:
            profile = MemberProfile.objects.get(user=request.user)
            enrolled_program_ids = list(ProgramParticipation.objects.filter(member=profile).values_list('program_id', flat=True))
        except MemberProfile.DoesNotExist:
            pass
    
    context = {
        'programs': programs,
        'enrolled_program_ids': enrolled_program_ids,
    }
    return render(request, 'main/programs.html', context)

def program_detail(request, slug):
    """View for individual program details"""
    program = get_object_or_404(Program, slug=slug, is_active=True)
    # Get related programs, ordered by newest first
    related_programs = Program.objects.filter(is_active=True).exclude(id=program.id).order_by('-created_at')[:3]
    
    context = {
        'program': program,
        'related_programs': related_programs,
    }
    return render(request, 'main/program_detail.html', context)

def gallery(request):
    """View for gallery page"""
    categories = GalleryCategory.objects.all()
    selected_category = request.GET.get('category')
    
    # Use select_related to optimize database queries
    if selected_category:
        images = GalleryImage.objects.select_related('category').filter(category__name=selected_category)
    else:
        images = GalleryImage.objects.select_related('category').all()
        
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


# ========================
# MEMBER PORTAL VIEWS
# ========================

def member_register(request):
    """Registration view for new members"""
    if request.user.is_authenticated:
        return redirect('member_dashboard')
    
    if request.method == 'POST':
        form = MemberRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to Shanti Yuwa Club! Your account has been created successfully.')
            return redirect('member_dashboard')
    else:
        form = MemberRegistrationForm()
    
    return render(request, 'members/register.html', {'form': form})


def member_login(request):
    """Login view for members"""
    if request.user.is_authenticated:
        return redirect('member_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            next_url = request.GET.get('next', 'member_dashboard')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'members/login.html')


def member_logout(request):
    """Logout view for members"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')


@login_required(login_url='member_login')
def member_dashboard(request):
    """Dashboard view for logged-in members"""
    # Get or create member profile
    profile, created = MemberProfile.objects.get_or_create(user=request.user)
    
    # Get upcoming events the member registered for
    upcoming_registrations = EventAttendance.objects.filter(
        member=profile,
        event__date__gte=timezone.now()
    ).select_related('event').order_by('event__date')[:5]
    
    # Get active program participations
    active_programs = ProgramParticipation.objects.filter(
        member=profile,
        status='active'
    ).select_related('program')[:5]
    
    # Get recent activity (last 5 attended events)
    recent_events = EventAttendance.objects.filter(
        member=profile,
        status='attended'
    ).select_related('event').order_by('-event__date')[:5]
    
    # Stats
    stats = {
        'total_events': profile.total_events_attended,
        'total_programs': profile.total_programs_participated,
        'upcoming_events': upcoming_registrations.count(),
        'active_programs': active_programs.count(),
    }
    
    context = {
        'profile': profile,
        'upcoming_registrations': upcoming_registrations,
        'active_programs': active_programs,
        'recent_events': recent_events,
        'stats': stats,
    }
    return render(request, 'members/dashboard.html', context)


@login_required(login_url='member_login')
def member_profile(request):
    """Profile edit view for members"""
    profile, created = MemberProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = MemberProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('member_profile')
    else:
        form = MemberProfileForm(instance=profile)
    
    return render(request, 'members/profile.html', {'form': form, 'profile': profile})


@login_required(login_url='member_login')
def member_events(request):
    """View all events and member's registrations"""
    profile = get_object_or_404(MemberProfile, user=request.user)
    
    # Get all upcoming events
    upcoming_events = Event.objects.filter(is_active=True, date__gte=timezone.now()).order_by('date')
    
    # Get member's registered event IDs
    registered_event_ids = EventAttendance.objects.filter(member=profile).values_list('event_id', flat=True)
    
    # Get member's event history
    event_history = EventAttendance.objects.filter(member=profile).select_related('event').order_by('-event__date')
    
    context = {
        'upcoming_events': upcoming_events,
        'registered_event_ids': list(registered_event_ids),
        'event_history': event_history,
    }
    return render(request, 'members/events.html', context)


@login_required(login_url='member_login')
def register_for_event(request, event_id):
    """Register member for an event"""
    event = get_object_or_404(Event, id=event_id, is_active=True)
    profile = get_object_or_404(MemberProfile, user=request.user)
    
    # Check if already registered
    attendance, created = EventAttendance.objects.get_or_create(
        member=profile,
        event=event,
        defaults={'status': 'registered'}
    )
    
    if created:
        messages.success(request, f'You have successfully registered for "{event.title}"!')
    else:
        messages.info(request, f'You are already registered for "{event.title}".')
    
    return redirect('member_events')


@login_required(login_url='member_login')
def cancel_event_registration(request, event_id):
    """Cancel member's registration for an event"""
    profile = get_object_or_404(MemberProfile, user=request.user)
    
    try:
        attendance = EventAttendance.objects.get(member=profile, event_id=event_id)
        attendance.status = 'cancelled'
        attendance.save()
        messages.success(request, 'Your registration has been cancelled.')
    except EventAttendance.DoesNotExist:
        messages.error(request, 'Registration not found.')
    
    return redirect('member_events')


@login_required(login_url='member_login')
def member_programs(request):
    """View all programs and member's participations"""
    profile = get_object_or_404(MemberProfile, user=request.user)
    
    # Get all active programs
    all_programs = Program.objects.filter(is_active=True)
    
    # Get member's enrolled program IDs
    enrolled_program_ids = ProgramParticipation.objects.filter(member=profile).values_list('program_id', flat=True)
    
    # Get member's program history
    program_history = ProgramParticipation.objects.filter(member=profile).select_related('program').order_by('-enrolled_at')
    
    context = {
        'all_programs': all_programs,
        'enrolled_program_ids': list(enrolled_program_ids),
        'program_history': program_history,
    }
    return render(request, 'members/programs.html', context)


@login_required(login_url='member_login')
def enroll_in_program(request, program_id):
    """Enroll member in a program"""
    program = get_object_or_404(Program, id=program_id, is_active=True)
    profile = get_object_or_404(MemberProfile, user=request.user)
    
    # Check if already enrolled
    participation, created = ProgramParticipation.objects.get_or_create(
        member=profile,
        program=program,
        defaults={'status': 'active', 'role': 'participant'}
    )
    
    if created:
        messages.success(request, f'You have successfully enrolled in "{program.title}"!')
    else:
        messages.info(request, f'You are already enrolled in "{program.title}".')
    
    return redirect('member_programs')

