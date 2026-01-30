from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import messages
from django.utils.html import format_html
from django.db.models import Count
from django.utils import timezone
from .models import Program, GalleryCategory, GalleryImage, TeamMember, Event, ContactMessage, MemberProfile, EventAttendance, ProgramParticipation, OTPVerification
from .forms import MultipleImageUploadForm
from .admin_dashboard import DashboardStats

# Customize the default admin site
admin.site.site_header = "Shanti Yuwa Club Administration"
admin.site.site_title = "Shanti Yuwa Club Admin"
admin.site.index_title = "Welcome to Shanti Yuwa Club Admin Portal"

# Override the index view to include dashboard stats
_original_index = admin.site.index

def custom_index(request, extra_context=None):
    extra_context = extra_context or {}
    extra_context['stats'] = DashboardStats.get_stats()
    extra_context['recent'] = DashboardStats.get_recent_activity()
    extra_context['engagement'] = DashboardStats.get_member_engagement()
    extra_context['program_stats'] = DashboardStats.get_program_stats()
    admin.site.index_template = 'admin/custom/dashboard.html'
    return _original_index(request, extra_context)

admin.site.index = custom_index

# Register your models here.
@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'image_preview', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'short_description', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'image_preview')
    list_editable = ('is_active',)
    list_per_page = 20
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'short_description', 'is_active')
        }),
        ('Content', {
            'fields': ('content',),
            'classes': ('wide',),
        }),
        ('Media', {
            'fields': ('image', 'image_preview'),
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 150px; border-radius: 8px;" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Preview"
    
    actions = ['activate_programs', 'deactivate_programs']
    
    def activate_programs(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} program(s) successfully activated.', messages.SUCCESS)
    activate_programs.short_description = "Activate selected programs"
    
    def deactivate_programs(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} program(s) successfully deactivated.', messages.SUCCESS)
    deactivate_programs.short_description = "Deactivate selected programs"


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_count', 'get_latest_image')
    search_fields = ('name',)
    
    def image_count(self, obj):
        count = obj.galleryimage_set.count()
        return format_html('<span style="font-weight: bold; color: #007bff;">{}</span>', count)
    image_count.short_description = "Total Images"
    
    def get_latest_image(self, obj):
        latest = obj.galleryimage_set.first()
        if latest and latest.image:
            return format_html('<img src="{}" style="max-height: 60px; max-width: 80px; border-radius: 4px;" />', latest.image.url)
        return "No Images"
    get_latest_image.short_description = "Latest Image"


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'image_thumbnail', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('image_preview', 'created_at')
    list_per_page = 20
    date_hierarchy = 'created_at'
    change_list_template = 'admin/gallery_image_changelist.html'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'category', 'description')
        }),
        ('Image', {
            'fields': ('image', 'image_preview'),
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 60px; max-width: 80px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />', obj.image.url)
        return "No Image"
    image_thumbnail.short_description = "Thumbnail"
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 300px; max-width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Full Preview"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload/', self.admin_site.admin_view(self.upload_view), name='gallery-direct-upload'),
        ]
        return custom_urls + urls
    
    def upload_view(self, request):
        if request.method == 'POST':
            form = MultipleImageUploadForm(request.POST, request.FILES)
            if form.is_valid():
                files = request.FILES.getlist('images')
                category = form.cleaned_data['category']
                for file in files:
                    GalleryImage.objects.create(
                        title=file.name.split('.')[0],
                        category=category,
                        image=file,
                    )
                self.message_user(request, f'{len(files)} image(s) uploaded successfully.', messages.SUCCESS)
                return redirect('..')
        else:
            form = MultipleImageUploadForm()
        
        return render(request, 'admin/gallery_direct_upload.html', {
            'form': form,
            'title': 'Upload Gallery Images',
            'opts': self.model._meta,
            'has_add_permission': True,
            'has_permission': True,
        })



@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'image_thumbnail', 'is_active', 'display_order', 'social_links')
    list_filter = ('is_active', 'position')
    search_fields = ('name', 'position', 'bio')
    list_editable = ('is_active', 'display_order')
    readonly_fields = ('image_preview',)
    list_per_page = 20
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'position', 'bio', 'is_active', 'display_order')
        }),
        ('Image', {
            'fields': ('image', 'image_preview'),
        }),
        ('Social Media', {
            'fields': ('facebook', 'instagram', 'twitter'),
            'classes': ('collapse',),
        }),
    )
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 60px; max-width: 60px; border-radius: 50%; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />', obj.image.url)
        return "No Image"
    image_thumbnail.short_description = "Photo"
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 200px; max-width: 200px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Full Preview"
    
    def social_links(self, obj):
        links = []
        if obj.facebook:
            links.append('<i class="fab fa-facebook" style="color: #1877f2;"></i>')
        if obj.instagram:
            links.append('<i class="fab fa-instagram" style="color: #e4405f;"></i>')
        if obj.twitter:
            links.append('<i class="fab fa-twitter" style="color: #1da1f2;"></i>')
        return format_html(' '.join(links)) if links else "—"
    social_links.short_description = "Social Media"
    
    actions = ['activate_members', 'deactivate_members']
    
    def activate_members(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} team member(s) successfully activated.', messages.SUCCESS)
    activate_members.short_description = "Activate selected members"
    
    def deactivate_members(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} team member(s) successfully deactivated.', messages.SUCCESS)
    deactivate_members.short_description = "Deactivate selected members"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'image_thumbnail', 'is_active', 'days_until_event')
    list_filter = ('is_active', 'date')
    search_fields = ('title', 'location', 'description')
    readonly_fields = ('created_at', 'image_preview')
    list_editable = ('is_active',)
    list_per_page = 20
    date_hierarchy = 'date'
    
    fieldsets = (
        ('Event Information', {
            'fields': ('title', 'date', 'location', 'is_active')
        }),
        ('Description', {
            'fields': ('description',),
            'classes': ('wide',),
        }),
        ('Image', {
            'fields': ('image', 'image_preview'),
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 60px; max-width: 80px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);" />', obj.image.url)
        return "No Image"
    image_thumbnail.short_description = "Thumbnail"
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 300px; max-width: 100%; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Full Preview"
    
    def days_until_event(self, obj):
        today = timezone.now()
        delta = (obj.date - today).days
        if delta < 0:
            return format_html('<span style="color: #dc3545;">Past Event</span>')
        elif delta == 0:
            return format_html('<span style="color: #28a745; font-weight: bold;">Today!</span>')
        elif delta <= 7:
            return format_html('<span style="color: #ffc107; font-weight: bold;">In {} days</span>', delta)
        else:
            return format_html('<span style="color: #007bff;">In {} days</span>', delta)
    days_until_event.short_description = "Status"
    
    actions = ['activate_events', 'deactivate_events']
    
    def activate_events(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} event(s) successfully activated.', messages.SUCCESS)
    activate_events.short_description = "Activate selected events"
    
    def deactivate_events(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} event(s) successfully deactivated.', messages.SUCCESS)
    deactivate_events.short_description = "Deactivate selected events"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'read_status', 'message_preview')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at', 'formatted_message')
    list_per_page = 30
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Sender Information', {
            'fields': ('name', 'email', 'created_at')
        }),
        ('Message Details', {
            'fields': ('subject', 'formatted_message', 'is_read'),
            'classes': ('wide',),
        }),
    )
    
    def read_status(self, obj):
        if obj.is_read:
            return format_html('<span style="color: #28a745;">✓ Read</span>')
        return format_html('<span style="color: #dc3545; font-weight: bold;">✉ Unread</span>')
    read_status.short_description = "Status"
    
    def message_preview(self, obj):
        preview = obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
        return format_html('<span style="color: #6c757d; font-style: italic;">{}</span>', preview)
    message_preview.short_description = "Preview"
    
    def formatted_message(self, obj):
        return format_html('<div style="background: #f8f9fa; padding: 15px; border-radius: 4px; white-space: pre-wrap;">{}</div>', obj.message)
    formatted_message.short_description = "Full Message"
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f'{updated} message(s) marked as read.', messages.SUCCESS)
    mark_as_read.short_description = "Mark as read"
    
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f'{updated} message(s) marked as unread.', messages.SUCCESS)
    mark_as_unread.short_description = "Mark as unread"


