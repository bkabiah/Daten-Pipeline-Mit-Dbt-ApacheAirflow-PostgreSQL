-- Singular Test: Stellt sicher, dass keine Dokumente mit 0 Wörtern existieren.
-- Ein Dokument mit 0 Wörtern deutet auf eine fehlgeschlagene PDF-Extraktion hin.

SELECT
    id,
    file_name,
    word_count
FROM {{ ref('doc_metrics') }}
WHERE word_count = 0
