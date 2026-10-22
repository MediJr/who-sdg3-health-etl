-- Contrôles de recette (cahier des charges, section 10). Chaque ligne doit afficher « OK ».
SELECT 'C2 · dernière exécution sans insertion ni mise à jour (relance à l''identique)' AS controle,
       CASE WHEN rows_inserted = 0 AND rows_updated = 0 THEN 'OK' ELSE 'À VÉRIFIER' END AS resultat,
       format('run %s : %s insérées, %s mises à jour, %s inchangées', run_id, rows_inserted, rows_updated, rows_unchanged) AS detail
FROM (SELECT * FROM ops.pipeline_run WHERE status = 'success' ORDER BY run_id DESC LIMIT 1) AS derniere
UNION ALL
SELECT 'C3 · aucun doublon sur la clé métier complète',
       CASE WHEN count(*) = 0 THEN 'OK' ELSE 'ÉCHEC' END,
       count(*)::text || ' doublon(s)'
FROM (SELECT 1 FROM core.fact_observation
      GROUP BY indicator_code, location_type, location_code, year, sex, age_group, wealth_quintile
      HAVING count(*) > 1) AS doublons
UNION ALL
SELECT 'C4 · toute ligne extraite est soit chargée, soit en quarantaine',
       CASE WHEN rows_extracted = rows_inserted + rows_updated + rows_unchanged + rows_quarantined THEN 'OK' ELSE 'ÉCHEC' END,
       format('%s extraites = %s chargées + %s en quarantaine', rows_extracted,
              rows_inserted + rows_updated + rows_unchanged, rows_quarantined)
FROM (SELECT * FROM ops.pipeline_run WHERE status = 'success' ORDER BY run_id DESC LIMIT 1) AS derniere
UNION ALL
SELECT 'Volumétrie · observations en base', 'INFO', count(*)::text FROM core.fact_observation
UNION ALL
SELECT 'Volumétrie · exécutions réussies', 'INFO', count(*)::text FROM ops.pipeline_run WHERE status = 'success';
