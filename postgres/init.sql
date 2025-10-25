CREATE DATABASE user_data;

\c user_data;

CREATE TABLE devices (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE user_devices (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    device_id INT REFERENCES devices(id),
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
