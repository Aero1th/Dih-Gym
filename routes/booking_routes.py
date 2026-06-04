from flask import Blueprint, render_template, request, redirect, session

from models.db import connection, cursor

booking = Blueprint('booking', __name__)

@booking.route('/book-coach')
def book_coach_page():

    cursor.execute(
        """
        SELECT coaches.coach_id,
               coaches.specialization,
               coaches.hourly_rate,
               users.first_name,
               users.last_name

        FROM coaches

        JOIN users
        ON coaches.user_id = users.user_id
        """
    )

    coaches = cursor.fetchall()

    return render_template(
        'coach_booking.html',
        coaches=coaches
    )

@booking.route('/book-session', methods=['POST'])
def book_session():

    if 'user_id' not in session:
        return redirect('/login')

    coach_id = request.form['coach_id']
    session_date = request.form['session_date']
    session_time = request.form['session_time']

    sql = """
    INSERT INTO coach_bookings
    (
        member_user_id,
        coach_id,
        session_date,
        session_time
    )
    VALUES (%s,%s,%s,%s)
    """

    values = (
        session['user_id'],
        coach_id,
        session_date,
        session_time
    )
    cursor.execute(sql, values)
    connection.commit()

    return redirect('/book-coach')