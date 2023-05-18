DROP VIEW IF EXISTS memberships;

CREATE VIEW memberships AS
SELECT member.user_id,
member_rights.id AS memberno,
concat(first_name, ' ', last_name) as name,
club.name as club,
is_active as status,
expiration_date
FROM member_rights
INNER JOIN member on member_rights.user_id = member.user_id
INNER JOIN club on member_rights.club_id = club.club_id
ORDER BY memberno;