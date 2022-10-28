from sqlalchemy import create_engine, MetaData, Table, Column, String
import pandas as pd


class HolidayDatabase:
    '''Class for interaction with australian holiday sqlite database'''

    def __init__(self, database_name):
        self._database_engine = create_engine(
            f'sqlite:///{database_name}'
        )

        self.create_holiday_table()


    def create_holiday_table(self):
        '''Create table for australian holidays'''

        metadata = MetaData()
        holidays = Table(
            'australian_holidays',
            metadata,
            Column('Holiday Name', String, primary_key=True),
            Column('2022', String),
            Column('2023', String)
        )

        metadata.create_all(self._database_engine)


    def save_holiday_data(self, holiday_data: pd.DataFrame):
        '''Save australian holidays dataframe into database'''

        holiday_data.to_sql(
            'australian_holidays',
            self._database_engine.connect(),
            index=False,
            if_exists='append'
        )


    def read_holiday_data(self) -> pd.DataFrame:
        '''Read australian holidays dataframe from database'''

        holiday_data = pd.read_sql(
            'australian_holidays',
            self._database_engine.connect()
        )

        return holiday_data
