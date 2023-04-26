set
    search_path = snomedct;

with inactive_termid as (
    select
        spfk.lineid,
        spfk.in_use,
        spfk.lang,
        spfk.legacy_termid,
        spfk.sct_termid,
        spfk.sct_term
    from
        thl_sct_pat_fi spfk
        left join snap_description sd on spfk.sct_termid = sd.id
    where
        spfk.in_use = 'Y'
        and sd.active = '0'
),
reason as (
    select
        it.lineid,
        case
            when sav.valueid = '723278000' then 'Not semantically equivalent component '
            when sav.valueid = '723277005' then 'Nonconformance to editorial polity component'
            when sav.valueid = '900000000000483008' then 'Outdated'
            when sav.valueid = '900000000000485001' then 'Erroneous'
            when sav.valueid = '900000000000495008' then 'Concept non-current'
            else 'Unknown'
        end as reason_for_inactivation
    from
        inactive_termid it
        left join snap_attributevaluerefset sav on it.sct_termid = sav.referencedcomponentid
    where
        sav.active = '1'
),
replaced_by as (
    select
        it.lineid,
        'Replaced by' as association,
        saf.targetcomponentid as new_id
    from
        inactive_termid it
        left join snap_associationrefset saf on it.sct_termid = saf.referencedcomponentid
    where
        saf.refsetid = '900000000000526001'
        and saf.active = '1'
),
same_as as (
    select
        it.lineid,
        'Same as' as association,
        saf.targetcomponentid as new_id
    from
        inactive_termid it
        left join snap_associationrefset saf on it.sct_termid = saf.referencedcomponentid
    where
        saf.refsetid = '900000000000527005'
        and saf.active = '1'
),
alternative as (
    select
        it.lineid,
        'Alternative' as association,
        saf.targetcomponentid as new_id
    from
        inactive_termid it
        left join snap_associationrefset saf on it.sct_termid = saf.referencedcomponentid
    where
        saf.refsetid = '900000000000530003'
        and saf.active = '1'
),
possibly_replaced_by as (
    select
        it.lineid,
        'Possibly replaced by' as association,
        saf.targetcomponentid as new_id
    from
        inactive_termid it
        left join snap_associationrefset saf on it.sct_termid = saf.referencedcomponentid
    where
        saf.refsetid = '1186921001'
        and saf.active = '1'
),
partially_equivalent_to as (
    select
        it.lineid,
        'Partially equivalent to' as association,
        saf.targetcomponentid as new_id
    from
        inactive_termid it
        left join snap_associationrefset saf on it.sct_termid = saf.referencedcomponentid
    where
        saf.refsetid = '1186924009'
        and saf.active = '1'
),
possibly_equivalent_to as (
    select
        it.lineid,
        'Possibly equivalent to' as association,
        saf.targetcomponentid as new_id
    from
        inactive_termid it
        left join snap_associationrefset saf on it.sct_termid = saf.referencedcomponentid
    where
        saf.refsetid = '900000000000523009'
        and saf.active = '1'
),
refers_to as (
    select
        it.lineid,
        'Refers to' as association,
        saf.targetcomponentid as new_id
    from
        inactive_termid it
        left join snap_associationrefset saf on it.sct_termid = saf.referencedcomponentid
    where
        saf.refsetid = '900000000000531004'
        and saf.active = '1'
),
all_replacements as (
    (
        select
            *
        from
            replaced_by
    )
    union
    (
        select
            *
        from
            same_as
    )
    union
    (
        select
            *
        from
            alternative
    )
    union
    (
        select
            *
        from
            possibly_replaced_by
    )
    union
    (
        select
            *
        from
            possibly_equivalent_to
    )
    union
    (
        select
            *
        from
            partially_equivalent_to
    )
    union
    (
        select
            *
        from
            refers_to
    )
)
select
    it.*,
    rzn.reason_for_inactivation,
    arep.association as association_type,
    arep.new_id as "new_conceptid",
    sf.term as "new_fsn",
    sc.active,
    sc.effectivetime
from
    inactive_termid it
    left join reason rzn on it.lineid = rzn.lineid
    left join all_replacements arep on rzn.lineid = arep.lineid
    left join snap_concept sc on arep.new_id = sc.id
    left join snap_fsn sf on sc.id = sf.conceptid
    
    
    
    