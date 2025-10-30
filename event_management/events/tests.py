from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import datetime, timedelta
from .models import Event, RSVP, Review, UserProfile


class EventModelTest(TestCase):
    """Test cases for Event model."""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            organizer=self.user,
            location='Test Location',
            start_time=datetime.now() + timedelta(days=1),
            end_time=datetime.now() + timedelta(days=2),
            is_public=True
        )

    def test_event_creation(self):
        """Test event is created correctly."""
        self.assertEqual(self.event.title, 'Test Event')
        self.assertEqual(self.event.organizer, self.user)
        self.assertTrue(self.event.is_public)

    def test_event_str(self):
        """Test event string representation."""
        self.assertEqual(str(self.event), 'Test Event')


class EventAPITest(APITestCase):
    """Test cases for Event API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.event = Event.objects.create(
            title='Public Event',
            description='Public Description',
            organizer=self.user,
            location='Public Location',
            start_time=datetime.now() + timedelta(days=1),
            end_time=datetime.now() + timedelta(days=2),
            is_public=True
        )

    def test_list_events_unauthenticated(self):
        """Test listing events without authentication."""
        response = self.client.get('/api/events/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_event_authenticated(self):
        """Test creating event with authentication."""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Event',
            'description': 'New Description',
            'location': 'New Location',
            'start_time': (datetime.now() + timedelta(days=3)).isoformat(),
            'end_time': (datetime.now() + timedelta(days=4)).isoformat(),
            'is_public': True
        }
        response = self.client.post('/api/events/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_event_unauthenticated(self):
        """Test creating event without authentication fails."""
        data = {
            'title': 'New Event',
            'description': 'New Description',
            'location': 'New Location',
            'start_time': (datetime.now() + timedelta(days=3)).isoformat(),
            'end_time': (datetime.now() + timedelta(days=4)).isoformat(),
            'is_public': True
        }
        response = self.client.post('/api/events/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RSVPAPITest(APITestCase):
    """Test cases for RSVP API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            organizer=self.user,
            location='Test Location',
            start_time=datetime.now() + timedelta(days=1),
            end_time=datetime.now() + timedelta(days=2),
            is_public=True
        )

    def test_create_rsvp(self):
        """Test creating RSVP."""
        self.client.force_authenticate(user=self.user)
        data = {
            'event': self.event.id,
            'status': 'going'
        }
        response = self.client.post('/api/rsvps/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_rsvp_unauthenticated(self):
        """Test creating RSVP without authentication fails."""
        data = {
            'event': self.event.id,
            'status': 'going'
        }
        response = self.client.post('/api/rsvps/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReviewAPITest(APITestCase):
    """Test cases for Review API endpoints."""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            organizer=self.user,
            location='Test Location',
            start_time=datetime.now() + timedelta(days=1),
            end_time=datetime.now() + timedelta(days=2),
            is_public=True
        )

    def test_create_review(self):
        """Test creating review."""
        self.client.force_authenticate(user=self.user)
        data = {
            'event': self.event.id,
            'rating': 5,
            'comment': 'Great event!'
        }
        response = self.client.post('/api/reviews/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_review_invalid_rating(self):
        """Test creating review with invalid rating."""
        self.client.force_authenticate(user=self.user)
        data = {
            'event': self.event.id,
            'rating': 6,  # Invalid rating
            'comment': 'Great event!'
        }
        response = self.client.post('/api/reviews/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
