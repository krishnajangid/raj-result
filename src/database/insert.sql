BEGIN;

INSERT INTO role (name) VALUES ('superuser');
INSERT INTO users (email, password, active) VALUES ('admin', 'admin', true);
INSERT INTO roles_users (user_id, role_id) VALUES (1, 1);


INSERT INTO branch (name) VALUES ('SSLC'), ('ARTS'), ('COMMERCE'), ('SCIENCE');

COMMIT;