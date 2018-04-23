-- subjects_by_race_ethnicity_and_gender.sql

SELECT d.demo_race AS race_code,
       dr.display AS race,
       d.demo_ethnicity AS ethnicity_code,
       de.display AS ethnicity,
       d.demo_gender AS gender_code,
       dg.display AS gender
FROM icare.demographics AS d
LEFT JOIN icare.dropdown_demo_race AS dr ON (d.demo_race = dr.val)
LEFT JOIN icare.radio_demo_ethnicity AS de ON (d.demo_ethnicity = de.val)
LEFT JOIN icare.radio_demo_gender AS dg ON (d.demo_gender = dg.val);

