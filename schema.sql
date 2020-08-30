CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    role_id INTEGER REFERENCES roles (id)
);

CREATE TABLE roles
(
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

INSERT INTO roles (name)
VALUES ('student'), ('teacher'), ('admin');

CREATE TABLE courses
(
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    teacher_id INTEGER REFERENCES users (id),
    created_at TIMESTAMP
);

CREATE TABLE participants
(
    course_id INTEGER REFERENCES courses (id),
    user_id INTEGER REFERENCES users (id)
);

CREATE TABLE chapters
(
    id SERIAL PRIMARY KEY,
    ordinal INTEGER,
    name TEXT NOT NULL,
    content TEXT,
    course_id INTEGER REFERENCES courses (id),
    creator_id INTEGER REFERENCES users (id),
    created_at TIMESTAMP
);

CREATE TABLE exercises
(
    id SERIAL PRIMARY KEY,
    ordinal INTEGER,
    name TEXT NOT NULL,
    question TEXT,
    course_id INTEGER REFERENCES courses (id),
    chapter_id INTEGER REFERENCES chapters (id),
    creator_id INTEGER REFERENCES users (id),
    created_at TIMESTAMP
);

CREATE TABLE choices
(
    id SERIAL PRIMARY KEY,
    correct BOOLEAN,
    description TEXT NOT NULL,
    exercise_id INTEGER REFERENCES exercises (id),
    created_at TIMESTAMP
);

CREATE TABLE answers
(
    exercise_id INTEGER REFERENCES exercises (id),
    choice_id INTEGER REFERENCES choices (id),
    user_id INTEGER REFERENCES users (id),
    answered_at TIMESTAMP
);