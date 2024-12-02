import mysql.connector
import random
import string
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=8))

users = {
    "admin": "admin"
}

connection = mysql.connector.connect(
    user="kamiluk", 
    password="pythonanywhere",
    host="kamiluk.mysql.pythonanywhere-services.com",
    database="kamiluk$students"
)


@app.route('/')
def default():
    if 'username' not in session:
       return redirect(url_for('login'))

    return redirect(url_for('display_students'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users and users[username] == password:
            session['username'] = username
            session.pop('_flashes', None)
            flash('Zalogowałeś się pomyślnie!', 'success')

            return redirect(url_for('display_students'))
        else:
            session.pop('_flashes', None)
            flash('Złe dane logowania.', 'danger')

    return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout():
    if 'username' not in session:
       return

    session.pop('username', None)
    session.pop('_flashes', None)
    flash('Wylogowałeś się.', 'success')
    return redirect(url_for('login'))


@app.route('/students', methods=['POST'])
def insert_student():
    if 'username' not in session:
        flash('Musisz się zalogować żeby widzieć ten formularz.', 'warning')
        return redirect(url_for('login'))

    try:
        name = request.form['name']
        last_name = request.form['last_name']
        age = request.form['age']

        cursor = connection.cursor()
        query = "INSERT INTO students (name, last_name, age) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, last_name, age))
        connection.commit()
        cursor.close()

        flash('Pomyślnie dodano studenta!', 'success')
        return redirect(url_for('display_students'))
    except mysql.connector.Error as err:
        flash(f'Błąd: {str(err)}', 'danger')
        return redirect(url_for('display_students'))


@app.route('/students', methods=['GET'])
def display_students():
    if 'username' not in session:
        flash('Musisz się zalogować żeby widzieć ten formularz.', 'warning')
        return redirect(url_for('login'))
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students;")
        students = cursor.fetchall()
        cursor.close()

        return render_template('display_form.html', students=students)
    except mysql.connector.Error as err:
        flash(f'Błąd: {str(err)}', 'danger')
        return redirect(url_for('login'))
    

@app.route('/students/update', methods=['POST'])
def update_student():
    if 'username' not in session:
        flash('Musisz się zalogować żeby widzieć ten formularz.', 'warning')
        return redirect(url_for('login'))

    try:
        name = request.form['student_name']
        last_name = request.form['student_last_name']
        age = request.form['student_age']
        student_id = request.form['student_id']
        

        cursor = connection.cursor()
        query = "UPDATE students SET name = %s, last_name = %s, age = %s WHERE id = %s"
        cursor.execute(query, (name, last_name, age, student_id))
        connection.commit()
        cursor.close()

        flash('Pomyślnie zaktualizowano studenta!', 'success')
        return redirect(url_for('display_students'))
    except mysql.connector.Error as err:
        flash(f'Błąd: {str(err)}', 'danger')
        return redirect(url_for('display_students'))
    
    
@app.route('/students/delete', methods=['POST'])
def delete_student():
    if 'username' not in session:
            flash('Musisz się zalogować żeby widzieć ten formularz.', 'warning')
            return redirect(url_for('login'))

    try:
        student_id = request.form['student_id']

        cursor = connection.cursor()
        query = "DELETE FROM students WHERE id = %s"
        cursor.execute(query, (student_id,))
        connection.commit()
        cursor.close()

        if cursor.rowcount == 0:
            flash(f'Błąd: {"Nie znaleziono studenta"}', 'danger')
            return redirect(url_for('display_students'))

        return redirect(url_for('display_students'))
    except mysql.connector.Error as err:
        flash(f'Błąd: {str(err)}', 'danger')
        return redirect(url_for('display_students'))


@app.route('/db/health_check', methods=['GET'])
def db_health_check():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();") 
        db_name = cursor.fetchone()
        cursor.close()

        return f"Połączono z bazą danych: {db_name[0]}", 200
    except mysql.connector.Error as err:
        return f"Nie udało się połączyć z bazą danych: {err}", 500


if __name__ == '__main__':
    app.run(debug=True)
