INSERT INTO al_ongoing_anime_schema (al_ongoing_id, anime_schema_id)
SELECT
    ao.id,
    t.id
FROM anime_schema t
JOIN al_ongoing ao
    ON ao.original_name = t.title_orig
LEFT JOIN al_ongoing_anime_schema aias
    ON aias.al_ongoing_id = ao.id
   AND aias.anime_schema_id = t.id
WHERE aias.id IS NULL;

-- docker exec -i postgres-prod psql -U postgres -d anime_db < /var/www/html/Back/database/insert_al_ongoing.sql