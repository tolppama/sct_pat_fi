SET SCHEMA 'snomedct';

DO $$
DECLARE
  folder TEXT := '/RF2Release'; -- Change the root directory based on your file location
  nursingactivity TEXT := '/SnomedCT_NursingActivities_PRODUCTION_20211031T120000Z';
  nursinghealthissues TEXT := '/SnomedCT_NursingHealthIssues_PRODUCTION_20211031T120000Z';
  type TEXT := 'Full'; -- Change between Full, Delta, Snapshot.
  release TEXT := 'INT_20210731'; -- Change between each release
  -- suffix TEXT := '_f'; -- Suffix of the database table. _f stands for full, _d stands for delta, _s stands for snapshot
BEGIN
  suffix := CASE type WHEN 'Full' THEN '_f' WHEN 'Delta' THEN '_d' WHEN 'Snapshot' THEN '_s' ELSE '' END;

  EXECUTE 'TRUNCATE TABLE nursingactivityrefset' || suffix;
  EXECUTE 'COPY nursingactivityrefset' || suffix || '(id, effectivetime, active, moduleid, refsetid, referencedcomponentid) FROM '''
        || folder || nursingactivity || '/' || type || '/Refset/Content/der2_Refset_NursingActivitiesSimple' || type || '_' || release || '.txt'' WITH (FORMAT csv, HEADER true, DELIMITER ''	'')';

  EXECUTE 'TRUNCATE TABLE nursinghealthissuesrefset' || suffix;
  EXECUTE 'COPY nursinghealthissuesrefset' || suffix || '(id, effectivetime, active, moduleid, refsetid, referencedcomponentid) FROM '''
        || folder || nursinghealthissues ||'/' || type || '/Refset/Content/der2_Refset_NursingHealthIssuesSimple' || type || '_' || release || '.txt'' WITH (FORMAT csv, HEADER true, DELIMITER ''	'')';
END $$
