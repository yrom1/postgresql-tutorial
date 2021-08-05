# PostgreSQL Views

## Managing PostgreSQL views – introduce you to the concept of the view and show you how to create, modify, and remove PostgreSQL views.

```sql
-- A view is a database object that is of a stored query.
-- A view can be accessed as a virtual table in PostgreSQL.
CREATE OR REPLACE view_name AS SELECT * FROM mytable;
ALTER VIEW customer_master RENAME TO customer_info;
DROP VIEW IF EXISTS customer_info;
```

## Drop view – learn how to drop one or more views from the database.

```sql
DROP VIEW film_master CASCADE;
/*NOTICE:  drop cascades to view horror_film*/
DROP VIEW film_length_stat, film_category_stat;
```

## Create updatable views – give you examples of creating updatable views that allow you to issue INSERT, UPDATE, and DELETE statements to update data in the base tables through the views.

```sql
/*
The defining query of the view must have exactly one entry in the FROM clause,
which can be a table or another updatable view.
The defining query must not contain one of the following clauses at the top
level: GROUP BY, HAVING, LIMIT, OFFSET, DISTINCT, WITH, UNION, INTERSECT, and
EXCEPT.
The selection list must not contain any window function , any set-returning
function, or any aggregate function such as SUM, COUNT, AVG, MIN, and MAX.
*/
DELETE
FROM
	usa_cities
WHERE
	city = 'San Jose';
-- The entry has been deleted from the city table through the usa_cities view.
```

## Materialized views – introduce you to materialized views and provide you with the steps of creating and refreshing data for materialized views.

```sql
-- Materialized views cache the result of a complex and expensive query and allow
-- you to refresh this result periodically.
CREATE MATERIALIZED VIEW view_name
AS
query
WITH [NO] DATA;
REFRESH MATERIALIZED VIEW view_name; -- locks table
REFRESH MATERIALIZED VIEW CONCURRENTLY view_name; -- doesnt lock table
DROP MATERIALIZED VIEW view_name;
```

## Creating updatable views using the WITH CHECK OPTION clause – show you how to use the WITH CHECK OPTION clause to check the view-defining condition when you make a change to the base table through the view.

```sql
CREATE
OR REPLACE VIEW usa_city AS SELECT
	city_id,
	city,
	country_id
FROM
	city
WHERE
	country_id = 103
ORDER BY
	city WITH CHECK OPTION;
```

## Create recursive views – introduce you to the recursive view and show you an example of creating a recursive view in PostgreSQL.

```sql
WITH RECURSIVE reporting_line AS (
	SELECT
		employee_id,
		full_name AS subordinates
	FROM
		employees
	WHERE
		manager_id IS NULL
	UNION ALL
		SELECT
			e.employee_id,
			(
				rl.subordinates || ' > ' || e.full_name
			) AS subordinates
		FROM
			employees e
		INNER JOIN reporting_line rl ON e.manager_id = rl.employee_id
) SELECT
	employee_id,
	subordinates
FROM
	reporting_line
ORDER BY
	employee_id;
/*
 employee_id |                         subordinates
-------------+--------------------------------------------------------------
           1 | Michael North
           2 | Michael North > Megan Berry
           3 | Michael North > Sarah Berry
           4 | Michael North > Zoe Black
           5 | Michael North > Tim James
           6 | Michael North > Megan Berry > Bella Tucker
           7 | Michael North > Megan Berry > Ryan Metcalfe
           8 | Michael North > Megan Berry > Max Mills
           9 | Michael North > Megan Berry > Benjamin Glover
          10 | Michael North > Sarah Berry > Carolyn Henderson
          11 | Michael North > Sarah Berry > Nicola Kelly
          12 | Michael North > Sarah Berry > Alexandra Climo
          13 | Michael North > Sarah Berry > Dominic King
          14 | Michael North > Zoe Black > Leonard Gray
          15 | Michael North > Zoe Black > Eric Rampling
          16 | Michael North > Megan Berry > Ryan Metcalfe > Piers Paige
          17 | Michael North > Megan Berry > Ryan Metcalfe > Ryan Henderson
          18 | Michael North > Megan Berry > Max Mills > Frank Tucker
          19 | Michael North > Megan Berry > Max Mills > Nathan Ferguson
          20 | Michael North > Megan Berry > Max Mills > Kevin Rampling
(20 rows)
*/
```
