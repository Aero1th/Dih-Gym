from flask import Blueprint, render_template, request, redirect, session
from datetime import datetime, timedelta

from models.db import connection, cursor

membership = Blueprint('membership', __name__)

@membership.route('/memberships')
def memberships_page():

    cursor.execute("SELECT * FROM memberships")

    memberships = cursor.fetchall()

    return render_template(
        'memberships.html',
        memberships=memberships
    )
@membership.route('/subscribe/<int:membership_id>')
def subscribe(membership_id):

    if 'user_id' not in session:
        return redirect('/login')

    cursor.execute(
        "SELECT * FROM memberships WHERE membership_id=%s",
        (membership_id,)
    )

    membership_data = cursor.fetchone()

    start_date = datetime.now().date()

    end_date = start_date + timedelta(
        days=membership_data['duration_days']
    )
    sql = """
        INSERT INTO member_subscriptions
        (
            user_id,
            membership_id,
            start_date,
            end_date
        )
        VALUES (%s,%s,%s,%s)
        """

    values = (
        session['user_id'],
        membership_id,
        start_date,
        end_date
    )
    cursor.execute(sql, values)
    connection.commit()

    return redirect('/dashboard')