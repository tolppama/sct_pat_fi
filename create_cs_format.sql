
-- TODO
select
    lineid as CodeID,
    term as LongName,
    legacy_termid as 'A:Legacy_TermID',
    sct_termid as 'A:SNOMEDCT',
    lang as 'A:Lang',
    case
        when lang = 'en' then 0
        else 1
    end as 'HierarchyLevel',
    parent_id as 'ParentID',
    case
        when left(tmdc, 1) in ('A', 'D', 'M') then 'diagnosis'
        when left(tmdc, 1) in ('C') then 'cytology'
        when left(tmdc, 1) in ('T') then 'topography'
        else 'error'
    end as 'A:GUI_category',
    legacy_conceptid as 'A:Legacy_ConceptID',
    conceptid as 'A:SCT_ConceptID',
    concept_fsn as 'A:SCT_Concept_FSN',
    icdo3 as 'A:ICD-O-3',
    active as 'A:Active',
    effectivetime as "BegginningDate",
	supersededtime as "ExpiringDate"
from 
    sct_pat_fi_kanta_20220927
where 
    in_use is null or in_use = "kesken"

