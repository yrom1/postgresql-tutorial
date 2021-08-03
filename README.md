# Basic PostgreSQL Tutorial

```sql
-- order of operations:
/*
FROM
WHERE
GROUP BY
HAVING
SELECT
DISTINCT
ORDER BY
LIMIT
*/
```

## Section 1. Querying Data

### Select – show you how to query data from a single table.

```sql
SELECT
   first_name,
   last_name,
   email
FROM
   customer;
SELECT * FROM customer;
SELECT
   first_name || ' ' || last_name,
   email
FROM
   customer;
SELECT 5 * 3; -- expression
```

### Column aliases – learn how to assign temporary names to columns or expressions in a query.

```sql
SELECT
   first_name,
   last_name AS surname
FROM customer;
column_name AS "column alias"
SELECT
    first_name || ' ' || last_name "full name"
FROM
    customer;
```

### Order By – guide you on how to sort the result set returned from a query.

```sql
SELECT
	select_list
FROM
	table_name
ORDER BY
	sort_expression1 [ASC | DESC],
        ...
	sort_expressionN [ASC | DESC];
-- default is ASC
SELECT
	first_name,
	LENGTH(first_name) len
FROM
	customer
ORDER BY
	len DESC;
-- When you sort rows that contains NULL, you can specify the order
-- of NULL with other non-null values by using the NULLS FIRST or
-- NULLS LAST option of the ORDER BY clause:
-- ORDER BY sort_expresssion [ASC | DESC] [NULLS FIRST | NULLS LAST]
SELECT num
FROM sort_demo
ORDER BY num DESC NULLS LAST;
```

### Select Distinct – provide you a clause that removes duplicate rows in the result set.

```sql
SELECT
   DISTINCT column1
FROM
   table_name;
SELECT
	DISTINCT bcolor,
	fcolor
FROM
	distinct_demo
ORDER BY
	bcolor,
	fcolor;
-- Because we specified both bcolor and fcolor columns in the
-- SELECT DISTINCT clause, PostgreSQL combined the values in both
-- bcolor and fcolor columns to evaluate the uniqueness of the rows.
SELECT
	DISTINCT ON (bcolor) bcolor,
	fcolor
FROM
	distinct_demo
ORDER BY
	bcolor,
	fcolor;
-- PostgreSQL also provides the DISTINCT ON (expression) to keep the
-- “first” row of each group of duplicates using the following syntax:
```

## Section 2. Filtering Data

### Where – filter rows based on a specified condition.

```
Operator	Description
=	Equal
>	Greater than
<	Less than
>=	Greater than or equal
<=	Less than or equal
<> or !=	Not equal
AND	Logical operator AND
OR	Logical operator OR
IN	Return true if a value matches any value in a list
BETWEEN	Return true if a value is between a range of values
LIKE	Return true if a value matches a pattern
IS NULL	Return true if a value is NULL
NOT	Negate the result of other operators
```

```sql
SELECT select_list
FROM table_name
WHERE condition
ORDER BY sort_expression;
SELECT
	first_name,
	last_name
FROM
	customer
WHERE
	last_name = 'Rodriguez' OR
	first_name = 'Adam';
SELECT
	first_name,
	last_name
FROM
	customer
WHERE
	first_name IN ('Ann','Anne','Annie');
SELECT
	first_name,
	LENGTH(first_name) name_length
FROM
	customer
WHERE
	first_name LIKE 'A%' AND
	LENGTH(first_name) BETWEEN 3 AND 5
ORDER BY
	name_length;
```

### Limit – get a subset of rows generated by a query.

```sql
SELECT select_list
FROM table_name
LIMIT row_count OFFSET row_to_skip;
```

### Fetch– limit the number of rows returned by a query.

```sql
SELECT
    film_id,
    title
FROM
    film
ORDER BY
    title
OFFSET 5 ROWS
FETCH FIRST 5 ROW ONLY;
-- The LIMIT clause is not a SQL-standard. To conform with the
-- SQL standard, PostgreSQL supports the FETCH clause
```

### In – select data that matches any value in a list of values.

