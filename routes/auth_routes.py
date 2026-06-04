from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

from models.db import connection, cursor

auth = Blueprint('auth', __name__)

@auth.route('/')
def frontpage():
    return render_template('Main Page.html')

@auth.route('/benefits')
def benefits():
    return render_template('Challenge your body page.html')

@auth.route('/goals')
def goals():
    return render_template('Choose your goal page.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':

        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])
        height = request.form['height']
        weight = request.form['weight']
        sql = """
                INSERT INTO users
                (first_name, last_name, email, password, height, weight)
                VALUES (%s,%s,%s,%s,%s,%s)
                """

        values = (
            first_name,
            last_name,
            email,
            password,
            height,
            weight
        )

        cursor.execute(sql, values)
        connection.commit()

        return redirect('/login')

    return render_template('signup.html')
@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            (email,)
        )

        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):

            session['user_id'] = user['user_id']
            session['role'] = user['role']

            if user['role'] == 'Admin':
                return redirect('/admin-dashboard')

            return redirect('/dashboard')

    return render_template('SIgn In.html')

@auth.route('/logout')
def logout():

    session.clear()

    return redirect('/login')
