import unittest
from datetime import datetime
from pandas import DataFrame
from services import Update


class MockExcel:
    def __init__(self):
        self.fake_table = {
            "CodeID": [1, 2, 3, 4, 5],
            "status": [None, None, None, None, None],
            "lang": ['en', 'fi', 'fi', 'sv', 'en'],
            "legacy_conceptid": [
                'M14100-400048001',
                'M14100-400048001',
                'M14100-400048001',
                'M14100-400048001',
                'M14110-15498001'
            ],
            "legacy_termid": [
                'M14100-1779318014',
                'M14100-22821000288114',
                'M14100-22831000288111',
                'M14100-6491000052116',
                'M14110-26278019'
            ],
            "conceptid": [
                '400048001',
                '400048001',
                '400048001',
                '400048001',
                '15498001'
            ],
            "termid": [
                '1779318014',
                '22821000288114',
                '22831000288111',
                '6491000052116',
                '26278019'
            ],
            "term": [
                'Excoriation',
                'Ekskoriaatio',
                'Hiertymä',
                'Exkoriation',
                'Erosion'
            ],
            "fsn": [
                'Excoriation (morphologic abnormality)',
                'Excoriation (morphologic abnormality)',
                'Excoriation (morphologic abnormality)',
                'Excoriation (morphologic abnormality)',
                'Superficial ulcer (morphologic abnormality)'
            ],
            "fsnid": [
                '1779318014',
                '1779318014',
                '1779318014',
                '1779318014',
                '26278019'
            ],
            "parentid": [None, 1, 1, 1, None],
            "expiringdate": [
                '2099-12-31',
                '2099-12-31',
                '2099-12-31',
                '2099-12-31',
                '2099-12-31'
            ],
            "supersededby": [None, None, None, None, None],
            "reason_for_inactivation": [None, None, None, None, None]
        }


class UpdateTest(unittest.TestCase):
    def setUp(self):
        self.update = Update()
        self.table = self.update.set_lineid_as_index(
            DataFrame.from_dict(MockExcel().fake_table))
        self.excel = MockExcel().fake_table

    def test_get_new_lines(self):
        self.excel['CodeID'] = [None, None, 3, 4, 5]
        tmp_table = DataFrame.from_dict(self.excel)
        print(tmp_table)
        new_lines = self.update.get_new_lines(tmp_table)
        self.assertEqual(new_lines.shape[0], 2)

    def test_get_updated_lines(self):
        self.excel['status'] = ['edit', 'edit', None, None, None]
        tmp_table = DataFrame.from_dict(self.excel)
        updated_lines = self.update.get_updated_lines(tmp_table)
        self.assertEqual(updated_lines.shape[0], 2)
        self.assertEqual(updated_lines['CodeID'].unique()[0], 1)
        self.assertEqual(updated_lines['CodeID'].unique()[1], 2)

    def test_get_inactivated_lines(self):
        self.excel['status'] = [None, None, None, None, 'inactivate']
        tmp_table = DataFrame.from_dict(self.excel)
        inactivated_lines = self.update.get_inactivated_lines(tmp_table)
        self.assertEqual(inactivated_lines.shape[0], 1)
        self.assertEqual(inactivated_lines['CodeID'].unique()[0], 5)

    def test_get_lang_rows(self):
        en_row = self.table.loc[self.table['lang'] == 'en'].index[0]
        lang_rows = self.update.get_lang_rows(self.table, en_row)
        self.assertEqual(lang_rows.shape[0], 3)

    def test_set_new_parentid_to_lang_rows(self):
        en_row = self.table.loc[self.table['lang'] == 'en'].index[0]
        lang_rows = self.update.get_lang_rows(self.table, en_row)
        lang_rows = self.update.set_new_parentid_to_lang_rows(
            lang_rows.copy(), 100)
        self.assertEqual(
            (lang_rows['parentid'].astype(int) == 100).all(), True)

    def test_get_next_lineid(self):
        self.assertEqual(self.update.get_next_lineid(self.table), 6)

    def test_create_new_lineids(self):
        self.assertEqual(self.update.create_new_lineids(
            self.update.get_next_lineid(self.table), 2), [6, 7])

    def test_insert_new_lineids(self):
        self.excel['CodeID'] = [None, None, 3, 4, 5]
        tmp_table = DataFrame.from_dict(self.excel)
        new_lines = self.update.get_new_lines(tmp_table)
        next_lineid = self.update.get_next_lineid(self.table)
        new_lineids = self.update.create_new_lineids(next_lineid, 2)
        new_lines = self.update.insert_new_lineids(
            new_lines.copy(), new_lineids)
        self.assertEqual(new_lines['CodeID'].unique()[0], 6)
        self.assertEqual(new_lines['CodeID'].unique()[1], 7)

    def test_concat_new_lines(self):
        self.excel['CodeID'] = [None, None, 3, 4, 5]
        tmp_table = DataFrame.from_dict(self.excel)
        new_lines = self.update.get_new_lines(tmp_table)
        next_lineid = self.update.get_next_lineid(self.table)
        new_lineids = self.update.create_new_lineids(next_lineid, 2)
        new_lines = self.update.insert_new_lineids(
            new_lines.copy(), new_lineids)
        new_table = self.update.concat_new_lines(self.table.copy(), new_lines)
        self.assertEqual(new_table.shape[0], 7)

    def test_inactivate_updated_line(self):
        self.excel['status'] = [None, None, None, None, 'edit']
        tmp_table = DataFrame.from_dict(self.excel)
        updated_line = self.update.get_updated_lines(tmp_table)
        inactivated_line = self.update.inactivate_old_line(
            updated_line.index[0], self.table.copy(), 6)
        self.assertEqual(
            inactivated_line.loc[updated_line.index[0], 'status'], 'ei')
        self.assertEqual(
            inactivated_line.loc[updated_line.index[0], 'expiringdate'], datetime.now().strftime('%Y-%m-%d'))
        self.assertEqual(
            inactivated_line.loc[updated_line.index[0], 'supersededby'], 6)
        self.assertEqual(
            inactivated_line.loc[updated_line.index[0], 'reason_for_inactivation'], '12')

    
