from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    User profile model extending Django's User model.
    Stores additional user information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    profile_picture = models.URLField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Event(models.Model):
    """
    Event model representing an event in the system.
    Can be public or private.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    location = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class RSVP(models.Model):
    """
    RSVP model for event attendance tracking.
    Each user can only RSVP once per event.
    """
    GOING = 'going'
    MAYBE = 'maybe'
    NOT_GOING = 'not_going'
    
    STATUS_CHOICES = [
        (GOING, 'Going'),
        (MAYBE, 'Maybe'),
        (NOT_GOING, 'Not Going'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='rsvps')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rsvps')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=GOING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('event', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.event.title} - {self.status}"


class Review(models.Model):
    """
    Review model for events.
    Users can leave ratings and comments for events.
    """
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.event.title} - {self.rating} stars"
