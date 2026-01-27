from django.db.models import Count, Q
from .models import Program, GalleryImage, TeamMember, MemberProfile, EventAttendance, ProgramParticipation, Event
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import json


class DashboardStats:
    """Dashboard statistics for admin panel"""
    
    @staticmethod
    def get_stats():
        """Get overall dashboard statistics"""
        stats = {
            'total_members': MemberProfile.objects.count(),
            'total_programs': Program.objects.count(),
            'active_programs': Program.objects.filter(is_active=True).count(),
            'total_images': GalleryImage.objects.count(),
            'total_team': TeamMember.objects.count(),
            'total_events': Event.objects.count(),
            'total_users': User.objects.count(),
        }
        # Build traffic data (new member signups) for the last 7 days
        try:
            labels = []
            data = []
            for days_back in range(6, -1, -1):
                day = timezone.now().date() - timedelta(days=days_back)
                labels.append(day.strftime('%a'))
                # joined_date is a DateField; use exact match instead of __date lookup
                count = MemberProfile.objects.filter(joined_date=day).count()
                data.append(count)
            stats['traffic_labels'] = labels
            stats['traffic_last_7'] = data
            # Also provide JSON-serialized strings for safe template insertion
            import json
            stats['traffic_labels_json'] = json.dumps(labels)
            stats['traffic_last_7_json'] = json.dumps(data)
        except Exception:
            # Fallback sensible defaults
            fallback_labels = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
            fallback_data = [0,0,0,0,0,0,0]
            stats['traffic_labels'] = fallback_labels
            stats['traffic_last_7'] = fallback_data
            stats['traffic_labels_json'] = json.dumps(fallback_labels)
            stats['traffic_last_7_json'] = json.dumps(fallback_data)

        return stats
    
    @staticmethod
    def get_recent_activity():
        """Get recent activity data"""
        activity = {
            'new_members_this_month': MemberProfile.objects.filter(
                joined_date__gte=timezone.now() - timedelta(days=30)
            ).count(),
            'recent_gallery': GalleryImage.objects.order_by('-id')[:5],
            'recent_programs': Program.objects.order_by('-created_at')[:5],
            'recent_members': MemberProfile.objects.order_by('-joined_date')[:5],
        }
        return activity
    
    @staticmethod
    def get_program_stats():
        """Get program participation statistics"""
        programs = Program.objects.annotate(
            participant_count=Count('participations')
        ).order_by('-participant_count')[:5]
        return programs
    
    @staticmethod
    def get_member_engagement():
        """Get member engagement metrics"""
        total_members = MemberProfile.objects.count()
        active_members = MemberProfile.objects.filter(
            Q(event_attendances__isnull=False) | Q(program_participations__isnull=False)
        ).distinct().count()
        
        engagement = {
            'total': total_members,
            'active': active_members,
            'inactive': total_members - active_members,
            'engagement_rate': (active_members / total_members * 100) if total_members > 0 else 0,
        }
        return engagement
