#!/usr/bin/env python3
"""
Seed demo data into the gym management system database.
Run this script to populate sample coaches, members, and other data.
"""

import os
from dotenv import load_dotenv
from models.db import connection, cursor

load_dotenv()

def seed_data():
    print("🌱 Seeding demo data...")
    
    try:
        # Insert demo coaches
        coaches_data = [
            ('John', 'Smith', 'john.smith@gym.com', 'coach_password_1', 1800, 1200, 'Strength Training', 500.00),
            ('Maria', 'Garcia', 'maria.garcia@gym.com', 'coach_password_2', 1650, 1000, 'Yoga & Flexibility', 400.00),
            ('Alex', 'Johnson', 'alex.johnson@gym.com', 'coach_password_3', 1750, 1100, 'HIIT & Cardio', 450.00),
            ('Sofia', 'Rodriguez', 'sofia.rodriguez@gym.com', 'coach_password_4', 1700, 950, 'Pilates', 380.00),
        ]
        
        for first, last, email, pwd, height, weight, spec, rate in coaches_data:
            # Check if coach email already exists
            cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
            if cursor.fetchone():
                print(f"  ⏭️  {first} {last} already exists, skipping...")
                continue
            
            # Hash the password (simple for demo)
            from werkzeug.security import generate_password_hash
            hashed_pwd = generate_password_hash(pwd)
            
            # Insert user as coach
            sql_user = """
                INSERT INTO users (first_name, last_name, email, password, height, weight, role)
                VALUES (%s, %s, %s, %s, %s, %s, 'Coach')
            """
            cursor.execute(sql_user, (first, last, email, hashed_pwd, height, weight))
            connection.commit()
            
            user_id = cursor.lastrowid
            
            # Insert coach record
            sql_coach = "INSERT INTO coaches (user_id, specialization, hourly_rate) VALUES (%s, %s, %s)"
            cursor.execute(sql_coach, (user_id, spec, rate))
            connection.commit()
            
            print(f"  ✅ Added coach: {first} {last}")
        
        # Insert demo members
        members_data = [
            ('Jane', 'Doe', 'jane.doe@email.com', 'member_pwd_1', 1650, 650),
            ('Robert', 'Brown', 'robert.brown@email.com', 'member_pwd_2', 1800, 850),
            ('Emily', 'Wilson', 'emily.wilson@email.com', 'member_pwd_3', 1600, 600),
            ('Michael', 'Davis', 'michael.davis@email.com', 'member_pwd_4', 1780, 820),
        ]
        
        for first, last, email, pwd, height, weight in members_data:
            cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
            if cursor.fetchone():
                print(f"  ⏭️  {first} {last} already exists, skipping...")
                continue
            
            from werkzeug.security import generate_password_hash
            hashed_pwd = generate_password_hash(pwd)
            
            sql_member = """
                INSERT INTO users (first_name, last_name, email, password, height, weight, role)
                VALUES (%s, %s, %s, %s, %s, %s, 'Member')
            """
            cursor.execute(sql_member, (first, last, email, hashed_pwd, height, weight))
            connection.commit()
            
            print(f"  ✅ Added member: {first} {last}")
        
        print("\n✨ Demo data seeding complete!")
        
    except Exception as e:
        print(f"❌ Error seeding data: {e}")
        connection.rollback()
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    seed_data()
