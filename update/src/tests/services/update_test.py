import unittest
import os
import pandas as pd
from services import Component


class MockExcel:
    # read the csv files and convert them to pandas dataframes
    def __init__(self):
        self.dirname = os.path.dirname(__file__)
        self.fake_excel = self.read_test_data(os.path.join(
            self.dirname, "..", "data", "test_excel.csv"))
        self.fake_db = self.read_test_data(os.path.join(
            self.dirname, "..", "data", "test_db.csv"))

    def read_test_data(self, filename):
        return pd.read_csv(filename, dtype=str)


class UpdateTest(unittest.TestCase):
    def setUp(self):
        self.component = Component(None)
        self.db = MockExcel().fake_db
        self.excel = MockExcel().fake_excel

    def test_get_next_lineid(self):
        self.assertEqual(self.component.get_next_codeid(self.db), 15961)

    def test_create_new_lineids(self):
        self.assertEqual(
            self.component.create_new_lineids(6, 5),
            [6, 7, 8, 9, 10]
        )

    def test_next_fin_extension_id(self):
        self.assertEqual(self.component.next_fin_extension_id(
            self.db, 'sct_termid'), 2547)

    def test_check_legacyid(self):
        self.assertEqual(self.component.check_legacyid(
            self.db.iloc[0], 'legacy_termid'), '194003013')
        self.assertEqual(self.component.check_legacyid(
            self.db.iloc[1], 'legacy_termid'), '25451000288114')
        self.assertEqual(self.component.check_legacyid(
            self.db.iloc[2], 'legacy_termid'), '25461000288112')

    def test_legacyid_sn2(self):
        self.assertEqual(self.component.check_legacyid(
            self.db.iloc[0], 'legacy_termid', True), 'M01000')
        self.assertEqual(self.component.check_legacyid(
            self.db.iloc[1], 'legacy_termid', True), 'M01000')
        self.assertEqual(self.component.check_legacyid(
            self.db.iloc[2], 'legacy_termid', True), 'M01000')

    def test_get_edit_lines(self):
        self.assertEqual(self.component.get_edit_rows(self.db).shape[0], 0)
        self.assertEqual(self.component.get_edit_rows(self.excel).shape[0], 6)
