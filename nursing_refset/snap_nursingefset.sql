set
    search_path = snomedct;

drop view if exists snap_nursingactivityrefset;

CREATE VIEW snap_nursingactivityrefset as (
    select
        *
    from
        nursingactivityrefset_f tbl
    where
        tbl.effectiveTime = (
            select
                max(sub.effectiveTime)
            from
                nursingactivityrefset_f sub
            where
                sub.id = tbl.id
        )
);

drop view if exists snap_nursinghealthissuesrefset;

CREATE VIEW snap_nursinghealthissuesrefset as (
    select
        *
    from
        nursinghealthissuesrefset_f tbl
    where
        tbl.effectiveTime = (
            select
                max(sub.effectiveTime)
            from
                nursinghealthissuesrefset_f sub
            where
                sub.id = tbl.id
        )
);