```sql
-- value IN (value1,value2,...)
value IN (SELECT column_name FROM table_name);
SELECT
	customer_id,
	first_name,
	last_name
FROM
	customer
WHERE
	customer_id IN (
		SELECT customer_id
		FROM rental
		WHERE CAST (return_date AS DATE) = '2005-05-27'
	)
ORDER BY customer_id;
```

### Between – select data that is a range of values.

```sql
-- value BETWEEN low AND high;
-- (value >= low AND value <= high;)
SELECT
	amount
FROM
	payment
WHERE
	amount NOT BETWEEN 8 AND 9;
SELECT
   payment_date
FROM
	payment
WHERE
	payment_date BETWEEN '2007-02-07' AND '2007-02-15';
```

### Like – filter data based on pattern matching.

```sql
SELECT
	'foo' LIKE 'foo', -- true
	'foo' LIKE 'f%', -- true
	'foo' LIKE '_o_', -- true
	'bar' LIKE 'b_'; -- false
```

```
Operator	Equivalent
~~	LIKE
~~*	ILIKE
!~~	NOT LIKE
!~~*	NOT ILIKE
```

```sql
select 'abc' LIKE 'a__';
-- is equal to:
select 'abc' ~~ 'a__';
```

### Is Null – check if a value is null or not.

```sql
-- select NULL = NULL; -> NULL
-- value IS NULL
SELECT
    phone
FROM
    contacts
WHERE
    phone IS /* NOT */ NULL;
```

## Section 3. Joining Multiple Tables

### Joins – show you a brief overview of joins in PostgreSQL.

```sql
-- inner join
SELECT
    a,
    fruit_a,
    b,
    fruit_b
FROM
    basket_a
INNER JOIN basket_b
    ON fruit_a = fruit_b;

-- left outer join
SELECT
    a,
    fruit_a,
    b,
    fruit_b
FROM
    basket_a
LEFT JOIN basket_b
   ON fruit_a = fruit_b;

-- left outer join, only left rows
SELECT
    a,
    fruit_a,
    b,
    fruit_b
FROM
    basket_a
LEFT JOIN basket_b
    ON fruit_a = fruit_b
WHERE b IS NULL;

-- right outer join
SELECT
    a,
    fruit_a,
    b,
    fruit_b
FROM
    basket_a
RIGHT JOIN basket_b ON fruit_a = fruit_b;

-- right outer join, only right rows
SELECT
    a,
    fruit_a,
    b,
    fruit_b
FROM
    basket_a
RIGHT JOIN basket_b
   ON fruit_a = fruit_b
WHERE a IS NULL;

-- full outer join
SELECT
    a,
    fruit_a,
    b,
    fruit_b
FROM
    basket_a
FULL OUTER JOIN basket_b
    ON fruit_a = fruit_b;

-- full outer join, only unique to both tables
SELECT
    a,
    fruit_a,
    b,
    fruit_b
FROM
    basket_a
FULL JOIN basket_b
   ON fruit_a = fruit_b
WHERE a IS NULL OR b IS NULL;
```

### Table aliases – describes how to use table aliases in the query.

```sql
-- a_very_long_table_name.column_name
-- a_very_long_table_name AS alias
-- alias.column_name
SELECT
    e.first_name employee,
    m .first_name manager
FROM
    employee e
INNER JOIN employee m
    ON m.employee_id = e.manager_id
ORDER BY manager;
```

### Self-join – join a table to itself by comparing a table to itself.

```sql
SELECT select_list
FROM table_name t1
INNER JOIN table_name t2 ON join_predicate;
SELECT select_list
FROM table_name t1
LEFT JOIN table_name t2 ON join_predicate;
```

### Cross Join – produce a Cartesian product of the rows in two or more tables.

```sql
SELECT select_list
FROM T1
CROSS JOIN T2;
SELECT select_list
FROM T1, T2;
-- Also, you can use an INNER JOIN clause with a condition that always
-- evaluates to true to simulate the cross join:

SELECT *
FROM T1
INNER JOIN T2 ON true;
```

### Natural Join – join two or more tables using implicit join condition based on the common column names in the joined tables.

```sql
-- A natural join is a join that creates an implicit join based
-- on the same column names in the joined tables.
SELECT	* FROM products
INNER JOIN categories USING (category_id); -- brackets NECESSARY
-- becomes:
SELECT * FROM products
NATURAL JOIN categories;
```

