from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class gsheet(object):
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        secret_file = 'credentials.json'
        self.creds = service_account.Credentials.from_service_account_file(secret_file, scopes=SCOPES)    
        
        #self.creds = service_account.Credentials.scopes(SCOPES)
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