import os
import json
import shutil
import shutil
import logging
import tempfile
import requests
from datetime import datetime, timedelta
import time


class PagarMeAPI:

    def __init__(self, token) -> None:
        self.token = token

    @staticmethod
    def convert_to_unix_milliseconds(datetime_to_convert):
        return int(time.mktime(datetime_to_convert.timetuple())*1e3)

    def request_data_from_api(self, report_type:str, start_date, end_date):
   
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        print(f"Date Rage between: {start_date} and {end_date}")

        all_data = []
        page = 1
        while True:
            print(f"Getting page {page}")
            url = f"https://api.pagar.me/1/{report_type}?count=1000&page={page}&date_created=>={self.convert_to_unix_milliseconds(start_date)}&date_created=<={self.convert_to_unix_milliseconds(end_date)}&api_key={self.token}"
            resp = requests.get(url, headers=headers)
            if len(resp.json())==0:
                break
            else:
                all_data.extend(resp.json())
            page += 1

        print("-> Got the API data")

        return all_data


   
    
    

            


if __name__=="__main__":
    REPORT_TYPE = "transactions"
    token = ''

    end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)  + timedelta(hours=3)
    start_date = end_date - timedelta(days=1)

    api = PagarMeAPI(token=token)
    data = api.request_data_from_api(report_type=REPORT_TYPE, start_date=start_date, end_date=end_date)