## Section 4. Grouping Data

### Group By – divide rows into groups and applies an aggregate function on each.

```sql
SELECT
   customer_id
FROM
   payment
GROUP BY
   customer_id;
-- In this case, the GROUP BY works like the DISTINCT clause
-- that removes duplicate rows from the result set.

SELECT
	customer_id,
	SUM (amount)
FROM
	payment
GROUP BY
	customer_id;
SELECT
	DATE(payment_date) paid_date,
	SUM(amount) sum
FROM
	payment
GROUP BY
	DATE(payment_date);
```

### Having – apply conditions to groups.

```sql
SELECT
	store_id,
	COUNT (customer_id)
FROM
	customer
GROUP BY
	store_id
HAVING
	COUNT (customer_id) > 300;
```

## Section 5. Set Operations

### Union – combine result sets of multiple queries into a single result set.

```sql
SELECT * FROM top_rated_films
UNION
SELECT * FROM most_popular_films;
SELECT * FROM top_rated_films
UNION ALL
SELECT * FROM most_popular_films;
```

### Intersect – combine the result sets of two or more queries and returns a single result set that has the rows appear in both result sets.

```sql
SELECT * FROM most_popular_films
INTERSECT
SELECT * FROM top_rated_films;
```

### Except – return the rows in the first query that does not appear in the output of the second query.

```sql
SELECT * FROM top_rated_films
EXCEPT
SELECT * FROM most_popular_films;
```

## Section 6. Grouping sets, Cube, and Rollup

### Grouping Sets – generate multiple grouping sets in reporting.

```sql
-- For example, the following query uses the GROUP BY clause
-- to return the number of products sold by brand and segment.
-- In other words, it defines a grouping set of the brand
-- and segment which is denoted by (brand, segement)

SELECT
    brand,
    segment,
    SUM (quantity)
FROM
    sales
GROUP BY
    brand,
    segment;
SELECT
    c1,
    c2,
    aggregate_function(c3)
FROM
    table_name
SELECT
    brand,
    segment,
    SUM (quantity) -- not in GROUPING SETS
FROM
    sales
GROUP BY
    GROUPING SETS (
        (brand, segment),
        (brand),
        (segment),
        ()
    );
```

### Cube – define multiple grouping sets that include all possible combinations of dimensions.

```sql
SELECT
    c1,
    c2,
    c3,
    aggregate (c4)
FROM
    table_name
GROUP BY
    CUBE (c1, c2, c3);
-- The query generates all possible grouping sets based
-- on the dimension columns specified in CUBE.
/*
CUBE(c1,c2,c3)

GROUPING SETS (
    (c1,c2,c3),
    (c1,c2),
    (c1,c3),
    (c2,c3),
    (c1),
    (c2),
    (c3),
    ()
 )
*/
```

### Rollup – generate reports that contain totals and subtotals.

```sql
SELECT
    c1,
    c2,
    c3,
    aggregate(c4)
FROM
    table_name
GROUP BY
    ROLLUP (c1, c2, c3);
/*
(c1, c2, c3)
(c1, c2)
(c1)
()
*/

```

## Section 7. Subquery

### Subquery – write a query nested inside another query.

```sql
SELECT
	film_id,
	title,
	rental_rate
FROM
	film
WHERE
	rental_rate > (
		SELECT
			AVG (rental_rate)
		FROM
			film
	);
```

### ANY – retrieve data by comparing a value with a set of values returned by a subquery.

```sql
-- expresion operator ANY(subquery)
SELECT title
FROM film
WHERE length >= ANY(
    SELECT MAX( length )
    FROM film
    INNER JOIN film_category USING(film_id)
    GROUP BY  category_id );
-- The `= ANY` operator is different from NOT IN.
-- The following expression x <> ANY (a,b,c) is equivalent to:
-- x <> a OR <> b OR x <> c
```

### ALL – query data by comparing a value with a list of values returned by a subquery.

```sql
-- comparison_operator ALL (subquery)
SELECT
    title,
FROM
    film
WHERE
    length > ALL (
            SELECT
                ROUND(AVG (length),2)
            FROM
                film
            GROUP BY
                rating
    )
ORDER BY
    length;
```

### EXISTS – check for the existence of rows returned by a subquery.

