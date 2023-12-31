CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname TEXT NOT NULL, lastname TEXT NOT NULL,
    gender TEXT NOT NULL,
    hash TEXT NOT NULL UNIQUE
);


CREATE TABLE services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name TEXT UNIQUE NOT NULL
    
);

CREATE TABLE images (
    image_path TEXT NOT NULL,
    person_id INTEGER UNIQUE NOT NULL,
    FOREIGN KEY(person_id) REFERENCES users(id)
);


CREATE TABLE masons (
    person_id INTEGER,
    phone_number NUMERIC,
    email TEXT,
    service_id INTEGER,
    town TEXT,
    state TEXT,
    FOREIGN KEY (person_id) REFERENCES users(id),
    FOREIGN KEY (service_id) REFERENCES services(id)
);


CREATE TABLE liverequest (
    service_id INTEGER NOT NULL,
    town TEXT NOT NULL,
    state TEXT NOT NULL,
    FOREIGN KEY (requester_id) REFERENCES users(id),
    FOREIGN KEY (service_id) REFERENCES services (id)
);

