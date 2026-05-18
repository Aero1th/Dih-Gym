from flask import Blueprint, render_template, session, redirect

from models.db import cursor

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
def user_dashboard():

    if 'user_id' not in session:
        return redirect('/login')

    cursor.execute(
        "SELECT * FROM users WHERE user_id=%s",
        (session['user_id'],)
    )

    user = cursor.fetchone()

    cursor.execute(
        """
        SELECT memberships.plan_name,
               member_subscriptions.start_date,
               member_subscriptions.end_date,
               member_subscriptions.status

        FROM member_subscriptions

        JOIN memberships
        ON member_subscriptions.membership_id = memberships.membership_id

        WHERE member_subscriptions.user_id=%s

        ORDER BY member_subscriptions.subscription_id DESC

        LIMIT 1
        """,
        (session['user_id'],)
    )

    subscription = cursor.fetchone()

    return render_template(
        'dashboard.html',
        user=user,
        subscription=subscription
    )