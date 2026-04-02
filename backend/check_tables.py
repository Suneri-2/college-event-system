import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'college_system.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Add the column if it doesn't exist
try:
    cursor.execute("ALTER TABLE registrations ADD COLUMN student_name TEXT;")
    print("Column 'student_name' added successfully!")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e).lower():
        print("Column 'student_name' already exists, nothing to do.")
    else:
        raise e

conn.commit()
conn.close()