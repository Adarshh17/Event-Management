from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.shortcuts import get_object_or_404

from .models import Event, RSVP, Review, UserProfile
from .serializers import (
    EventSerializer, RSVPSerializer, ReviewSerializer, 
    RegisterSerializer, UserProfileSerializer
)
from .permissions import IsOrganizerOrReadOnly, IsInvitedOrPublic


class RegisterView(generics.CreateAPIView):
    """
    API view for user registration.
    Allows anyone to create a new user account.
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'user': {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'message': 'User registered successfully. Please login to get your token.'
        }, status=status.HTTP_201_CREATED)


class EventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Event model.
    Provides CRUD operations for events with filtering and search.
    """
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOrganizerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['location', 'is_public', 'organizer__username']
    search_fields = ['title', 'description', 'location', 'organizer__username']
    ordering_fields = ['start_time', 'created_at', 'title']

    def get_queryset(self):
        """
        Filter queryset to show only public events for unauthenticated users.
        Authenticated users can see public events and their own private events.
        """
        queryset = Event.objects.all()
        
        if not self.request.user.is_authenticated:
            # Unauthenticated users can only see public events
            return queryset.filter(is_public=True)
        
        # Authenticated users can see public events and events they organize
        return queryset.filter(
            models.Q(is_public=True) | models.Q(organizer=self.request.user)
        )

    def perform_create(self, serializer):
        """Set the organizer to the current user when creating an event."""
        serializer.save(organizer=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single event.
        Apply IsInvitedOrPublic permission check.
        """
        instance = self.get_object()
        
        # Check if user has permission to view this event
        permission = IsInvitedOrPublic()
        if not permission.has_object_permission(request, self, instance):
            return Response(
                {'detail': 'You do not have permission to view this private event.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticatedOrReadOnly])
    def rsvps(self, request, pk=None):
        """Get all RSVPs for a specific event."""
        event = self.get_object()
        rsvps = event.rsvps.all()
        serializer = RSVPSerializer(rsvps, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticatedOrReadOnly])
    def reviews(self, request, pk=None):
        """Get all reviews for a specific event."""
        event = self.get_object()
        reviews = event.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class RSVPViewSet(viewsets.ModelViewSet):
    """
    ViewSet for RSVP model.
    Allows users to RSVP to events.
    """
    serializer_class = RSVPSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return RSVPs for the current user."""
        return RSVP.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set the user to the current user when creating an RSVP."""
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new RSVP or update existing one.
        """
        event_id = request.data.get('event')
        
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response(
                {'detail': 'Event not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if RSVP already exists
        existing_rsvp = RSVP.objects.filter(event=event, user=request.user).first()
        
        if existing_rsvp:
            # Update existing RSVP
            serializer = self.get_serializer(existing_rsvp, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Create new RSVP
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Review model.
    Allows users to leave reviews for events.
    """
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Return all reviews or filter by event_id if provided.
        """
        queryset = Review.objects.all()
        event_id = self.request.query_params.get('event', None)
        
        if event_id is not None:
            queryset = queryset.filter(event_id=event_id)
        
        return queryset

    def perform_create(self, serializer):
        """Set the user to the current user when creating a review."""
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new review.
        Check if user has already reviewed this event.
        """
        event_id = request.data.get('event')
        
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response(
                {'detail': 'Event not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if user has already reviewed this event
        existing_review = Review.objects.filter(event=event, user=request.user).first()
        
        if existing_review:
            return Response(
                {'detail': 'You have already reviewed this event. Use PUT/PATCH to update.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create new review
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Import models for Q query
from django.db import models
