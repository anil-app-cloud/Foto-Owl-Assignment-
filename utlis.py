from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from functools import wraps
from datetime import datetime
from models import mysql

# Database Utility Function
def get_cursor():
    """Get a database cursor for executing queries."""
    return mysql.connection.cursor()

# Error Response
def error_response(message, status_code=400):
    """Return a standardized error response."""
    return jsonify({"error": message}), status_code

# Admin Check Decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_jwt_identity()
        if not user or not user.get('is_admin'):
            return error_response("Admin access required", 403)
        return f(*args, **kwargs)
    return decorated_function

# Validate Date Format
def validate_date_format(date_string):
    """Validate if a date string is in the correct format (YYYY-MM-DD)."""
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False

# Check Book Availability
def is_book_available(book_id, start_date, end_date):
    """
    Check if a book is available for the requested period.
    A book is unavailable if it has already been borrowed during the requested dates.
    """
    cursor = get_cursor()
    query = """
        SELECT COUNT(*) FROM BorrowRequests 
        WHERE book_id = %s AND status = 'Approved' 
        AND ((start_date BETWEEN %s AND %s) OR (end_date BETWEEN %s AND %s) OR (start_date <= %s AND end_date >= %s))
    """
    cursor.execute(query, (book_id, start_date, end_date, start_date, end_date, start_date, end_date))
    count = cursor.fetchone()[0]
    return count == 0

# Validate Request Payload
def validate_request_payload(payload, required_keys):
    """
    Check if the payload contains all the required keys.
    Returns a tuple (is_valid, missing_keys).
    """
    missing_keys = [key for key in required_keys if key not in payload]
    if missing_keys:
        return False, missing_keys
    return True, None

# Export Borrow History to CSV
def export_borrow_history_to_csv(user_id):
    """
    Export a user's borrow history to a CSV file.
    """
    import csv
    from io import StringIO
    cursor = get_cursor()
    query = """
        SELECT Books.title, Books.author, BorrowRequests.start_date, BorrowRequests.end_date, BorrowRequests.status 
        FROM BorrowRequests 
        JOIN Books ON BorrowRequests.book_id = Books.book_id 
        WHERE BorrowRequests.user_id = %s
    """
    cursor.execute(query, (user_id,))
    borrow_history = cursor.fetchall()

    # Create CSV content
    csv_output = StringIO()
    writer = csv.writer(csv_output)
    writer.writerow(['Title', 'Author', 'Start Date', 'End Date', 'Status'])
    writer.writerows(borrow_history)
    csv_output.seek(0)
    return csv_output.getvalue()
