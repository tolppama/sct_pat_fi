from database import Database


def db_table_to_dataframe(db):
    table = db.get()
    return table

def sct_termid_en_to_lineid(df):
    for index, row in df.iterrows():
        parents = df.loc[(df["sct_termid"] == row["sct_termid_en"]) & (
            df["lang"] == "en")]
        if len(parents) == 1:
            parent_id = parents.iloc[0]["lineid"]
        elif len(parents) > 1:
            if row["in_use"] == "ei":
                sub_parents = parents.loc[parents["in_use"] == "ei" & parents["sct_concept_fsn"] == row["sct_concept_fsn"]]
            else:
                sub_parents = parents.loc[parents["in_use"] != "ei" & parents["sct_concept_fsn"] == row["sct_concept_fsn"]]
            if len(sub_parents) == 1:
                parent_id = sub_parents.iloc[0]["lineid"]
            else:
                parent_id = "error: multiple parents"
        else:
            parent_id = "error: no parent"
        
        df.at[index, "sct_termid_en"] = parent_id
    return df

def main():
    db = Database()
    df = db_table_to_dataframe(db)
    df = sct_termid_en_to_lineid(df)
    db.post(df)

if __name__ == "__main__":
    main()
