from lib2to3.pytree import Base
import os
from dotenv import load_dotenv
from apartments import get_prices
from gmail import send_mail

from sheets import get_values, write_values

def main():
    load_dotenv()
    SHEET_ID = str(os.environ.get('SPREADSHEET'))
    places = get_values(SHEET_ID, "Setup!A2:B")

    for complex in places:
        tab_name = complex[0]
        url = complex[1]

        range = f"{tab_name}!C:J"

        try:
            print("Getting prices for: ", tab_name)
            rows = get_prices(url=url, range=range, sheet_id=SHEET_ID)

            write_values(spreadsheet_id=SHEET_ID, range=range, values=rows)
            print("Wrote values for: ", tab_name)
        except BaseException as err:
            print(f"{tab_name} failed. {err}")
            continue

    send_mail()

if __name__ == "__main__":
    main()
