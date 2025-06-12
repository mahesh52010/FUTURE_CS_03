from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# MongoDB connection
client = MongoClient("mongodb+srv://maheshyandrapu78:Mahesh%401234@mahesh.zit48.mongodb.net/?retryWrites=true&w=majority&appName=Mahesh")
db = client['user_db']
users_collection = db['users']

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        error = None

        if not username or len(username) < 6:
            error = "Username must be at least 6 characters long."
        elif not email or not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            error = "Invalid email format."
        elif not password or len(password) < 8:
            error = "Password must be at least 8 characters long."
        elif not re.search(r'[A-Z]', password):
            error = "Password must contain at least one uppercase letter."
        elif not re.search(r'[\W_]', password):
            error = "Password must contain at least one special character."
        elif password != confirm_password:
            error = "Password and Confirm Password do not match."
        elif users_collection.find_one({"username": username}):
            error = "Username already exists."
        elif users_collection.find_one({"email": email}):
            error = "Email already registered."

        if error:
            return render_template('signup.html', error=error, username=username, name=name, email=email)
        
        # Store user in DB
        users_collection.insert_one({
            "username": username,
            "name": name,
            "email": email,
            "password": password  # Note: In production, passwords should be hashed!
        })

        return redirect(url_for('signin'))
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username_or_email = request.form.get('username_or_email')
        password = request.form.get('password')

        user = users_collection.find_one({
            "$or": [
                {"username": username_or_email},
                {"email": username_or_email}
            ],
            "password": password
        })

        if user:
            session['user'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid username/email or password."
            return render_template('signin.html', error=error)

    return render_template('signin.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('signin'))
    return render_template('dashboard.html', username=session['user'])

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'user' not in session:
        return redirect(url_for('signin'))
    if request.method == 'POST':
        # Placeholder for handling uploaded files
        files = request.files.getlist('files')
        # For now, just acknowledge the number of files uploaded
        return f"{len(files)} file(s) uploaded successfully."
    return render_template('upload.html')

@app.route('/download')
def download_file():
    if 'user' not in session:
        return redirect(url_for('signin'))
    # Placeholder for download functionality
    return "Download file page - to be implemented"

if __name__ == '__main__':
    app.run(debug=True)
