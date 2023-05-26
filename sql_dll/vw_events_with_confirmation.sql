DROP VIEW IF EXISTS events_with_confirmation;

CREATE VIEW events_with_confirmation AS
SELECT member.user_id, event.event_id, CONCAT(first_name, ' ', last_name) AS name, event.name AS event_name, club.name AS club_name, is_confirmed 
FROM member_events
INNER JOIN member ON member_events.user_id = member.user_id
INNER JOIN event on member_events.event_id = event.event_id
INNER JOIN club on event.club_id = club.club_id
WHERE is_confirmed = true
ORDER BY club_name;