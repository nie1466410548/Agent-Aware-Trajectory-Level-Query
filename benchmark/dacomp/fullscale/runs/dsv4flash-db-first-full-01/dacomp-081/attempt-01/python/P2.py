import pandas as pd
import json

# Get all responses for a single survey_response_id to see the question structure
result = db.query("""
    SELECT survey_response_id, survey_id, question_id, question_text, 
           question_type, value, response_text, sub_question_key,
           sub_question_text, question_option_key, user_language,
           contact_language, embedded_data
    FROM qualtrics__response
    WHERE survey_response_id = 'SUR10008772252'
    ORDER BY question_id
""")
df = db.frame(result)
print("Full survey session for one respondent:")
print(df.to_string())

# Also look at the distribution of question_types per survey
result2 = db.query("""
    SELECT survey_id, question_type, COUNT(*) as cnt
    FROM qualtrics__response
    GROUP BY survey_id, question_type
    HAVING COUNT(*) >= 10
    ORDER BY cnt DESC
    LIMIT 20
""")
df2 = db.frame(result2)
print("\n\nQuestion type distribution per survey:")
print(df2.to_string())

# Let's look at how many different question_ids appear per survey_response
result3 = db.query("""
    SELECT survey_response_id, COUNT(*) as n_questions
    FROM qualtrics__response
    GROUP BY survey_response_id
    ORDER BY n_questions DESC
    LIMIT 20
""")
df3 = db.frame(result3)
print("\n\nQuestions per survey response:")
print(df3.to_string())

# Check if there's a pattern of specific question_ids relating to "revenue" or "performance"
# by looking at the question_text distribution
result4 = db.query("""
    SELECT question_text, COUNT(*) as cnt
    FROM qualtrics__response
    GROUP BY question_text
    ORDER BY cnt DESC
    LIMIT 30
""")
df4 = db.frame(result4)
print("\n\nQuestion text distribution:")
print(df4.to_string())