from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'relational', 'sql', 'ProduCast.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # Enforce the ON DELETE CASCADE constraints from your DDL
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    movies = conn.execute('SELECT * FROM Movie').fetchall()
    persons = conn.execute('SELECT * FROM Person').fetchall()
    conn.close()
    return render_template('index.html', movies=movies, persons=persons)

@app.route('/add_talent', methods=('POST',))
def add_talent():
    name = request.form['name']
    if name:
        conn = get_db_connection()
        # Insert into base Person table
        cursor = conn.execute('INSERT INTO Person (Name) VALUES (?)', (name,))
        # Insert into Actor subclass to maintain ISA hierarchy
        conn.execute('INSERT INTO Actor (PersonID) VALUES (?)', (cursor.lastrowid,))
        conn.commit()
        conn.close()
    return redirect(url_for('index'))

@app.route('/search', methods=('GET', 'POST'))
def search():
    results = []
    conn = get_db_connection()
    if request.method == 'POST':
        genre = request.form['genre']
        results = conn.execute('SELECT Title FROM Movie WHERE Genre = ?', (genre,)).fetchall()
    
    # Fetch the full lists again so Section 3 doesn't vanish
    movies = conn.execute('SELECT * FROM Movie').fetchall()
    persons = conn.execute('SELECT * FROM Person').fetchall()
    conn.close()
    
    return render_template('index.html', search_results=results, show_search=True, movies=movies, persons=persons)

@app.route('/delete_movie/<int:id>', methods=('POST',))
def delete_movie(id):
    conn = get_db_connection()
    # Your DDL handles the bridge tables automatically due to ON DELETE CASCADE
    conn.execute('DELETE FROM Movie WHERE MovieID = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)