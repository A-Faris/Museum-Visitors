DROP TABLE species, subject, encolsure, encolsure_assignment;

CREATE TABLE species(
    species_id INT GENERATED ALWAYS AS IDENTITY,
    name TEXT NOT NULL,
    scientific_name TEXT UNIQUE NOT NULL,
    PRIMARY KEY(species_id),
    CONSTRAINT no_humans CHECK (
        LOWER(name) != 'chris' AND LOWER(scientific_name) NOT LIKE 'homo%'
    )
);

CREATE TABLE subject(
    subject_id INT GENERATED ALWAYS AS IDENTITY,
    species_id INT,
    acquisition_date DATE DEFAULT CURRENT_DATE CHECK (acquisition_date <= CURRENT_DATE),
    PRIMARY KEY(subject_id),
    FOREIGN KEY(species_id) REFERENCES species(species_id)
);

CREATE TABLE encolsure(
    encolsure_id INT GENERATED ALWAYS AS IDENTITY,
    type TEXT NOT NULL,
    status INT NOT NULL,
    PRIMARY KEY (encolsure_id)
);

CREATE TABLE encolsure_assignment(
    encolsure_assignment_id INT GENERATED ALWAYS AS IDENTITY,
    subject_id INT NOT NULL,
    encolsure_id INT NOT NULL,
    start_date DATE DEFAULT CURRENT_DATE NOT NULL CHECK (start_date <= CURRENT_DATE),
    end_date DATE CHECK (end_date <= start_date),
    PRIMARY KEY (encolsure_assignment_id),
    FOREIGN KEY (subject_id) REFERENCES (subject_id),
    FOREIGN KEY (encolsure_id) REFERENCES (encolsure_id)
);

-- INSERT INTO species(name, scientific_name) 
-- VALUES ('T-Rex', 'T-rexious');

-- INSERT INTO species(name, scientific_name) 
-- VALUES ('Bob', 'Homosapien');

-- INSERT INTO subject(species_id, acquisition_date) 
-- VALUES (1, '2024-01-01');


-- SELECT * FROM species;
-- SELECT * FROM subject;