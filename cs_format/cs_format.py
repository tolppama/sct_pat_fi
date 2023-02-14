import re
import pandas as pd
from db import Database
from collections import namedtuple


def transpose_table_lineid(df):
    Row = namedtuple('Row', "CodeID LongName legacy_termid sct_termid lang HierarchyLevel ParentID gui_category concept_category legacy_conceptid sct_conceptid sct_concept_fsn icdo3 active BeginningDate ExpiringDate korvaava_koodi ShortName Abbreviation")
    t_rows = []
    for _, row in df.iterrows():
        if row["tmdc"][0] in ['A', 'D', 'M']:
            qui_category = "diagnosis"
        elif row["tmdc"][0] == "C":
            qui_category = "cytology"
        elif row["tmdc"][0] == "T":
            qui_category = "topography"
        else:
            qui_category = "unknown"

        match = re.search(
            '(?P<category>\(([^()]*)\))$', row['sct_concept_fsn'])
        if match:
            if match.group('category'):
                concept_category = match.group('category')[1:-1]

        if not row["in_use"] or row["in_use"] == "kesken":
            active = "Y"
        elif row["in_use"] == "ei":
            active = "N"
        else:
            active = "unknown"

        if len(row["sct_term"]) > 50:
            sct_term = row["sct_term"][:50]
        else:
            sct_term = row["sct_term"]

        parents = df.loc[(df["sct_termid"] == row["sct_termid_en"]) & (
            df["lang"] == "en")]
        if len(parents) == 1:
            parent_id = parents.iloc[0]["lineid"]
        elif len(parents) > 1:
            if row["in_use"] == "ei":
                sub_parents = parents.loc[parents["in_use"] == "ei"]
            else:
                sub_parents = parents.loc[parents["in_use"] != "ei"]
            if len(sub_parents) == 1:
                parent_id = sub_parents.iloc[0]["lineid"]
            else:
                parent_id = "error: multiple parents"
        else:
            parent_id = "error: no parent"

        t_row = Row(
            CodeID=row['lineid'],
            LongName=row['sct_term'],
            legacy_termid=row['legacy_termid'],
            sct_termid=row['sct_termid'],
            lang=row['lang'],
            HierarchyLevel=0 if row["lang"] == "en" else 1,
            ParentID=parent_id,
            gui_category=qui_category,
            concept_category=concept_category,
            legacy_conceptid=row['legacy_conceptid'],
            sct_conceptid=row['sct_conceptid'],
            sct_concept_fsn=row['sct_concept_fsn'],
            icdo3=row['icdo_code_ssr'],
            active=active,
            BeginningDate=row['effectivetime'],
            ExpiringDate=row["supersededtime"],
            korvaava_koodi=None,
            ShortName=sct_term,
            Abbreviation=sct_term
        )
        t_rows.append(t_row)
    final_df = pd.DataFrame(t_rows).sort_values(
        by=["legacy_conceptid", "ParentID", "lang"])
    for i, row in final_df.iterrows():
        if row["lang"] == "en":
            final_df.at[i, "ParentID"] = None
    # column headers:, CodeID, LongName, A:Legacy_TermID, SNOMEDCT, A:Lang, HierarchyLevel, ParentID, A:Gui_Category, A:Concept_Category, A:Legacy_ConceptID, A:SCT_ConceptID, A:SCT_Concept_FSN, A:Active, BeginningDate, ExpiringDate, Korvaava koodi, ShortName, Abbreviation
    final_df = final_df.rename(columns={"legacy_termid": "A:Legacy_TermID", "sct_termid": "SNOMEDCT", "lang": "A:Lang", "gui_category": "A:GUI_Category", "concept_category": "A:Concept_Category",
                               "legacy_conceptid": "A:Legacy_ConceptID", "sct_conceptid": "A:SCT_ConceptID", "sct_concept_fsn": "A:SCT_Concept_FSN", "icdo3": "A:ICD-O-3_Morfologia", "active": "A:Active", "korvaava_koodi": "Korvaava koodi"})
    return final_df


def to_excel(final_df):
    final_df.to_excel(
        "sct_pat_fi_kanta_20221101_cs_20221101.xlsx", index=False)


def main():
    db = Database()
    df = db.table_to_df("sct_pat_fi_kanta_20221101_final")
    df = df[df["in_use"] != "ei"]
    final_df = transpose_table_lineid(df)
    to_excel(final_df)


main()
