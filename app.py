from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            dob TEXT NOT NULL,
            therapist TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Get form values
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    dob = request.form.get('dob')
    therapist = request.form.get('therapist')

    # Validation
    errors = []
    if not all([first_name, last_name, dob, therapist]): 
        errors.append("All fields are required.")
    try:
        dob_date = datetime.strptime(dob, '%Y-%m-%d') # Matches the format YYYY-MM-DD
        if dob_date >= datetime.now():
            errors.append("Date of birth must be in the past.")
    except ValueError:
        errors.append("Invalid date format.")

    if errors:
        return render_template('form.html', errors=errors, form_data=request.form)

    # Save to DB
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO patients (first_name, last_name, dob, therapist)
        VALUES (?, ?, ?, ?)
    ''', (first_name, last_name, dob, therapist))
    conn.commit()
    conn.close()

    return render_template('confirmation.html', first_name=first_name,
                           last_name=last_name, dob=dob, therapist=therapist)

init_db()  # Only once, to create the DB table to make it run both locally and in the cloud
if __name__ == '__main__':
    app.run(debug=True)
