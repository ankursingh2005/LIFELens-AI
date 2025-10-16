import sqlite3
import os
from datetime import datetime
from auth import hash_password, verify_password

DB_PATH = "lifelens_ai.db"

def get_connection():
    """Get database connection"""
    return sqlite3.connect(DB_PATH)

def init_database():
    """Initialize the database with required tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Demographics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS demographics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            weight REAL,
            height REAL,
            daily_water_intake REAL,
            medical_history TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_email) REFERENCES users (email)
        )
    ''')
    
    # Uploads table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_type TEXT NOT NULL,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            analysis_status TEXT DEFAULT 'pending',
            FOREIGN KEY (user_email) REFERENCES users (email)
        )
    ''')
    
    # Reports table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT NOT NULL,
            upload_id INTEGER,
            report_type TEXT NOT NULL,
            report_content TEXT,
            generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_email) REFERENCES users (email),
            FOREIGN KEY (upload_id) REFERENCES uploads (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def create_user(email, password, full_name):
    """Create a new user"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        password_hash = hash_password(password)
        
        cursor.execute(
            "INSERT INTO users (email, password_hash, full_name) VALUES (?, ?, ?)",
            (email, password_hash, full_name)
        )
        
        conn.commit()
        conn.close()
        return True, "User created successfully"
    
    except sqlite3.IntegrityError:
        return False, "Email already exists"
    except Exception as e:
        return False, f"Error creating user: {str(e)}"

def verify_user(email, password):
    """Verify user credentials"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT password_hash FROM users WHERE email = ?", (email,))
        result = cursor.fetchone()
        conn.close()
        
        if result and verify_password(password, result[0]):
            return True
        return False
    
    except Exception as e:
        print(f"Error verifying user: {str(e)}")
        return False

def save_demographics(user_email, demographics_data):
    """Save or update user demographics"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Check if demographics already exist
        cursor.execute("SELECT id FROM demographics WHERE user_email = ?", (user_email,))
        existing = cursor.fetchone()
        
        if existing:
            # Update existing record
            cursor.execute('''
                UPDATE demographics 
                SET age = ?, gender = ?, weight = ?, height = ?, 
                    daily_water_intake = ?, medical_history = ?, updated_at = ?
                WHERE user_email = ?
            ''', (
                demographics_data['age'],
                demographics_data['gender'],
                demographics_data['weight'],
                demographics_data['height'],
                demographics_data['daily_water_intake'],
                demographics_data['medical_history'],
                datetime.now(),
                user_email
            ))
        else:
            # Insert new record
            cursor.execute('''
                INSERT INTO demographics 
                (user_email, age, gender, weight, height, daily_water_intake, medical_history)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                user_email,
                demographics_data['age'],
                demographics_data['gender'],
                demographics_data['weight'],
                demographics_data['height'],
                demographics_data['daily_water_intake'],
                demographics_data['medical_history']
            ))
        
        conn.commit()
        conn.close()
        return True, "Demographics saved successfully"
    
    except Exception as e:
        return False, f"Error saving demographics: {str(e)}"

def get_user_demographics(user_email):
    """Get user demographics"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT age, gender, weight, height, daily_water_intake, medical_history
            FROM demographics WHERE user_email = ?
        ''', (user_email,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'age': result[0],
                'gender': result[1],
                'weight': result[2],
                'height': result[3],
                'daily_water_intake': result[4],
                'medical_history': result[5]
            }
        return None
    
    except Exception as e:
        print(f"Error getting demographics: {str(e)}")
        return None

def save_upload(user_email, filename, file_path, file_type):
    """Save upload information"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO uploads (user_email, filename, file_path, file_type)
            VALUES (?, ?, ?, ?)
        ''', (user_email, filename, file_path, file_type))
        
        upload_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return upload_id
    
    except Exception as e:
        print(f"Error saving upload: {str(e)}")
        return None

def get_user_uploads(user_email):
    """Get all uploads for a user"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, filename, file_type, upload_date, analysis_status
            FROM uploads WHERE user_email = ?
            ORDER BY upload_date DESC
        ''', (user_email,))
        
        results = cursor.fetchall()
        conn.close()
        
        uploads = []
        for row in results:
            uploads.append({
                'id': row[0],
                'filename': row[1],
                'file_type': row[2],
                'upload_date': row[3],
                'analysis_status': row[4]
            })
        
        return uploads
    
    except Exception as e:
        print(f"Error getting uploads: {str(e)}")
        return []

def save_report(user_email, upload_id, report_type, report_content):
    """Save a generated report"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO reports (user_email, upload_id, report_type, report_content)
            VALUES (?, ?, ?, ?)
        ''', (user_email, upload_id, report_type, report_content))
        
        report_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return report_id
    
    except Exception as e:
        print(f"Error saving report: {str(e)}")
        return None

def get_user_reports(user_email):
    """Get all reports for a user"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT r.id, r.report_type, r.report_content, r.generated_at, u.filename
            FROM reports r
            LEFT JOIN uploads u ON r.upload_id = u.id
            WHERE r.user_email = ?
            ORDER BY r.generated_at DESC
        ''', (user_email,))
        
        results = cursor.fetchall()
        conn.close()
        
        reports = []
        for row in results:
            reports.append({
                'id': row[0],
                'report_type': row[1],
                'report_content': row[2],
                'generated_at': row[3],
                'filename': row[4] if row[4] else 'General Report'
            })
        
        return reports
    
    except Exception as e:
        print(f"Error getting reports: {str(e)}")
        return []
