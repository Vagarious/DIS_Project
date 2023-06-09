DROP VIEW IF EXISTS events_for_overview;

CREATE VIEW events_for_overview AS
SELECT event_id, event.club_id, CONCAT(club.name, ': ', event.name) AS name, event.zipcode, event.city, is_cancelled, date_from, signup_opens, signup_closes, max_spots FROM event
INNER JOIN club ON event.club_id = club.club_id;