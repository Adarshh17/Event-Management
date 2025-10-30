from django.contrib import admin
from .models import UserProfile, Event, RSVP, Review


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile model."""
    list_display = ['user', 'full_name', 'location']
    search_fields = ['user__username', 'full_name', 'location']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin interface for Event model."""
    list_display = ['title', 'organizer', 'location', 'start_time', 'is_public', 'created_at']
    list_filter = ['is_public', 'created_at', 'start_time']
    search_fields = ['title', 'description', 'location', 'organizer__username']
    date_hierarchy = 'start_time'


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    """Admin interface for RSVP model."""
    list_display = ['event', 'user', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['event__title', 'user__username']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Admin interface for Review model."""
    list_display = ['event', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['event__title', 'user__username', 'comment']
