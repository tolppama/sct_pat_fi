set
    search_path = snomedct;

with nursing_refset as (
    SELECT
        *
    FROM
        snap_nursingactivityrefset
    WHERE
        active = '1'
    UNION
    SELECT
        *
    from
        snap_nursinghealthissuesrefset
    WHERE
        active = '1'
), descriptions as (
    Select
        conceptid,
        'FSN' as description_type,
        id as term_id,
        term
    from
        snap_fsn
    WHERE
        active = '1'
    UNION
    Select
        conceptid,
        'Pref' as description_type,
        id as term_id,
        term
    from
        snap_pref
    WHERE
        active = '1'
    UNION
    Select
        conceptid,
        'Syn' as description_type,
        id as term_id,
        term
    from
        snap_syn
    where
        active = '1'
)

select
    d.*
from
    nursing_refset nf
    left join snap_concept c on nf.referencedcomponentid = c.id
    left join descriptions d on c.id = d.conceptid
where
    c.active = '1'
order by 
	d.conceptid, d.description_type