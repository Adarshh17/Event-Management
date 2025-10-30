# HOW TO RUN - Event Management System API

## Quick Start (3 Steps)

### Step 1: Install Dependencies
Open PowerShell/Command Prompt in the project folder and run:
```bash
pip install -r requirements.txt
```

### Step 2: Setup Database
Run the migrations to create database tables:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Start the Server
```bash
python manage.py runserver
```

The server will start at: **http://127.0.0.1:8000/**

---

## Alternative: Use Batch Files (Windows)

### One-Click Setup (First Time Only)
Double-click: **`setup.bat`**

This will:
- Install all dependencies
- Create database migrations
- Apply migrations
- Prompt you to create a superuser (optional)

### Start Server
Double-click: **`start.bat`**

---

## Accessing the API

### 1. Home Page
Open in browser: **http://127.0.0.1:8000/**

You'll see a welcome message with available endpoints.

### 2. API Root
Open in browser: **http://127.0.0.1:8000/api/**

You'll see a list of all available API endpoints.

### 3. Admin Panel (Optional)
Open in browser: **http://127.0.0.1:8000/admin/**

First create a superuser:
```bash
python manage.py createsuperuser
```

---

## Testing the API

### Using Browser
1. **View Events**: http://127.0.0.1:8000/api/events/
2. **Register User**: POST to http://127.0.0.1:8000/api/auth/register/
3. **Login**: POST to http://127.0.0.1:8000/api/auth/login/

### Using PowerShell

#### 1. Register a New User
```powershell
$body = @{
    username = "testuser"
    email = "test@example.com"
    password = "Test@12345"
    password2 = "Test@12345"
    first_name = "Test"
    last_name = "User"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/register/" -Method POST -ContentType "application/json" -Body $body
```

#### 2. Login to Get Token
```powershell
$body = @{
    username = "testuser"
    password = "Test@12345"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/auth/login/" -Method POST -ContentType "application/json" -Body $body
$token = $response.access
Write-Host "Your Token: $token"
```

#### 3. Create an Event (Requires Token)
```powershell
$headers = @{
    "Authorization" = "Bearer $token"
    "Content-Type" = "application/json"
}

$body = @{
    title = "Tech Conference 2025"
    description = "Annual technology conference"
    location = "New York"
    start_time = "2025-12-01T10:00:00Z"
    end_time = "2025-12-01T17:00:00Z"
    is_public = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/events/" -Method POST -Headers $headers -Body $body
```

#### 4. View All Events
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/events/" -Method GET
```

#### 5. RSVP to Event
```powershell
$body = @{
    event = 1
    status = "going"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/rsvps/" -Method POST -Headers $headers -Body $body
```

#### 6. Leave a Review
```powershell
$body = @{
    event = 1
    rating = 5
    comment = "Amazing event!"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/reviews/" -Method POST -Headers $headers -Body $body
```

---

## Run Tests

To verify everything is working:
```bash
python manage.py test events
```

---

## Available Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Home page | No |
| GET | `/api/` | API root | No |
| POST | `/api/auth/register/` | Register user | No |
| POST | `/api/auth/login/` | Login (get token) | No |
| POST | `/api/auth/token/refresh/` | Refresh token | No |
| GET | `/api/events/` | List events | No |
| POST | `/api/events/` | Create event | Yes |
| GET | `/api/events/{id}/` | Get event details | No* |
| PUT/PATCH | `/api/events/{id}/` | Update event | Yes** |
| DELETE | `/api/events/{id}/` | Delete event | Yes** |
| GET | `/api/rsvps/` | List my RSVPs | Yes |
| POST | `/api/rsvps/` | Create/update RSVP | Yes |
| GET | `/api/reviews/` | List reviews | No |
| POST | `/api/reviews/` | Create review | Yes |
| GET | `/admin/` | Admin panel | Yes*** |

*Private events require organizer authentication  
**Only organizer can update/delete  
***Requires superuser account

---

## Troubleshooting

### "No such table" error
Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

### "Port already in use" error
Change the port:
```bash
python manage.py runserver 8080
```

### Module not found error
Install dependencies:
```bash
pip install -r requirements.txt
```

### Server not starting
Make sure you're in the correct directory:
```bash
cd d:\new\event_management
python manage.py runserver
```

---

## Project Structure

```
event_management/
├── manage.py              ← Django management script
├── requirements.txt       ← Dependencies
├── README.md             ← Full documentation
├── setup.bat             ← Quick setup (Windows)
├── start.bat             ← Start server (Windows)
├── migrate.bat           ← Run migrations (Windows)
├── event_management/     ← Django configuration
└── events/               ← Main application
    ├── models.py         ← 4 models
    ├── serializers.py    ← 5 serializers
    ├── views.py          ← API views
    └── ...
```

---

## Quick Command Reference

```bash
# Setup (first time)
pip install -r requirements.txt
python manage.py migrate

# Start server
python manage.py runserver

# Create admin user
python manage.py createsuperuser

# Run tests
python manage.py test events

# Check for errors
python manage.py check

# View migrations
python manage.py showmigrations
```

---

## Default Configuration

- **Server**: http://127.0.0.1:8000/
- **Database**: SQLite (db.sqlite3)
- **Pagination**: 5 items per page
- **Token Lifetime**: 60 minutes (access), 1 day (refresh)

---

## Need Help?

See **README.md** for complete documentation including:
- Detailed API endpoint examples
- Model descriptions
- Permission rules
- Advanced features

See **ASSIGNMENT_VERIFICATION.md** for verification report.

---

**That's it! Your Event Management API is ready to use.** 🚀
