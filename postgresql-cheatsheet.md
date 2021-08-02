# Basic PostgreSQL Tutorial

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
-- When you sort rows that contains NULL, you can specify the order of NULL with other non-null values by using the NULLS FIRST or NULLS LAST option of the ORDER BY clause:
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
```
