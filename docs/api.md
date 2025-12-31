# Zenith API Reference

## Authentication

All API endpoints require a Bearer token obtained via login.

### POST /api/v1/auth/login
Login and obtain access token.

**Request:**
json
{
  "username": "user",
  "password": "pass"
}

Response:

{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "token_type": "bearer"
}
