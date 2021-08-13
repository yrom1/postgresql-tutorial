# Functions

## PostgreSQL Aggregate Functions
```
AVG() – return the average value.
COUNT() – return the number of values.
MAX() – return the maximum value.
MIN() – return the minimum value.
SUM() – return the sum of all or distinct values.
```
```sql
ryan=# SELECT * FROM func;
 val 
-----
   1
    
   5
(3 rows)

ryan=# SELECT COUNT(*) FROM func;
 count 
-------
     3
(1 row)

ryan=# SELECT COUNT(val) FROM func;
 count 
-------
     2
(1 row)
```
## PostgreSQL Window Functions

```sql
SELECT
	product_name,
	price,
	group_name,
	AVG (price) OVER (
	   PARTITION BY group_name
	)
FROM
	products
	INNER JOIN 
		product_groups USING (group_id);
-- The term window describes the set of rows on which the window
-- function operates. A window function returns values from the
-- rows in a window.
window_function(arg1, arg2,..) OVER (
   [PARTITION BY partition_expression]
   [ORDER BY sort_expression [ASC | DESC] [NULLS {FIRST | LAST }])  
   [frame_clause]
-- frame_clause can be:
{ RANGE | ROWS | GROUPS } frame_start [ frame_exclusion ]
{ RANGE | ROWS | GROUPS } BETWEEN frame_start AND frame_end [ frame_exclusion ]
-- where frame_start and frame_end can be one of
UNBOUNDED PRECEDING
offset PRECEDING
CURRENT ROW
offset FOLLOWING
UNBOUNDED FOLLOWING
-- and frame_exclusion can be one of
EXCLUDE CURRENT ROW
EXCLUDE GROUP
EXCLUDE TIES
EXCLUDE NO OTHERS
```
```
CUME_DIST	Return the relative rank of the current row.
DENSE_RANK	Rank the current row within its partition without gaps.
FIRST_VALUE	Return a value evaluated against the first row within its partition.
LAG	        Return a value evaluated at the row that is at a specified physical 
            offset row before the current row within the partition.
LAST_VALUE	Return a value evaluated against the last row within its partition.
LEAD	    Return a value evaluated at the row that is offset rows after the 
            current row within the partition.
NTILE	    Divide rows in a partition as equally as possible and assign each row 
            an integer starting from 1 to the argument value.
NTH_VALUE	Return a value evaluated against the nth row in an ordered partition.
PERCENT_RANK	Return the relative rank of the current row (rank-1) / (total 
                rows – 1)
RANK	    Rank the current row within its partition with gaps.
ROW_NUMBER	Number the current row within its partition starting from 1.
```
### CUME_DIST()
```sql
-- The CUME_DIST() a double precision value which is greater than 0 and less than or equal to 1:
-- 0 < CUME_DIST() <= 1
SELECT 
    name,
	year,
	amount,
    CUME_DIST() OVER (
		PARTITION BY year
        ORDER BY amount
    )
FROM 
    sales_stats;

      name      | year |  amount   | cume_dist 
----------------+------+-----------+-----------
 Yin Yang       | 2018 |  30000.00 |       0.2
 Jane Doe       | 2018 | 110000.00 |       0.4
 John Doe       | 2018 | 120000.00 |       0.6
 Jack Daniel    | 2018 | 150000.00 |       0.8
 Stephane Heady | 2018 | 200000.00 |         1
 Yin Yang       | 2019 |  25000.00 |       0.2
 Jane Doe       | 2019 | 130000.00 |       0.4
 John Doe       | 2019 | 150000.00 |       0.6
 Jack Daniel    | 2019 | 180000.00 |       0.8
 Stephane Heady | 2019 | 270000.00 |         1
(10 rows)
```

### RANK()
```sql
-- The RANK() function assigns a rank to every row within a partition of a result set.
-- The RANK() function adds the number of tied rows to the tied rank to calculate 
-- the rank of the next row, so the ranks may not be sequential.
-- In addition, rows with the same values will get the same rank.
ryan=# SELECT
        c,
        RANK () OVER ( 
                ORDER BY c 
        ) rank_number 
FROM
        ranks;
 c | rank_number 
---+-------------
 A |           1
 A |           1
 B |           3
 B |           3
 B |           3
 C |           6
 E |           7
```

