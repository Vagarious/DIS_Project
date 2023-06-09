INSERT INTO 
    member_rights(user_id, club_id, right_id, is_active, expiration_date)
VALUES 
    -- Camilla is admin for Teitur
    (1,44,2,true,'2023-12-31'),
    -- Sofie is member of Hrimnir Vestskoven
    (2,29,1,true,'2023-12-31'),
    -- Admin is global_admin
    (3,null,3,true,null);