
import sqlite3
import hashlib
from datetime import datetime

class Database:
    def __init__(self, db_name='feedback_portal.db'):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        """Initialize database with tables and sample data"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL CHECK (role IN ('student', 'admin'))
            )
        ''')
        
        # Create feedback table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_username TEXT NOT NULL,
                feedback_text TEXT NOT NULL,
                rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
                submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_username) REFERENCES users(username)
            )
        ''')
        
        # Insert default users if they don't exist
        self.create_default_users(cursor)
        
        conn.commit()
        conn.close()
    
    def create_default_users(self, cursor):
        """Create default student and admin users"""
        default_users = [
            ('student1', 'password123', 'student'),
            ('admin', 'admin123', 'admin')
        ]
        
        for username, password, role in default_users:
            # Hash password for security
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            cursor.execute('''
                INSERT OR IGNORE INTO users (username, password, role)
                VALUES (?, ?, ?)
            ''', (username, hashed_password, role))
    
    def authenticate_user(self, username, password):
        """Authenticate user login"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute('''
            SELECT username, role FROM users 
            WHERE username = ? AND password = ?
        ''', (username, hashed_password))
        
        user = cursor.fetchone()
        conn.close()
        
        return user
    
    def submit_feedback(self, student_username, feedback_text, rating):
        """Submit student feedback"""
        if not feedback_text.strip():
            raise ValueError("Feedback text cannot be empty")
        
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO feedback (student_username, feedback_text, rating)
            VALUES (?, ?, ?)
        ''', (student_username, feedback_text.strip(), rating))
        
        conn.commit()
        conn.close()
        return True
    
    def get_all_feedback(self):
        """Get all feedback for admin view"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT f.id, f.student_username, f.feedback_text, f.rating, f.submission_date
            FROM feedback f
            ORDER BY f.submission_date DESC
        ''')
        
        feedback_list = cursor.fetchall()
        conn.close()
        
        return feedback_list