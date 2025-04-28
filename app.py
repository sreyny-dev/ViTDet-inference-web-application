import os
import subprocess
import json
import hashlib
from flask import Flask, render_template, request, send_file, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'your-secret-key'  

# Configure upload and output directories
UPLOAD_FOLDER = 'demo/data'
OUTPUT_FOLDER = 'outputs/vis'
USERS_FILE = 'templates/users/users.txt'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def hash_password(password):
    """Create a secure hash of the password."""
    if not password:
        raise ValueError("Password cannot be None or empty")
    return hashlib.sha256(str(password).encode()).hexdigest()

def save_user(email, password, name):
    """Save user to text file."""
    if not email or not password:
        raise ValueError("Email and password are required")
    
    with open(USERS_FILE, 'a') as f:
        user_data = {
            'email': email,
            'password': hash_password(password),
            'name': name or email.split('@')[0]
        }
        f.write(json.dumps(user_data) + '\n')

def find_user(email, password):
    """Find user in text file."""
    # Validate inputs
    if not email or not password:
        return None
    
    if not os.path.exists(USERS_FILE):
        return None
    
    try:
        hashed_password = hash_password(password)
    except ValueError:
        return None
    
    with open(USERS_FILE, 'r') as f:
        for line in f:
            try:
                user = json.loads(line.strip())
                if user['email'] == email and user['password'] == hashed_password:
                    return user
            except json.JSONDecodeError:
                continue
    return None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        
        # Validate inputs
        if not email or not password:
            return render_template('login.html', error='Email and password are required')
        
        user = find_user(email, password)
        if user:
            # Store user info in session
            session['user'] = {
                'email': user['email'],
                'name': user.get('name', email.split('@')[0])
            }
            # Redirect to index page for image upload
            return redirect(url_for('upload_file'))
        
        # Login failed
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        name = request.form.get('name', '').strip()
        
        # Basic validation
        if not email or not password:
            return render_template('signup.html', error='Email and password are required')
        
        # Check if user already exists
        if find_user(email, password):
            return render_template('signup.html', error='User already exists')
        
        try:
            # Save new user
            save_user(email, password, name)
        except ValueError as e:
            return render_template('signup.html', error=str(e))
        
        # Automatically log in the user
        session['user'] = {
            'email': email,
            'name': name or email.split('@')[0]
        }
        
        return redirect(url_for('upload_file'))
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # Check if user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part', 400
        file = request.files['file']
        
        if file.filename == '':
            return 'No selected file', 400
        
        if file and allowed_file(file.filename):
            # Get file extension
            file_ext = os.path.splitext(file.filename)[1]
            
            # Create a unique filename based on original filename
            unique_filename = f"{os.path.splitext(file.filename)[0]}{file_ext}"
            
            # Save the file with the unique filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(filepath)
            
            # Run inference command with the unique filename
            try:
                subprocess.run([
                    'python', 'demo/image_demo.py', 
                    filepath, 
                    'projects/ViTDet/configs/vitdet_mask-rcnn_vit-b-mae_lsj-100e.py', 
                    '--weights', 'vitdet_mask-rcnn_vit-b-mae_lsj-100e_20230328_153519-e15fe294.pth', 
                    '--device', 'cpu'
                ], check=True)
            except subprocess.CalledProcessError as e:
                return f'Inference failed: {str(e)}', 500
            
            # Create output filename with the same unique identifier
            output_filename = f"{os.path.splitext(file.filename)[0]}{file_ext}"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
            if os.path.exists(output_path):
                # Store the output filename in session
                session['output_filename'] = output_filename
                return render_template('index.html', 
                                     image_path='/get_output_image', 
                                     original_filename=file.filename,
                                     user=session['user'])
            else:
                return 'Output image not generated', 500
    
    return render_template('index.html', user=session['user'])

@app.route('/get_output_image')
def get_output_image():
    # Check if user is logged in
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Retrieve the output filename from session
    output_filename = session.get('output_filename')
    if not output_filename:
        return 'No output image specified', 404
    
    # Construct the full path to the output image
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
    
    if os.path.exists(output_path):
        return send_file(output_path, mimetype='image/png')
    else:
        return 'Output image not found', 404

if __name__ == '__main__':
    # Ensure upload and output directories exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    app.run(debug=True)