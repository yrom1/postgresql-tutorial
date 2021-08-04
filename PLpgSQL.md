# PostgreSQL PL/pgSQL

## Section 1. Getting started

### Dollar-quoted string constants – learn how to use dollar-quoted string constant syntax.

```sql
select 'String constant';
select 'I''m also a string constant'; -- escape with '
```

```
select E'I\'m also a string constant'; -- old style
```

```sql
select $$\$$; -- \
select $abc$\$abc$; -- \
```

```
create function find_film_by_id(
   id int
) returns film
language sql
as
  'select * from film
   where film_id = id'; -- notice the weird quotes
```

```sql
create function find_film_by_id(id int) returns film
language sql
as
$$
  select * from film
  where film_id = id;
$$;
```

```sql
-- procedures can use transactions
-- and dont return values
create procedure proc_name(param_list)
language lang_name
as $$
  -- stored procedure body
$$
create or replace procedure transfer(
   sender int,
   receiver int,
   amount dec
)
language plpgsql
as $$
begin
    -- subtracting the amount from the sender's account
    update accounts
    set balance = balance - amount
    where id = sender;

    -- adding the amount to the receiver's account
    update accounts
    set balance = balance + amount
    where id = receiver;

    commit;
end;$$
```

### Block Structure – introduce you to the PL/pgSQL block structure and show you how to develop and execute anonymous blocks.

```sql
-- PL/pgSQL allows you to place a block inside the body of another block.
-- The block nested inside another block is called a subblock. The block
-- that contains the subblock is referred to as an outer block.
do $$
<<first_block>>
declare
  film_count integer := 0;
begin
   -- get the number of films
   select count(*)
   into film_count
   from film;
   -- display a message
   raise notice 'The number of films is %', film_count;
end first_block $$;
```

## Section 2. Variables & constants

### Variables – show you how to declare variables in PL/pgSQL.

```sql
do $$
declare
   counter    integer := 1;
   first_name varchar(50) := 'John';
   last_name  varchar(50) := 'Doe';
   payment    numeric(11,2) := 20.5;
begin
   raise notice '% % % has been paid % USD',
       counter,
	   first_name,
	   last_name,
	   payment;
end $$;

do $$
declare
   film_title film.title%type;
   featured_title film_title%type;
begin
   -- get title of the film id 100
   select title
   from film
   into film_title
   where film_id = 100;

   -- show the film title
   raise notice 'Film title id 100: %s', film_title;
end; $$

do $$
<<outer_block>>
declare
  counter integer := 0;
begin
   counter := counter + 1;
   raise notice 'The current value of the counter is %', counter;

   declare
       counter integer := 0;
   begin
       counter := counter + 10;
       raise notice 'Counter in the subblock is %', counter;
       raise notice 'Counter in the outer block is %', outer_block.counter;
   end;

   raise notice 'Counter in the outer block is %', counter;

end outer_block $$;
/*
NOTICE:  The current value of the counter is 1
NOTICE:  Counter in the subblock is 10
NOTICE:  Counter in the outer block is 1
NOTICE:  Counter in the outer block is 1
*/
```

### Select into – guide you on how to use the select into to select data and assign it to a variable.

```sql
do $$
declare
   actor_count integer;
begin
   -- select the number of actors from the actor table
   select count(*)
   into actor_count
   from actor;

   -- show the number of actors
   raise notice 'The number of actors: %', actor_count;
end; $$
```

### Row type variables – learn how to use the row variables to store a complete row of a result set.

```sql
do $$
declare
   selected_actor actor%rowtype;
begin
   -- select actor with id 10
   select *
   from actor
   into selected_actor
   where actor_id = 10;

   -- show the number of actor
   raise notice 'The actor name is % %',
      selected_actor.first_name,
      selected_actor.last_name;
end; $$
```

### Record type variables – show you how to declare record variables to hold a single row of a result set.

```sql
do
$$
declare
	rec record; -- similar to rowtype
begin
	-- select the film
	select film_id, title, length
	into rec
	from film
	where film_id = 200;

	raise notice '% % %', rec.film_id, rec.title, rec.length;

end;
$$
language plpgsql;

do
$$
declare
	rec record; -- rec can hold a single row of a result set
begin
	for rec in select title, length
			from film
			where length > 50
			order by length
	loop
		raise notice '% (%)', rec.title, rec.length;
	end loop;
end;
$$
```

