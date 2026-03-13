CREATE TABLE IF NOT EXISTS grades (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    group_name VARCHAR(255) NOT NULL,
    student_name VARCHAR(255) NOT NULL,
    grade INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_student_name ON grades(student_name);
CREATE INDEX IF NOT EXISTS idx_grade ON grades(grade);
