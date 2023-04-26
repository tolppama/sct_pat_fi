set
	search_path = snomedct;

with inactive_conceptid as (
	select
		spfk.lineid,
		spfk.in_use,
		spfk.lang,
		spfk.legacy_conceptid,
		spfk.sct_conceptid,
		spfk.sct_concept_fsn
	from
		thl_sct_pat_fi spfk
		left join snap_concept sc on spfk.sct_conceptid = sc.id
	where
		spfk.in_use = 'Y'
		and sc.active = '0'
),
reason as (
	select
		ic.lineid,
		case
			when sav.valueid = '900000000000482003' then 'Duplicate'
			when sav.valueid = '900000000000483008' then 'Outdated'
			when sav.valueid = '900000000000484002' then 'Ambiguous'
			when sav.valueid = '900000000000485001' then 'Erroneous'
			when sav.valueid = '900000000000486000' then 'Limited'
			when sav.valueid = '900000000000487009' then 'Moved elsewhere'
			when sav.valueid = '900000000000492006' then 'Pending move'
			when sav.valueid = '1186917008' then 'Classification derived'
			when sav.valueid = '1186919006' then 'Unknown meaning'
			when sav.valueid = '723277005' then 'Nonconformance to editorial policy'
			else 'Unknown'
		end as reason_for_inactivation
	from
		inactive_conceptid ic
		left join snap_attributevaluerefset sav on ic.sct_conceptid = sav.referencedcomponentid
	where
		sav.active = '1'
),
replaced_by as (
	select
		ic.lineid,
		'Replaced by' as association,
		saf.targetcomponentid as new_conceptid
	from
		inactive_conceptid ic
		left join snap_associationrefset saf on ic.sct_conceptid = saf.referencedcomponentid
	where
		saf.refsetid = '900000000000526001'
		and saf.active = '1'
),
same_as as (
	select
		ic.lineid,
		'Same as' as association,
		saf.targetcomponentid as new_conceptid
	from
		inactive_conceptid ic
		left join snap_associationrefset saf on ic.sct_conceptid = saf.referencedcomponentid
	where
		saf.refsetid = '900000000000527005'
		and saf.active = '1'
),
alternative as (
	select
		ic.lineid,
		'Alternative' as association,
		saf.targetcomponentid as new_conceptid
	from
		inactive_conceptid ic
		left join snap_associationrefset saf on ic.sct_conceptid = saf.referencedcomponentid
	where
		saf.refsetid = '900000000000530003'
		and saf.active = '1'
),
possibly_replaced_by as (
	select
		ic.lineid,
		'Possibly replaced by' as association,
		saf.targetcomponentid as new_conceptid
	from
		inactive_conceptid ic
		left join snap_associationrefset saf on ic.sct_conceptid = saf.referencedcomponentid
	where
		saf.refsetid = '1186921001'
		and saf.active = '1'
),
partially_equivalent_to as (
	select
		ic.lineid,
		'Partially equivalent to' as association,
		saf.targetcomponentid as new_conceptid
	from
		inactive_conceptid ic
		left join snap_associationrefset saf on ic.sct_conceptid = saf.referencedcomponentid
	where
		saf.refsetid = '1186924009'
		and saf.active = '1'
),
possibly_equivalent_to as (
	select
		ic.lineid,
		'Possibly equivalent to' as association,
		saf.targetcomponentid as new_conceptid
	from
		inactive_conceptid ic
		left join snap_associationrefset saf on ic.sct_conceptid = saf.referencedcomponentid
	where
		saf.refsetid = '900000000000523009'
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
)
select
	ic.*,
	rzn.reason_for_inactivation,
	arep.association as association_type,
	arep.new_conceptid,
	sf.term as new_fsn,
	sc.active,
	sc.effectivetime as intl_effectivetime
from
	inactive_conceptid ic
	left join reason rzn on ic.lineid = rzn.lineid
	left join all_replacements arep on rzn.lineid = arep.lineid
	left join snap_fsn sf on arep.new_conceptid = sf.conceptid
	left join snap_concept sc on sf.conceptid = sc.id