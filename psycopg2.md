# PostgreSQL Python

https://www.python.org/dev/peps/pep-0249/

## Connecting to the PostgreSQL database server – show you how to connect to the PostgreSQL database server from Python.

```
#!/bin/bash
sudo apt install libpq-dev # https://www.postgresql.org/docs/9.5/libpq.html
pip3 install psycopg2
```

```sql
CREATE DATABASE suppliers;
```

```py
import psycopg2
conn = psycopg2.connect("dbname=suppliers user=ryan password=''")
conn = psycopg2.connect(
    host="localhost",
    database="suppliers",
    user="postgres",
    password="Abcd1234")
    # port: the port number that defaults to 5432 if it is not provided.
```

```
# database.ini
[postgresql]
host=localhost
database=suppliers
user=postgres
password=SecurePas$1
```

```py
#!/usr/bin/python
#config.py
from configparser import ConfigParser

def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db
```

```py
#!/usr/bin/python
#connect.py
import psycopg2
from config import config

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        """
        connect( parameters... )
            Constructor for creating a connection to the database.

            Returns a Connection Object. It takes a number of parameters which are database dependent. [1]
        """
        # create a cursor
        cur = conn.cursor()
        """
        .cursor()
            Return a new Cursor Object using the connection.

            If the database does not provide a direct cursor concept, the module will have to emulate cursors using other means to the extent needed by this specification. [4]
        """
	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        """
        .execute(operation [, parameters])
            Prepare and execute a database operation (query or command).

            Parameters may be provided as sequence or mapping and will be bound to variables in the operation. Variables are specified in a database-specific notation (see the module's paramstyle attribute for details). [5]

            A reference to the operation will be retained by the cursor. If the same operation object is passed in again, then the cursor can optimize its behavior. This is most effective for algorithms where the same operation is used, but different parameters are bound to it (many times).

            For maximum efficiency when reusing an operation, it is best to use the .setinputsizes() method to specify the parameter types and sizes ahead of time. It is legal for a parameter to not match the predefined information; the implementation should compensate, possibly with a loss of efficiency.

            The parameters may also be specified as list of tuples to e.g. insert multiple rows in a single operation, but this kind of usage is deprecated: .executemany() should be used instead.

            Return values are not defined.
        """
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
        """
        .fetchone()
            Fetch the next row of a query result set, returning a single sequence, or None when no more data is available. [6]

            An Error (or subclass) exception is raised if the previous call to .execute*() did not produce any result set or no call was issued yet.
        """
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            """
            .close()
                Close the connection now (rather than whenever .__del__() is called).

                The connection will be unusable from this point forward; an Error (or subclass) exception will be raised if any operation is attempted with the connection. The same applies to all cursor objects trying to use the connection. Note that closing a connection without committing the changes first will cause an implicit rollback to be performed.
            """
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
```

## Creating new PostgreSQL tables in Python – show you how to create new tables in PostgreSQL from Python.

```py
#!/usr/bin/python
#create_table.py
import psycopg2
from config import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE vendors (
            vendor_id SERIAL PRIMARY KEY,
            vendor_name VARCHAR(255) NOT NULL
        )
        """,
        """ CREATE TABLE parts (
                part_id SERIAL PRIMARY KEY,
                part_name VARCHAR(255) NOT NULL
                )
        """,
        """
        CREATE TABLE part_drawings (
                part_id INTEGER PRIMARY KEY,
                file_extension VARCHAR(5) NOT NULL,
                drawing_data BYTEA NOT NULL,
                FOREIGN KEY (part_id)
                REFERENCES parts (part_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """
        CREATE TABLE vendor_parts (
                vendor_id INTEGER NOT NULL,
                part_id INTEGER NOT NULL,
                PRIMARY KEY (vendor_id , part_id),
                FOREIGN KEY (vendor_id)
                    REFERENCES vendors (vendor_id)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (part_id)
                    REFERENCES parts (part_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        """
        .commit()
            Commit any pending transaction to the database.

            Note that if the database supports an auto-commit feature, this must be initially off. An interface method may be provided to turn it back on.

            Database modules that do not support transactions should implement this method with void functionality.
        """
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


if __name__ == '__main__':
    create_tables()
```

