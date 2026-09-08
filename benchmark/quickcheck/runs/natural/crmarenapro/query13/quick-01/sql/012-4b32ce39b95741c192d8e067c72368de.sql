SELECT DISTINCT REPLACE(AccountId,'#','') AS acct FROM Contract WHERE CompanySignedDate >= '2022-06-25' AND CompanySignedDate <= '2022-11-25'
