# CertiChain: Certificate Verification System with Blockchain

A secure web-based application for certificate storage and verification using blockchain technology. This system provides dual portals for users to upload certificates and companies to verify their authenticity through secure access codes.

## 🌟 Features

### User Portal
- **Secure Registration & Login**: Individual user accounts with password protection
- **Certificate Upload**: Support for PDF, JPG, and PNG files up to 16MB
- **Blockchain Storage**: SHA-256 hash generation and immutable blockchain storage
- **Access Code Generation**: Create secure 12-character codes for certificate sharing
- **Dashboard Management**: View uploaded certificates and their blockchain status

### Company Portal
- **Company Registration & Login**: Separate portal for organizations
- **User Search**: Find candidates by name or username
- **Certificate Verification**: Verify certificates using access codes
- **Blockchain Integrity**: Real-time blockchain verification status
- **Document Download**: Download verified certificates securely

### Blockchain Simulation
- **Proof-of-Work Mining**: Educational blockchain implementation with configurable difficulty
- **SHA-256 Hashing**: Secure certificate hash storage
- **Immutable Records**: Tamper-proof certificate verification
- **Block Integrity**: Complete blockchain validation system

## 🚀 Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLAlchemy with PostgreSQL/SQLite support
- **Authentication**: Flask-Login with session management
- **Frontend**: Bootstrap 5 with dark theme
- **Blockchain**: Custom Python implementation with mining simulation
- **Security**: Werkzeug password hashing, secure file uploads

## 📋 Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- PostgreSQL (optional, SQLite used by default)

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd certificate-verification-system
```

### 2. Install Dependencies
```bash
# Option A: Using the project file
pip install -e .

# Option B: Install packages individually
pip install flask>=3.1.2 flask-sqlalchemy>=3.1.1 flask-login>=0.6.3 gunicorn>=23.0.0 psycopg2-binary>=2.9.10 email-validator>=2.3.0 oauthlib>=3.3.1 pyjwt>=2.10.1 flask-dance>=7.1.0 sqlalchemy>=2.0.43 werkzeug>=3.1.3
```

### 3. Environment Configuration
Create environment variables for the application:

```bash
# Required: Set a secure session secret
export SESSION_SECRET="your-secure-secret-key-here"

# Optional: Database configuration (defaults to SQLite)
export DATABASE_URL="postgresql://username:password@localhost/certificate_db"
```

### 4. Database Setup

**Option 1: SQLite (Recommended for development)**
- No additional setup required
- Database file created automatically as `certificate_system.db`

**Option 2: PostgreSQL (For production)**
- Install PostgreSQL server
- Create a database for the application
- Set the `DATABASE_URL` environment variable

### 5. Run the Application

**Development Mode:**
```bash
python main.py
```

**Production Mode:**
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

### 6. Access the Application
Open your web browser and navigate to:
```
http://localhost:5000
```

## 🎯 Usage Guide

### For Users (Certificate Owners)

1. **Register**: Create a user account with your details
2. **Login**: Access your personal dashboard
3. **Upload Certificates**: 
   - Select PDF, JPG, or PNG files
   - Files are automatically hashed with SHA-256
   - Hash is stored on the blockchain through mining
4. **Generate Access Codes**: 
   - Create secure 12-character codes for each certificate
   - Codes expire after 24 hours
   - Share codes with companies for verification

### For Companies (Verifiers)

1. **Register**: Create a company account
2. **Search Users**: Find candidates by name or username
3. **Verify Certificates**:
   - Request access code from the certificate owner
   - Enter the code to view and verify the certificate
   - Check blockchain verification status
   - Download verified certificates

## 📁 Project Structure

```
certificate-verification-system/
├── app.py                  # Flask application configuration
├── main.py                 # Application entry point
├── models.py               # Database models
├── routes.py               # URL routes and request handlers
├── blockchain.py           # Blockchain simulation implementation
├── pyproject.toml          # Project dependencies
├── uploads/                # Certificate file storage
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   ├── index.html          # Homepage
│   ├── user_login.html     # User login page
│   ├── user_register.html  # User registration
│   ├── user_dashboard.html # User dashboard
│   ├── company_login.html  # Company login
│   ├── company_register.html # Company registration
│   ├── company_dashboard.html # Company dashboard
│   └── certificate_view.html # Certificate verification page
└── static/                 # CSS and JavaScript files
    ├── css/style.css       # Custom styles
    └── js/main.js          # JavaScript functionality
```

## 🔒 Security Features

- **Password Hashing**: Werkzeug secure password storage
- **File Validation**: Strict file type and size checking
- **Access Control**: Login-required decorators for protected routes
- **Session Management**: Secure Flask sessions
- **Hash Verification**: SHA-256 file integrity checking
- **Blockchain Integrity**: Immutable certificate records

## 🧪 Educational Blockchain Implementation

This project includes a simplified blockchain implementation for educational purposes:

- **Mining Simulation**: Proof-of-work algorithm with configurable difficulty
- **Block Structure**: Previous hash linking, certificate storage, timestamps
- **Hash Functions**: SHA-256 for both file content and block hashing
- **Integrity Verification**: Complete blockchain validation
- **Genesis Block**: Automatic initialization

## 🚨 Troubleshooting

### Common Issues

**Port Already in Use:**
```bash
# Use a different port
gunicorn --bind 0.0.0.0:8080 --reuse-port --reload main:app
```

**Database Connection Issues:**
- Verify PostgreSQL is running (if using PostgreSQL)
- Check database credentials in `DATABASE_URL`
- Ensure SQLite file permissions (if using SQLite)

**Dependency Issues:**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -e .
```

**File Upload Issues:**
- Check `uploads/` directory permissions
- Verify file size limits (16MB maximum)
- Ensure allowed file types: PDF, JPG, PNG

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request



## 📞 Support

For questions or issues, please create an issue in the GitHub repository or contact the development team.
Email: raiv5253@gmail.com

---

**Note**: This blockchain implementation is designed for educational purposes and should not be used for production-level security without additional hardening and security reviews.