## Inserting data into the PostgreSQL table in Python – explain to you how to insert data into a PostgreSQL database table in Python.

```py
#!/usr/bin/python
#insert.py

import psycopg2
from config import config


def insert_vendor(vendor_name):
    """ insert a new vendor into the vendors table """
    sql = """INSERT INTO vendors(vendor_name)
             VALUES(%s) RETURNING vendor_id;"""
    conn = None
    vendor_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (vendor_name,))
        # get the generated id back
        vendor_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return vendor_id
def insert_vendor_list(vendor_list):
    """ insert multiple vendors into the vendors table  """
    sql = "INSERT INTO vendors(vendor_name) VALUES(%s)"
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql,vendor_list)
        """
        .executemany( operation, seq_of_parameters )
            Prepare a database operation (query or command) and then execute it against all parameter sequences or mappings found in the sequence seq_of_parameters.

            Modules are free to implement this method using multiple calls to the .execute() method or by using array operations to have the database process the sequence as a whole in one call.

            Use of this method for an operation which produces one or more result sets constitutes undefined behavior, and the implementation is permitted (but not required) to raise an exception when it detects that a result set has been created by an invocation of the operation.

            The same comments as for .execute() also apply accordingly to this method.

            Return values are not defined.
        """
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    # insert one vendor
    insert_vendor("3M Co.")
    # insert multiple vendors
    insert_vendor_list([
        ('AKM Semiconductor Inc.',),
        ('Asahi Glass Co Ltd.',),
        ('Daikin Industries Ltd.',),
        ('Dynacast International Inc.',),
        ('Foster Electric Co. Ltd.',),
        ('Murata Manufacturing Co. Ltd.',)
    ])
```

## Updating data in the PostgreSQL table in Python – learn various ways to update data in the PostgreSQL table.

```py
#!/usr/bin/python
# update.py

import psycopg2
from config import config


def update_vendor(vendor_id, vendor_name):
    """ update vendor name based on the vendor id """
    sql = """ UPDATE vendors
                SET vendor_name = %s
                WHERE vendor_id = %s"""
    conn = None
    updated_rows = 0
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql, (vendor_name, vendor_id))
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows


if __name__ == '__main__':
    # Update vendor id 1
    update_vendor(1, "3M Corp")
```

## Transaction – show you how to perform transactions in Python.

```py
#!/usr/bin/python
# transaction.py

import psycopg2
from config import config


def add_part(part_name, vendor_list):
    # statement for inserting a new row into the parts table
    insert_part = "INSERT INTO parts(part_name) VALUES(%s) RETURNING part_id;"
    # statement for inserting a new row into the vendor_parts table
    assign_vendor = "INSERT INTO vendor_parts(vendor_id,part_id) VALUES(%s,%s)"

    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # insert a new part
        cur.execute(insert_part, (part_name,))
        # get the part id
        part_id = cur.fetchone()[0]
        # assign parts provided by vendors
        for vendor_id in vendor_list:
            cur.execute(assign_vendor, (vendor_id, part_id))

        # commit changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
```

## Querying data from the PostgreSQL tables – walk you through the steps of querying data from the PostgreSQL tables in a Python application.

```py
#!/usr/bin/python
# query.py

import psycopg2
from config import config


def get_vendors():
    """ query data from the vendors table """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT vendor_id, vendor_name FROM vendors ORDER BY vendor_name")
        print("The number of parts: ", cur.rowcount)

        colnames = [desc[0] for desc in cur.description]
        """
        .description
            This read-only attribute is a sequence of 7-item sequences.

            Each of these sequences contains information describing one result column:

            name
            type_code
            display_size
            internal_size
            precision
            scale
            null_ok
            The first two items (name and type_code) are mandatory, the other five are optional and are set to None if no meaningful values can be provided.

            This attribute will be None for operations that do not return rows or if the cursor has not had an operation invoked via the .execute*() method yet.

            The type_code can be interpreted by comparing it to the Type Objects specified in the section below.
        """
        print(colnames)

        row = cur.fetchone()

        while row is not None:
            print(row)
            row = cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    get_vendors()
```

