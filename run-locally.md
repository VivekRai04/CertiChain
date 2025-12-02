# Running the Certificate Verification System Locally

This guide explains how to run the blockchain-based certificate verification system on your local computer.

## System Requirements

**Python Environment:**
- Python 3.11 or higher
- pip or uv (package manager)

## Installation Steps

### 1. Clone/Download the Project
Make sure you have all the project files including:
- `app.py` - Flask application setup
- `main.py` - Application entry point
- `models.py` - Database models
- `routes.py` - URL routes and handlers
- `blockchain.py` - Blockchain simulation
- `pyproject.toml` - Dependencies
- `templates/` directory with 9 HTML files
- `static/` directory with CSS and JS files

### 2. Install Python Dependencies

**Option A: Using pip with the project file**
```bash
pip install -e .
```

**Option B: Install packages individually**
```bash
pip install flask>=3.1.2 flask-sqlalchemy>=3.1.1 flask-login>=0.6.3 gunicorn>=23.0.0 psycopg2-binary>=2.9.10 email-validator>=2.3.0 oauthlib>=3.3.1 pyjwt>=2.10.1 flask-dance>=7.1.0 sqlalchemy>=2.0.43 werkzeug>=3.1.3
```

### 3. Database Setup

**Option 1: SQLite (Default - Recommended for local testing)**
- No additional setup needed
- Database file `certificate_system.db` will be created automatically
- Perfect for development and testing

**Option 2: PostgreSQL (Optional)**
- Install PostgreSQL server locally
- Create a database for the application
- Set the `DATABASE_URL` environment variable (see below)

### 4. Environment Variables

**Required:**
- `SESSION_SECRET` - Flask session secret key
  ```bash
  export SESSION_SECRET="your-secret-key-here"
  ```

**Optional:**
- `DATABASE_URL` - Database connection string
  ```bash
  # For PostgreSQL (if not using SQLite)
  export DATABASE_URL="postgresql://username:password@localhost/certificate_db"
  
  # For SQLite (default if not set)
  # Uses: sqlite:///certificate_system.db
  ```

### 5. Create Required Directories
The application will create these automatically, but you can create them manually if needed:
```bash
mkdir uploads
```

## Running the Application

### Development Mode (Recommended for local testing)
```bash
python main.py
```

### Production Mode
```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

## Accessing the Application

Once running, open your web browser and navigate to:
```
http://localhost:5000
```

## Application Features

The system includes two main portals:

**User Portal:**
- User registration and login
- Certificate upload (PDF, JPG, PNG files up to 16MB)
- SHA-256 hash generation and blockchain storage
- Access code generation for secure sharing
- Certificate management dashboard

**Company Portal:**
- Company registration and login
- User search functionality
- Certificate verification using access codes
- Blockchain integrity verification
- Certificate download for verified documents

## File Structure

```
project/
├── app.py              # Flask application setup
├── main.py             # Application entry point
├── models.py           # Database models
├── routes.py           # URL routes and handlers
├── blockchain.py       # Blockchain simulation
├── pyproject.toml      # Dependencies
├── uploads/            # Certificate storage (created automatically)
├── templates/          # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── user_login.html
│   ├── user_register.html
│   ├── user_dashboard.html
│   ├── company_login.html
│   ├── company_register.html
│   ├── company_dashboard.html
│   └── certificate_view.html
└── static/             # CSS and JavaScript
    ├── css/style.css
    └── js/main.js
```

## Troubleshooting

**Database Issues:**
- If using SQLite, ensure the application has write permissions in the project directory
- If using PostgreSQL, verify the database server is running and accessible

**Port Issues:**
- If port 5000 is busy, you can change it in `main.py` or use a different port with gunicorn:
  ```bash
  gunicorn --bind 0.0.0.0:8080 --reuse-port --reload main:app
  ```

**Dependencies Issues:**
- Ensure you're using Python 3.11 or higher
- Try upgrading pip: `pip install --upgrade pip`
- Use a virtual environment to avoid conflicts:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install -e .
  ```

## Security Notes

- The default `SESSION_SECRET` is for development only
- For production, always set a secure `SESSION_SECRET`
- Certificate files are stored locally in the `uploads/` directory
- The blockchain implementation is a simulation for educational purposes