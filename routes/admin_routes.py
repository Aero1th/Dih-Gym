from flask import Blueprint, render_template, redirect, session, request

from models.db import connection, cursor

admin = Blueprint('admin', __name__)

# =========================================
# ADMIN ACCESS CHECK
# =========================================

def admin_required():

    if 'user_id' not in session:
        return False

    if session.get('role') != 'Admin':
        return False

    return True


# =========================================
# ADMIN DASHBOARD
# =========================================

@admin.route('/admin-dashboard')
def admin_dashboard():

    if not admin_required():
        return redirect('/login')

    # Total Members
    cursor.execute(
        "SELECT COUNT(*) AS total_members FROM users WHERE role='Member'"
    )

    total_members = cursor.fetchone()

    # Total Staff
    cursor.execute(
        "SELECT COUNT(*) AS total_staff FROM staff"
    )

    total_staff = cursor.fetchone()

    # Total Coach Bookings
    cursor.execute(
        "SELECT COUNT(*) AS total_bookings FROM coach_bookings"
    )

    total_bookings = cursor.fetchone()

    return render_template(
        'admin_dashboard.html',
        total_members=total_members,
        total_staff=total_staff,
        total_bookings=total_bookings
    )


# =========================================
# MEMBERS LIST
# =========================================

@admin.route('/members-list')
def members_list():

    if not admin_required():
        return redirect('/login')

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE role='Member'
        ORDER BY created_at DESC
        """
    )

    members = cursor.fetchall()

    return render_template(
        'members_list.html',
        members=members
    )


# =========================================
# DELETE MEMBER
# =========================================

@admin.route('/delete-member/<int:user_id>')
def delete_member(user_id):

    if not admin_required():
        return redirect('/login')

    cursor.execute(
        "DELETE FROM users WHERE user_id=%s",
        (user_id,)
    )

    connection.commit()

    return redirect('/members-list')


# =========================================
# STAFF LIST
# =========================================

@admin.route('/staff-list')
def staff_list():

    if not admin_required():
        return redirect('/login')

    cursor.execute(
        """
        SELECT
            staff.staff_id,
            staff.position,
            staff.salary,
            users.first_name,
            users.last_name,
            users.email

        FROM staff

        JOIN users
        ON staff.user_id = users.user_id

        ORDER BY staff.staff_id DESC
        """
    )

    staff = cursor.fetchall()

    return render_template(
        'staff_list.html',
        staff=staff
    )


# =========================================
# DELETE STAFF
# =========================================

@admin.route('/delete-staff/<int:staff_id>')
def delete_staff(staff_id):

    if not admin_required():
        return redirect('/login')

    cursor.execute(
        "DELETE FROM staff WHERE staff_id=%s",
        (staff_id,)
    )

    connection.commit()

    return redirect('/staff-list')


# =========================================
# COACH BOOKINGS
# =========================================

@admin.route('/coach-bookings')
def coach_bookings():

    if not admin_required():
        return redirect('/login')

    cursor.execute(
        """
        SELECT

            coach_bookings.booking_id,
            coach_bookings.session_date,
            coach_bookings.session_time,
            coach_bookings.status,

            member.first_name AS member_first_name,
            member.last_name AS member_last_name,

            coach_user.first_name AS coach_first_name,
            coach_user.last_name AS coach_last_name

        FROM coach_bookings

        JOIN users AS member
        ON coach_bookings.member_user_id = member.user_id

        JOIN coaches
        ON coach_bookings.coach_id = coaches.coach_id

        JOIN users AS coach_user
        ON coaches.user_id = coach_user.user_id

        ORDER BY coach_bookings.booking_id DESC
        """
    )

    bookings = cursor.fetchall()

    return render_template(
        'coach_bookings.html',
        bookings=bookings
    )


# =========================================
# UPDATE BOOKING STATUS
# =========================================

@admin.route('/update-booking/<int:booking_id>', methods=['POST'])
def update_booking_status(booking_id):

    if not admin_required():
        return redirect('/login')

    new_status = request.form['status']

    cursor.execute(
        """
        UPDATE coach_bookings
        SET status=%s
        WHERE booking_id=%s
        """,
        (new_status, booking_id)
    )

    connection.commit()

    return redirect('/coach-bookings')


# =========================================
# VIEW MEMBERSHIPS
# =========================================

@admin.route('/view-memberships')
def view_memberships():

    if not admin_required():
        return redirect('/login')

    cursor.execute(
        "SELECT * FROM memberships"
    )

    memberships = cursor.fetchall()

    return render_template(
        'view_memberships.html',
        memberships=memberships
    )


# =========================================
# LOGOUT
# =========================================

@admin.route('/admin-logout')
def admin_logout():

    session.clear()

    return redirect('/login')