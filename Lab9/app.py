import time

import mysql.connector
import random
import string
from flask import Flask, jsonify, render_template, request

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
    return render_template('search_engine.html')


@app.route('/students', methods=['GET'])
def get_students():
    data = request.args.get('query', '').strip()

    if not data:
        return jsonify({'error': 'Złe dane.'}), 400

    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT * FROM students 
            WHERE name LIKE %s 
            OR last_name LIKE %s 
            OR CONCAT(name, ' ', last_name) LIKE %s
        """

        cursor.execute(query, [f"%{data}%", f"%{data}%", f"%{data}%"])
        students = cursor.fetchall()
        cursor.close()

        time.sleep(3)  # Simulate delay in response :)

        return jsonify({'students': students}), 200

    except mysql.connector.Error as err:
        return jsonify({'error': str(err)}), 500


@app.route('/db/health_check', methods=['GET'])
def db_health_check():
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT DATABASE();")
        db_name = cursor.fetchone()
        cursor.close()

        return f"Połączono z bazą danych: {db_name[0]}", 200
    except mysql.connector.Error as err:
        return jsonify({'error': str(err), 'message': 'Nie udało się połączyć z bazą danych.'}), 500


if __name__ == '__main__':
    app.run(debug=True)
