-- Sample data. Run this SECOND (after schema.sql).

INSERT INTO departments (name) VALUES
    ('Training'), ('Administration'), ('Student Support');

INSERT INTO employees (full_name, email, role, department_id) VALUES
    ('Meera Kulkarni', 'meera@peakprosys.example', 'trainer', 1),
    ('Rahul Deshmukh', 'rahul@peakprosys.example', 'trainer', 1),
    ('Sneha Pawar',    'sneha@peakprosys.example', 'admin',   2),
    ('Vikram Joshi',   'vikram@peakprosys.example', 'counsellor', 3);

INSERT INTO courses (title, description, duration_weeks, fee, trainer_id) VALUES
    ('Python Basics',      'Core Python for beginners',        6, 8000.00, 1),
    ('Django Web Dev',     'Build websites with Django',       8, 12000.00, 1),
    ('React Frontend',     'Modern UI with React',             8, 12000.00, 2),
    ('SQL and PostgreSQL', 'Databases from scratch',           4, 6000.00, 2);

INSERT INTO students (full_name, email, phone, city) VALUES
    ('Asha Patil',  'asha@example.com',  '9000000001', 'Pune'),
    ('Ravi Kumar',  'ravi@example.com',  '9000000002', 'Mumbai'),
    ('Neha Joshi',  'neha@example.com',  '9000000003', 'Satara'),
    ('Amit Shah',   'amit@example.com',  '9000000004', 'Pune'),
    ('Priya Nair',  'priya@example.com', '9000000005', 'Sangli'),
    ('Omkar Jadhav','omkar@example.com', '9000000006', 'Palus');

INSERT INTO enrollments (student_id, course_id, status) VALUES
    (1, 1, 'completed'), (1, 2, 'active'),
    (2, 1, 'active'),    (2, 4, 'active'),
    (3, 3, 'active'),    (4, 2, 'dropped'),
    (5, 3, 'active'),    (6, 1, 'active');