### Constants – guide you on how to use constants to make the code more readable and easier to maintain.

```sql
do $$
declare
   vat constant numeric := 0.1; -- cant re-assign
   net_price    numeric := 20.5;
begin
   raise notice 'The selling price is %', net_price * (1 + vat);
end $$;
```

## Section 3. Reporting messages and errors

### Raising errors and reporting messages – show you how to report messages and raise errors in PL/pgSQL.

```sql
do $$
begin
  raise info 'information message %', now() ;
  raise log 'log message %', now();
  raise debug 'debug message %', now();
  raise warning 'warning message %', now();
  raise notice 'notice message %', now();
end $$;
-- Notice that not all messages are reported back to the client. PostgreSQL
-- only reports the info, warning, and notice level messages back to the
-- client. This is controlled by client_min_messages and log_min_messages
-- configuration parameters.
do $$
declare
  email varchar(255) := 'info@postgresqltutorial.com';
begin
  -- check email for duplicate
  -- ...
  -- report duplicate email
  raise exception 'duplicate email: %', email
		using hint = 'check the email again';
end $$;
```

### Assert – show you how to use the assert statement to add debugging checks to PL/pgSQL code.

```sql
do $$
declare
   film_count integer;
begin
   select count(*)
   into film_count
   from film;

   assert film_count > 1000, '1000 Film found, check the film table';
end$$;
/*
ERROR:  1000 Film found, check the film table
CONTEXT:  PL/pgSQL function inline_code_block line 9 at ASSERT
SQL state: P0004
*/
```

## Section 4. Control structures

### If statement – introduce you to three forms of the if statement.

```sql
do $$
declare
   v_film film%rowtype;
   len_description varchar(100);
begin

  select * from film
  into v_film
  where film_id = 100;
-- found is a global variable that is available in PL/pgSQL procedure
-- language. If the select into statement sets the found variable if a row is
-- assigned or false if no row is returned.
  if not found then
     raise notice 'Film not found';
  else
      if v_film.length >0 and v_film.length <= 50 then
      len_description := 'Short';
      elsif v_film.length > 50 and v_film.length < 120 then
      len_description := 'Medium';
      elsif v_film.length > 120 then
      len_description := 'Long';
      else
      len_description := 'N/A';
      end if;

	  raise notice 'The % film is %.',
	     v_film.title,
	     len_description;
  end if;
end $$;
```

### Case statements – explain case statements including the simple and searched case statements.

```sql
do $$
declare
	rate   film.rental_rate%type;
	price_segment varchar(50);
begin
    -- get the rental rate
    select rental_rate into rate
    from film
    where film_id = 100;

	-- assign the price segment
	if found then
		case rate
		   when 0.99 then
              price_segment =  'Mass';
		   when 2.99 then
              price_segment = 'Mainstream';
		   when 4.99 then
              price_segment = 'High End';
		   else
	    	  price_segment = 'Unspecified';
		   end case;
		raise notice '%', price_segment;
    end if;
end; $$
```

### Loop statements – show you how to use loop statements to execute a block of code repeatedly based on a condition.

```sql
<<label>>
loop
   statements;
   if condition then
      exit;
   end if;
end loop;

<<outer>>
loop
   statements;
   <<inner>>
   loop
     /* ... */
     exit <<inner>>
   end loop;
end loop;

do $$
declare
   n integer:= 10;
   fib integer := 0;
   counter integer := 0 ;
   i integer := 0 ;
   j integer := 1 ;
begin
	if (n < 1) then
		fib := 0 ;
	end if;
	loop
		exit when counter = n ;
		counter := counter + 1 ;
		select j, i + j into i,	j ; -- just like python
		raise notice '%', j ;
	end loop;
	fib := i;
    raise notice '%', fib;
end; $$;
/*
NOTICE:  0
NOTICE:  1
NOTICE:  1
NOTICE:  2
NOTICE:  3
NOTICE:  5
NOTICE:  8
NOTICE:  13
NOTICE:  21
NOTICE:  34
NOTICE:  55
NOTICE:  55
DO
*/
```

### While loop – learn how to use the while loop statement to create a pre-test loop.