# Member Management Admin
@admin.register(MemberProfile)
class MemberProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_full_name', 'phone', 'member_since', 'membership_type', 'is_verified')
    list_filter = ('membership_type', 'is_verified', 'joined_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'user__email', 'phone')
    readonly_fields = ('user', 'member_since', 'joined_date')
    list_editable = ('is_verified',)
    list_per_page = 25
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'member_since')
        }),
        ('Profile Details', {
            'fields': ('phone', 'address', 'date_of_birth', 'bio', 'profile_picture', 'blood_group')
        }),
        ('Membership', {
            'fields': ('membership_type', 'is_verified')
        }),
    )
    
    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = "Full Name"
    
    def member_since(self, obj):
        return obj.user.date_joined.strftime('%b %d, %Y')
    member_since.short_description = "Member Since"


@admin.register(EventAttendance)
class EventAttendanceAdmin(admin.ModelAdmin):
    list_display = ('get_member_name', 'event', 'status', 'registered_at')
    list_filter = ('status', 'event', 'registered_at')
    search_fields = ('member__user__username', 'member__user__first_name', 'member__user__last_name', 'event__title')
    readonly_fields = ('registered_at',)
    list_per_page = 30
    date_hierarchy = 'registered_at'
    
    def get_member_name(self, obj):
        return obj.member.user.get_full_name() or obj.member.user.username
    get_member_name.short_description = "Member"
    
    actions = ['mark_as_attended', 'mark_as_absent']
    
    def mark_as_attended(self, request, queryset):
        updated = queryset.update(status='attended')
        self.message_user(request, f'{updated} attendance(s) marked as attended.', messages.SUCCESS)
    mark_as_attended.short_description = "Mark as attended"
    
    def mark_as_absent(self, request, queryset):
        updated = queryset.update(status='absent')
        self.message_user(request, f'{updated} attendance(s) marked as absent.', messages.SUCCESS)
    mark_as_absent.short_description = "Mark as absent"


