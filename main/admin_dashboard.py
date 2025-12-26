from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import Program, GalleryImage, TeamMember, Event, ContactMessage


class DashboardStats:
    """Custom dashboard statistics for admin"""
    
    @staticmethod
    def get_stats():
        today = timezone.now()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        stats = {
            # Program Statistics
            'total_programs': Program.objects.count(),
            'active_programs': Program.objects.filter(is_active=True).count(),
            'new_programs_this_week': Program.objects.filter(created_at__gte=week_ago).count(),
            
            # Gallery Statistics
            'total_gallery_images': GalleryImage.objects.count(),
            'gallery_images_this_month': GalleryImage.objects.filter(created_at__gte=month_ago).count(),
            'images_by_category': list(
                GalleryImage.objects.values('category__name')
                .annotate(count=Count('id'))
                .order_by('-count')[:5]
            ),
            
            # Team Statistics
            'total_team_members': TeamMember.objects.count(),
            'active_team_members': TeamMember.objects.filter(is_active=True).count(),
            
            # Event Statistics
            'total_events': Event.objects.count(),
            'upcoming_events': Event.objects.filter(date__gte=today, is_active=True).count(),
            'past_events': Event.objects.filter(date__lt=today).count(),
            'events_this_month': Event.objects.filter(
                date__year=today.year,
                date__month=today.month
            ).count(),
            
            # Contact Message Statistics
            'total_messages': ContactMessage.objects.count(),
            'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
            'messages_this_week': ContactMessage.objects.filter(created_at__gte=week_ago).count(),
            'messages_this_month': ContactMessage.objects.filter(created_at__gte=month_ago).count(),
        }
        
        return stats
    
    @staticmethod
    def get_recent_activity():
        """Get recent activity across all models"""
        recent_programs = Program.objects.order_by('-created_at')[:5]
        recent_events = Event.objects.order_by('-created_at')[:5]
        recent_messages = ContactMessage.objects.order_by('-created_at')[:5]
        recent_gallery = GalleryImage.objects.order_by('-created_at')[:5]
        
        return {
            'programs': recent_programs,
            'events': recent_events,
            'messages': recent_messages,
            'gallery': recent_gallery,
        }
