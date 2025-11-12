import unittest
import sys
import os
from datetime import datetime
import HtmlTestRunner

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import test modules
from test_login import LoginTestCase
from test_feedback import FeedbackTestCase  
from test_admin import AdminTestCase

def create_test_suite():
    """Create test suite with all test cases"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    print("Loading test cases...")
    
    # Load login tests
    login_tests = loader.loadTestsFromTestCase(LoginTestCase)
    suite.addTests(login_tests)
    print(f"Loaded {login_tests.countTestCases()} login tests")
    
    # Load feedback tests
    feedback_tests = loader.loadTestsFromTestCase(FeedbackTestCase)
    suite.addTests(feedback_tests)
    print(f"Loaded {feedback_tests.countTestCases()} feedback tests")
    
    # Load admin tests
    admin_tests = loader.loadTestsFromTestCase(AdminTestCase)
    suite.addTests(admin_tests)
    print(f"Loaded {admin_tests.countTestCases()} admin tests")
    
    print(f"Total tests loaded: {suite.countTestCases()}")
    return suite

def main():
    """Main test runner function"""
    # Create reports directory if it doesn't exist
    reports_dir = os.path.join(os.path.dirname(__file__), '..', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    # Create test suite
    suite = create_test_suite()
    
    # Configure HTML test runner with encoding fix
    runner = HtmlTestRunner.HTMLTestRunner(
        output=reports_dir,
        report_name=f'test_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
        report_title='Student Feedback Portal - Test Report',
        descriptions=True,
        verbosity=2,
        # Add encoding parameter to handle Unicode issues
        combine_reports=True,
        add_timestamp=True
    )
    
    # Also create a console runner for immediate feedback
    console_runner = unittest.TextTestRunner(verbosity=1)
    
    print("\nRunning Student Feedback Portal Test Suite...")
    print("-" * 50)
    
    # Run tests with console output first
    print("Console Test Results:")
    console_result = console_runner.run(suite)
    
    print("\nGenerating HTML Report...")
    
    # Try to generate HTML report with error handling
    try:
        # Create a new test suite for HTML runner (since suite may be consumed)
        html_suite = create_test_suite()
        html_result = runner.run(html_suite)
        print(f"HTML report generated successfully in: {reports_dir}")
    except Exception as e:
        print(f"HTML report generation failed: {e}")
        print("Using console results for summary...")
        html_result = console_result
    
    # Use console results for summary
    result = console_result
    
    print("\n" + "=" * 50)
    print("TEST EXECUTION SUMMARY")
    print("=" * 50)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.testsRun > 0:
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100)
        print(f"Success Rate: {success_rate:.1f}%")
    else:
        print("Success Rate: 0.0%")
    
    # Show failures and errors
    if result.failures:
        print(f"\nFAILURES ({len(result.failures)}):")
        for i, (test, error) in enumerate(result.failures, 1):
            print(f"  {i}. {test}")
            print(f"     {error.split(chr(10))[0]}")
    
    if result.errors:
        print(f"\nERRORS ({len(result.errors)}):")
        for i, (test, error) in enumerate(result.errors, 1):
            print(f"  {i}. {test}")
            print(f"     {error.split(chr(10))[0]}")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    try:
        success = main()
        print(f"\nTest execution {'PASSED' if success else 'FAILED'}")
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Test runner failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)