## Calling a PostgreSQL function in Python – show you step by step how to call a PostgreSQL function in Python.

```py
"""
CREATE OR REPLACE FUNCTION get_parts_by_vendor(id integer)
  RETURNS TABLE(part_id INTEGER, part_name VARCHAR) AS
$$
BEGIN
 RETURN QUERY

 SELECT parts.part_id, parts.part_name
 FROM parts
 INNER JOIN vendor_parts on vendor_parts.part_id = parts.part_id
 WHERE vendor_id = id;

END; $$

LANGUAGE plpgsql;
"""

#!/usr/bin/python
# call.py

import psycopg2
from config import config

def get_parts(vendor_id):
    """ get parts provided by a vendor specified by the vendor_id """
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a cursor object for execution
        cur = conn.cursor()
        # another way to call a function
        # cur.execute("SELECT * FROM get_parts_by_vendor( %s); ",(vendor_id,))
        cur.callproc('get_parts_by_vendor', (vendor_id,))
        # process the result set
        row = cur.fetchone()
        while row is not None:
            print(row)
            row = cur.fetchone()
        # close the communication with the PostgreSQL database server
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    get_parts(1)
```

## Calling a PostgreSQL stored procedure in Python – guide you on how to call a stored procedure from in a Python application.

```py
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
```

## Handling PostgreSQL BLOB data in Python– give you an example of inserting and selecting the PostgreSQL BLOB data in a Python application.

```py
#!/usr/bin/python
# blob.py

import psycopg2
from config import config


def write_blob(part_id, path_to_file, file_extension):
    """ insert a BLOB into a table """
    conn = None
    try:
        # read data from a picture
        drawing = open(path_to_file, 'rb').read()
        # read database configuration
        params = config()
        # connect to the PostgresQL database
        conn = psycopg2.connect(**params)
        # create a new cursor object
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute("INSERT INTO part_drawings(part_id,file_extension,drawing_data) " +
                    "VALUES(%s,%s,%s)",
                    (part_id, file_extension, psycopg2.Binary(drawing)))
        """
        Binary(string)
            This function constructs an object capable of holding a binary (long) string value.
        """
        # commit the changes to the database
        conn.commit()
        # close the communication with the PostgresQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def read_blob(part_id, path_to_dir):
    """ read BLOB data from a table """
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgresQL database
        conn = psycopg2.connect(**params)
        # create a new cursor object
        cur = conn.cursor()
        # execute the SELECT statement
        cur.execute(""" SELECT part_name, file_extension, drawing_data
                        FROM part_drawings
                        INNER JOIN parts on parts.part_id = part_drawings.part_id
                        WHERE parts.part_id = %s """,
                    (part_id,))

        blob = cur.fetchone()
        open(path_to_dir + blob[0] + '.' + blob[1], 'wb').write(blob[2])
        # close the communication with the PostgresQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    write_blob(1, 'images/1.jpg', 'jpg')
    write_blob(2, 'images/2.jpg', 'jpg')
```

## Deleting data from PostgreSQL tables in Python – show you how to delete data in a table in Python.

```py
#!/usr/bin/python
# delete.py

import psycopg2
from config import config

def delete_part(part_id):
    """ delete part by part id """
    conn = None
    rows_deleted = 0
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute("DELETE FROM parts WHERE part_id = %s", (part_id,))
        # get the number of updated rows
        rows_deleted = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return rows_deleted

if __name__ == '__main__':
    deleted_rows = delete_part(2)
    print('The number of deleted rows: ', deleted_rows)
```
