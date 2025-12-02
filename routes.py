import os
import hashlib
from datetime import datetime, timedelta
from flask import render_template, request, redirect, url_for, flash, session, send_file
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import app, db
from models import User, Company, Certificate, AccessCode
from blockchain import blockchain

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calculate_file_hash(file_path):
    """Calculate SHA-256 hash of a file"""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

@app.route('/')
def index():
    return render_template('index.html')

# User Authentication Routes
@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            session['user_type'] = 'user'
            flash('Login successful!', 'success')
            return redirect(url_for('user_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('user_login.html')

@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        full_name = request.form['full_name']
        password = request.form['password']
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('user_register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('user_register.html')
        
        # Create new user
        user = User(username=username, email=email, full_name=full_name)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('user_login'))
    
    return render_template('user_register.html')

@app.route('/user/dashboard')
@login_required
def user_dashboard():
    if not hasattr(current_user, 'username'):  # Check if it's a user, not company
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    certificates = Certificate.query.filter_by(user_id=current_user.id).all()
    blockchain_stats = blockchain.get_blockchain_stats()
    
    return render_template('user_dashboard.html', 
                         certificates=certificates, 
                         blockchain_stats=blockchain_stats)

@app.route('/user/upload', methods=['POST'])
@login_required
def upload_certificate():
    if not hasattr(current_user, 'username'):
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    if 'certificate' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('user_dashboard'))
    
    file = request.files['certificate']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('user_dashboard'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to filename to avoid conflicts
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        file.save(file_path)
        
        # Calculate file hash
        file_hash = calculate_file_hash(file_path)
        file_size = os.path.getsize(file_path)
        file_type = filename.rsplit('.', 1)[1].lower()
        
        # Check if certificate with same hash already exists
        existing_cert = Certificate.query.filter_by(file_hash=file_hash).first()
        if existing_cert:
            os.remove(file_path)  # Remove the uploaded file
            flash('This certificate already exists in the system', 'warning')
            return redirect(url_for('user_dashboard'))
        
        # Mine block for this certificate hash
        try:
            block = blockchain.mine_block(file_hash)
            
            # Create certificate record
            certificate = Certificate(
                filename=filename,
                original_filename=file.filename,
                file_hash=file_hash,
                file_type=file_type,
                file_size=file_size,
                user_id=current_user.id,
                blockchain_block_id=block.id
            )
            
            db.session.add(certificate)
            db.session.commit()
            
            flash('Certificate uploaded and stored on blockchain successfully!', 'success')
        except Exception as e:
            # Clean up file if blockchain operation fails
            if os.path.exists(file_path):
                os.remove(file_path)
            flash(f'Error processing certificate: {str(e)}', 'error')
    else:
        flash('Invalid file type. Please upload PDF, JPG, or PNG files only.', 'error')
    
    return redirect(url_for('user_dashboard'))

@app.route('/user/generate_access_code/<int:cert_id>')
@login_required
def generate_access_code(cert_id):
    if not hasattr(current_user, 'username'):
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    certificate = Certificate.query.filter_by(id=cert_id, user_id=current_user.id).first()
    if not certificate:
        flash('Certificate not found', 'error')
        return redirect(url_for('user_dashboard'))
    
    # Deactivate any existing access codes for this certificate
    AccessCode.query.filter_by(certificate_id=cert_id, user_id=current_user.id).update({'is_active': False})
    
    # Generate new access code
    access_code = AccessCode(
        code=AccessCode.generate_code(),
        certificate_id=cert_id,
        user_id=current_user.id,
        expires_at=datetime.utcnow() + timedelta(hours=24)  # Valid for 24 hours
    )
    
    db.session.add(access_code)
    db.session.commit()
    
    flash(f'Access code generated: {access_code.code} (Valid for 24 hours)', 'success')
    return redirect(url_for('user_dashboard'))

# Company Authentication Routes
@app.route('/company/login', methods=['GET', 'POST'])
def company_login():
    if request.method == 'POST':
        company_name = request.form['company_name']
        password = request.form['password']
        
        company = Company.query.filter_by(company_name=company_name).first()
        
        if company and company.check_password(password):
            login_user(company)
            session['user_type'] = 'company'
            flash('Login successful!', 'success')
            return redirect(url_for('company_dashboard'))
        else:
            flash('Invalid company name or password', 'error')
    
    return render_template('company_login.html')

@app.route('/company/register', methods=['GET', 'POST'])
def company_register():
    if request.method == 'POST':
        company_name = request.form['company_name']
        email = request.form['email']
        contact_person = request.form['contact_person']
        password = request.form['password']
        
        # Check if company already exists
        if Company.query.filter_by(company_name=company_name).first():
            flash('Company name already exists', 'error')
            return render_template('company_register.html')
        
        if Company.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('company_register.html')
        
        # Create new company
        company = Company(
            company_name=company_name, 
            email=email, 
            contact_person=contact_person
        )
        company.set_password(password)
        
        db.session.add(company)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('company_login'))
    
    return render_template('company_register.html')

@app.route('/company/dashboard')
@login_required
def company_dashboard():
    if not hasattr(current_user, 'company_name'):  # Check if it's a company, not user
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    # Get search results if any
    search_query = request.args.get('search', '')
    users = []
    
    if search_query:
        users = User.query.filter(
            User.full_name.contains(search_query) | 
            User.username.contains(search_query)
        ).all()
    
    blockchain_stats = blockchain.get_blockchain_stats()
    
    return render_template('company_dashboard.html', 
                         users=users, 
                         search_query=search_query,
                         blockchain_stats=blockchain_stats)

@app.route('/company/search', methods=['POST'])
@login_required
def search_users():
    if not hasattr(current_user, 'company_name'):
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    search_query = request.form.get('search_query', '').strip()
    
    if not search_query:
        flash('Please enter a search term', 'warning')
        return redirect(url_for('company_dashboard'))
    
    return redirect(url_for('company_dashboard', search=search_query))

@app.route('/company/verify_certificate', methods=['POST'])
@login_required
def verify_certificate():
    if not hasattr(current_user, 'company_name'):
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    access_code = request.form.get('access_code', '').strip().upper()
    
    if not access_code:
        flash('Please enter an access code', 'warning')
        return redirect(url_for('company_dashboard'))
    
    # Find the access code
    code_obj = AccessCode.query.filter_by(code=access_code).first()
    
    if not code_obj or not code_obj.is_valid():
        flash('Invalid or expired access code', 'error')
        return redirect(url_for('company_dashboard'))
    
    return redirect(url_for('view_certificate', access_code=access_code))

@app.route('/certificate/<access_code>')
def view_certificate(access_code):
    # Find the access code
    code_obj = AccessCode.query.filter_by(code=access_code.upper()).first()
    
    if not code_obj or not code_obj.is_valid():
        flash('Invalid or expired access code', 'error')
        return redirect(url_for('index'))
    
    certificate = code_obj.certificate
    user = code_obj.user
    
    # Get blockchain verification
    blockchain_verification = blockchain.get_certificate_verification(certificate.file_hash)
    
    return render_template('certificate_view.html', 
                         certificate=certificate, 
                         user=user,
                         blockchain_verification=blockchain_verification,
                         access_code=access_code)

@app.route('/download_certificate/<access_code>')
def download_certificate(access_code):
    # Find the access code
    code_obj = AccessCode.query.filter_by(code=access_code.upper()).first()
    
    if not code_obj or not code_obj.is_valid():
        flash('Invalid or expired access code', 'error')
        return redirect(url_for('index'))
    
    certificate = code_obj.certificate
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], certificate.filename)
    
    if not os.path.exists(file_path):
        flash('Certificate file not found', 'error')
        return redirect(url_for('view_certificate', access_code=access_code))
    
    return send_file(file_path, as_attachment=True, download_name=certificate.original_filename)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user_type', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(413)
def file_too_large(error):
    flash('File too large. Maximum size is 16MB.', 'error')
    return redirect(request.url or url_for('index'))
