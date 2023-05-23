DROP TABLE IF EXISTS member CASCADE;
CREATE TABLE member(
    user_id SERIAL PRIMARY KEY,
    email VARCHAR NOT NULL,
    password VARCHAR NOT NULL,
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    gender VARCHAR NOT NULL,
    birth_date DATE NOT NULL,
    country VARCHAR NOT NULL,
    address VARCHAR NOT NULL,
    zipcode INT NOT NULL,
    city VARCHAR NOT NULL,
    phone VARCHAR
);

DROP TABLE IF EXISTS club CASCADE;
CREATE TABLE club(
    club_id SERIAL PRIMARY KEY,
    info TEXT NOT NULL,
    name VARCHAR NOT NULL,
    zipcode INT NOT NULL,
    city VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    website_url VARCHAR
);

DROP TABLE IF EXISTS event CASCADE;
CREATE TABLE event(
    event_id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    info TEXT NOT NULL,
    max_spots INT,
    date_from DATE NOT NULL,
    date_to DATE NOT NULL,
    time_from TIME WITHOUT TIME ZONE,
    time_to TIME WITHOUT TIME ZONE,
    signup_opens DATE NOT NULL,
    signup_closes DATE NOT NULL,
    price INT NOT NULL,
    club_id INT NOT NULL,
    address VARCHAR NOT NULL,
    zipcode INT NOT NULL,
    city VARCHAR NOT NULL,
    country VARCHAR NOT NULL,
    is_cancelled BOOLEAN NOT NULL,
    participants INT NOT NULL,
    FOREIGN KEY (club_id) REFERENCES club(club_id)
);

DROP TABLE IF EXISTS type_right CASCADE;
CREATE TABLE type_right(
    right_id SERIAL PRIMARY KEY,
    type_right VARCHAR NOT NULL
);

DROP TABLE IF EXISTS member_rights;
CREATE TABLE member_rights(
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    club_id INT NOT NULL,
    right_id INT NOT NULL,
    is_active BOOLEAN NOT NULL,
    expiration_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES member(user_id),
    FOREIGN KEY (club_id) REFERENCES club(club_id),
    FOREIGN KEY (right_id) REFERENCES type_right(right_id)
);

DROP TABLE IF EXISTS member_events;
CREATE TABLE member_events(
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    event_id INT NOT NULL,
    is_confirmed BOOLEAN NOT NULL,
    date_for_signup DATE,
    FOREIGN KEY (user_id) REFERENCES member(user_id),
    FOREIGN KEY (event_id) REFERENCES event(event_id)
);

INSERT INTO member (email, password, first_name, last_name, gender, birth_date, country, address, zipcode, city, phone)
VALUES ('camillapasser@gmail.com', '$password1', 'Camilla', 'Passer Hvidman', 'Kvinde', '1997-03-01', 'Danmark', 'Valnøddegården 21', 2620, 'Albertslund', '20661013');

INSERT INTO type_right(type_right)
VALUES ('member'), ('admin'), ('global_admin');

