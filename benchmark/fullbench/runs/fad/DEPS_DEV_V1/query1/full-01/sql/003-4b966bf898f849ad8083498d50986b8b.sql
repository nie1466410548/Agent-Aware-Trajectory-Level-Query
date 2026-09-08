SELECT table_name, column_name, data_type FROM information_schema.columns WHERE table_name IN ('project_info','project_packageversion') ORDER BY table_name, ordinal_position
