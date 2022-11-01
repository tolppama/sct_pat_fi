import json
from datetime import datetime
import pandas as pd
from db import Database
from verhoeff import Verhoeff


class CheckRow:
    """Class for storing every check method"""
    
    # basic checks

    @staticmethod
    def check_lineid_unique(df):
        """Check if lineid is unique. """

        return df[df.duplicated(subset=["lineid"])], "duplicate lineid"

    @staticmethod
    def check_tmdc(df):
        """Check if tmdc is valid.

        Valid tmdc(atmdc) values include: 'M', 'DF', 'TU', 'MF_L', 'TF_L', 'TT', 'TF', 'D', 'M_L', 'MT', 'MU', 'T', 'DT', 'MT_L', 'T_L', 'A', 'MU_L', 'C', 'CT', 'MF'
        """

        return df[~df['tmdc'].isin(['M', 'DF', 'TU', 'MF_L', 'TF_L', 'TT', 'TF', 'D', 'M_L', 'MT', 'MU', 'T', 'DT', 'MT_L', 'T_L', 'A', 'MU_L', 'C', 'CT', 'MF'])], "Invalid tmdc value"

    @staticmethod
    def check_lang(df):
        """Check if lang is valid. 

        Valide values include: fi, sv, en
        """

        return df[~df['lang'].isin(['fi', 'sv', 'en'])], "Invalid lang value"

    @staticmethod
    def check_in_use(df):
        """Check if in_use is valid. 

        Valid values include: None, kesken, ei
        """

        return df[~df['in_use'].isin([None, 'kesken', 'ei'])], "Invalid in_use value"

    @staticmethod
    def check_legacy_conceptid(df):
        """Check if legacy_conceptid is valid. 

        Starts with 6 alphanumeric characters, followed by a dash and an SCT ID.
        """

        return df[~df['legacy_conceptid'].str.contains("^[\w\d]{6}-\d+$")], "Invalid legacy_conceptid value"

    @staticmethod
    def check_legacy_termid(df):
        """Check if legacy_termid is valid.

        Starts with 6 alphanumeric characters, followed by a dash and an SCTID.
        """

        return df[~df['legacy_termid'].str.contains("^[\w\d]{6}-\d+$")], "Invalid legacy_termid value"

    @staticmethod
    def check_sct_concept_fsn(df):
        """Check if sct_concept_fsn is valid. 

        Includes a semantic tag.
        """

        return df[~df['sct_concept_fsn'].str.contains(".+\(([^()]*)\)$")], "Invalid sct_concept_fsn value"

    @staticmethod
    def check_sct_term(df):
        """Check sct_term is not empty."""

        return df[df['sct_term'].isna()], "Empty sct_term value"

    @staticmethod
    def check_ok_not_ok(df):
        """Check if ok_not_ok is valid.

        Valid values include: ok, not_ok
        """

        return df[~df['ok_not_ok'].isin(['ok', 'not_ok'])], "Invalid ok_not_ok value"

    @staticmethod
    def check_effective_time(df):
        """Check if effectivetime is right format.

        Valid format: YYYY-MM-DD
        """

        return df[~df['effectivetime'].str.contains("^\d{4}-\d{2}-\d{2}$", na=False)], "Invalid effective_time value"

    @staticmethod
    def check_supersededtime(df):
        """Check if supersededtime is right format.

        Valid format: YYYY-MM-DD
        """

        return df[~df['supersededtime'].str.contains("^\d{4}-\d{2}-\d{2}$", na=False)], "Invalid supersededtime value"

    @staticmethod
    def check_sct_concept_fsn_capital(df):
        """Check if sct_concept_fsn begins with capital letter."""

        return df[~df['sct_concept_fsn'].str.contains("^[A-Z].+$")], "sct_concept_fsn begins with lowercase letter"

    @staticmethod
    def check_sct_term_capital(df):
        """Check if sct_term begins with capital letter."""

        return df[~df['sct_term'].str.contains("^[A-Z].+$")], "sct_term begins with lowercase letter"

    # advanced checks

    @staticmethod
    def check_sct_conceptid_checksum(df):
        """Check if sct_conceptid has correct checksum."""

        mask = df.apply(Verhoeff.verify_conceptid, axis=1)
        return df[~mask], "Invalid sct_conceptid checksum"

    @staticmethod
    def check_sct_termid_checksum(df):
        """Check if sct_termid has correct checksum."""

        mask = df.apply(Verhoeff.verify_termid, axis=1)
        return df[~mask], "Invalid sct_termid checksum"

    @staticmethod
    def check_sct_conceptid_legacy_conceptid(df):
        """Check if sct_conceptid and legacy_conceptids SCTID part are equal."""

        return df[~df['sct_conceptid'].eq(df['legacy_conceptid'].str.split("-").str[1])], "sct_conceptid and legacy_conceptid not equal"

    @staticmethod
    def check_sct_termid_legacy_termid(df):
        """Check if sct_termid and legacy_termids SCTID part are equal."""

        return df[~df['sct_termid'].eq(df['legacy_termid'].str.split("-").str[1])], "sct_termid and legacy_termid not equal"

    @staticmethod
    def check_legacy_conceptid_legacy_termid(df):
        """Check if legacy_conceptids and legacy_termids SN2 part are equal."""

        return df[~df['legacy_conceptid'].str.split("-").str[0].eq(df['legacy_termid'].str.split("-").str[0])], "legacy_conceptid and legacy_termid not equal"

    @staticmethod
    def check_effective_time_supersededtime(df):
        """Check if effective_time is before supersededtime."""

        return df[~df['effectivetime'].le(df['supersededtime'])], "effective_time is not less than supersededtime"

    @staticmethod
    def check_supersededtime_in_use(df):
        """Check if in_use is ei, then supersededtime is in the past """

        return df[df['in_use'].eq('ei') & df['supersededtime'].ge(datetime.now().strftime("%Y-%m-%d"))], "supersededtime is not in the past"

    @staticmethod
    def check_in_use_supersededtime(df):
        """Check if supersededtime is in the past, then in_use is ei"""

        return df[df['supersededtime'].lt(datetime.now().strftime("%Y-%m-%d")) & df['in_use'].ne('ei')], "in_use is not ei"

    # en row checks

    @staticmethod
    def get_lang_rows(df, en_row):
        """Tool for retrieving lang rows."""

        return df.loc[(df["sct_termid_en"] == en_row["sct_termid"]) & (df["lang"] != "en")]

    @staticmethod
    def check_sct_conceptid_lang_same_as_sct_conceptid_en(df, en_row):
        """Check conceptid is same in lang rows as in en row."""

        lang_rows = CheckRow.get_lang_rows(df, en_row)
        return lang_rows[~lang_rows['sct_conceptid'].eq(en_row['sct_conceptid'])], "lang rows and en row sct_conceptid differ"

    @staticmethod
    def check_sct_concept_fsn_lang_same_as_sct_concept_fsn_en(df, en_row):
        """Check concept_fsn is same in lang rows as in en row."""

        lang_rows = CheckRow.get_lang_rows(df, en_row)
        return lang_rows[~lang_rows['sct_concept_fsn'].eq(en_row['sct_concept_fsn'])], "lang rows and en row sct_concept_fsn differ"

    @staticmethod
    def check_sct_term_lang_same_as_sct_term_en(df, en_row):
        """Check that if term is same in lang rows as in en row, then sct_termid is also the same."""

        lang_rows = CheckRow.get_lang_rows(df, en_row)
        same_term = lang_rows.loc[lang_rows["sct_term"] == en_row["sct_term"]]
        if not same_term.empty:
            return same_term[same_term["sct_termid"] != en_row["sct_termid"]], "sct_term same in en and lang rows but different sct_termid"
        return pd.DataFrame(), ""

    @staticmethod
    def check_sct_termid_lang_same_as_sct_termid_en(df, en_row):
        """Check that if termid is same in lang rows as is en row, then sct_term is also the same."""

        lang_rows = CheckRow.get_lang_rows(df, en_row)
        same_termid = lang_rows.loc[lang_rows["sct_termid"]
                                    == en_row["sct_termid"]]
        if not same_termid.empty:
            return same_termid[same_termid["sct_term"] != en_row["sct_term"]], "sct_termid same in en and lang rows but different sct_term"
        return pd.DataFrame(), ""


