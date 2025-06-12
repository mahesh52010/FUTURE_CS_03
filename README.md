# File Upload/Download Portal with AES Encryption

## Project Overview

This project is a secure file upload and download platform built using Python Flask as the backend framework. It provides user authentication (signup and signin), encrypted file storage, and secure file retrieval. The platform ensures files are encrypted at rest and decrypted only when downloaded by the authorized user.

---

## Key Features

### User Authentication
- **Signup:** Users can create an account by providing a username, name, email, and password.
  - Passwords must meet complexity requirements (minimum length, uppercase letter, special character).
  - Usernames and emails are checked for uniqueness.
- **Signin:** Users can log in using their username or email along with their password.
- **Session Management:** User sessions are managed securely with session cookies. Cookies are cleared after login for enhanced security.

### File Upload
- Authenticated users can upload one or multiple files.
- Files are encrypted using AES-128 encryption with a randomly generated key per upload.
- The encrypted file data and the encryption key (encoded in base64) are stored securely in a MongoDB database.
- Each file is associated with the uploading user's username to enforce access control.

### File Download
- Users can view a list of their uploaded files.
- Files are decrypted on-the-fly when downloaded, using the stored encryption key.
- Only the owner of the file can download it.
- Users can delete their files from the database with a confirmation prompt.

---

## How It Works

1. **Signup and Signin:**
   - Users register via the signup page with validation on input fields.
   - Upon successful signup, users can log in via the signin page.
   - After login, a session is created and cookies are cleared for security.

2. **Uploading Files:**
   - Users navigate to the upload page.
   - Selected files are read and encrypted using AES-128 with a unique key.
   - Encrypted data and keys are stored in MongoDB along with metadata.

3. **Downloading Files:**
   - Users see a list of their files on the download page.
   - Clicking a file triggers decryption and download of the original file.
   - Users can also delete files, which removes them from the database.

---

## Dependencies

To run this project, ensure the following dependencies are installed:

- Python 3.8 or higher
- Flask
- PyCryptodome
- pymongo
- MongoDB (cloud or local instance)
- Other Python standard libraries: re, base64, io

---

## Installation and Setup

1. **Clone the repository:**

```bash
git clone <repository-url>
cd <repository-folder>
```

2. **Create and activate a Python virtual environment:**

```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. **Install required Python packages:**

```bash
pip install Flask pymongo pycryptodome
```

4. **Configure MongoDB connection:**

- Update the MongoDB connection string in `app_full.py` with your credentials.  
  Make sure to replace the placeholder URL with your actual MongoDB connection URI to enable database connectivity.

5. **Run the application:**

```bash
python app_full.py
```

6. **Access the application:**

- Open your browser and navigate to `http://127.0.0.1:5000`

---

## Usage

- **Signup:** Create a new user account.
- **Signin:** Log in with your credentials.
- **Dashboard:** Access upload and download options.
- **Upload:** Select files to upload; files will be encrypted and stored.
- **Download:** View your files, download decrypted versions, or delete files.

---

## Security Notes

- Passwords are stored in plaintext for demonstration purposes; in production, always hash passwords securely.
- Encryption keys are stored alongside encrypted data in the database for demo only; in production, use secure key management.
- The Flask development server is used; for production, deploy with a production-grade WSGI server.

---

## Testing

- Automated tests are included in the `tests` directory.
- Tests cover file upload, download, deletion, and access control.
- Run tests using:

```bash
python -m unittest discover tests
```

---

## WEBSITE LINK
You can test the website here
https://secure-file-upload-and-download-website.onrender.com



## License

This project is provided as-is for educational purposes.
