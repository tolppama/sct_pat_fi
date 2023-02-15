import re
from database import Database


def qui_category(row):
    if row["tmdc"][0] in ["A", "D", "M"]:
        return "diagnosis"
    elif row["tmdc"][0] == "C":
        return"cytology"
    elif row["tmdc"][0] == "T":
        return "topography"
    else:
        return "unknown"

def concept_category(row):
    match = re.search("(?P<category>\(([^()]*)\))$", row["sct_concept_fsn"])
    if match and match.group("category"):
        return match.group("category")[1:-1]

def short_term(row):
    if len(row["sct_term"]) > 50:
        return row["sct_term"][:50]
    return row["sct_term"]

def parent_id(row):
    if row["lang"] == "en":
        return None
    return row["sct_termid_en"]

def hierarchy_level(row):
    if row["lang"] == "en":
        return 0
    return 1

def cs_columns(df):
    df["hierarchy_level"] = df.apply(hierarchy_level, axis=1)
    df["sct_termid_en"] = df.apply(parent_id, axis=1)
    df["gui_category"] = df.apply(qui_category, axis=1)
    df["concept_category"] = df.apply(concept_category, axis=1)
    df["short_name"] = df.apply(short_term, axis=1)
    df["abbreviation"] = df.apply(short_term, axis=1)
    df["order_number"] = range(1, 1 + len(df))
    return df

def select_columns(df):
    # CodeID LongName legacy_termid sct_termid lang HierarchyLevel ParentID gui_category concept_category legacy_conceptid sct_conceptid sct_concept_fsn icdo3 active BeginningDate ExpiringDate korvaava_koodi ShortName Abbreviation")
    df = df[[
        "lineid",
        "abbreviation",
        "short_name",
        "sct_term",
        "sct_termid_en",
        "hierarchy_level",
        "in_use",
        "effectivetime",
        "supersededtime",
        "superceded_by",
        "inaktivoinnin_selite",
        "concept_category",
        "gui_category",
        "icdo_code_ssr",
        "order_number",
        "lang",
        "legacy_conceptid",
        "legacy_termid",
        "sct_termid",
        "sct_concept_fsn",
        "sct_conceptid"
    ]]
    return df

def sort_df(df):
    df = df.sort_values(by=["legacy_conceptid", "lang", "sct_termid_en"])
    return df

def rename_columns(df):
    df = df.rename(columns={
        "lineid": "CodeID",
        "abbreviation": "Abbreviation",
        "short_name": "ShortName",
        "sct_term": "LongName",
        "sct_termid_en": "ParentID",
        "hierarchy_level": "HierarchyLevel",
        "in_use": "A:Active",
        "effectivetime": "BeginningDate",
        "supersededtime": "ExpiringDate",
        "superceded_by": "A:KorvaavaKoodi",
        "inaktivoinnin_selite": "A:InaktivoinninSelite",
        "concept_category": "A:Concept_Category",
        "gui_category": "A:GUI_Category",
        "icdo_code_ssr": "A:ICD-O-3_Morfologia", 
        "order_number": "ANUM:JarjestysNro",
        "lang": "A:Lang",
        "legacy_conceptid": "A:Legacy_ConceptID", 
        "legacy_termid": "A:Legacy_TermID",
        "sct_termid": "A:SCT_TermID",
        "sct_concept_fsn": "A:SCT_Concept_FSN",
        "sct_conceptid": "A:SNOMEDCT"
    })
    return df

def to_excel(final_df):
    final_df.to_excel(
        "test_cs_format.xlsx", index=False)

def main():
    db = Database()
    df = db.get()
    df = cs_columns(df)
    df = select_columns(df)
    df = sort_df(df)
    df = rename_columns(df)
    to_excel(df)








# def transpose_table_lineid(df):
#     Row = namedtuple("Row", "CodeID LongName legacy_termid sct_termid lang HierarchyLevel ParentID gui_category concept_category legacy_conceptid sct_conceptid sct_concept_fsn icdo3 active BeginningDate ExpiringDate korvaava_koodi ShortName Abbreviation")
#     t_rows = []
#     for _, row in df.iterrows():
#         if row["tmdc"][0] in ["A", "D", "M"]:
#             qui_category = "diagnosis"
#         elif row["tmdc"][0] == "C":
#             qui_category = "cytology"
#         elif row["tmdc"][0] == "T":
#             qui_category = "topography"
#         else:
#             qui_category = "unknown"

#         match = re.search(
#             "(?P<category>\(([^()]*)\))$", row["sct_concept_fsn"])
#         if match:
#             if match.group("category"):
#                 concept_category = match.group("category")[1:-1]

#         if len(row["sct_term"]) > 50:
#             short_term = row["sct_term"][:50]
#         else:
#             short_term = row["sct_term"]

#         t_row = Row(
#             CodeID=row["lineid"],
#             LongName=row["sct_term"],
#             legacy_termid=row["legacy_termid"],
#             sct_termid=row["sct_termid"],
#             lang=row["lang"],
#             HierarchyLevel=0 if row["lang"] == "en" else 1,
#             ParentID=row["sct_termid_en"],
#             gui_category=qui_category,
#             concept_category=concept_category,
#             legacy_conceptid=row["legacy_conceptid"],
#             sct_conceptid=row["sct_conceptid"],
#             sct_concept_fsn=row["sct_concept_fsn"],
#             icdo3=row["icdo_code_ssr"],
#             active=row["in_use"],
#             BeginningDate=row["effectivetime"],
#             ExpiringDate=row["supersededtime"],
#             korvaava_koodi=row["korvaava_koodi"],
#             ShortName=short_term,
#             Abbreviation=short_term
#         )
#         t_rows.append(t_row)
#     final_df = pd.DataFrame(t_rows).sort_values(
#         by=["legacy_conceptid", "ParentID", "lang"])
#     for i, row in final_df.iterrows():
#         if row["lang"] == "en":
#             final_df.at[i, "ParentID"] = None
#     # column headers:, CodeID, LongName, A:Legacy_TermID, SNOMEDCT, A:Lang, HierarchyLevel, ParentID, A:Gui_Category, A:Concept_Category, A:Legacy_ConceptID, A:SCT_ConceptID, A:SCT_Concept_FSN, A:Active, BeginningDate, ExpiringDate, Korvaava koodi, ShortName, Abbreviation
#     final_df = final_df.rename(columns={"legacy_termid": "A:Legacy_TermID", "sct_termid": "A:SCT_TermID", "lang": "A:Lang", "gui_category": "A:GUI_Category", "concept_category": "A:Concept_Category",
#                                "legacy_conceptid": "A:Legacy_ConceptID", "sct_conceptid": "SNOMEDCT", "sct_concept_fsn": "A:SCT_Concept_FSN", "icdo3": "A:ICD-O-3_Morfologia", "active": "A:Active", "korvaava_koodi": "Korvaava koodi"})

#     final_df.insert(0, 'New_ID', range(1, len(final_df) + 1))
#     return final_df





# def main():
#     db = Database()
#     df = db.table_to_df("sct_pat_fi_kanta_20221101_final")
#     df = df[df["in_use"] != "ei"]
#     final_df = transpose_table_lineid(df)
#     to_excel(final_df)


if __name__ == "__main__":
    main()
