from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
import re
from encryption_utils import encrypt_file
from Crypto.Random import get_random_bytes
import base64

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

# MongoDB connection

client = MongoClient("mongodb+srv://<username>:<password>@cluster0.abcde.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client['user_db']
users_collection = db['users']
files_collection = db['files']

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
            # Clear cookies after successful login for security
            @app.after_request
            def clear_cookies(response):
                response.delete_cookie('session')
                return response
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
        files = request.files.getlist('files')
        key = get_random_bytes(16)  # AES-128 key, in production store/manage securely
        for file in files:
            file_data = file.read()
            encrypted_data = encrypt_file(file_data, key)
            try:
                files_collection.insert_one({
                    "username": session['user'],
                    "filename": file.filename,
                    "data": encrypted_data,
                    "key": base64.b64encode(key).decode('utf-8')  # storing key as base64 string (for demo only)
                })
            except Exception as e:
                return f"Error storing file {file.filename}: {str(e)}"
        return f"{len(files)} file(s) uploaded and encrypted successfully."
    return render_template('upload.html')

from bson.objectid import ObjectId
from flask import send_file
import io
from encryption_utils import decrypt_file

@app.route('/download')
def download_file():
    if 'user' not in session:
        return redirect(url_for('signin'))
    user_files = list(files_collection.find({"username": session['user']}))
    return render_template('download.html', files=user_files)

@app.route('/download/<file_id>')
def download_file_by_id(file_id):
    if 'user' not in session:
        return redirect(url_for('signin'))
    file_doc = files_collection.find_one({"_id": ObjectId(file_id), "username": session['user']})
    if not file_doc:
        return "File not found or access denied", 404
    encrypted_data = file_doc['data']
    key = base64.b64decode(file_doc['key'])
    decrypted_data = decrypt_file(encrypted_data, key)
    return send_file(
        io.BytesIO(decrypted_data),
        as_attachment=True,
        download_name=file_doc['filename']
    )

@app.route('/delete/<file_id>')
def delete_file(file_id):
    if 'user' not in session:
        return redirect(url_for('signin'))
    file_doc = files_collection.find_one({"_id": ObjectId(file_id), "username": session['user']})
    if not file_doc:
        return "File not found or access denied", 404
    files_collection.delete_one({"_id": ObjectId(file_id), "username": session['user']})
    return redirect(url_for('download_file'))

if __name__ == '__main__':
    app.run(debug=True)