### ROW_NUMBER()
```sql
-- The ROW_NUMBER() function is a window function that assigns a sequential 
-- integer to each row in a result set. The following illustrates the syntax of 
-- the ROW_NUMBER() function:
ryan=# SELECT
        product_id,
        product_name,
        group_id,
        ROW_NUMBER () OVER (ORDER BY product_id)
FROM
        products;
 product_id |    product_name    | group_id | row_number 
------------+--------------------+----------+------------
          1 | Microsoft Lumia    |        1 |          1
          2 | HTC One            |        1 |          2
          3 | Nexus              |        1 |          3
          4 | iPhone             |        1 |          4
          5 | HP Elite           |        2 |          5
          6 | Lenovo Thinkpad    |        2 |          6
          7 | Sony VAIO          |        2 |          7
          8 | Dell Vostro        |        2 |          8
          9 | iPad               |        3 |          9
         10 | Kindle Fire        |        3 |         10
         11 | Samsung Galaxy Tab |        3 |         11
```

## PERCENT_RANK()
```sql
-- The PERCENT_RANK() function returns a result that is greater than 0 and less 
-- than or equal to 1.
ryan=# SELECT 
    name,
        amount,
    PERCENT_RANK() OVER (
        ORDER BY amount
    )
FROM 
    sales_stats
WHERE 
    year = 2019;
      name      |  amount   | percent_rank 
----------------+-----------+--------------
 Yin Yang       |  25000.00 |            0
 Jane Doe       | 130000.00 |         0.25
 John Doe       | 150000.00 |          0.5
 Jack Daniel    | 180000.00 |         0.75
 Stephane Heady | 270000.00 |            1
```

### NTH_VALUE()

```sql
-- return all products with the second most expensive product for each product 
-- group:
ryan=# SELECT 
    product_id,
    product_name,
    price,
    group_id,
    NTH_VALUE(product_name, 2) 
    OVER(
        PARTITION BY group_id
        ORDER BY price DESC
        RANGE BETWEEN 
            UNBOUNDED PRECEDING AND 
            UNBOUNDED FOLLOWING
    )
FROM 
    products;
 product_id |    product_name    |  price  | group_id |     nth_value      
------------+--------------------+---------+----------+--------------------
          4 | iPhone             |  900.00 |        1 | Nexus
          3 | Nexus              |  500.00 |        1 | Nexus
          2 | HTC One            |  400.00 |        1 | Nexus
          1 | Microsoft Lumia    |  200.00 |        1 | Nexus
          5 | HP Elite           | 1200.00 |        2 | Dell Vostro
          8 | Dell Vostro        |  800.00 |        2 | Dell Vostro
          6 | Lenovo Thinkpad    |  700.00 |        2 | Dell Vostro
          7 | Sony VAIO          |  700.00 |        2 | Dell Vostro
          9 | iPad               |  700.00 |        3 | Samsung Galaxy Tab
         11 | Samsung Galaxy Tab |  200.00 |        3 | Samsung Galaxy Tab
         10 | Kindle Fire        |  150.00 |        3 | Samsung Galaxy Tab
```

### NTILE()
```sql
-- The PostgreSQL NTILE() function allows you to divide ordered rows in the 
-- partition into a specified number of ranked groups as equal size as possible. 
-- These ranked groups are called buckets.
ryan=# SELECT 
        name,
        amount,
        NTILE(3) OVER(
                PARTITION BY year
                ORDER BY amount
        )
FROM
        sales_stats;
      name      |  amount   | ntile 
----------------+-----------+-------
 Yin Yang       |  30000.00 |     1
 Jane Doe       | 110000.00 |     1
 John Doe       | 120000.00 |     2
 Jack Daniel    | 150000.00 |     2
 Stephane Heady | 200000.00 |     3
 Yin Yang       |  25000.00 |     1
 Jane Doe       | 130000.00 |     1
 John Doe       | 150000.00 |     2
 Jack Daniel    | 180000.00 |     2
 Stephane Heady | 270000.00 |     3
```

### LEAD()

