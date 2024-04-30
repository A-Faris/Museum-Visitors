-- This file should contain all code required to create & seed database tables.

DROP TABLE exhibition, floor, department, assistance_request, assistance, review, rating;

CREATE TABLE exhibition(
    exhibition_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
);

CREATE TABLE floor(
    floor_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
);

CREATE TABLE department(
    department_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
);

CREATE TABLE assistance_request(
    assistance_request_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
);

CREATE TABLE assistance(
    assistance_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
);

CREATE TABLE review(
    review_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
);

CREATE TABLE rating(
    rating_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
);