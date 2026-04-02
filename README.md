# College Event System

Flask-based web app for managing college events with Docker support.

## Features
- User Management (Admin/Student)
- Event Management
- Registration system
- Reports

## Run with Docker
```bash
docker build -t college-event-system .
docker run -d -p 5000:5000 college-event-system
