import pandas as pd
import numpy as np

# Load response data columns of interest
result = db.query("""
    SELECT value, sub_question_text, question_option_key, sub_question_key,
           user_language, question_type, question_id
    FROM qualtrics__response
    WHERE sub_question_text IS NOT NULL
    LIMIT 50000
""")
df = db.frame(result)
print(f"Rows: {len(df)}")
print(df.describe())

# Correlation between value and sub_question_text
print("\nCorrelation value vs sub_question_text:", df['value'].corr(df['sub_question_text']))
print("Correlation value vs question_option_key:", df['value'].corr(df['question_option_key']))
print("Correlation sub_question_text vs question_option_key:", df['sub_question_text'].corr(df['question_option_key']))

# Check distribution of sub_question_text - is it uniform or bimodal?
print("\nSub_question_text percentiles:")
print(df['sub_question_text'].quantile([0, 0.25, 0.5, 0.75, 1.0]))
print("\nQuestion_option_key percentiles:")
print(df['question_option_key'].quantile([0, 0.25, 0.5, 0.75, 1.0]))

# Check if sub_question_text is correlated with language
print("\nAvg sub_question_text by language:")
print(df.groupby('user_language')['sub_question_text'].agg(['mean','count']).to_string())

# Check if there's any question_type where value distribution is different
print("\nAvg value by question_type:")
print(df.groupby('question_type')['value'].agg(['mean','count']).to_string())