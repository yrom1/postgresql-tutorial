# PostgreSQL Indexes

## Create Index – shows you how to define a new index for a table.

```sql
CREATE INDEX idx_address_phone -- USING btree is default
ON address(phone);
```

## Drop Index – guides you on how to remove an existing index.

```sql
DROP INDEX idx_actor_first_name;
```

## List indexes – shows you how to list all indexes in the PostgreSQL database.

```sql
\d table_name
SELECT
    indexname,
    indexdef
FROM
    pg_indexes
WHERE
    tablename = 'customer';
```

## Index Types – discusses various types of indexes in PostgreSQL.

```sql
/*
B-tree indexes  default
Hashs indexes   Hash indexes can handle only simple equality comparison (=).
GIN indexes     GIN stands for generalized inverted indexes.
                GIN indexes are most useful when you have multiple values
                stored in a single column, for example, hstore, array, jsonb, and
                range types.
BRIN            stands for block range indexes. BRIN is much smaller and less
                costly to maintain in comparison with a B-tree index.
                BRIN allows the use of an index on a very large table
GiST Indexes    GiST stands for Generalized Search Tree. GiST indexes allow a
                building of general tree structures. GiST indexes are useful in
                indexing geometric data types and full-text search.
SP-GiST Indexes SP-GiST stands for space-partitioned GiST. SP-GiST indexes are
                most useful for data that has a natural clustering element to it
                and is also not an equally balanced tree, for example, GIS...
*/
```

## Unique Index – provides you with steps of defining unique indexes.

```sql
-- When you define a primary key or a unique constraint for a table,
-- PostgreSQL automatically creates a corresponding UNIQUE index.
CREATE UNIQUE INDEX idx_employees_mobile_phone
ON employees(mobile_phone);
```

## Index on Expression – shows you how to define an index based on expressions.

```sql
CREATE INDEX idx_ic_last_name
ON customer(LOWER(last_name));
EXPLAIN
SELECT
    customer_id,
    first_name,
    last_name
FROM
    customer
WHERE
    LOWER(last_name) = 'purdy'; -- this now uses index scan rather than seq scan
```

## Partial index – illustrates how to use partial indexes.

```sql
-- The partial index is useful in case you have commonly used WHERE conditions
CREATE INDEX idx_customer_inactive
ON customer(active)
WHERE active = 0;
EXPLAIN SELECT
    customer_id,
    first_name,
    last_name,
    email
FROM
    customer
WHERE
    active = 0; -- now uses index scan
```

## Reindex – shows you how to use the REINDEX statement to rebuild one or more indices.

```sql
-- In practice, an index can become corrupted and no longer contains valid data
-- due to hardware failures or software bugs.
REINDEX INDEX index_name;
REINDEX TABLE table_name;
REINDEX SCHEMA schema_name;
REINDEX DATABASE database_name;
REINDEX SYSTEM database_name;
```

## Multicolumn Indexes – shows you how to use multicolumn indexes to speed up queries with various conditions in WHERE clause.

```sql
CREATE INDEX idx_people_names
ON people (last_name, first_name);
EXPLAIN SELECT
    *
FROM
    people
WHERE
    last_name = 'Adams'; -- no index scan with idx_people_names
EXPLAIN SELECT
    *
FROM
    people
WHERE
    last_name = 'Adams'
AND first_name = 'Lou'; -- idx_people_names index scan
```
