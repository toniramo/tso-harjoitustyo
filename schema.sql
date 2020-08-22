CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    first_name TEXT,
    last_name TEXT
);

CREATE TABLE courses (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    description TEXT,
    teacher_id INTEGER REFERENCES users (id),
    created_at TIMESTAMP
);

CREATE TABLE participants (
    course_id INTEGER REFERENCES courses (id),
    user_id INTEGER REFERENCES users (id)
);