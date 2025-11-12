# Student Feedback Portal

A complete web-based student feedback system with comprehensive automated testing suite.

## Features

- **Student Portal**: Students can log in and submit feedback with ratings (1-5)
- **Admin Dashboard**: Admins can view all submitted feedback with statistics
- **User Authentication**: Role-based access control (student/admin)
- **Data Validation**: Both client-side and server-side validation
- **Automated Testing**: Comprehensive test suite with HTML reports
- **Responsive Design**: Works on desktop and mobile devices

## Technology Stack

- **Backend**: Python Flask 2.3.3
- **Frontend**: HTML5, CSS3, JavaScript (ES6)
- **Database**: SQLite
- **Testing**: Python unittest framework with Flask test client
- **Reporting**: Custom HTML test reports
- **Styling**: Custom CSS with responsive design

## Project Structure

```
student_feedback_portal/
├── app.py                 # Main Flask application
├── database.py           # Database operations
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
├── feedback_portal.db   # SQLite database (auto-generated)
├── static/              # Static assets
│   ├── style.css        # Application styling
│   └── script.js        # Frontend JavaScript
├── templates/           # HTML templates
│   ├── base.html        # Base template
│   ├── login.html       # Login page
│   ├── feedback.html    # Student feedback form
│   └── admin.html       # Admin dashboard
├── tests/              # Automated test suite
│   ├── __init__.py      # Test package init
│   ├── test_runner.py   # Main test runner
│   ├── test_login.py    # Login functionality tests (6 tests)
│   ├── test_feedback.py # Feedback submission tests (7 tests)
│   └── test_admin.py    # Admin functionality tests (6 tests)
└── reports/            # Generated test reports
    └── test_report_*.html
```

## Quick Start

### 1. Setup Environment

```bash
# Clone or create project directory
mkdir student_feedback_portal
cd student_feedback_portal

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

### 3. Default User Accounts

- **Student**: 
  - Username: `student1`
  - Password: `password123`
- **Admin**: 
  - Username: `admin`
  - Password: `admin123`

### 4. Run Automated Tests

```bash
cd tests
python test_runner.py
```

Test reports will be generated in the `reports/` directory.

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('student', 'admin'))
);
```

### Feedback Table
```sql
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_username TEXT NOT NULL,
    feedback_text TEXT NOT NULL,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    submission_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_username) REFERENCES users(username)
);
```

## Testing

The project includes a comprehensive test suite with **19 tests** covering all functionality:

### Test Categories

- **Login Tests (6 tests)**:
  - Page loading and form validation
  - Valid student/admin authentication
  - Invalid credential handling
  - Logout functionality

- **Feedback Tests (7 tests)**:
  - Form loading and element validation
  - Valid feedback submission
  - Empty/invalid input handling
  - Multiple submission scenarios
  - Access control verification

- **Admin Tests (6 tests)**:
  - Dashboard loading and content
  - Feedback viewing capabilities
  - Access control and security
  - Role-based authorization

### Running Specific Tests

```bash
# Run only login tests
python -m unittest tests.test_login -v

# Run only feedback tests  
python -m unittest tests.test_feedback -v

# Run only admin tests
python -m unittest tests.test_admin -v

# Run all tests with detailed output
python tests/test_runner.py
```

### Test Reports

- **Console Output**: Immediate feedback during test execution
- **HTML Reports**: Detailed reports generated in `reports/` directory
- **Coverage**: 100% functionality coverage with edge case testing

## Application Features

### Student Features
- **Login System**: Secure authentication with session management
- **Feedback Form**: Text input with 1-5 star rating system
- **Validation**: Client-side and server-side input validation
- **Success Messages**: Confirmation of successful submissions
- **Responsive Design**: Works on all device sizes

### Admin Features
- **Dashboard**: Overview of all submitted feedback
- **Statistics**: Total feedback count and summary information
- **Table View**: Sortable feedback table with student details
- **Security**: Role-based access with unauthorized access prevention
- **Real-time Data**: Live updates when new feedback is submitted

### Security Features
- **Password Hashing**: SHA-256 encryption for user passwords
- **Session Management**: Secure session handling with Flask sessions
- **Role-based Access**: Different permissions for students and admins
- **Input Validation**: XSS and injection prevention
- **Access Control**: Unauthorized access prevention

## API Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|---------|
| GET | `/` | Home page (redirects to login) | Public |
| GET/POST | `/login` | User authentication | Public |
| GET | `/logout` | User logout | Authenticated |
| GET/POST | `/feedback` | Student feedback form | Student only |
| GET | `/admin` | Admin dashboard | Admin only |

## Error Handling

The application includes comprehensive error handling:

- **Input Validation**: Both client-side (JavaScript) and server-side (Python)
- **Database Errors**: Graceful handling of database connection issues
- **Authentication Errors**: Clear error messages for login failures
- **Access Control**: Proper redirection for unauthorized access attempts
- **Form Validation**: Real-time validation with user-friendly messages

## Development

### Adding New Features

1. **Database Changes**: Update `database.py` with new schema
2. **Routes**: Add new Flask routes in `app.py`
3. **Templates**: Create/update HTML templates in `templates/`
4. **Styling**: Update CSS in `static/style.css`
5. **JavaScript**: Add functionality in `static/script.js`
6. **Tests**: Add corresponding tests in `tests/` directory

### Code Structure

- **MVC Pattern**: Model (database.py), View (templates), Controller (app.py)
- **Separation of Concerns**: Clear separation between frontend and backend
- **Modular Design**: Each component has a specific responsibility
- **Error Handling**: Comprehensive error handling throughout the application

## Deployment

### Local Development
The application is configured for local development with debug mode enabled.

### Production Deployment
For production deployment, make these changes in `app.py`:

```python
# Change secret key
app.secret_key = os.environ.get('SECRET_KEY', 'your-production-secret-key')

# Disable debug mode
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
```

## Troubleshooting

### Common Issues

1. **Database Issues**
   - Delete `feedback_portal.db` to reset database
   - Check database permissions

2. **Test Failures**
   - Ensure Flask app is not running on test ports (5001-5003)
   - Check Python version compatibility (3.7+)

3. **Port Conflicts**
   - Change port in `app.py` if 5000 is in use
   - Update test ports in test files if needed

### Getting Help

1. Check the error logs in the console
2. Verify all dependencies are installed: `pip list`
3. Ensure correct Python version: `python --version`
4. Review test output for specific error details

## Performance

- **Database**: SQLite for development (easily replaceable with PostgreSQL/MySQL)
- **Caching**: Session-based caching for user data
- **Frontend**: Optimized CSS and JavaScript with minimal dependencies
- **Testing**: Fast test execution with Flask test client (no browser overhead)

## License

This project is for educational purposes. Feel free to modify and extend for your needs.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite to ensure all tests pass
6. Submit a pull request

## Version History

- **v1.0**: Initial release with basic functionality
- **v1.1**: Added comprehensive test suite
- **v1.2**: Improved error handling and validation
- **v1.3**: Enhanced UI/UX and responsive design
- **v1.4**: Added HTML test reporting and documentation