import re
from database import Database


def qui_category(row):
    if row["tmdc"][0] in ["A", "D", "M"]:
        return "diagnosis"
    elif row["tmdc"][0] == "C":
        return "cytology"
    elif row["tmdc"][0] == "T":
        return "topography"
    else:
        return "unknown"


def concept_category(row):
    match = re.search("(?P<category>\(([^()]*)\))$", row["sct_concept_fsn"])
    if match and match.group("category"):
        return match.group("category")[1:-1]
    return "unknown"


def short_term(row):
    return row["sct_term"][:50] if len(row["sct_term"]) > 50 else row["sct_term"]


def hierarchy_level(row):
    return 0 if row["lang"] == "en" else 1


def cs_columns(df):
    df["hierarchy_level"] = df.apply(hierarchy_level, axis=1)
    df["gui_category"] = df.apply(qui_category, axis=1)
    df["concept_category"] = df.apply(concept_category, axis=1)
    df["short_name"] = df.apply(short_term, axis=1)
    df["abbreviation"] = df.apply(short_term, axis=1)
    df["order_number"] = None
    df["order_number"] = None
    return df


def select_columns(df):
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
        # "superceded_by",
        # "inaktivoinnin_selite",
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


def rename_columns(df):
    df = df.rename(columns={
        "lineid": "CodeID",
        "abbreviation": "Abbreviation",
        "short_name": "ShortName",
        "sct_term": "LongName",
        "sct_termid_en": "ParentId",
        "hierarchy_level": "HierarchyLevel",
        "in_use": "A:Active",
        "effectivetime": "BeginningDate",
        "supersededtime": "ExpiringDate",
        # "superceded_by": "A:KorvaavaKoodi",
        # "inaktivoinnin_selite": "A:InaktivoinninSelite",
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


def sort_df(df):
    df = df.sort_values(by=["A:Legacy_ConceptID", "ParentId", "A:Lang"])
    df["ANUM:JarjestysNro"] = range(1, 1 + len(df))
    df["ANUM:JarjestysNro"] = df["ANUM:JarjestysNro"].astype(int)
    return df


def parent_id(row):
    return None if row["A:Lang"] == "en" else row["ParentId"]


def to_excel(final_df):
    final_df.to_excel(
        "test_cs_format.xlsx", index=False)


def main():
    db = Database()
    df = db.get()
    df = cs_columns(df)
    df = select_columns(df)
    df = rename_columns(df)
    df = sort_df(df)
    df["ParentId"] = df.apply(parent_id, axis=1)
    to_excel(df)


if __name__ == "__main__":
    main()
