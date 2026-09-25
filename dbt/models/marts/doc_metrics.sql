{{ config(materialized='table', schema='analytics') }}

SELECT 
    id,
    file_name,
    page_count,
    word_count,
    -- Einfache NLP-Metrik: Durchschnittliche Wortlänge
    CASE WHEN word_count > 0 THEN LENGTH(extracted_text)::FLOAT / word_count ELSE 0 END as avg_word_length,
    -- Keyword Dichte (Simuliert: Suche nach "Vertrag" oder "contract")
    CASE 
        WHEN LOWER(extracted_text) LIKE '%vertrag%' OR LOWER(extracted_text) LIKE '%contract%' THEN TRUE 
        ELSE FALSE 
    END as is_contract,
    created_at
FROM {{ ref('stg_documents') }}
