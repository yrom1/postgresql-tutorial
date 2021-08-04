# PostgreSQL Triggers

## Introduction to PostgreSQL trigger – give you a brief overview of PostgreSQL triggers, why you should use triggers, and when to use them.

```sql
-- A PostgreSQL trigger is a function invoked automatically whenever an event
-- associated with a table occurs. An event could be any of the following:
-- INSERT, UPDATE, DELETE or TRUNCATE.
```

## Create trigger – show you step by step how to create your first trigger in PostgreSQL.

```sql
CREATE OR REPLACE FUNCTION log_last_name_changes()
  RETURNS TRIGGER
  LANGUAGE PLPGSQL
  AS
$$
BEGIN
-- The OLD represents the row before update while the NEW represents the
-- new row that will be updated.
	IF NEW.last_name <> OLD.last_name THEN
		 INSERT INTO employee_audits(employee_id,last_name,changed_on)
		 VALUES(OLD.id,OLD.last_name,now());
	END IF;

	RETURN NEW;
END; $$;
CREATE TRIGGER last_name_changes
  BEFORE UPDATE
  ON employees
  FOR EACH ROW
  EXECUTE PROCEDURE log_last_name_changes();

CREATE FUNCTION check_staff_user()
    RETURNS TRIGGER
AS $$
BEGIN
    IF length(NEW.username) < 8 OR NEW.username IS NULL THEN
        RAISE EXCEPTION 'The username cannot be less than 8 characters';
    END IF;
    IF NEW.NAME IS NULL THEN
        RAISE EXCEPTION 'Username cannot be NULL';
    END IF;
    RETURN NEW;
END; $$ LANGUAGE plpgsql;
CREATE TRIGGER username_check
    BEFORE INSERT OR UPDATE
ON staff
FOR EACH ROW
    EXECUTE PROCEDURE check_staff_user();
```

## Drop trigger– describe steps of how to use the DROP TRIGGER statement to delete a trigger from a table.

```sql
DROP TRIGGER trigger_name;
DROP TRIGGER username_check ON staff;
```

## Alter trigger – guide you on how to use the ALTER TRIGGER statement to rename a trigger.

```sql
ALTER TRIGGER trigger_name
ON table_name
RENAME TO new_trigger_name;
--  \dS employees -- show triggers on table

BEGIN;
DROP TRIGGER IF EXISTS salary_before_update;
CREATE TRIGGER salary_before_udpate
  BEFORE UPDATE
  ON employees
  FOR EACH ROW
  EXECUTE PROCEDURE validate_salary();
COMMIT;
```

## Disable trigger – show how how to disable a trigger or all triggers that belong to a table.

```sql
ALTER TABLE employees
DISABLE TRIGGER log_last_name_changes;
ALTER TABLE employees
DISABLE TRIGGER ALL;
```

## Enable triggers – learn how to enable a trigger or all triggers associated with a table.

```sql
ALTER TABLE employees
ENABLE TRIGGER salary_before_update;
ALTER TABLE employees
ENABLE TRIGGER ALL;
```