```sql
ryan=# SELECT
        year, 
        amount,
        group_id,
        LEAD(amount,1) OVER (
                PARTITION BY group_id
                ORDER BY year
        ) next_year_sales
FROM
        sales;
 year | amount  | group_id | next_year_sales 
------+---------+----------+-----------------
 2018 | 1474.00 |        1 |         1915.00
 2019 | 1915.00 |        1 |         1646.00
 2020 | 1646.00 |        1 |                
 2018 | 1787.00 |        2 |         1911.00
 2019 | 1911.00 |        2 |         1975.00
 2020 | 1975.00 |        2 |                
 2018 | 1760.00 |        3 |         1118.00
 2019 | 1118.00 |        3 |         1516.00
 2020 | 1516.00 |        3 |                
(9 rows)
```

### LAG()

```sql
ryan=# SELECT
        year, 
        amount,
        group_id,
        LAG(amount,1) OVER (
                PARTITION BY group_id
                ORDER BY year
        ) previous_year_sales
FROM
        sales;
 year | amount  | group_id | previous_year_sales 
------+---------+----------+---------------------
 2018 | 1474.00 |        1 |                    
 2019 | 1915.00 |        1 |             1474.00
 2020 | 1646.00 |        1 |             1915.00
 2018 | 1787.00 |        2 |                    
 2019 | 1911.00 |        2 |             1787.00
 2020 | 1975.00 |        2 |             1911.00
 2018 | 1760.00 |        3 |                    
 2019 | 1118.00 |        3 |             1760.00
 2020 | 1516.00 |        3 |             1118.00
(9 rows)
```

### LAST_VALUE()

```sql
ryan=# SELECT 
    product_id,
    product_name,
    group_id,
    price,
    LAST_VALUE(product_name) 
    OVER(
        PARTITION BY group_id
        ORDER BY price
        RANGE BETWEEN -- this is necessary
            UNBOUNDED PRECEDING AND 
            UNBOUNDED FOLLOWING
    ) highest_price
FROM 
    products;
 product_id |    product_name    | group_id |  price  | highest_price 
------------+--------------------+----------+---------+---------------
          1 | Microsoft Lumia    |        1 |  200.00 | iPhone
          2 | HTC One            |        1 |  400.00 | iPhone
          3 | Nexus              |        1 |  500.00 | iPhone
          4 | iPhone             |        1 |  900.00 | iPhone
          6 | Lenovo Thinkpad    |        2 |  700.00 | HP Elite
          7 | Sony VAIO          |        2 |  700.00 | HP Elite
          8 | Dell Vostro        |        2 |  800.00 | HP Elite
          5 | HP Elite           |        2 | 1200.00 | HP Elite
         10 | Kindle Fire        |        3 |  150.00 | iPad
         11 | Samsung Galaxy Tab |        3 |  200.00 | iPad
          9 | iPad               |        3 |  700.00 | iPad
(11 rows)
```

### FIRST_VALUE()
```sql
ryan=# SELECT 
    product_id,
    product_name,
        group_id,
    price,
    FIRST_VALUE(product_name) 
    OVER(
        PARTITION BY group_id
        ORDER BY price
        RANGE BETWEEN 
            UNBOUNDED PRECEDING AND 
            UNBOUNDED FOLLOWING
    ) lowest_price
FROM 
    products;
 product_id |    product_name    | group_id |  price  |  lowest_price   
------------+--------------------+----------+---------+-----------------
          1 | Microsoft Lumia    |        1 |  200.00 | Microsoft Lumia
          2 | HTC One            |        1 |  400.00 | Microsoft Lumia
          3 | Nexus              |        1 |  500.00 | Microsoft Lumia
          4 | iPhone             |        1 |  900.00 | Microsoft Lumia
          6 | Lenovo Thinkpad    |        2 |  700.00 | Lenovo Thinkpad
          7 | Sony VAIO          |        2 |  700.00 | Lenovo Thinkpad
          8 | Dell Vostro        |        2 |  800.00 | Lenovo Thinkpad
          5 | HP Elite           |        2 | 1200.00 | Lenovo Thinkpad
         10 | Kindle Fire        |        3 |  150.00 | Kindle Fire
         11 | Samsung Galaxy Tab |        3 |  200.00 | Kindle Fire
          9 | iPad               |        3 |  700.00 | Kindle Fire
(11 rows)
```

