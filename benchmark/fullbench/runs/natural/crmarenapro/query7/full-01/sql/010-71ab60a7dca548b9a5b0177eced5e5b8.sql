SELECT id, subject, textbody, fromaddress, toids, messagedate, parentid, relatedtoid FROM emailmessage WHERE parentid LIKE '%DDyzn%' OR relatedtoid LIKE '%DDyzn%' ORDER BY messagedate
