from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from database import Database
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

# Initialize database
db = Database()

@app.route('/')
def index():
    """Home page - redirect to login"""
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page for students and admin"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            user = db.authenticate_user(username, password)
            
            if user:
                session['username'] = user[0]
                session['role'] = user[1]
                
                # Redirect based on role
                if user[1] == 'admin':
                    return redirect(url_for('admin_dashboard'))
                else:
                    return redirect(url_for('feedback_form'))
            else:
                flash('Invalid username or password', 'error')
                
        except Exception as e:
            flash('Login error occurred', 'error')
            print(f"Login error: {e}")
    
    return render_template('login.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback_form():
    """Student feedback submission page"""
    if 'username' not in session or session.get('role') != 'student':
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        feedback_text = request.form['feedback_text']
        rating = request.form['rating']
        
        try:
            rating = int(rating)
            db.submit_feedback(session['username'], feedback_text, rating)
            flash('Feedback submitted successfully!', 'success')
            return redirect(url_for('feedback_form'))
            
        except ValueError as e:
            flash(str(e), 'error')
        except Exception as e:
            flash('Error submitting feedback', 'error')
            print(f"Feedback submission error: {e}")
    
    return render_template('feedback.html', username=session['username'])

@app.route('/admin')
def admin_dashboard():
    """Admin dashboard to view all feedback"""
    if 'username' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    
    try:
        feedback_list = db.get_all_feedback()
        return render_template('admin.html', feedback_list=feedback_list)
    except Exception as e:
        flash('Error loading feedback', 'error')
        print(f"Admin dashboard error: {e}")
        return render_template('admin.html', feedback_list=[])

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('login.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    flash('An internal error occurred', 'error')
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Ensure database is initialized
    db.init_database()
    app.run(debug=True, port=5000)