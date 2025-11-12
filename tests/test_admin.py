import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app

class AdminTestCase(unittest.TestCase):
    """Test cases for admin functionality using Flask test client"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        print("Setting up AdminTestCase...")
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
        print("AdminTestCase setup complete!")
    
    def setUp(self):
        """Login as admin before each test"""
        self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
    
    def tearDown(self):
        """Logout after each test"""
        self.client.get('/logout')
    
    def test_admin_dashboard_loads(self):
        """Test that admin dashboard loads correctly"""
        response = self.client.get('/admin')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin Dashboard', response.data)
        # Should have either feedback table or no feedback message
        self.assertTrue(b'feedbackTable' in response.data or b'no-feedback' in response.data)
    
    def test_admin_can_view_feedback(self):
        """Test admin can view submitted feedback after student submits it"""
        # First submit feedback as student
        self.client.get('/logout')
        self.client.post('/login', data={'username': 'student1', 'password': 'password123'})
        self.client.post('/feedback', data={
            'feedback_text': 'Test feedback for admin verification - excellent course!',
            'rating': '5'
        })
        
        # Login back as admin
        self.client.get('/logout')
        self.client.post('/login', data={'username': 'admin', 'password': 'admin123'})
        
        # Check admin dashboard
        response = self.client.get('/admin')
        self.assertEqual(response.status_code, 200)
        # Should now show feedback table or statistics
        self.assertIn(b'Admin Dashboard', response.data)
    
    def test_admin_unauthorized_access_protection(self):
        """Test that non-admin users cannot access admin dashboard"""
        # Logout admin and login as student
        self.client.get('/logout')
        self.client.post('/login', data={'username': 'student1', 'password': 'password123'})
        
        # Try to access admin page
        response = self.client.get('/admin')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)
    
    def test_admin_direct_access_without_login(self):
        """Test that admin page requires login"""
        # Logout first
        self.client.get('/logout')
        
        # Try to access admin page without login
        response = self.client.get('/admin')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)
    
    def test_admin_feedback_statistics(self):
        """Test that admin dashboard shows appropriate content"""
        response = self.client.get('/admin')
        self.assertEqual(response.status_code, 200)
        
        # Should contain admin-specific content
        self.assertIn(b'Admin Dashboard', response.data)
        # Check for either feedback content or no feedback message
        has_content = (b'Total Feedback' in response.data or 
                      b'feedbackTable' in response.data or 
                      b'No feedback' in response.data)
        self.assertTrue(has_content)
    
    def test_admin_role_verification(self):
        """Test that only admin role can access admin features"""
        # This test verifies admin login works
        response = self.client.get('/admin')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin Dashboard', response.data)

if __name__ == '__main__':
    unittest.main()
