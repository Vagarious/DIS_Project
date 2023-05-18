DROP VIEW IF EXISTS signUps;

CREATE VIEW signUps AS
SELECT event.name AS event_name, concat(firstname, ' ', lastname) AS name, date_for_signup
FROM member_events
INNER JOIN member ON member_events.userid = member.userid
INNER JOIN event ON member_events.eventid = event.eventid
ORDER BY date_for_signup DESC