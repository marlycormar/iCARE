-- subjects_by_race_ethnicity_and_gender.sql

SELECT d.demo_race,
       dr.display AS race_2,
       d.demo_ethnicity,
       de.display AS ethnicity_2,
       d.demo_gender,
       dg.display as gender
FROM malignant.demographics AS d
LEFT JOIN malignant.dropdown_demo_race AS dr ON (d.demo_race = dr.val)
LEFT JOIN malignant.radio_demo_ethnicity AS de ON (d.demo_ethnicity = de.val)
LEFT JOIN malignant.radio_demo_gender AS dg ON (d.demo_gender = dg.val);
