"""
CodeRefine - Database Module
Handles SQLite operations for user authentication and review history.
"""

import sqlite3
import hashlib
import os
from datetime import datetime

DB_PATH = "coderefine.db"


def get_connection():
    """Get SQLite database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables."""
    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Review history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS review_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            language TEXT NOT NULL,
            code_snippet TEXT NOT NULL,
            review_result TEXT,
            bugs_count INTEGER DEFAULT 0,
            performance_score INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password: str) -> str:
    """Hash password using SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(username: str, email: str, password: str) -> tuple[bool, str]:
    """Create a new user. Returns (success, message)."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        password_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash)
        )
        conn.commit()
        return True, "Account created successfully!"
    except sqlite3.IntegrityError as e:
        if "username" in str(e):
            return False, "Username already exists."
        elif "email" in str(e):
            return False, "Email already registered."
        return False, "Registration failed."
    finally:
        conn.close()


def authenticate_user(username: str, password: str) -> dict | None:
    """Authenticate user. Returns user dict or None."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        password_hash = hash_password(password)
        cursor.execute(
            "SELECT id, username, email, created_at FROM users WHERE username=? AND password_hash=?",
            (username, password_hash)
        )
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    finally:
        conn.close()


def save_review(user_id: int, language: str, code: str, review: str, bugs: int, perf_score: int):
    """Save a code review to history."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO review_history (user_id, language, code_snippet, review_result, bugs_count, performance_score)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, language, code[:500], review[:2000], bugs, perf_score)
        )
        conn.commit()
    finally:
        conn.close()


def get_user_history(user_id: int, limit: int = 10) -> list:
    """Get review history for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """SELECT language, code_snippet, bugs_count, performance_score, created_at
               FROM review_history WHERE user_id=? ORDER BY created_at DESC LIMIT ?""",
            (user_id, limit)
        )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


def get_user_stats(user_id: int) -> dict:
    """Get aggregate stats for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """SELECT COUNT(*) as total_reviews, SUM(bugs_count) as total_bugs,
                      AVG(performance_score) as avg_performance
               FROM review_history WHERE user_id=?""",
            (user_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else {"total_reviews": 0, "total_bugs": 0, "avg_performance": 0}
    finally:
        conn.close()


# Initialize DB on import
init_db()
