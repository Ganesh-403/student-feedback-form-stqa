import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app

class FeedbackTestCase(unittest.TestCase):
    """Test cases for feedback functionality using Flask test client"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        print("Setting up FeedbackTestCase...")
        cls.app = app
        cls.app.config['TESTING'] = True
        cls.client = cls.app.test_client()
        print("FeedbackTestCase setup complete!")
    
    def setUp(self):
        """Login as student before each test"""
        self.client.post('/login', data={
            'username': 'student1',
            'password': 'password123'
        })
    
    def tearDown(self):
        """Logout after each test"""
        self.client.get('/logout')
    
    def test_feedback_page_loads(self):
        """Test that feedback page loads correctly"""
        response = self.client.get('/feedback')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Submit Your Feedback', response.data)
        self.assertIn(b'feedback_text', response.data)
        self.assertIn(b'rating', response.data)
    
    def test_valid_feedback_submission(self):
        """Test successful feedback submission"""
        response = self.client.post('/feedback', data={
            'feedback_text': 'This is a test feedback. The course was excellent and very informative.',
            'rating': '5'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Feedback submitted successfully', response.data)
    
    def test_empty_feedback_submission(self):
        """Test feedback submission with empty text"""
        response = self.client.post('/feedback', data={
            'feedback_text': '',
            'rating': '4'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Should show error or stay on same page
        self.assertIn(b'Submit Your Feedback', response.data)
    
    def test_no_rating_submission(self):
        """Test feedback submission without rating"""
        response = self.client.post('/feedback', data={
            'feedback_text': 'This is good feedback but no rating selected',
            'rating': ''
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Should show error or stay on same page
        self.assertIn(b'Submit Your Feedback', response.data)
    
    def test_multiple_feedback_submissions(self):
        """Test submitting multiple feedback entries"""
        # First submission
        response1 = self.client.post('/feedback', data={
            'feedback_text': 'First feedback submission - very good course content',
            'rating': '4'
        }, follow_redirects=True)
        self.assertEqual(response1.status_code, 200)
        
        # Second submission
        response2 = self.client.post('/feedback', data={
            'feedback_text': 'Second feedback - excellent instructor teaching methods',
            'rating': '5'
        }, follow_redirects=True)
        self.assertEqual(response2.status_code, 200)
        self.assertIn(b'Feedback submitted successfully', response2.data)
    
    def test_feedback_requires_login(self):
        """Test that feedback page requires login"""
        # Logout first
        self.client.get('/logout')
        
        # Try to access feedback page
        response = self.client.get('/feedback')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)
    
    def test_feedback_validation(self):
        """Test feedback form validation"""
        # Test with short feedback
        response = self.client.post('/feedback', data={
            'feedback_text': 'Bad',
            'rating': '2'
        }, follow_redirects=True)
        # Server-side validation should handle this
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()