### DENSE_RANK()
```sql
ryan=# SELECT
        product_id,
        product_name,
        price,
        DENSE_RANK () OVER ( 
                ORDER BY price DESC
        ) price_rank 
FROM
        products;
 product_id |    product_name    |  price  | price_rank 
------------+--------------------+---------+------------
          5 | HP Elite           | 1200.00 |          1
          4 | iPhone             |  900.00 |          2
          8 | Dell Vostro        |  800.00 |          3
          6 | Lenovo Thinkpad    |  700.00 |          4
          7 | Sony VAIO          |  700.00 |          4
          9 | iPad               |  700.00 |          4
          3 | Nexus              |  500.00 |          5
          2 | HTC One            |  400.00 |          6
         11 | Samsung Galaxy Tab |  200.00 |          7
          1 | Microsoft Lumia    |  200.00 |          7
         10 | Kindle Fire        |  150.00 |          8
(11 rows)
```

## PostgreSQL Date Functions
```
Function	        Return Type	Description
AGE	                INTERVAL	Calculate ages between two timestamps and returns a
                                “symbolic” result which uses years and months
AGE	                INTERVAL	Calculate ages between current date (at midnight) and 
                                a timestamp and returns a “symbolic” result which uses years and months
CLOCK_TIMESTAMP	    TIMESTAMPTZ	Return the current date and time which changes during
                                statement execution
CURRENT_DATE	    DATE	    Return the current date
CURRENT_TIME	    TIMESTAMPTZ	Return the current time
CURRENT_TIMESTAMP	TIMESTAMPTZ	Return the current date and time with time zone at which
                                the current transaction starts
DATE_PART	        DOUBLE PRECISION	Get a field of a timestamp or an interval
                                        e.g., year, month, day, etc.
DATE_TRUNC	        TIMESTAMP	Return a timestamp truncated to a specified precision
EXTRACT	            DOUBLE PRECISION	Same as DATE_PART() function
ISFINITE	        BOOLEAN	    Check if a date, a timestamp, or an interval is finite or not (not +/-infinity)
JUSTIFY_DAYS	    INTERVAL	Adjust interval so 30-day time periods are represented as months
JUSTIFY_HOURS	    INTERVAL	Adjust interval so 24-hour time periods are represented as days
JUSTIFY_INTERVAL	INTERVAL	Adjust interval using justify_days and justify_hours, with
                                additional sign adjustments
LOCALTIME	        TIME	    Return the time at which the current transaction start
LOCALTIMESTAMP	    TIMESTAMP	Return the date and time at which the current transaction start
NOW	                TIMESTAMPTZ	Return the date and time with time zone at which the current transaction start
STATEMENT_TIMESTAMP	TIMESTAMPTZ	Return the current date and time at which the current statement executes
TIMEOFDAY	        TEXT	    Return the current date and time, like clock_timestamp, as a text string)
TRANSACTION_TIMESTAMP	TIMESTAMPTZ	Same as NOW() function
TO_DATE	            DATE	    Convert a string to a date
TO_TIMESTAMP	    TIMESTAMPTZ	Convert a string to a timestamp
```
```
ryan=# SELECT extract(second from now()::time);
 date_part 
-----------
 29.445282
(1 row)

ryan=# SELECT extract(year from date(now()));
 date_part 
-----------
      2021
(1 row)

ryan=# SELECT extract(day from date(now()));
 date_part 
-----------
        12
(1 row)

ryan=# SELECT extract(dow from date(now()));
 date_part 
-----------
         4
(1 row)
```

## PostgreSQL String Functions

