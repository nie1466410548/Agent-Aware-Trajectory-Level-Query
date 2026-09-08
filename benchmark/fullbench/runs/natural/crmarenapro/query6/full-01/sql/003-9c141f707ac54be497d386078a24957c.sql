SELECT p.Id, p.Name, p.Description, p.IsActive, pe.Id AS PbeId, pe.UnitPrice AS ListPrice, pb.Name AS PricebookName, pb.IsActive AS PbActive, pb.ValidFrom, pb.ValidTo
FROM Product2 p
JOIN PricebookEntry pe ON pe.Product2Id = p.Id
JOIN Pricebook2 pb ON pb.Id = pe.Pricebook2Id
WHERE pe.Id IN ('01uWt0000027P8bIAE','01uWt0000027P8cIAE','01uWt0000027PADIA2','01uWt0000027Pi5IAE')

