-- Singular Test: Prüft, ob die durchschnittliche Wortlänge in einem plausiblen Bereich liegt.
-- Für deutsche Texte liegt die durchschnittliche Wortlänge typischerweise zwischen 3 und 15 Zeichen.
-- Werte außerhalb dieses Bereichs deuten auf fehlerhafte Extraktion hin.

SELECT
    id,
    file_name,
    avg_word_length
FROM {{ ref('doc_metrics') }}
WHERE avg_word_length < 1.0 OR avg_word_length > 50.0
