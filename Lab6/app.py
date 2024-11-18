import random
import string
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=8))

users = {
    "admin": "admin"
}


@app.route('/')
def home():
    if 'username' in session:
        return render_template('form.html', username=session['username'])

    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users and users[username] == password:
            session['username'] = username
            flash('Login successful!', 'success')

            return redirect(url_for('form'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')


@app.route('/form')
def form():
    if 'username' not in session:
        flash('Musisz się zalogować żeby widzieć ten formularz.', 'warning')
        return redirect(url_for('login'))

    return render_template('form.html')


@app.route('/form/display', methods=['POST'])
def display_form():
    if 'username' not in session:
        flash('Musisz się zalogować żeby widzieć ten formularz.', 'warning')
        return redirect(url_for('login'))

    form_data = request.form.to_dict()

    return render_template('display_form.html', username=session['username'], form_data=form_data)


if __name__ == '__main__':
    app.run(debug=True)
