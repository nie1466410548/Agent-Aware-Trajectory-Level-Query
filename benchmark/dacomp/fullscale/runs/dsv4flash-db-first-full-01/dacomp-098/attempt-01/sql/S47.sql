
SELECT contact_id, all_contact_tags,
  CASE WHEN instr(all_contact_tags,'source:')>0 THEN
    substr(all_contact_tags, instr(all_contact_tags,'source:')+7,
      CASE WHEN instr(substr(all_contact_tags,instr(all_contact_tags,'source:')+7),'|')>0
        THEN instr(substr(all_contact_tags,instr(all_contact_tags,'source:')+7),'|')-1
        ELSE length(substr(all_contact_tags,instr(all_contact_tags,'source:')+7)) END)
  END AS lead_source
FROM intercom__contact_enhanced
