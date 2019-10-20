BEGIN;

-- Create tables

CREATE TABLE branch(
  "id" SERIAL PRIMARY  KEY ,
  "name" VARCHAR(50) NOT NULL,
  "class" VARCHAR(20) NOT NULL,
  "created" TIMESTAMP  DEFAULT NOW()

);

CREATE TABLE school(
  "id" SERIAL PRIMARY  KEY ,
  "name" VARCHAR(50) NOT NULL,
  "code" VARCHAR(20) NOT NULL,
  "created" TIMESTAMP  DEFAULT NOW()

);

-- CREATE TABLE class(
--   "id" SERIAL PRIMARY  KEY ,
--   "name" VARCHAR(50) NOT NULL,
--   "code" VARCHAR(20) NOT NULL,
--
-- );

CREATE TABLE year(
  "id" SERIAL PRIMARY  KEY ,
  "year" VARCHAR(50) NOT NULL
);


CREATE TABLE student(
  "id" SERIAL PRIMARY  KEY ,
  "school_id" INTEGER  NOT NULL,
  "branch_id" INTEGER  NOT NULL,
  "reg_num" INTEGER  NOT NULL,
  "name" VARCHAR(50) NOT NULL,
  "father_name" VARCHAR(50) NOT NULL,
  "mother_name" VARCHAR(50) NOT NULL,
  "views" INTEGER  NOT NULL DEFAULT 0,
  "last_views" TIMESTAMP ,
  "created" TIMESTAMP  DEFAULT NOW(),
  "updated" TIMESTAMP  DEFAULT NOW(),

  CONSTRAINT "student_school_id_fkey" FOREIGN KEY ("school_id") REFERENCES school("id"),
  CONSTRAINT "student_branch_id_fkey" FOREIGN KEY ("branch_id") REFERENCES branch("id"),
  CONSTRAINT "student_uk" UNIQUE ("reg_num", "name")

);
CREATE INDEX "student_name_idx" ON student("name");
CREATE INDEX "student_reg_num_idx" ON student("reg_num");

CREATE TABLE subject(
  "id" SERIAL PRIMARY  KEY ,
  "name" VARCHAR(50) NOT NULL
);

CREATE TABLE marks(
  "id" SERIAL PRIMARY  KEY ,
  "student_id" INTEGER  NOT NULL,
  "subject_id" INTEGER  NOT NULL,
  "theory" INTEGER  NOT NULL,
  "sessional" INTEGER  NOT NULL,
  "th_ss" INTEGER  NOT NULL,
  "practical" INTEGER  NOT NULL,

  CONSTRAINT "marks_student_id_fkey" FOREIGN KEY ("student_id") REFERENCES student("id"),
  CONSTRAINT "marks_subject_id_fkey" FOREIGN KEY ("subject_id") REFERENCES subject("id")
);

COMMIT;
