with n_conceptid as (
	select
		left(tmdc,1) as sn2_dimension,	
		count(distinct sct_conceptid) as n_conceptid
	from 
		sct_pat_fi_pub.sct_pat_fi_kanta_20220927_new -- change name
	group by
		sn2_dimension
), n_termid as (
	select
		left(tmdc,1) as sn2_dimension,
		count(distinct sct_termid) as n_termid
	from 
		sct_pat_fi_pub.sct_pat_fi_kanta_20220927_new -- change name
	group by
		sn2_dimension
), fi_concepts as (
	select
		left(tmdc,1) as sn2_dimension,
		count(distinct sct_conceptid) as fi_concepts
	from 
		sct_pat_fi_pub.sct_pat_fi_kanta_20220927_new -- change name
	where 
		sct_conceptid ~ '.*1000288...'
	group by
		sn2_dimension
), fi_terms AS (
	select
		left(tmdc,1) as sn2_dimension,
		count(distinct sct_termid) as fi_terms
	from 
		sct_pat_fi_pub.sct_pat_fi_kanta_20220927_new -- change name
	where 
		sct_termid ~ '.*1000288...'
	group by
		sn2_dimension
)
select
	c.*, t.n_termid, fi_c.fi_concepts, fi_t.fi_terms
from 
	n_conceptid c LEFT JOIN n_termid t ON c.sn2_dimension = t.sn2_dimension
					LEFT JOIN fi_concepts fi_c ON t.sn2_dimension = fi_c.sn2_dimension
					LEFT JOIN fi_terms fi_t ON fi_c.sn2_dimension = fi_t.sn2_dimension
order by 
 	t.n_termid desc, fi_t.fi_terms desc, c.n_conceptid desc, fi_c.fi_concepts desc
 	
 