__author__ = 'shako'
import json
import time
import gspread
import argparse
import datetime
from argparse import ArgumentDefaultsHelpFormatter
from oauth2client.client import SignedJwtAssertionCredentials



{'Pure Idle': {'v2.2': {'Run1': [0, 0, 0], 'Run2':[0, 0, 0], 'Run3':[0, 0, 0], 'Average': [0,0,0]},
               'v3.0': {'Run1': [0, 0, 0], 'Run2':[0, 0, 0], 'Run3':[0, 0, 0], 'Average': [0,0,0]}}}

class PowerDataUploader(object):
    SCOPE = ['https://spreadsheets.google.com/feeds']

    def __init__(self):
        self.arg_parser = argparse.ArgumentParser(description='Generate raptor json data from Google Sheets',
                                                  formatter_class=ArgumentDefaultsHelpFormatter)
        self.arg_parser.add_argument('-c', '--credential-path', action='store', dest='credential_json_file_path', default=None,
                                     help='Specify the path of credential to access google sheets.', required=True)

        self.arg_parser.add_argument('-t', '--sheet-title', action='store', dest='sheet_title', default=None,
                                     help='Specify the title of monitored sheet.', required=True)

        self.arg_parser.add_argument('-o', '--output-file-path', action='store', dest='output_json_file', default=None,
                                     help='Output json file path.', required=True)

        self.args = self.arg_parser.parse_args()
        self.credential_json_file_path = self.args.credential_json_file_path
        self.sheet_title = self.args.sheet_title
        self.output_json_path = self.args.output_json_file

    def get_max_column_no(self, worksheet):
        col_no = 1
        while True:
            if worksheet.cell(2, col_no).value == "":
                break
            col_no += 1
        return col_no

    def get_worksheet_content(self, worksheet, version_list, max_row_no=15):
        result = {}
        max_col_no = self.get_max_column_no(worksheet)
        for row_no in range(1, max_row_no):
            if worksheet.cell(row_no, 1).value in version_list:
                version = worksheet.cell(row_no, 1).value
                result[version] = {}
                for scope_index in range(1, 5):
                    result[version][worksheet.cell(row_no + scope_index, 1).value] = []
                    for col_no in range(2, max_col_no):
                        result[version][worksheet.cell(row_no + scope_index, 1).value].append(worksheet.cell(row_no + scope_index, col_no).value)
        return result

    def get_version_list(self, worksheet, max_row_no=15):
        result = []
        empty_cell_no = 1
        for row_no in range(1, max_row_no):
            if worksheet.cell(row_no, 1).value != "":
                result.append(worksheet.cell(row_no, 1).value)
            else:
                empty_cell_no += 1
            if empty_cell_no >= 4:
                break

        return result

    def get_spreadsheet_content(self):
        result = {}
        spreadsheet = self.gs_obj.open(self.sheet_title)
        version_list = ['v2.2', 'v3.0']
        for worksheet in spreadsheet.worksheets():
            if worksheet.title != "Build Information":
                result[worksheet.title] = self.get_worksheet_content(worksheet, version_list)
            else:
                version_list = self.get_version_list(worksheet)
        return result

    def login_google_sheet(self):
        json_key = json.load(open(self.credential_json_file_path))
        credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(), self.SCOPE)
        self.gs_obj = gspread.authorize(credentials)

    def output_raptor_data(self, sheet_content):
        result = []
        [{"fields": {"value": 0.3754589877777778}, "timestamp": "1443284155000000001", "key": "power",
          "tags": {"device": "flame-kk", "branch": "master", "memory": "1024"}, "test": "camera_preview",
          "context": "camera.gaiamobile.org"}]
        current_timestamp = str((int(time.mktime(datetime.datetime.now().timetuple()) * 1000) * 1000000) + 1)
        for test_name in sheet_content:
            test_result = {}
            test_result['test'] = test_name
            test_result['fields'] = {'value': sheet_content[test_name]['master']}

    def run(self):
        self.login_google_sheet()
        sheet_content = self.get_spreadsheet_content()
        self.output_raptor_data(sheet_content)



def main():
    pdu_obj = PowerDataUploader()
    pdu_obj.run()

if __name__ == "__main__":
    main()

