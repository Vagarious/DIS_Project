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
    website_url VARCHAR NOT NULL
);

DROP TABLE IF EXISTS event CASCADE;
CREATE TABLE event(
    event_id SERIAL PRIMARY KEY,
    info TEXT NOT NULL,
    name VARCHAR NOT NULL,
    price INT NOT NULL,
    club_id INT NOT NULL,
    address VARCHAR NOT NULL,
    zipcode INT NOT NULL,
    city VARCHAR NOT NULL,
    country VARCHAR NOT NULL,
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
    is_in_future BOOLEAN NOT NULL,
    is_confirmed BOOLEAN NOT NULL,
    date_for_signup DATE,
    FOREIGN KEY (user_id) REFERENCES member(user_id),
    FOREIGN KEY (event_id) REFERENCES event(event_id)
);

INSERT INTO member (email, password, first_name, last_name, gender, birth_date, country, address, zipcode, city, phone)
VALUES ('camillapasser@gmail.com', '$password1', 'Camilla', 'Passer Hvidman', 'Kvinde', '1997-03-01', 'Danmark', 'Valnøddegården 21', 2620, 'Albertslund', '20661013');

INSERT INTO club (info, name, zipcode, city, email, website_url)
VALUES ('Dette er en beskrivelse af lokalklubben Teitur', 'Teitur', 2300, 'København S', 'sofinejensen@gmail,com', 'www.teitur-amager.dk');

INSERT INTO event (info, name, price, club_id, address, zipcode, city, country)
VALUES ('Dette en en beskrivelse af et event af lokalklubben Teitur', 'Teitur: Istur', 0, 1, 'Hollænderhallen - Mødelokale 3\nHalvejen 3',2791,'Dragør','Danmark');

INSERT INTO event (info, name, price, club_id, address, zipcode, city, country)
VALUES ('Event2', 'Event2',2,1,'test',2791,'Dragør','Danmark');

INSERT INTO type_right(type_right) VALUES ('Admin');
INSERT INTO type_right(type_right) VALUES ('Member');

INSERT INTO member_rights(user_id, club_id, right_id, is_active, expiration_date) VALUES (1,1,1,true,'2023-12-31');

INSERT INTO member_events(user_id, event_id, is_in_future, is_confirmed, date_for_signup) VALUES (1,1,'false','true', '2023-05-18');
INSERT INTO member_events(user_id, event_id, is_in_future, is_confirmed, date_for_signup) VALUES (1,2,'false','true','2040-02-15');
