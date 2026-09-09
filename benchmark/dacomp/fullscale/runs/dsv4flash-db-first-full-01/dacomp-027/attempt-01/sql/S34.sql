
SELECT f."Disaster Reference ID", f."fundingstate", f."costbene(USD)", f."budgetallot(USD)", f."donorcommitments(USD)",
       c."Secincident Count"
FROM financials1 f
JOIN coordination_and_evaluation c ON c."Distribution Reference ID" = f."Disaster Reference ID"
