
    SELECT conversation_id, count_reopens, time_to_last_close_minutes,
           time_to_first_close_minutes, conversation_created_at, conversation_last_updated_at
    FROM intercom__conversation_metrics
