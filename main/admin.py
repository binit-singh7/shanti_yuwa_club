from django.contrib import admin
from django.shortcuts import render, redirect
from django.urls import path
from django.contrib import messages
from .models import Program, GalleryCategory, GalleryImage, TeamMember, Event, ContactMessage
from .forms import MultipleImageUploadForm

# Register your models here.
@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'short_description')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')
    change_list_template = 'admin/gallery_image_changelist.html'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-multiple/', self.admin_site.admin_view(self.upload_multiple_view), name='gallery-upload-multiple'),
            path('direct-upload/', self.admin_site.admin_view(self.direct_upload_view), name='gallery-direct-upload'),
        ]
        return custom_urls + urls
    
    def upload_multiple_view(self, request):
        if request.method == 'POST':
            form = MultipleImageUploadForm(request.POST)
            if form.is_valid():
                category = form.cleaned_data['category']
                title_prefix = form.cleaned_data['title_prefix']
                description = form.cleaned_data['description']
                
                # Debug information
                has_files = 'images' in request.FILES
                images = request.FILES.getlist('images')
                file_count = len(images) if has_files else 0
                
                if not has_files or file_count == 0:
                    messages.error(request, f"No images selected for upload. Request contains files: {has_files}, File count: {file_count}")
                    return render(request, 'admin/gallery_upload_multiple.html', {
                        'form': form,
                        'title': 'Upload Multiple Images',
                        'site_title': 'Shanti Yuwa Club Admin',
                        'site_header': 'Shanti Yuwa Club Administration',
                        'has_permission': True,
                        'opts': self.model._meta,
                    })
                
                # Process multiple images
                counter = 0
                for image in images:
                    counter += 1
                    gallery_image = GalleryImage(
                        title=f"{title_prefix}_{counter}",
                        category=category,
                        image=image,
                        description=description
                    )
                    gallery_image.save()
                
                messages.success(request, f"Successfully uploaded {counter} images to the '{category}' category.")
                return redirect('admin:main_galleryimage_changelist')
        else:
            form = MultipleImageUploadForm()
        
        return render(request, 'admin/gallery_upload_multiple.html', {
            'form': form,
            'title': 'Upload Multiple Images',
            'site_title': 'Shanti Yuwa Club Admin',
            'site_header': 'Shanti Yuwa Club Administration',
            'has_permission': True,
            'opts': self.model._meta,
        })

    def direct_upload_view(self, request):
        if request.method == 'POST':
            form = MultipleImageUploadForm(request.POST)
            if form.is_valid():
                category = form.cleaned_data['category']
                title_prefix = form.cleaned_data['title_prefix']
                description = form.cleaned_data['description']
                
                # Debug information
                has_files = 'images' in request.FILES
                images = request.FILES.getlist('images')
                file_count = len(images) if has_files else 0
                
                if not has_files or file_count == 0:
                    messages.error(request, f"No images selected for upload. Request contains files: {has_files}, File count: {file_count}")
                    return render(request, 'admin/gallery_direct_upload.html', {
                        'form': form,
                        'title': 'Upload Multiple Images',
                        'site_title': 'Shanti Yuwa Club Admin',
                        'site_header': 'Shanti Yuwa Club Administration',
                        'has_permission': True,
                        'opts': self.model._meta,
                    })
                
                # Process multiple images
                counter = 0
                for image in images:
                    counter += 1
                    gallery_image = GalleryImage(
                        title=f"{title_prefix}_{counter}",
                        category=category,
                        image=image,
                        description=description
                    )
                    gallery_image.save()
                
                messages.success(request, f"Successfully uploaded {counter} images to the '{category}' category.")
                return redirect('admin:main_galleryimage_changelist')
        else:
            form = MultipleImageUploadForm()
        
        return render(request, 'admin/gallery_direct_upload.html', {
            'form': form,
            'title': 'Direct Upload Multiple Images',
            'site_title': 'Shanti Yuwa Club Admin',
            'site_header': 'Shanti Yuwa Club Administration',
            'has_permission': True,
            'opts': self.model._meta,
        })

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'is_active', 'display_order')
    list_filter = ('is_active', 'position')
    search_fields = ('name', 'position', 'bio')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'is_active')
    list_filter = ('is_active', 'date')
    search_fields = ('title', 'location', 'description')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
