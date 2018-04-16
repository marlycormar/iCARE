-- subjects_by_race_and_gender

SELECT d.demo_race,
       dr.display,
       d.demo_ethnicity,
       d.demo_gender
FROM malignant.demographics as d
left join malignant.dropdown_demo_race as dr on (d.demo_race = dr.val);

#outer join malignant.radio_demo_ethnicity as de on (d.demo_ethnicity = de.val)
#outer join malignant.malignant.radio_demo_gender as dg on (d.demo_gender = dg.val);
