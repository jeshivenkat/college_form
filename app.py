from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('contact_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_form (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        conn = sqlite3.connect('contact_data.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO contact_form (name, email, message) VALUES (?, ?, ?)",
                       (name, email, message))
        conn.commit()
        conn.close()
        return redirect('/contact')
    return render_template('contact.html')

@app.route('/admin')
def admin():
    conn = sqlite3.connect('contact_data.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contact_form")
    contacts = cursor.fetchall()
    conn.close()
    return render_template('admin.html', contacts=contacts)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
