import unittest
import os
from app_full import app, files_collection, users_collection
from bson.objectid import ObjectId
from base64 import b64decode

class FileIntegritySecurityTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Create a test user
        self.test_user = {
            "username": "testuser",
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "Test@1234"
        }
        users_collection.insert_one(self.test_user)

        # Login the test user
        response = self.app.post('/signin', data={
            'username_or_email': self.test_user['username'],
            'password': self.test_user['password']
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        # Remove test user and files
        users_collection.delete_one({"username": self.test_user['username']})
        files_collection.delete_many({"username": self.test_user['username']})

    def test_file_upload_download_delete(self):
        # Upload a file
        data = {
            'files': (open(__file__, 'rb'), 'test_file.py')
        }
        response = self.app.post('/upload', data=data, content_type='multipart/form-data', follow_redirects=True)
        self.assertIn(b'file(s) uploaded and encrypted successfully', response.data)

        # Check file stored in DB
        stored_file = files_collection.find_one({"username": self.test_user['username'], "filename": 'test_file.py'})
        self.assertIsNotNone(stored_file)
        self.assertIn('data', stored_file)
        self.assertIn('key', stored_file)

        # Download the file
        file_id = str(stored_file['_id'])
        response = self.app.get(f'/download/{file_id}')
        self.assertEqual(response.status_code, 200)
        # Check content matches original file content
        with open(__file__, 'rb') as f:
            original_content = f.read()
        self.assertEqual(response.data, original_content)

        # Delete the file
        response = self.app.get(f'/delete/{file_id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        deleted_file = files_collection.find_one({"_id": ObjectId(file_id)})
        self.assertIsNone(deleted_file)

    def test_unauthorized_access(self):
        # Logout user by clearing session cookie
        with self.app.session_transaction() as sess:
            sess.clear()

        # Try to access download page without login
        response = self.app.get('/download')
        self.assertEqual(response.status_code, 302)  # redirect to signin

        # Try to delete a file without login
        response = self.app.get('/delete/1234567890abcdef12345678')
        self.assertEqual(response.status_code, 302)  # redirect to signin

if __name__ == '__main__':
    unittest.main()
