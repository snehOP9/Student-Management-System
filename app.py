from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('db.sqlite')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM student').fetchall()
    conn.close()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        roll_number = request.form['roll_number']
        branch = request.form['branch']
        email = request.form['email']
        marks = request.form['marks']
        conn = get_db_connection()
        conn.execute('INSERT INTO student (name, roll_number, branch, email, marks) VALUES (?, ?, ?, ?, ?)',
                     (name, roll_number, branch, email, marks))
        conn.commit()
        conn.close()
        flash('Student added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM student WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        name = request.form['name']
        roll_number = request.form['roll_number']
        branch = request.form['branch']
        email = request.form['email']
        marks = request.form['marks']
        conn.execute('UPDATE student SET name = ?, roll_number = ?, branch = ?, email = ?, marks = ? WHERE id = ?',
                     (name, roll_number, branch, email, marks, id))
        conn.commit()
        conn.close()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('update_student.html', student=student)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM student WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
