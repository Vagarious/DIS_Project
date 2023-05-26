CREATE OR REPLACE FUNCTION add_participant()
	RETURNS trigger AS
$$
BEGIN
	IF NEW.is_confirmed THEN
		UPDATE event
		SET participants = participants + 1
    	WHERE event_id = NEW.event_id;

		IF (SELECT EXISTS(SELECT max_spots FROM event WHERE event_id = NEW.event_id AND max_spots IS NOT NULL)) THEN
			IF (SELECT EXISTS(SELECT max_spots FROM event WHERE event_id = NEW.event_id AND max_spots > 0)) THEN
				UPDATE event
				SET max_spots = max_spots - 1
				WHERE event_id = NEW.event_id;
			END IF;
		END IF;
	END IF;
	RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE OR REPLACE TRIGGER update_participants
	AFTER UPDATE
	ON member_events
	FOR EACH ROW
	EXECUTE PROCEDURE add_participant();