@admin.register(ProgramParticipation)
class ProgramParticipationAdmin(admin.ModelAdmin):
    list_display = ('get_member_name', 'program', 'role', 'status', 'enrolled_at', 'certificate_issued')
    list_filter = ('status', 'role', 'program', 'certificate_issued', 'enrolled_at')
    search_fields = ('member__user__username', 'member__user__first_name', 'member__user__last_name', 'program__title')
    readonly_fields = ('enrolled_at',)
    list_editable = ('role', 'status')
    list_per_page = 30
    date_hierarchy = 'enrolled_at'
    
    fieldsets = (
        ('Program & Member', {
            'fields': ('program', 'member')
        }),
        ('Participation', {
            'fields': ('role', 'status', 'certificate_issued', 'enrolled_at')
        }),
    )
    
    def get_member_name(self, obj):
        return obj.member.user.get_full_name() or obj.member.user.username
    get_member_name.short_description = "Member"
    
    actions = ['mark_as_completed', 'mark_as_active', 'issue_certificates']
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} participation(s) marked as completed.', messages.SUCCESS)
    mark_as_completed.short_description = "Mark as completed"
    
    def mark_as_active(self, request, queryset):
        updated = queryset.update(status='active')
        self.message_user(request, f'{updated} participation(s) marked as active.', messages.SUCCESS)
    mark_as_active.short_description = "Mark as active"
    
    def issue_certificates(self, request, queryset):
        updated = queryset.filter(status='completed').update(certificate_issued=True)
        self.message_user(request, f'{updated} certificate(s) issued.', messages.SUCCESS)
    issue_certificates.short_description = "Issue certificates to completed participants"

@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ('email', 'otp', 'created_at', 'expires_at', 'is_verified', 'attempts', 'status_badge')
    list_filter = ('is_verified', 'created_at', 'expires_at')
    search_fields = ('email',)
    readonly_fields = ('otp', 'created_at', 'expires_at')
    list_per_page = 50
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('OTP Details', {
            'fields': ('email', 'otp', 'is_verified')
        }),
        ('Timing', {
            'fields': ('created_at', 'expires_at'),
        }),
        ('Verification', {
            'fields': ('attempts',),
        }),
    )
    
    def status_badge(self, obj):
        if obj.is_expired():
            return format_html('<span style="background-color: #dc3545; color: white; padding: 4px 8px; border-radius: 4px;">Expired</span>')
        elif obj.is_verified:
            return format_html('<span style="background-color: #28a745; color: white; padding: 4px 8px; border-radius: 4px;">✓ Verified</span>')
        else:
            return format_html('<span style="background-color: #ffc107; color: black; padding: 4px 8px; border-radius: 4px;">Pending</span>')
    status_badge.short_description = "Status"
    
    actions = ['mark_as_verified']
    
    def mark_as_verified(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} OTP(s) marked as verified.', messages.SUCCESS)
    mark_as_verified.short_description = "Mark as verified"