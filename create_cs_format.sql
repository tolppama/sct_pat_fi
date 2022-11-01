
-- TODO
select
    lineid as CodeID,
    term as LongName,
    legacy_termid as 'Legacy_TermID',
    sct_termid as SNOMEDCT,
    lang as 'A:lang',
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
    substring(
        concept_fsn
        from
            '\(([^()]*)\)$'
    ) as 'A:Concept_Category',
    legacy_conceptid as 'A:Legacy_ConceptID',
    conceptid as 'A:SCT_ConceptID',
    concept_fsn as 'A:SCT_Concept_FSN',
    icdo3 as 'A:ICD-O-3',
    active as 'A:Active',
    "BegginningDate",
    "ExpiringDate",
    left(term, 50) as 'ShortName',
    left(term, 50) as 'Abbreviation',
from 
    sct_pat_fi_kanta_20220927
where 
    active = 'Y'

