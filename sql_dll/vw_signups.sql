DROP VIEW IF EXISTS signups;

CREATE VIEW signups AS
SELECT member.user_id, event.event_id, event.name AS event_name, concat(first_name, ' ', last_name) AS name, date_for_signup
FROM member_events
INNER JOIN member ON member_events.user_id = member.user_id
INNER JOIN event ON member_events.event_id = event.event_id
WHERE member_events.is_confirmed = true
ORDER BY date_for_signup DESC