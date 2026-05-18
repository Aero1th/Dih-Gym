CREATE DATABASE gym_management_system;

USE gym_management_system;

CREATE TABLE users (

    user_id INT AUTO_INCREMENT PRIMARY KEY,

    first_name VARCHAR(50) NOT NULL,

    last_name VARCHAR(50) NOT NULL,

    email VARCHAR(100) UNIQUE NOT NULL,

    password VARCHAR(255) NOT NULL,

    height FLOAT,

    weight FLOAT,

    credit_balance DECIMAL(10,2) DEFAULT 0.00,

    role ENUM('Admin', 'Member', 'Coach', 'Staff')
    DEFAULT 'Member',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE memberships (

    membership_id INT AUTO_INCREMENT PRIMARY KEY,

    plan_name VARCHAR(50) NOT NULL,

    description TEXT,

    price DECIMAL(10,2) NOT NULL,

    duration_days INT NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE member_subscriptions (

    subscription_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT NOT NULL,

    membership_id INT NOT NULL,

    start_date DATE NOT NULL,

    end_date DATE NOT NULL,

    status ENUM(
        'Active',
        'Expired',
        'Cancelled'
    ) DEFAULT 'Active',

    payment_status ENUM(
        'Paid',
        'Pending'
    ) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE,

    FOREIGN KEY (membership_id)
    REFERENCES memberships(membership_id)
    ON DELETE CASCADE
);

CREATE TABLE coaches (

    coach_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT UNIQUE NOT NULL,

    specialization VARCHAR(100),

    hourly_rate DECIMAL(10,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE
);

CREATE TABLE coach_bookings (

    booking_id INT AUTO_INCREMENT PRIMARY KEY,

    member_user_id INT NOT NULL,

    coach_id INT NOT NULL,

    session_date DATE NOT NULL,

    session_time TIME NOT NULL,

    status ENUM(
        'Pending',
        'Confirmed',
        'Completed',
        'Cancelled'
    ) DEFAULT 'Pending',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (member_user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE,

    FOREIGN KEY (coach_id)
    REFERENCES coaches(coach_id)
    ON DELETE CASCADE
);

CREATE TABLE staff (

    staff_id INT AUTO_INCREMENT PRIMARY KEY,

    user_id INT UNIQUE NOT NULL,

    position VARCHAR(50),

    salary DECIMAL(10,2),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id)
    REFERENCES users(user_id)
    ON DELETE CASCADE
);

INSERT INTO memberships
(plan_name, description, price, duration_days)
VALUES
('Basic', 'Gym access only', 500, 30),
('Premium', 'Gym + Group Classes', 1200, 30),
('VIP', 'All Access + Personal Coach', 2500, 30);