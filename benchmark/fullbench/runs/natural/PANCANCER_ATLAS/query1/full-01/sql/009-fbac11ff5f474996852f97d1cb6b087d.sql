SELECT Symbol, COUNT(*) FROM RNASeq_Expression WHERE Symbol ILIKE 'IGF2%' GROUP BY Symbol
