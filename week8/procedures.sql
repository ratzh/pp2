CREATE OR REPLACE PROCEDURE upsert_contact_2(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts_2 WHERE name = p_name) THEN
        UPDATE contacts_2
        SET phone = p_phone
        WHERE name = p_name;
    ELSE
        INSERT INTO contacts_2(name, phone)
        VALUES (p_name, p_phone);
    END IF;
END;
$$;


CREATE OR REPLACE PROCEDURE insert_many_contacts_2(
    p_names TEXT[], 
    p_phones TEXT[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(p_names, 1) LOOP
        IF length(p_phones[i]) = 11 THEN
            CALL upsert_contact_2(p_names[i], p_phones[i]);
        ELSE
            RAISE NOTICE 'Invalid phone: %', p_phones[i];
        END IF;
    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact_2(p_value TEXT)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts_2
    WHERE name = p_value OR phone = p_value;
END;
$$;