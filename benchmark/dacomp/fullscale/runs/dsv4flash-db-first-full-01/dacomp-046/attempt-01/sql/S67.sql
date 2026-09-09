
SELECT u."Age group" as age, m."Event Feedback Rating" as rating,
       m."Number of Shares" as shares, m."Event Conversion Rate" as conv,
       m."Event Dwell Time" as dwell, m."Number of Participants" as participants
FROM user_basic_information_table_1 u
JOIN marketing_campaign_interaction m ON u."User ID"=m."User ID"
