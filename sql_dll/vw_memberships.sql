DROP VIEW IF EXISTS memberships;

CREATE VIEW memberships AS
SELECT member_rights.id AS memberno,
member.userid,
concat(firstname, ' ', lastname) as name,
club.name as club,
active as status,
expiration_date
FROM member_rights
INNER JOIN member on member_rights.userid = member.userid
INNER JOIN club on member_rights.clubid = club.clubid
ORDER BY memberno;