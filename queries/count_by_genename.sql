-- count_by_genename.sql

SELECT genename,
       count(*) COUNT
FROM farsight
GROUP BY genename
order by count desc;