```sql
-- EXISTS (subquery)
-- If the subquery returns at least one row, the result of EXISTS
-- is true. In case the subquery returns no row, the result is
-- of EXISTS is false.

SELECT first_name;
FROM customer c
WHERE EXISTS
    (SELECT 1
     FROM payment p
     WHERE p.customer_id = c.customer_id
       AND amount > 11 )
ORDER BY first_name;
```

## Section 8. Common Table Expressions

### PostgreSQL CTE – introduce you to PostgreSQL common table expressions or CTEs.

```sql
WITH cte_film AS (
    SELECT
        film_id,
        title,
        (CASE
            WHEN length < 30 THEN 'Short'
            WHEN length < 90 THEN 'Medium'
            ELSE 'Long'
        END) length
    FROM
        film
)
SELECT
    film_id,
    title,
    length
FROM
    cte_film
WHERE
    length = 'Long'
ORDER BY
    title;
```

### Recursive query using CTEs – discuss the recursive query and learn how to apply it in various contexts.

```sql
WITH RECURSIVE cte_count (n)
AS (
      SELECT 1
      UNION ALL
      SELECT n + 1
      FROM cte_count
      WHERE n < 3
    )
SELECT n
FROM cte_count;

/*
+---+
| n |
+---+
  1
  2
  3
*/
```

## Section 9. Modifying Data

### Insert – guide you on how to insert single row into a table.

```sql
-- PostgreSQL automatically generates a sequential number for the
-- serial column so you do not have to supply a value for the
-- serial column in the INSERT statement.
INSERT INTO links (url, name)
VALUES('http://www.oreilly.com','O''Reilly Media'); -- escape quote
INSERT INTO links (url, name)
VALUES('http://www.postgresql.org','PostgreSQL')
RETURNING id;
```

### Insert multiple rows – show you how to insert multiple rows into a table.

```sql
INSERT INTO
    links(url, description)
VALUES
    ('https://duckduckgo.com/','Privacy & Simplified Search Engine'),
    ('https://swisscows.com/','Privacy safe WEB-search')
RETURNING *; -- returns table of inserted rows

```

### Update – update existing data in a table.

```sql
UPDATE courses
SET published_date = '2020-07-01'
WHERE course_id = 2
RETURNING *;
```

### Update join – update values in a table based on values in another table.

```sql
UPDATE product
SET net_price = price - price * discount
FROM product_segment
WHERE product.segment_id = product_segment.id;
```

### Delete – delete data in a table.

```sql
DELETE FROM links
WHERE id = 7
RETURNING *;
```

### Upsert – insert or update data if the new row already exists in the table.

```sql
-- The idea is that when you insert a new row into the table, PostgreSQL
-- will update the row if it already exists, otherwise, it will insert
-- the new row. That is why we call the action is upsert
-- (the combination of update or insert).
INSERT INTO customers (NAME, email)
VALUES('Microsoft','hotline@microsoft.com')
ON CONFLICT ON CONSTRAINT customers_name_key
DO NOTHING;
-- this is the same as:
INSERT INTO customers (name, email)
VALUES('Microsoft','hotline@microsoft.com')
ON CONFLICT (name)
DO NOTHING;
INSERT INTO customers (name, email)
VALUES('Microsoft','hotline@microsoft.com')
ON CONFLICT (name)
DO
   UPDATE SET email = EXCLUDED.email || ';' || customers.email;
```

## Section 10. Transactions

### PostgreSQL Transactions – show you how to handle transactions in PostgreSQL using BEGIN, COMMIT, and ROLLBACK statements.

```sql
BEGIN TRANSACTION;
-- same as:
BEGIN WORK;
-- same as:
BEGIN;

COMMIT WORK;
-- same as:
COMMIT TRANSACTION;
-- same as:
COMMIT;

BEGIN;

UPDATE accounts
SET balance = balance - 1000
WHERE id = 1;

UPDATE accounts
SET balance = balance + 1000
WHERE id = 2;

SELECT id, name, balance
FROM accounts;

COMMIT;

ROLLBACK WORK;
-- same as:
ROLLBACK TRANSACTION;
-- same as:
ROLLBACK;

BEGIN;

UPDATE accounts
SET balance = balance - 1500
WHERE id = 1;

UPDATE accounts
SET balance = balance + 1500
WHERE id = 3;

-- roll back the transaction
ROLLBACK;
```

