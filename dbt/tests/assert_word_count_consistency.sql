-- Singular Test: Prüft, ob word_count zwischen Staging und Analytics konsistent ist.
-- Dieser Test schlägt fehl, wenn auch nur eine Zeile unterschiedliche Werte hat.

SELECT
    m.id,
    m.file_name,
    s.word_count AS staging_word_count,
    m.word_count AS analytics_word_count
FROM {{ ref('doc_metrics') }} m
JOIN {{ ref('stg_documents') }} s ON m.id = s.id
WHERE s.word_count != m.word_count
