SELECT COUNT(*) AS total_rows, COUNT(DISTINCT ParticipantBarcode) AS unique_patients, COUNT(DISTINCT Symbol) AS unique_genes FROM RNASeq_Expression