## Section 11. Import & Export Data

### Import CSV file into Table – show you how to import CSV file into a table.

```sql
-- First, create a new table named persons with the following columns:
CREATE TABLE persons (
  id SERIAL,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  dob DATE,
  email VARCHAR(255),
  PRIMARY KEY (id)
)
/*
user@ubuntu:~/Downloads$ cat persons.csv
First Name,Last Name,Date Of Birth,Email
John,Doe,1995-01-05,john.doe@postgresqltutorial.com
Jane,Doe,1995-02-05,jane.doe@postgresqltutorial.com
*/
COPY persons(first_name, last_name, dob, email) -- or \copy
FROM 'C:\sampledb\persons.csv'
DELIMITER ','
CSV HEADER;

-- clear table before reinserting again
TRUNCATE TABLE persons
RESTART IDENTITY;
```

### Export PostgreSQL Table to CSV file – show you how to export tables to a CSV file.

```sql
COPY persons(first_name,last_name,email) -- or \copy
TO 'C:\tmp\persons_partial_db.csv'
DELIMITER ','
CSV HEADER;

-- The \copy command basically runs the COPY statement above. However,
-- instead of server writing the CSV file, psql writes the CSV file,
-- transfers data from the server to your local file system. To use \copy
-- command, you just need to have sufficient privileges to your local
-- machine. It does not require PostgreSQL superuser privileges.
```

## Section 12. Managing Tables

### Data types – cover the most commonly used PostgreSQL data types.

```sql
/*
Boolean
Character types such as char, varchar, and text.
Numeric types such as integer and floating-point number.
Temporal types such as date, time, timestamp, and interval
UUID for storing Universally Unique Identifiers
Array for storing array strings, numbers, etc.
JSON stores JSON data
hstore stores key-value pair
Special types such as network address and geometric data.
*/
```

### Create table – guide you on how to create a new table in the database.

```sql
CREATE TABLE roles(
   role_id serial PRIMARY KEY,
   role_name VARCHAR (255) UNIQUE NOT NULL
);
CREATE TABLE IF NOT EXISTS account_roles (
  user_id INT NOT NULL,
  role_id INT NOT NULL,
  grant_date TIMESTAMP,
  PRIMARY KEY (user_id, role_id),
  FOREIGN KEY (role_id)
      REFERENCES roles (role_id),
  FOREIGN KEY (user_id)
      REFERENCES accounts (user_id)
);
```

### Select Into & Create table as– shows you how to create a new table from the result set of a query.

```sql
SELECT
    film_id,
    title,
    length
INTO TEMP TABLE short_film -- A temporary table, as its named implied, is a
                           -- short-lived table that exists for the duration
                           -- of a database session.
                           -- TEMP is ***optional*** here.
FROM
    film
WHERE
    length < 60
ORDER BY
    title;

-- CREATE TABLE new_table_name
-- AS query;

CREATE TABLE action_film AS
SELECT
    film_id,
    title,
    release_year,
    length,
    rating
FROM
    film
INNER JOIN film_category USING (film_id)
WHERE
    category_id = 1;

```

### Auto-increment column with SERIAL – uses SERIAL to add an auto-increment column to a table.

```sql
CREATE TABLE table_name(
    id SERIAL
);
-- is same as:
CREATE SEQUENCE table_name_id_seq; -- default is 1, 2, 3...

CREATE TABLE table_name (
    id integer NOT NULL DEFAULT nextval('table_name_id_seq')
);

ALTER SEQUENCE table_name_id_seq
OWNED BY table_name.id;


INSERT INTO fruits(id,name)
VALUES(DEFAULT,'Apple');
-- using same table:
INSERT INTO fruits(name)
VALUES('Orange');
```

### Sequences – introduce you to sequences and describe how to use a sequence to generate a sequence of numbers.

