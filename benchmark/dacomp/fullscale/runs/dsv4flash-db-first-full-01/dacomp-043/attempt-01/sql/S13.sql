SELECT "Outcome (Cured/Improved/Deceased)" AS outcome,
  "Complication Type (Pneumonia/Encephalitis/Skin Infection)" AS complication,
  "Associated Symptoms (Cough/Headache/Vomiting)" AS assoc_symptoms,
  "Rash Distribution (Head & Face/Trunk/Limbs)" AS rash_dist,
  "Rash Morphology (Macule/Papule/Vesicle)" AS rash_morph,
  "TCM Pattern Differentiation (Wind-Heat/Damp-Heat)" AS tcm,
  COUNT(*) AS n
FROM clinical_manifestations
GROUP BY outcome, complication, assoc_symptoms, rash_dist, rash_morph, tcm
ORDER BY outcome, n DESC;