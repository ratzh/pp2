CREATE OR REPLACE FUNCTION search_contacts_2(p_pattern TEXT)
RETURNS TABLE(name TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT c.name, c.phone
    FROM contacts_2 AS c
    WHERE c.name ILIKE '%' || p_pattern || '%'
       OR c.phone ILIKE '%' || p_pattern || '%';
END;
$$ LANGUAGE plpgsql;

-- 📄 PAGINATION FUNCTION (contacts_2)
CREATE OR REPLACE FUNCTION get_contacts_paginated_2(p_limit INT, p_offset INT)
RETURNS TABLE(name TEXT, phone TEXT) AS $$
BEGIN
    RETURN QUERY
    SELECT name, phone
    FROM contacts_2
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;