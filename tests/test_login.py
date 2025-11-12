
import unittest
import time
import sys
import os
import threading

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app

class LoginTestCase(unittest.TestCase):
    """Test cases for login functionality using Flask test client"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        print("Setting up LoginTestCase...")
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
        print("LoginTestCase setup complete!")
    
    def test_login_page_loads(self):
        """Test that login page loads correctly"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
        self.assertIn(b'username', response.data)
        self.assertIn(b'password', response.data)
    
    def test_home_redirects_to_login(self):
        """Test that home page redirects to login"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)
    
    def test_valid_student_login(self):
        """Test successful student login"""
        response = self.client.post('/login', data={
            'username': 'student1',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Submit Your Feedback', response.data)
    
    def test_valid_admin_login(self):
        """Test successful admin login"""
        response = self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin Dashboard', response.data)
    
    def test_invalid_login_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post('/login', data={
            'username': 'invalid_user',
            'password': 'invalid_password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)
    
    def test_logout_functionality(self):
        """Test user logout"""
        # Login first
        self.client.post('/login', data={
            'username': 'student1',
            'password': 'password123'
        })
        
        # Then logout
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'logged out', response.data)

if __name__ == '__main__':
    unittest.main()