```sql
do $$
declare
   counter integer := 0;
begin
   while counter < 5 loop
      raise notice 'Counter %', counter;
	  counter := counter + 1;
   end loop;
end $$;

/*
NOTICE:  Counter 0
NOTICE:  Counter 1
NOTICE:  Counter 2
NOTICE:  Counter 3
NOTICE:  Counter 4
*/
```

### For loop – show you how to use the for loop statement to iterate over rows of a result set.

```sql
do $$
begin
   for counter in reverse 5..1 loop -- 5, 4, 3, 2, 1
      raise notice 'counter: %', counter;
   end loop;
end; $$;
do $$
begin
  for counter in 1..6 by 2 loop -- 1, 3, 5
    raise notice 'counter: %', counter;
  end loop;
end; $$;

do $$
declare
  -- sort by 1: title, 2: release year
  sort_type smallint := 1;
	-- return the number of films
	rec_count int := 10;
	-- use to iterate over the film
	rec record;
	-- dynamic query
  query text;
begin

	query := 'select title, release_year from film ';

	if sort_type = 1 then
		query := query || 'order by title';
	elsif sort_type = 2 then
	  query := query || 'order by release_year';
	else
	   raise 'invalid sort type %s', sort_type;
	end if;

	query := query || ' limit $1'; -- variable query
                                 -- takes input with using

	for rec in execute query using rec_count
        loop
	     raise notice '% - %', rec.release_year, rec.title;
	end loop;
end;
$$;
```

### Exit – guide you on how to use the exit statement to terminate a loop.

```
if counter > 10 then
   exit;
end if;
-- is the same as:
exit when counter > 10;
```

```sql
do
$$
begin

  <<simple_block>>
   begin
  	 exit simple_block;
         -- for demo purposes
	 raise notice '%', 'unreachable!';
   end;
   raise notice '%', 'End of block';
end; $$;

do $$
declare
   i int = 0; -- note you can use `=` for assignment instead of `:=`
   j int = 0; -- but everyone will get confused and hate you.
              -- to be more clear, remember that `=` is usually comparison...
begin
  <<outer_loop>>
  loop
     i = i + 1;
     exit when i > 3;
	 -- inner loop
	 j = 0;
     <<inner_loop>>
     loop
		j = j + 1;
		exit when j > 3;
		raise notice '(i,j): (%,%)', i, j;
	 end loop inner_loop;
  end loop outer_loop;
end; $$;
/*
NOTICE:  (i,j): (1,1)
NOTICE:  (i,j): (1,2)
NOTICE:  (i,j): (1,3)
NOTICE:  (i,j): (2,1)
NOTICE:  (i,j): (2,2)
NOTICE:  (i,j): (2,3)
NOTICE:  (i,j): (3,1)
NOTICE:  (i,j): (3,2)
NOTICE:  (i,j): (3,3)
*/
```

### Continue – provide you with a way to use the continue statement to skip the current loop iteration and start a new one.

```sql
do
$$
declare
   counter int = 0;
begin

  loop
     counter = counter + 1;
	 -- exit the loop if counter > 10
	 exit when counter > 10;
	 -- skip the current iteration if counter is an even number
	 continue when mod(counter, 2) = 0;
	 -- print out the counter
	 raise notice '%', counter;
  end loop;
end; $$;
/*
NOTICE:  1
NOTICE:  3
NOTICE:  5
NOTICE:  7
NOTICE:  9
*/
```

## Section 5. User-defined functions

### Create Function – show you how to develop a user-defined function by using the create function statement.

```sql
create function get_film_count(len_from int, len_to int)
returns int -- a type, *not* a variable name
language plpgsql
as
$$
declare
   film_count integer;
begin
   select count(*)
   into film_count
   from film
   where length between len_from and len_to;

   return film_count;
end; $$;
SELECT get_film_count(40, 90);
select get_film_count(len_from => 40, len_to => 90);
select get_film_count(40, len_to => 90);
-- select get_film_count(len_from => 40, 90); -- ERROR (just like python)
```

### Function parameter modes – introduce you to various parameter modes including IN, OUT, and INOUT.