```sql
CREATE SEQUENCE mysequence
INCREMENT 5
START 100; -- inclusive start [...
SELECT nextval('mysequence'); -- 100
-- 105, ...

CREATE SEQUENCE three
INCREMENT -1
MINVALUE 1 -- inclusive
MAXVALUE 3 -- inclusive
START 3
CYCLE; -- 3, 2, 1, 3, 2, 1

CREATE SEQUENCE order_item_id
START 10
INCREMENT 10
MINVALUE 10
OWNED BY order_details.item_id;
INSERT INTO
    order_details(order_id, item_id, item_text, price)
VALUES
    (100, nextval('order_item_id'),'DVD Player',100),
    (100, nextval('order_item_id'),'Android TV',550),
    (100, nextval('order_item_id'),'Speaker',250);

-- DROP SEQUENCE [ IF EXISTS ] sequence_name [, ...][ CASCADE ];
DROP TABLE order_details; -- drops order_item_id sequence
```

### Identity column – show you how to use the identity column.

```sql
-- The GENERATED AS IDENTITY constraint is the SQL standard-conforming
-- variant of the good old SERIAL column.
CREATE TABLE color (
    color_id INT GENERATED ALWAYS AS IDENTITY,
    color_name VARCHAR NOT NULL
);
-- then this causes error:
INSERT INTO color (color_id, color_name)
VALUES (2, 'Green'); -- ERROR

CREATE TABLE color (
    color_id INT GENERATED BY DEFAULT AS IDENTITY,
    color_name VARCHAR NOT NULL
);
-- then this doesnt cause error:
INSERT INTO color (color_id, color_name)
VALUES (2, 'Yellow'); -- fine

CREATE TABLE color (
    color_id INT GENERATED BY DEFAULT AS IDENTITY
    (START WITH 10 INCREMENT BY 10), -- 10, 20,...
    color_name VARCHAR NOT NULL
);

ALTER TABLE shape
ALTER COLUMN shape_id ADD GENERATED ALWAYS AS IDENTITY; -- shape_id col
                                                    -- must be NOT NULL
ALTER TABLE shape
ALTER COLUMN shape_id
DROP IDENTITY IF EXISTS;
```

### Alter table – modify the structure of an existing table.

```sql
/*
ADD COLUMN
DROP COLUMN
SET/DROP DEFAULT
SET/DROP NOT NULL
ADD CHECK
ADD CONSTRAINT
RENAME TO
*/
ALTER TABLE table_name
ADD COLUMN column_name datatype column_constraint;
ALTER TABLE table_name
RENAME COLUMN column_name TO new_column_name;
```

### Rename table – change the name of the table to a new one.

```sql
-- When you rename a table to the new one, PostgreSQL will automatically
-- update its dependent objects such as foreign key constraints, views,
-- and indexes.
ALTER TABLE IF EXISTS table_name
RENAME TO new_table_name;
```

### Add column – show you how to use add one or more columns to an existing table.

```sql
ALTER TABLE customers
ADD COLUMN fax VARCHAR,
ADD COLUMN email VARCHAR NOT NULL;
```

### Drop column – demonstrate how to drop a column of a table.

```sql
ALTER TABLE table_name
DROP COLUMN IF EXISTS column_name CASCADE;
-- CASCADE If the column that you want to remove is used in other database
-- objects such as views, triggers, stored procedures, etc.,
```

### Change column data type – show you how to change the data of a column.

```sql
ALTER TABLE assets
ALTER COLUMN asset_no TYPE INT;
ALTER TABLE assets
ALTER COLUMN asset_no TYPE INT
USING asset_no::integer;
```

### Rename column – illustrate how to rename one or more columns of a table.

```sql
ALTER TABLE customer_groups
RENAME COLUMN name TO group_name;
```

### Drop table – remove an existing table and all of its dependent objects.

```sql
DROP TABLE IF EXISTS author CASCADE;
DROP TABLE tvshows, animes;
```

### Truncate table – remove all data in a large table quickly and efficiently.

```sql
TRUNCATE TABLE invoices CASCADE
RESTART IDENTITY;
```

### Temporary table – show you how to use the temporary table.

```sql
CREATE TEMP TABLE mytemp(c INT);
```

### Copy a table – show you how to copy a table to a new one.

```sql
CREATE TABLE new_table AS
TABLE existing_table;
CREATE TABLE new_table AS
TABLE existing_table
WITH NO DATA;
CREATE TABLE new_table AS
SELECT
*
FROM
    existing_table
WHERE
    condition;
```