def general_checks(df):
    """Run general checks on the entire dataframe."""

    invalid_values = {}
    df_checks = [
        CheckRow.check_lineid_unique,
        CheckRow.check_tmdc,
        CheckRow.check_lang,
        CheckRow.check_in_use,
        CheckRow.check_legacy_conceptid,
        CheckRow.check_legacy_termid,
        CheckRow.check_sct_concept_fsn,
        CheckRow.check_sct_term,
        CheckRow.check_ok_not_ok,
        CheckRow.check_effective_time,
        CheckRow.check_supersededtime,
        CheckRow.check_sct_conceptid_checksum,
        CheckRow.check_sct_termid_checksum,
        CheckRow.check_sct_conceptid_legacy_conceptid,
        CheckRow.check_sct_termid_legacy_termid,
        CheckRow.check_legacy_conceptid_legacy_termid,
        CheckRow.check_effective_time_supersededtime,
        CheckRow.check_in_use_supersededtime,
        CheckRow.check_supersededtime_in_use
    ]

    for check in df_checks:
        sub_df, message = check(df)
        if not sub_df.empty:
            lineids = sub_df["lineid"].tolist()
            invalid_values[message] = lineids

    return invalid_values


def en_row_checks(df):
    """Run checks on en rows + lang rows."""

    invalid_values = {}
    en_checks = [
        CheckRow.check_sct_conceptid_lang_same_as_sct_conceptid_en,
        CheckRow.check_sct_concept_fsn_lang_same_as_sct_concept_fsn_en,
        CheckRow.check_sct_term_lang_same_as_sct_term_en,
        CheckRow.check_sct_termid_lang_same_as_sct_termid_en
    ]
    en_rows = df.loc[df["lang"] == "en"]
    for _, en_row in en_rows.iterrows():
        for check in en_checks:
            sub_df, message = check(df, en_row)
            if not sub_df.empty:
                lineids = sub_df["lineid"].tolist()
                if message in invalid_values:
                    invalid_values[message].extend(lineids)
                else:
                    invalid_values[message] = lineids
    return invalid_values


def write_invalid_values_to_json(invalid_values):
    with open("invalid_values.json", "w") as f:
        json.dump(invalid_values, f, indent=4)


def main():
    con = Database()
    df = con.table_to_df("sct_pat_fi_kanta_20221101_paula_fsn_new")
    invalid_values = general_checks(df)
    invalid_values.update(en_row_checks(df))
    write_invalid_values_to_json(invalid_values)


if __name__ == "__main__":
    main()
