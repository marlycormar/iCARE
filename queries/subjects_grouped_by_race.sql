-- subjects_grouped_by_race.sql

SELECT dr.display AS race,
       count(*) AS qty
FROM icare.demographics AS d
LEFT JOIN icare.dropdown_demo_race AS dr ON (d.demo_race = dr.val)
GROUP BY race
ORDER BY qty desc;

