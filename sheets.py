from __future__ import print_function
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import auth
from dotenv import load_dotenv


def sheets():
    load_dotenv()

    # The ID and range of a sample spreadsheet.
    SPREADSHEET_ID = str(os.environ.get('SPREADSHEET'))
    DESIRED_NAME_RANGE = 'Testing bot!A:Z'


    try:
        creds = auth.get_auth()
        service = build('sheets', 'v4', credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()

        body = {
            "values": [
                ['', '', "This will start on C1"],
                ['C', 'D']
            ]
        }

        try:
            sheet.values().update(
                spreadsheetId=SPREADSHEET_ID, range=DESIRED_NAME_RANGE,
                valueInputOption="USER_ENTERED", body=body).execute()
        except BaseException as err:
            print("couldn't write")

        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=DESIRED_NAME_RANGE).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        for row in values:
            print(row)
    except HttpError as err:
        print(err)


sheets()
