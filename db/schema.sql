-- Tasks 121-124: database design (PostgreSQL)
-- Run this file FIRST, inside an empty database (for example: student_db).

DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;

-- Task 123: employee database ---------------------------------------------
CREATE TABLE departments (
    id    SERIAL PRIMARY KEY,
    name  VARCHAR(80) NOT NULL UNIQUE
);

CREATE TABLE employees (
    id            SERIAL PRIMARY KEY,
    full_name     VARCHAR(100) NOT NULL,
    email         VARCHAR(120) NOT NULL UNIQUE,
    role          VARCHAR(20)  NOT NULL
                  CHECK (role IN ('trainer', 'admin', 'counsellor')),
    department_id INTEGER REFERENCES departments(id) ON DELETE SET NULL,
    hire_date     DATE NOT NULL DEFAULT CURRENT_DATE,
    is_active     BOOLEAN NOT NULL DEFAULT TRUE
);

-- Task 121: normalized student database -----------------------------------
CREATE TABLE students (
    id            SERIAL PRIMARY KEY,
    full_name     VARCHAR(100) NOT NULL,
    email         VARCHAR(120) NOT NULL UNIQUE,
    phone         VARCHAR(20),
    date_of_birth DATE,
    city          VARCHAR(60),
    created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Task 122: course-management database ------------------------------------
CREATE TABLE courses (
    id             SERIAL PRIMARY KEY,
    title          VARCHAR(100) NOT NULL UNIQUE,
    description    TEXT,
    duration_weeks INTEGER NOT NULL CHECK (duration_weeks > 0),
    fee            NUMERIC(10, 2) NOT NULL DEFAULT 0 CHECK (fee >= 0),
    trainer_id     INTEGER REFERENCES employees(id) ON DELETE SET NULL
);

-- Task 124: foreign keys link students and courses (many-to-many) ---------
CREATE TABLE enrollments (
    id          SERIAL PRIMARY KEY,
    student_id  INTEGER NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    course_id   INTEGER NOT NULL REFERENCES courses(id)  ON DELETE RESTRICT,
    enrolled_on DATE NOT NULL DEFAULT CURRENT_DATE,
    status      VARCHAR(12) NOT NULL DEFAULT 'active'
                CHECK (status IN ('active', 'completed', 'dropped')),
    UNIQUE (student_id, course_id)   -- a student cannot join the same course twice
);

-- Indexes on foreign keys make JOINs faster
CREATE INDEX idx_courses_trainer     ON courses(trainer_id);
CREATE INDEX idx_enrollments_course  ON enrollments(course_id);
CREATE INDEX idx_employees_dept      ON employees(department_id);
