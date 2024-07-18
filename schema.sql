DROP TABLE IF EXISTS floor, department, exhibition, request, assistance, review, rating CASCADE;

CREATE TABLE floor(
    floor_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    floor_name VARCHAR(5) UNIQUE NOT NULL  
);

CREATE TABLE department(
    department_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    department_name VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE exhibition(
    exhibition_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    exhibition_name VARCHAR(30) NOT NULL,
    floor_id SMALLINT NOT NULL,
    department_id SMALLINT NOT NULL,
    start_date DATE DEFAULT CURRENT_DATE NOT NULL CHECK (start_date <= CURRENT_DATE),
    description VARCHAR,
    FOREIGN KEY (floor_id) REFERENCES floor(floor_id),
    FOREIGN KEY (department_id) REFERENCES department(department_id)
);

CREATE TABLE assistance(
    assistance_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    description VARCHAR(20) NOT NULL
);

CREATE TABLE request(
    request_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    exhibition_id SMALLINT NOT NULL,
    assistance_id SMALLINT NOT NULL,
    created_at TIMESTAMP(0) NOT NULL,
    FOREIGN KEY (assistance_id) REFERENCES assistance(assistance_id),
    FOREIGN KEY (exhibition_id) REFERENCES exhibition(exhibition_id)
);

CREATE TABLE rating(
    rating_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    description VARCHAR(20) NOT NULL
);

CREATE TABLE review(
    review_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    exhibition_id SMALLINT NOT NULL,
    rating_id SMALLINT NOT NULL,
    created_at TIMESTAMP(0) NOT NULL,
    FOREIGN KEY (rating_id) REFERENCES rating(rating_id),
    FOREIGN KEY (exhibition_id) REFERENCES exhibition(exhibition_id)
);

INSERT INTO floor(floor_id, floor_name)
OVERRIDING SYSTEM VALUE 
VALUES (0, 'Vault'), (1, '1'), (2, '2'), (3, '3');

INSERT INTO department(department_id, department_name)
OVERRIDING SYSTEM VALUE 
VALUES (1, 'Entomology'), (0, 'Geology'), (5, 'Paleontology'), (2, 'Zoology'), (4, 'Ecology');

INSERT INTO assistance(assistance_id, description) 
OVERRIDING SYSTEM VALUE 
VALUES (0, 'assistance'), (1, 'emergency');

INSERT INTO rating(rating_id, description)
OVERRIDING SYSTEM VALUE 
VALUES (0, 'Terrible'), (1, 'Bad'), (2, 'Neutral'), (3, 'Good'), (4, 'Amazing');

INSERT INTO exhibition(exhibition_id, exhibition_name, floor_id, department_id, start_date, description)
OVERRIDING SYSTEM VALUE 
VALUES (1, 'Adaptation', 0, 1, TO_DATE('01/07/19', 'DD/MM/YY'), 'How insect evolution has kept pace with an industrialised world'),
(0, 'Measureless to Man', 1, 0, TO_DATE('23/08/21', 'DD/MM/YY'), 'An immersive 3D experience: delve deep into a previously-inaccessible cave system.'),
(5, 'Thunder Lizards', 1, 5, TO_DATE('01/02/23', 'DD/MM/YY'), 'How new research is making scientists rethink what dinosaurs really looked like.'),
(2, 'The Crenshaw Collection', 2, 2, TO_DATE('03/03/21', 'DD/MM/YY'), 'An exhibition of 18th Century watercolours, mostly focused on South American wildlife.'),
(4, 'Our Polluted World', 3, 4, TO_DATE('12/05/21', 'DD/MM/YY'), 'A hard-hitting exploration of humanity''s impact on the environment.'),
(3, 'Cetacean Sensations', 1, 2, TO_DATE('01/07/19', 'DD/MM/YY'), 'Whales: from ancient myth to critically endangered.');

SELECT * FROM exhibition