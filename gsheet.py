from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class gsheet(object):
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.creds = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                self.creds = pickle.load(token)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server()

            with open('token.pickle', 'wb') as token:
                pickle.dump(self.creds, token)

        self.service = build('sheets', 'v4', credentials=self.creds)
    def update(self,sheetid,sheetrange,values):
        # Call the Sheets API
        sheet = self.service.spreadsheets()
        body = {
            'values': values
        }
        result = sheet.values().update(
            spreadsheetId=sheetid, range=sheetrange,
            valueInputOption='USER_ENTERED', body=body).execute()
        
    def get(self, sheetid, sheet_range):
        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheetid,
                                range=sheet_range).execute()
        return  result.get('values', [])