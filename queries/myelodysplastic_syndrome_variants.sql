-- myelodysplastic_syndrome_variants.sql

SELECT *
FROM
  (SELECT record_id,
          record_id_8c5d12,
          com1 AS com
   FROM cyp2c19_and_voriconazole
   UNION ALL SELECT record_id,
                    record_id_8c5d12,
                    com2 AS com
   FROM cyp2c19_and_voriconazole
   UNION ALL SELECT record_id,
                    record_id_8c5d12,
                    com3 AS com
   FROM cyp2c19_and_voriconazole
   UNION ALL SELECT record_id,
                    record_id_8c5d12,
                    com4 AS com
   FROM cyp2c19_and_voriconazole
   UNION ALL SELECT record_id,
                    record_id_8c5d12,
                    com5 AS com
   FROM cyp2c19_and_voriconazole
   UNION ALL SELECT record_id,
                    record_id_8c5d12,
                    com6 AS com
   FROM cyp2c19_and_voriconazole
   UNION ALL SELECT record_id,
                    record_id_8c5d12,
                    com7 AS com
   FROM cyp2c19_and_voriconazole) AS cm
INNER JOIN farsight AS f ON (cm.record_id_8c5d12 = f.study_id)
WHERE f.genename IN ("GATA2",
                     "DDX41",
                     "ANKRD26",
                     "ETV6",
                     "SRP72",
                     "ATG2B",
                     "GSKIP")
  AND cm.com IN ("D46.9");

