# Overview

This is a certificate verification system built with Flask that uses blockchain technology to ensure the authenticity and immutability of digital certificates. The system allows users to upload certificates, generates secure access codes for sharing, and enables companies to verify certificate authenticity. It implements a simple proof-of-work blockchain to store certificate hashes, providing tamper-proof verification.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Framework
- **Flask**: Core web framework handling HTTP requests and responses
- **Flask-SQLAlchemy**: ORM for database operations with declarative models
- **Flask-Login**: User session management and authentication
- **Werkzeug**: WSGI utilities including file upload handling and password hashing

## Database Layer
- **SQLAlchemy with SQLite**: Default database using SQLite for development, configurable via DATABASE_URL environment variable
- **Connection pooling**: Configured with pool recycling and pre-ping for production reliability
- **Model relationships**: User-Certificate and User-AccessCode relationships with cascade delete

## Authentication System
- **Dual user types**: Separate User and Company models both implementing Flask-Login's UserMixin
- **Password security**: Werkzeug password hashing with salt
- **Session management**: Flask sessions with configurable secret key
- **User identification**: Prefixed IDs (user_/company_) to distinguish user types

## Blockchain Implementation
- **Simple proof-of-work**: Custom blockchain with configurable difficulty for mining
- **SHA-256 hashing**: Certificate content hashing and block hashing
- **Genesis block**: Automatic creation of initial blockchain block
- **Block structure**: Previous hash linking, certificate hash storage, timestamp, and nonce

## File Management
- **Secure uploads**: Werkzeug secure filename handling with allowed extensions (PDF, PNG, JPG, JPEG)
- **File size limits**: 16MB maximum upload size
- **Hash verification**: SHA-256 file content hashing for integrity checking
- **Storage location**: Configurable upload folder with proper file organization

## Frontend Architecture
- **Template engine**: Jinja2 templates with base template inheritance
- **CSS framework**: Bootstrap with dark theme and Font Awesome icons
- **Responsive design**: Mobile-first approach with Bootstrap grid system
- **JavaScript enhancements**: Form validation, file upload previews, and auto-hiding alerts

## Security Features
- **Access control**: Login-required decorators for protected routes
- **File validation**: Extension and size checking before upload
- **CSRF protection**: Flask session-based protection
- **Proxy support**: ProxyFix middleware for proper header handling behind reverse proxies

# External Dependencies

## Core Framework Dependencies
- **Flask**: Web framework for Python
- **Flask-SQLAlchemy**: Database ORM integration
- **Flask-Login**: User authentication and session management
- **Werkzeug**: WSGI utilities and security functions

## Frontend Libraries
- **Bootstrap**: CSS framework via CDN (replit agent dark theme)
- **Font Awesome**: Icon library via CDN
- **Custom CSS**: Additional styling in static/css/style.css

## Database
- **SQLite**: Default development database (file-based)
- **PostgreSQL**: Production database option via DATABASE_URL environment variable

## File System
- **Local storage**: File uploads stored in uploads/ directory
- **No cloud storage**: Currently uses local file system only

## Environment Configuration
- **SESSION_SECRET**: Configurable session secret key
- **DATABASE_URL**: Database connection string
- **Upload configuration**: File size limits and allowed extensions

## Development Tools
- **Python logging**: Built-in logging with DEBUG level
- **Development server**: Flask development server with debug mode
- **Static file serving**: Flask static file handling for CSS/JS