# MedStat Backend API

FastAPI backend for handling form submissions from the MedStat landing page.

## Features

- 📧 Contact form endpoint with email notifications
- 🎯 Demo request endpoint with email notifications
- ✅ Input validation using Pydantic
- 🔒 CORS configuration for frontend integration
- 📊 Logging and error handling
- 📝 Auto-generated API documentation

## Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
```

### 2. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
copy .env.example .env
```

Edit `.env` file with your actual credentials:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
ADMIN_EMAIL=admin@medstat.in
FRONTEND_URL=http://localhost:8000
```

#### Gmail App Password Setup:
1. Go to Google Account settings
2. Enable 2-Factor Authentication
3. Generate an App Password: https://myaccount.google.com/apppasswords
4. Use the generated password in `SMTP_PASSWORD`

### 5. Run the Server

**Development (with auto-reload):**
```bash
uvicorn main:app --reload
```

**Production:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## API Endpoints

### Health Check
```
GET /api/health
```

### Contact Form
```
POST /api/contact
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "1234567890",
  "type": "Doctor / Private Practice",
  "message": "I'm interested in MedStat..."
}
```

### Demo Request
```
POST /api/demo-request
Content-Type: application/json

{
  "name": "Jane Smith",
  "clinic": "City Hospital",
  "role": "Administrator",
  "email": "jane@cityhospital.com",
  "phone": "9876543210",
  "interests": "AI Triage, Queue Management"
}
```

## Testing

### Using curl

**Contact Form:**
```bash
curl -X POST http://localhost:8000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "phone": "1234567890",
    "type": "Hospital / Clinic",
    "message": "This is a test message"
  }'
```

**Demo Request:**
```bash
curl -X POST http://localhost:8000/api/demo-request \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "clinic": "Test Clinic",
    "role": "Doctor",
    "email": "test@example.com",
    "phone": "1234567890",
    "interests": "AI Triage"
  }'
```

## Project Structure

```
backend/
├── main.py              # FastAPI application & routes
├── config.py            # Configuration management
├── email_service.py     # Email sending functionality
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
├── .env                 # Your actual config (git-ignored)
└── README.md           # This file
```

## Error Handling

The API includes comprehensive error handling:
- **400**: Bad Request (validation errors)
- **404**: Not Found
- **500**: Internal Server Error

All errors return JSON responses with details.

## Security Notes

- Never commit `.env` file to version control
- Use App Passwords for Gmail (not your actual password)
- In production, restrict CORS to specific domains
- Consider rate limiting for production deployment
- Use HTTPS in production

## Deployment

### Heroku
```bash
# Install Heroku CLI, then:
heroku create medstat-api
heroku config:set SMTP_USER=your-email@gmail.com
heroku config:set SMTP_PASSWORD=your-app-password
heroku config:set ADMIN_EMAIL=admin@medstat.in
git push heroku main
```

### Railway/Render
Add environment variables in the dashboard and deploy.

## Troubleshooting

**Email not sending:**
- Check Gmail App Password is correct
- Verify 2FA is enabled on Google account
- Check firewall/antivirus isn't blocking port 587

**CORS errors:**
- Verify `FRONTEND_URL` in `.env` matches your frontend
- Check browser console for detailed CORS errors

**Import errors:**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

## Support

For issues, please contact the development team or create an issue in the repository.
