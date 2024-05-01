-- This file should contain all code required to create & seed database tables.

DROP TABLE exhibition, floor, department, assistance_request, assistance, review, rating;

CREATE TABLE floor(
    floor_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    floor_name VARCHAR(5) UNIQUE NOT NULL  
);

CREATE TABLE department(
    department_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    department_name VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE exhibition(
    exhibition_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    exhibition_name VARCHAR(30) NOT NULL,
    floor_id SMALLINT NOT NULL,
    department_id SMALLINT NOT NULL,
    start_date DATE DEFAULT CURRENT_DATE NOT NULL CHECK (start_date <= CURRENT_DATE),
    description VARCHAR,
    FOREIGN KEY (floor_id) REFERENCES floor(floor_id),
    FOREIGN KEY (department_id) REFERENCES department(department_id)
);

CREATE TABLE assistance(
    assistance_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    value SMALLINT UNIQUE NOT NULL,
    description VARCHAR(20) NOT NULL
);

CREATE TABLE assistance_request(
    assistance_request_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    exhibition_id INT NOT NULL,
    assistance_id INT NOT NULL,
    created_at TIME NOT NULL,
    FOREIGN KEY (assistance_id) REFERENCES assistance(assistance_id),
    FOREIGN KEY (exhibition_id) REFERENCES exhibition(exhibition_id)
);

CREATE TABLE rating(
    rating_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    value SMALLINT UNIQUE NOT NULL,
    description VARCHAR(20) NOT NULL
);

CREATE TABLE review(
    review_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    exhibition_id INT NOT NULL,
    rating_id INT NOT NULL,
    created_at TIME NOT NULL,
    FOREIGN KEY (rating_id) REFERENCES rating(rating_id),
    FOREIGN KEY (exhibition_id) REFERENCES exhibition(exhibition_id)
);

INSERT INTO floor(floor_name) 
VALUES ('Vault', '1', '2', '3');

INSERT INTO department(department_name) 
VALUES ('Vault', '1', '2', '3');