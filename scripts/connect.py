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
        """
        .close()
            Close the connection now (rather than whenever .__del__() is called).

            The connection will be unusable from this point forward; an Error (or subclass) exception will be raised if any operation is attempted with the connection. The same applies to all cursor objects trying to use the connection. Note that closing a connection without committing the changes first will cause an implicit rollback to be performed.
        """
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
