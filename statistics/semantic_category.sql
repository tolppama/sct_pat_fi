with n_conceptid as (
	select 
		substring(sct_concept_fsn from '\(([^()]*)\)$') as semantic_category,
		count(distinct sct_conceptid) as n_conceptid
	from
		sct_pat_fi_pub.sct_pat_fi_kanta_20220927_new
	group by
		substring(sct_concept_fsn from '\(([^()]*)\)$')
), n_termid as (
	select 
		substring(sct_concept_fsn from '\(([^()]*)\)$') as semantic_category,
		count(distinct sct_termid) as n_termid
	from
		sct_pat_fi_pub.sct_pat_fi_kanta_20220927_new
	group by
		substring(sct_concept_fsn from '\(([^()]*)\)$')
), fi_concepts as (
	select 
		substring(sct_concept_fsn from '\(([^()]*)\)$') as semantic_category,
		count(distinct sct_conceptid) as fi_concepts
	from
		sct_pat_fi_pub.sct_pat_fi_kanta_20220927_new
	where 
		sct_conceptid ~ '.*1000288...'
	group by
		substring(sct_concept_fsn from '\(([^()]*)\)$')
), fi_terms as (
	select 
		substring(sct_concept_fsn from '\(([^()]*)\)$') as semantic_category,
		count(distinct sct_termid) as fi_terms
	from
		sct_pat_fi_pub.sct_pat_fi_kanta_20220927_new
	where 
		sct_termid~ '.*1000288...'
	group by
		substring(sct_concept_fsn from '\(([^()]*)\)$')
)

select
	c.semantic_category, 
	coalesce(c.n_conceptid, 0) as n_conceptid, 
	coalesce(t.n_termid, 0) as n_termid, 
	coalesce(fi_c.fi_concepts, 0) as fi_concepts, 
	coalesce(fi_t.fi_terms, 0) as fi_terms
from 
	n_conceptid c LEFT JOIN n_termid t ON c.semantic_category = t.semantic_category
					LEFT JOIN fi_concepts fi_c ON t.semantic_category = fi_c.semantic_category
					LEFT JOIN fi_terms fi_t ON fi_c.semantic_category = fi_t.semantic_category
order by 
	n_termid desc, fi_terms desc, n_conceptid desc, fi_concepts desc
