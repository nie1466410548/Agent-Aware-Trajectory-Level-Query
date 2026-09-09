
SELECT recipient_email AS email,
       MAX(CASE WHEN distribution_channel='email' THEN 1 ELSE 0 END) AS ch_email,
       MAX(CASE WHEN distribution_channel='sms' THEN 1 ELSE 0 END) AS ch_sms,
       MAX(CASE WHEN distribution_channel='mobile' THEN 1 ELSE 0 END) AS ch_mobile,
       MAX(CASE WHEN distribution_channel='web' THEN 1 ELSE 0 END) AS ch_web,
       MAX(CASE WHEN distribution_channel='social' THEN 1 ELSE 0 END) AS ch_social
FROM qualtrics__response
GROUP BY recipient_email
