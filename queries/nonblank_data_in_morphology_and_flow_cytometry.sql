-- nonblank_data_in_morphology_and_flow_cytometry.sql

SELECT *
FROM morphology_and_flow_cytometry
WHERE morph_tissue != ""
  OR morph_bm_cellularity != ""
  OR mORPH_DYSPLASTIC_CHANGES != "";

