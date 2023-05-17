\c sportilight

DROP TABLE IF EXISTS member CASCADE;
CREATE TABLE member(
    userID SERIAL PRIMARY KEY,
    email VARCHAR NOT NULL,
    firstName VARCHAR NOT NULL,
    lastName VARCHAR NOT NULL,
    gender VARCHAR NOT NULL,
    birthDate DATE NOT NULL,
    nationality VARCHAR NOT NULL,
    address VARCHAR NOT NULL,
    zipcode INT NOT NULL,
    city VARCHAR NOT NULL,
    phone VARCHAR
);

DROP TABLE IF EXISTS club CASCADE;
CREATE TABLE club(
    clubID SERIAL PRIMARY KEY,
    info TEXT NOT NULL,
    name VARCHAR NOT NULL,
    zipcode INT NOT NULL,
    city VARCHAR NOT NULL,
    email VARCHAR NOT NULL,
    websiteURL VARCHAR NOT NULL
);

DROP TABLE IF EXISTS event CASCADE;
CREATE TABLE event(
    eventID SERIAL PRIMARY KEY,
    info TEXT NOT NULL,
    name VARCHAR NOT NULL,
    price INT NOT NULL,
    clubID INT NOT NULL,
    locationAddress VARCHAR NOT NULL,
    locationZipcode INT NOT NULL,
    locationCity VARCHAR NOT NULL,
    locationCountry VARCHAR NOT NULL,
    FOREIGN KEY (clubID) REFERENCES club(clubID)
);

DROP TABLE IF EXISTS typeRight CASCADE;
CREATE TABLE typeRight(
    rightID SERIAL PRIMARY KEY,
    typeRight VARCHAR NOT NULL
);

DROP TABLE IF EXISTS member_rights;
CREATE TABLE member_rights(
    id SERIAL PRIMARY KEY,
    userID INT NOT NULL,
    clubID INT NOT NULL,
    rightID INT NOT NULL,
    FOREIGN KEY (userID) REFERENCES member(userID),
    FOREIGN KEY (clubID) REFERENCES club(clubID),
    FOREIGN KEY (rightID) REFERENCES typeRight(rightID)
);

DROP TABLE IF EXISTS member_events;
CREATE TABLE member_events(
    id SERIAL PRIMARY KEY,
    userID INT NOT NULL,
    eventID INT NOT NULL,
    is_in_future BOOLEAN NOT NULL,
    is_confirmed BOOLEAN NOT NULL,
    FOREIGN KEY (userID) REFERENCES member(userID),
    FOREIGN KEY (eventID) REFERENCES event(eventID)
);

INSERT INTO member (email, firstName, lastName, gender, birthDate, nationality, address, zipcode, city, phone)
VALUES ('camillapasser@gmail.com', 'Camilla', 'Passer Hvidman', 'Kvinde', '1997-03-01', 'Danmark', 'Valnøddegården 21', 2620, 'Albertslund', '20661013');

INSERT INTO club (info, name, zipcode, city, email, websiteURL)
VALUES ('Dette er en beskrivelse af lokalklubben Teitur', 'Teitur Amager', 2300, 'København S', 'sofinejensen@gmail,com', 'www.teitur-amager.dk');

INSERT INTO event (info, name, price, clubID, locationAddress, locationZipcode, locationCity, locationCountry)
VALUES ('Dette en en beskrivelse af et event af lokalklubben Teitur', 'Istur', 0, 1, 'Hollænderhallen - Mødelokale 3\nHalvejen 3',2791,'Dragør','Danmark');

INSERT INTO typeRight(typeRight) VALUES ('Admin');
INSERT INTO typeRight(typeRight) VALUES ('Member');

INSERT INTO member_rights(userID, clubID, rightID) VALUES (1,1,1);

INSERT INTO member_events(userID, eventID, is_in_future, is_confirmed) VALUES (1,1,'false','true')
