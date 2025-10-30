from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Event, RSVP, Review


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model with nested user information."""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'username', 'email', 'full_name', 'bio', 'location', 'profile_picture']
        read_only_fields = ['id', 'user']


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            password=validated_data['password']
        )
        # Create user profile
        UserProfile.objects.create(user=user)
        return user


class EventSerializer(serializers.ModelSerializer):
    """Serializer for Event model with nested organizer information."""
    organizer_username = serializers.CharField(source='organizer.username', read_only=True)
    organizer_name = serializers.SerializerMethodField()
    rsvp_count = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'organizer', 'organizer_username', 
            'organizer_name', 'location', 'start_time', 'end_time', 'is_public',
            'created_at', 'updated_at', 'rsvp_count', 'review_count', 'average_rating'
        ]
        read_only_fields = ['id', 'organizer', 'created_at', 'updated_at']

    def get_organizer_name(self, obj):
        """Get organizer's full name or username."""
        if hasattr(obj.organizer, 'profile') and obj.organizer.profile.full_name:
            return obj.organizer.profile.full_name
        return obj.organizer.get_full_name() or obj.organizer.username

    def get_rsvp_count(self, obj):
        """Get total RSVP count for the event."""
        return obj.rsvps.count()

    def get_review_count(self, obj):
        """Get total review count for the event."""
        return obj.reviews.count()

    def get_average_rating(self, obj):
        """Calculate average rating for the event."""
        reviews = obj.reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 2)
        return None


class RSVPSerializer(serializers.ModelSerializer):
    """Serializer for RSVP model."""
    user_username = serializers.CharField(source='user.username', read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)

    class Meta:
        model = RSVP
        fields = ['id', 'event', 'user', 'user_username', 'event_title', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate(self, attrs):
        """Validate that the event is public or user is invited."""
        event = attrs.get('event')
        user = self.context['request'].user

        if not event.is_public:
            # For private events, you could add invitation logic here
            # For now, we'll allow only if user is the organizer
            if event.organizer != user:
                raise serializers.ValidationError("This is a private event. You are not invited.")
        
        return attrs


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""
    user_username = serializers.CharField(source='user.username', read_only=True)
    event_title = serializers.CharField(source='event.title', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'event', 'user', 'user_username', 'event_title', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def validate_rating(self, value):
        """Validate that rating is between 1 and 5."""
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
