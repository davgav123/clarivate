import requests
import pandas as pd
from re import sub
from unicodedata import normalize


class HolidayParser:
    '''Class for reading the australian holidays data from web'''

    def __init__(self):
        self._url = 'https://www.commerce.wa.gov.au/labour-relations/public-holidays-western-australia'


    def get_holiday_data(self):
        raw_table = self.get_raw_table()
        return self.clean_table(raw_table)


    def get_raw_table(self) -> pd.DataFrame:
        '''Get raw data from url and convert it to dataframe'''

        page_data = requests.get(self._url)
        raw_table = self.parse_html_page(page_data.text)
        return raw_table

    
    def parse_html_page(self, contents):
        df_list = pd.read_html(contents)
        holidays_table = [
            df for df in df_list if '2022' in df.columns and '2023' in df.columns
        ][0]
        return holidays_table


    def clean_table(self, raw_holidays: pd.DataFrame) -> pd.DataFrame:
        '''Clean raw holiday data'''

        raw_holidays.drop(columns=['2024'], inplace=True)
        raw_holidays.columns = ['Holiday Name', '2022', '2023']

        holidays = raw_holidays.applymap(
            lambda text: normalize('NFKD', sub('[*#]', '', text).strip()) if pd.notnull(text) else text
        )
        return holidays
