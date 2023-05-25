DROP VIEW IF EXISTS events_need_confirmation;
CREATE VIEW events_need_confirmation AS
SELECT member.user_id, event.event_id, event.name AS event_name, CONCAT(first_name, ' ', last_name) AS name, club.name AS club_name, event.price
FROM member_events
INNER JOIN member ON member_events.user_id = member.user_id
INNER JOIN event ON member_events.event_id = event.event_id
INNER JOIN club ON event.club_id = club.club_id
WHERE member_events.is_confirmed = false
ORDER BY event.date_from