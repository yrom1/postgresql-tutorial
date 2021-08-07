"""
CREATE OR REPLACE PROCEDURE add_new_part(
	new_part_name varchar,
	new_vendor_name varchar
) 
AS $$
DECLARE
	v_part_id INT;
	v_vendor_id INT;
BEGIN
	-- insert into the parts table
	INSERT INTO parts(part_name) 
	VALUES(new_part_name) 
	RETURNING part_id INTO v_part_id;
	
	-- insert a new vendor
	INSERT INTO vendors(vendor_name)
	VALUES(new_vendor_name)
	RETURNING vendor_id INTO v_vendor_id;
	
	-- insert into vendor_parts
	INSERT INTO vendor_parts(part_id, vendor_id)
	VALUEs(v_part_id,v_vendor_id);
	
END;
$$
LANGUAGE PLPGSQL;
"""

#!/usr/bin/python
# stored_proc.py

import psycopg2
from config import config


def add_part(part_name, vendor_name):

    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a cursor object for execution
        cur = conn.cursor()

        # call a stored procedure
        cur.execute('CALL add_new_part(%s,%s)', (part_name, vendor_name))

        # commit the transaction
        conn.commit()

        # close the cursor
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    add_part('OLED', 'LG')