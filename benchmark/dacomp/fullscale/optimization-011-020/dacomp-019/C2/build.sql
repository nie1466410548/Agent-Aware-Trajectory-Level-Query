-- Execute once before S7; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_019_c2" AS
SELECT "Origin / Tier (Domestic/Imported/JV)" AS __g0, "GSP Certification Status" AS __g1, "Storage conditions (room temperature/cool/refrigerated)" AS __g2, "Transportation mode (land/cold chain)" AS __g3, COUNT(*) AS __a0 FROM "basic_drug_information"  GROUP BY "Origin / Tier (Domestic/Imported/JV)", "GSP Certification Status", "Storage conditions (room temperature/cool/refrigerated)", "Transportation mode (land/cold chain)";
