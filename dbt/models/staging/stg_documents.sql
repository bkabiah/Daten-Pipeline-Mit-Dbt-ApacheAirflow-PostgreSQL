{{ config(materialized='view', schema='staging') }}

SELECT 
    id,
    file_name,
    LOWER(file_name) as file_name_lower,
    page_count,
    word_count,
    extracted_text,
    created_at
FROM raw.documents
