
    SELECT state_name AS state, population, gdp_billion, gdp_per_capita,
           primary_industry, secondary_industry, tertiary_industry, quaternary_industry,
           market_maturity_score, competition_intensity, business_friendly_index,
           unemployment_rate, corporate_tax_rate
    FROM state_economic_data
