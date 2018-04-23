-- comorbidities.sql

SELECT com,
       count(*) AS COUNT
FROM
  (SELECT com1 AS com
   FROM cyp2c19_and_voriconazole
   UNION ALL SELECT com2 AS com
   FROM cyp2c19_and_voriconazole
   UNION ALL SELECT com3 AS com
   FROM cyp2c19_and_voriconazole
   UNION ALL SELECT com4 AS com
   FROM cyp2c19_and_voriconazole
   UNION ALL SELECT com5 AS com
   FROM cyp2c19_and_voriconazole
   UNION ALL SELECT com6 AS com
   FROM cyp2c19_and_voriconazole
   UNION ALL SELECT com7 AS com
   FROM cyp2c19_and_voriconazole) dummy
WHERE com IS NOT NULL
  AND com != ""
GROUP BY com
ORDER BY COUNT DESC ;

