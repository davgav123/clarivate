from pprint import pprint
from parsers.HolidayParser import HolidayParser
from database.HolidayDatabase import HolidayDatabase


def main():
    parser = HolidayParser()
    holiday_data = parser.get_holiday_data()
    pprint(holiday_data)

    database = HolidayDatabase('holidays')
    database.save_holiday_data(holiday_data)

    print('\n------------------------------------\n') # just a separator

    holiday_data = database.read_holiday_data()
    print(holiday_data)


if __name__ == '__main__':
    main()