```sql
-- Use the in mode if you want to pass a value to the function. [DEFAULT]
-- Use the out mode if you want to return a value from a function.
-- Use the inout mode when you want to pass in an initial value, update
-- the value in the function, and return it updated value back.

create or replace function find_film_by_id(p_film_id int)
returns varchar
language plpgsql
as $$
declare
   film_title film.title%type;
begin
  -- find film title by id
  select title
  into film_title
  from film
  where film_id = p_film_id;

  if not found then
     raise 'Film with id % not found', p_film_id;
  end if;

  return title;

end; $$;

create or replace function get_film_stat(
    out min_len int,
    out max_len int,
    out avg_len numeric)
language plpgsql
as $$
begin

  select min(length),
         max(length),
		 avg(length)::numeric(5,1)
  into min_len, max_len, avg_len
  from film;

end; $$;

create or replace function swap(
	inout x int,
	inout y int
)
language plpgsql
as $$
begin
   select x,y into y,x;
end; $$;
```

### Function overloading – introduce you to the function overloading.

```sql
-- PostgreSQL allows multiple functions to share the same name as
-- long as they have different arguments.
```

### Functions that return a table – show you how to develop a function that returns a table.

```sql
create or replace function get_film (p_pattern varchar)
returns table (
  film_title varchar,
  film_release_year int
)
language plpgsql
as $$
begin
	return query
		select
			title,
			release_year::integer
		from
			film
		where
			title ilike p_pattern;
end; $$;
SELECT * FROM get_film ('Al%');

create or replace function get_film (
	p_pattern varchar,
	p_year int
)
returns table (
	film_title varchar,
	film_release_year int
)
language plpgsql
as $$
declare
    var_r record;
begin
	for var_r in(
            select title, release_year
            from film
	     where title ilike p_pattern and
		    release_year = p_year
        ) loop  film_title := upper(var_r.title) ;
		film_release_year := var_r.release_year;
           return next;
	end loop;
end; $$;
```

### Drop function – learn how to remove an existing #.

```sql
drop function get_film_actors; -- if func not overloaded
drop function get_film_actors(); -- zero para func
drop function get_film_actors(int); -- int para func
```

## Section 6. Exception handling

### Handling exception – show you how to use the exception clause to catch and handle exceptions.

```sql
do
$$
declare
	rec record;
	v_film_id int = 2000;
begin
	-- select a film
	select film_id, title
	into strict rec
	from film
	where film_id = v_film_id;
        -- catch exception
	exception
	   when no_data_found then
	      raise exception 'film % not found', v_film_id;
end; $$
language plpgsql;

do
$$
declare
	rec record;
begin
	-- select film
	select film_id, title
	into strict rec
	from film
	where title LIKE 'A%';

	exception
	   when too_many_rows then
	      raise exception 'Search query returns too many rows';
end; $$
language plpgsql;
```

## Section 7. Stored procedures

### Create procedure – show you how to create and call a stored procedure.

```sql
create or replace procedure transfer(
   sender int,
   receiver int,
   amount dec
)
language plpgsql
as $$
begin
    -- subtracting the amount from the sender's account
    update accounts
    set balance = balance - amount
    where id = sender;

    -- adding the amount to the receiver's account
    update accounts
    set balance = balance + amount
    where id = receiver;

    commit; -- NOTICE ME!!! you can also ROLLBACK
end; $$;
call transfer(1, 2, 1000);
```

### Drop procedure – learn how to drop a stored procedure.

```sql
drop procedure delete_actor, update_actor;
drop procedure insert_actor(varchar);
```

## Section 8. Cursors

### Cursors – show you how to use cursors to process a result set, row by row.

```sql
-- A PL/pgSQL cursor allows you to encapsulate a query and process
-- each individual row at a time.

-- Typically, you use cursors when you want to divide a large result set
-- into parts and process each part individually. If you process it at
-- once, you may have a memory overflow error.
create or replace function get_film_titles(p_year integer)
   returns text as $$
declare
	 titles text default '';
	 rec_film   record;
	 cur_films cursor(p_year integer)
		 for select title, release_year
		 from film
		 where release_year = p_year;
begin
   -- open the cursor
   open cur_films(p_year);

   loop
    -- fetch row into the film
      fetch cur_films into rec_film;
    -- exit when no more row to fetch
      exit when not found;

    -- build the output
      if rec_film.title like '%ful%' then
         titles := titles || ',' || rec_film.title || ':' || rec_film.release_year;
      end if;
   end loop;

   -- close the cursor
   close cur_films;

   return titles;
end; $$
language plpgsql;
```
