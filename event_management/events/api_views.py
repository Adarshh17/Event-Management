from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.urls import reverse


@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request):
    """
    API Root endpoint - Welcome page with available endpoints.
    """
    return Response({
        'message': 'Welcome to Event Management System API',
        'version': '1.0',
        'endpoints': {
            'authentication': {
                'register': request.build_absolute_uri('/api/auth/register/'),
                'login': request.build_absolute_uri('/api/auth/login/'),
                'refresh_token': request.build_absolute_uri('/api/auth/token/refresh/'),
            },
            'events': {
                'list_create': request.build_absolute_uri('/api/events/'),
                'detail': request.build_absolute_uri('/api/events/{id}/'),
                'search': request.build_absolute_uri('/api/events/?search=keyword'),
                'filter': request.build_absolute_uri('/api/events/?location=New York'),
            },
            'rsvps': {
                'list_create': request.build_absolute_uri('/api/rsvps/'),
                'detail': request.build_absolute_uri('/api/rsvps/{id}/'),
            },
            'reviews': {
                'list_create': request.build_absolute_uri('/api/reviews/'),
                'detail': request.build_absolute_uri('/api/reviews/{id}/'),
                'filter_by_event': request.build_absolute_uri('/api/reviews/?event={event_id}'),
            },
            'admin': request.build_absolute_uri('/admin/'),
        },
        'documentation': {
            'quick_start': 'See README.md for setup instructions',
            'api_testing': 'See API_TESTING_GUIDE.md for testing examples',
            'quick_reference': 'See QUICK_REFERENCE.md for quick reference',
        },
        'features': [
            'JWT Authentication',
            'Event Management (CRUD)',
            'RSVP System',
            'Review System',
            'Public/Private Events',
            'Search & Filtering',
            'Pagination',
        ]
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def home(request):
    """
    Home page - Redirects to API root.
    """
    return Response({
        'message': 'Event Management System API',
        'version': '1.0',
        'status': 'Running',
        'api_root': request.build_absolute_uri('/api/'),
        'documentation': {
            'swagger': 'Install drf-spectacular for auto-generated API docs',
            'readme': 'See README.md in project root',
        },
        'quick_links': {
            'register': request.build_absolute_uri('/api/auth/register/'),
            'login': request.build_absolute_uri('/api/auth/login/'),
            'events': request.build_absolute_uri('/api/events/'),
            'admin': request.build_absolute_uri('/admin/'),
        }
    })
