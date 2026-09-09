-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_020_c1" AS
SELECT * FROM sheet1;

-- S17
SELECT "Student ID", "Age", "Gender", "Daily study time", "Social media usage time", "Part-time job", "Attendance rate", "Sleep duration", "Diet quality", "Exercise frequency", "Parents' education level", "Internet quality", "Mental health score", "Extracurricular activity participation", "Exam score" FROM temp."reuse_020_c1";

-- S18
SELECT "Student ID", "Age", "Gender", "Daily study time", "Social media usage time", "Part-time job", "Attendance rate", "Sleep duration", "Diet quality", "Exercise frequency", "Parents' education level", "Internet quality", "Mental health score", "Extracurricular activity participation", "Exam score" FROM temp."reuse_020_c1";

DROP TABLE temp."reuse_020_c1";
