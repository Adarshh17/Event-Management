# Event Management System API

## Overview
A Django REST Framework-based Event Management API that allows users to create and manage events, RSVP to them, and leave reviews with JWT-based authentication.

## Features
- JWT-based user authentication (register & login)
- Event management (Create, Read, Update, Delete)
- RSVP system (Going / Maybe / Not Going)
- Review system (1-5 star ratings with comments)
- Public/private event visibility
- Search and filtering by title, location, organizer
- Pagination (5 items per page)
- Custom permissions (organizer-only edit/delete)

## Technology Stack
- Django 5.2+
- Django REST Framework
- Simple JWT
- Django Filter
- Django CORS Headers
- SQLite Database

## Project Structure
```
event_management/
│
├── manage.py
├── event_management/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│
├── events/
│   ├── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py
│   ├── filters.py
│   ├── tests.py
│   ├── admin.py
│   ├── apps.py
│
└── requirements.txt
```

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 4. Run Development Server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

### 5. Run Tests
```bash
python manage.py test events
```

## API Endpoints

### Authentication Endpoints

#### Register a New User
```
POST /api/auth/register/
```
**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword",
  "password2": "securepassword",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### Login (Get JWT Token)
```
POST /api/auth/login/
```
**Request Body:**
```json
{
  "username": "johndoe",
  "password": "securepassword"
}
```
**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Refresh Token
```
POST /api/auth/token/refresh/
```
**Request Body:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Event Endpoints

#### List All Events (Public)
```
GET /api/events/
```
**Query Parameters:**
- `page`: Page number (default: 1)
- `search`: Search by title, description, location, or organizer username
- `location`: Filter by location
- `organizer__username`: Filter by organizer username
- `is_public`: Filter by public/private status

**Example:**
```
GET /api/events/?search=conference&location=New York&page=1
```

#### Create Event (Authenticated)
```
POST /api/events/
```
**Headers:**
```
Authorization: Bearer <access_token>
```
**Request Body:**
```json
{
  "title": "Tech Conference 2025",
  "description": "Annual technology conference",
  "location": "New York",
  "start_time": "2025-11-15T09:00:00Z",
  "end_time": "2025-11-15T18:00:00Z",
  "is_public": true
}
```

#### Get Event Details
```
GET /api/events/{id}/
```

#### Update Event (Organizer Only)
```
PUT /api/events/{id}/
PATCH /api/events/{id}/
```
**Headers:**
```
Authorization: Bearer <access_token>
```

#### Delete Event (Organizer Only)
```
DELETE /api/events/{id}/
```
**Headers:**
```
Authorization: Bearer <access_token>
```

#### Get Event RSVPs
```
GET /api/events/{id}/rsvps/
```

#### Get Event Reviews
```
GET /api/events/{id}/reviews/
```

### RSVP Endpoints

#### Create or Update RSVP
```
POST /api/rsvps/
```
**Headers:**
```
Authorization: Bearer <access_token>
```
**Request Body:**
```json
{
  "event": 1,
  "status": "going"
}
```
**Status Options:** `going`, `maybe`, `not_going`

#### List My RSVPs
```
GET /api/rsvps/
```
**Headers:**
```
Authorization: Bearer <access_token>
```

#### Get Specific RSVP
```
GET /api/rsvps/{id}/
```

#### Update RSVP
```
PATCH /api/rsvps/{id}/
```
**Request Body:**
```json
{
  "status": "maybe"
}
```

#### Delete RSVP
```
DELETE /api/rsvps/{id}/
```

### Review Endpoints

#### Create Review
```
POST /api/reviews/
```
**Headers:**
```
Authorization: Bearer <access_token>
```
**Request Body:**
```json
{
  "event": 1,
  "rating": 5,
  "comment": "Amazing event! Well organized and informative."
}
```
**Rating:** Integer between 1 and 5

#### List Reviews
```
GET /api/reviews/
```
**Query Parameters:**
- `event`: Filter by event ID

**Example:**
```
GET /api/reviews/?event=1
```

#### Get Specific Review
```
GET /api/reviews/{id}/
```

#### Update Review (Owner Only)
```
PUT /api/reviews/{id}/
PATCH /api/reviews/{id}/
```

#### Delete Review (Owner Only)
```
DELETE /api/reviews/{id}/
```

## Authentication

All protected endpoints require JWT authentication. Include the access token in the Authorization header:

```
Authorization: Bearer <your_access_token>
```

### Token Lifetime
- **Access Token**: 60 minutes
- **Refresh Token**: 1 day

## Permissions

### Event Permissions
- **List/View Public Events**: Anyone (unauthenticated)
- **Create Event**: Authenticated users
- **Update/Delete Event**: Event organizer only
- **View Private Event**: Event organizer only

### RSVP Permissions
- **Create/Update/Delete RSVP**: Authenticated users
- **View RSVPs**: Anyone

### Review Permissions
- **Create Review**: Authenticated users
- **View Reviews**: Anyone
- **Update/Delete Review**: Review owner only

## Models

### UserProfile
- Extends Django User model
- Fields: `full_name`, `bio`, `location`, `profile_picture`

### Event
- Fields: `title`, `description`, `organizer`, `location`, `start_time`, `end_time`, `is_public`, `created_at`, `updated_at`

### RSVP
- Fields: `event`, `user`, `status` (going/maybe/not_going)
- Unique constraint: One RSVP per user per event

### Review
- Fields: `event`, `user`, `rating` (1-5), `comment`

## Pagination

Default pagination is set to 5 items per page. Navigate through pages using:
```
GET /api/events/?page=2
```

## Filtering and Search

### Search
Search across multiple fields:
```
GET /api/events/?search=conference
```

### Filtering
Filter by specific fields:
```
GET /api/events/?location=New York&is_public=true
```

## Testing

Run the test suite:
```bash
python manage.py test
```

Run tests for specific app:
```bash
python manage.py test events
```

## Admin Panel

Access the Django admin panel at `http://127.0.0.1:8000/admin/`

Create a superuser to access the admin panel:
```bash
python manage.py createsuperuser
```

## Development Notes

### CORS Configuration
CORS is enabled for all origins in development. For production, update `CORS_ALLOW_ALL_ORIGINS` in `settings.py`.

### Database
The project uses SQLite by default. For production, consider using PostgreSQL or MySQL.

### Security
- Change `SECRET_KEY` in production
- Set `DEBUG = False` in production
- Configure `ALLOWED_HOSTS` for production deployment

## Example Usage Flow

1. **Register a new user:**
   ```bash
   POST /api/auth/register/
   ```

2. **Login to get JWT token:**
   ```bash
   POST /api/auth/login/
   ```

3. **Create an event (with token):**
   ```bash
   POST /api/events/
   Authorization: Bearer <token>
   ```

4. **RSVP to an event:**
   ```bash
   POST /api/rsvps/
   Authorization: Bearer <token>
   ```

5. **Leave a review:**
   ```bash
   POST /api/reviews/
   Authorization: Bearer <token>
   ```

6. **View all public events:**
   ```bash
   GET /api/events/
   ```

## Troubleshooting

### Migration Issues
If you encounter migration issues, try:
```bash
python manage.py makemigrations events
python manage.py migrate
```

### Port Already in Use
Change the port:
```bash
python manage.py runserver 8080
```

### CORS Errors
Ensure `corsheaders` is properly installed and configured in `INSTALLED_APPS` and `MIDDLEWARE`.

## License
This project is open source and available for educational purposes.

## Support
For issues and questions, please create an issue in the project repository.