```
Function	    Description	
                Example Result

ASCII	        Return the ASCII code value of a character or Unicode code point of a UTF8 character
                ASCII(‘A’)	65
CHR     	    Convert an ASCII code to a character or a Unicode code point to a UTF8 character	
                CHR(65)	‘A’
CONCAT	        Concatenate two or more strings into one	
                CONCAT(‘A’,’B’,’C’)	‘ABC’
CONCAT_WS	    Concatenate strings with a separator	
                CONCAT_WS(‘,’,’A’,’B’,’C’)	‘A,B,C’
FORMAT	        Format arguments based on a format string	
                FORMAT(‘Hello %s’,’PostgreSQL’)	‘Hello PostgreSQL’
INITCAP	        Convert words in a string to title case	
                INITCAP(‘hI tHERE’)	Hi There
LEFT	        Return the first n character in a string	
                LEFT(‘ABC’,1)	‘A’
LENGTH	        Return the number of characters in a string	
                LENGTH(‘ABC’)	3
LOWER	        Convert a string to lowercase	
                LOWER(‘hI tHERE’)	‘hi there’
LPAD	        Pad on the left a a string with a character to a certain length	
                LPAD(‘123′, 5, ’00’)	‘00123’
LTRIM	        Remove the longest string that contains specified characters from the left of the input string	
                LTRIM(‘00123’)	‘123’
MD5	            Return MD5 hash of a string in hexadecimal	
                MD5(‘ABC’)	
POSITION	    Return the location of a substring in a string	
                POSTION(‘B’ in ‘A B C’)	3
REGEXP_MATCHES	Match a POSIX regular expression against a string and returns the matching substrings	
                REGEXP_MATCHES(‘ABC’, ‘^(A)(..)$’, ‘g’);	{A,BC}
REGEXP_REPLACE	Replace substrings that match a POSIX regular expression by a new substring	
                REGEXP_REPLACE(‘John Doe’,'(.*) (.*)’,’\2, \1′);	‘Doe, John’
REPEAT	        Repeat string the specified number of times	
                REPEAT(‘*’, 5)	‘*****’
REPLACE	        Replace all occurrences in a string of substring from with substring to	
                REPLACE(‘ABC’,’B’,’A’)	‘AAC’
REVERSE	        Return reversed string.	
                REVERSE(‘ABC’)	‘CBA’
RIGHT	        Return last n characters in the string. When n is negative, return all but first |n| characters.	
                RIGHT(‘ABC’, 2)	‘BC’
RPAD	        Pad on the right of a string with a character to a certain length	
                RPAD(‘ABC’, 6, ‘xo’)	‘ABCxox’
RTRIM	        Remove the longest string that contains specified characters from the right of the input string	
                RTRIM(‘abcxxzx’, ‘xyz’)	‘abc’
SPLIT_PART	    Split a string on a specified delimiter and return nth substring	
                SPLIT_PART(‘2017-12-31′,’-‘,2)	’12’
SUBSTRING	    Extract a substring from a string	
                SUBSTRING(‘ABC’,1,1)	A’
TRIM	        Remove the longest string that contains specified characters from the left, right or both of the input string	
                TRIM(‘ ABC  ‘)	‘ABC’
UPPER	        Convert a string to uppercase	
                UPPER(‘hI tHERE’)	‘HI THERE’
```

## PostgreSQL Math Functions

```
Function	    Description
                Example	Result

ABS	            Calculate the absolute value of a number
                ABS(-10) 10
CBRT	        Calculate the cube root of a number
                CBRT(8)	2
CEIL	        Round a number up to the nearest integer, which is greater than or equal to number
                CEIL(-12.8)	-12
CEILING	        Same as CEIL		
DEGREES     	Convert radians to degrees	
                DEGREES(0.8)	45.83662361
DIV	            Return the integer quotient of two numeric values	
                DIV(8,3)	2
EXP	            Return the exponential value in scientific notation of a number	
                EXP(1)	2.718281828
FLOOR	        Round a number down to the nearest integer, which is less than or equal to number	
                FLOOR(10.6)	10
LN	            Return the natural logarithm of a numeric value	
                LN(3)	1.098612289
LOG	            Return the base 10 logarithm of a numeric value	
                LOG(1000)	3
LOG	            Return the logarithm of a numeric value to a specified base	
                LOG(2, 64)	6
MOD	            Divide the first parameter by the second one and return the remainder	
                MOD(10,4)	1
PI	            Return the value of PI	
                PI()	3.141592654
POWER	        Raise a numeric value to the power of a second numeric value	
                POWER(5, 3)	125
RADIANS     	Convert degrees to radians	
                RADIANS(60)	1.047197551
ROUND	        Round a number to the nearest integer or to a specified decimal places	
                ROUND(10.3)	10
SCALE	        Return the number of decimal digits in the fractional part	
                SCALE(1.234)	3
SIGN	        Return the sign (positive, negative) of a numeric value	
                SIGN(-1)	-1
SQRT	        Return the square root of a numeric value	
                SQRT(3.0)	1.732050808
TRUNC       	Truncate a numeric value to a whole number of  to the specified decimal places	
                TRUNC(12.3)	12
RANDOM	        Return a random number that ranges from 0 to 1
                RANDOM()  0.668190402080068
```
