import pytest
import pandas as pd
from parsers.HolidayParser import HolidayParser


def test_html_parser_one_table():
    html_data = '''
    <table>
      <thead>
        <tr>
          <th></th>
          <th>2022</th>
          <th>2023</th>
          <th>2024</th>
        </tr>
      </thead>
    <tbody>
      <tr>
        <th>holiday1</th>
        <td>Saturday 1 January</td>
        <td>Sunday 1 January</td>
        <td>Monday 1 January</td>
      </tr>
      <tr>
        <th>holiday2</th>
        <td>Sunday 2 January</td>
        <td>Monday 2 January</td>
        <td>Tuesday 2 January</td>
      </tr>
    </tbody>
    </table>
    '''

    raw_data = [
        ['holiday1', 'Saturday 1 January', 'Sunday 1 January', 'Monday 1 January'],
        ['holiday2', 'Sunday 2 January', 'Monday 2 January', 'Tuesday 2 January'],
    ]

    raw_df = pd.DataFrame(
        raw_data, columns=['Unnamed: 0', '2022', '2023', '2024']
    )

    parser = HolidayParser()
    assert parser.parse_html_page(html_data).equals(raw_df)


def test_html_parser_multiple_tables():
    html_data = '''
    <table>
      <thead>
        <tr>
          <th>Some</th>
          <th>Table</th>
          </tr>
      </thead>
      <tbody>
        <tr>
            <td>v1</td>
            <td>v2</td>
        </tr>
      </tbody>
    </table>

    <table>
      <thead>
        <tr>
          <th></th>
          <th>2022</th>
          <th>2023</th>
          <th>2024</th>
        </tr>
      </thead>
    <tbody>
      <tr>
        <th>holiday1</th>
        <td>Saturday 1 January</td>
        <td>Sunday 1 January</td>
        <td>Monday 1 January</td>
      </tr>
      <tr>
        <th>holiday2</th>
        <td>Sunday 2 January</td>
        <td>Monday 2 January</td>
        <td>Tuesday 2 January</td>
      </tr>
    </tbody>
    </table>

    <table>
      <thead>
        <tr>
          <th>Some</th>
          <th>Table</th>
          </tr>
      </thead>
      <tbody>
        <tr>
            <td>v1</td>
            <td>v2</td>
        </tr>
      </tbody>
    </table>
    '''

    raw_data = [
        ['holiday1', 'Saturday 1 January', 'Sunday 1 January', 'Monday 1 January'],
        ['holiday2', 'Sunday 2 January', 'Monday 2 January', 'Tuesday 2 January'],
    ]

    raw_df = pd.DataFrame(
        raw_data, columns=['Unnamed: 0', '2022', '2023', '2024']
    )

    parser = HolidayParser()
    assert parser.parse_html_page(html_data).equals(raw_df)


def test_html_parser_with_nan_values():
    html_data = '''
    <table>
      <thead>
        <tr>
          <th></th>
          <th>2022</th>
          <th>2023</th>
          <th>2024</th>
        </tr>
      </thead>
    <tbody>
      <tr>
        <th>holiday1</th>
        <td></td>
        <td>Sunday 1 January</td>
        <td>Monday 1 January</td>
      </tr>
      <tr>
        <th>holiday2</th>
        <td>Sunday 2 January</td>
        <td></td>
        <td>Tuesday 2 January</td>
      </tr>
    </tbody>
    </table>
    '''

    raw_data = [
        ['holiday1', None, 'Sunday 1 January', 'Monday 1 January'],
        ['holiday2', 'Sunday 2 January', None, 'Tuesday 2 January'],
    ]

    raw_df = pd.DataFrame(
        raw_data, columns=['Unnamed: 0', '2022', '2023', '2024']
    )

    parser = HolidayParser()
    assert parser.parse_html_page(html_data).equals(raw_df)


def test_clean_data_with_special_chars():
    test_data = [
        ['holiday1*', 'Saturday 1 January &  Monday 3 January', 'Sunday 1 January & Monday 2 January', 'Monday 1 January & Tuesday 2 January'],
        ['holiday2#', 'Saturday 1 January', 'Sunday 1 January', 'Monday 1 January'],
        ['holiday3**', 'Saturday 1 January**', 'Sunday 1 January**', 'Monday 1 January**'],
        ['holiday4 #', 'Saturday 1 January#', 'Sunday 1 January ', 'Monday 1 January'],
        ['holiday5 ***', 'Saturday 1 January ***', 'Sunday 1 January ***', 'Monday 1 January ***']
    ]
    test_df = pd.DataFrame(
        test_data, columns=['Unnamed', '2022', '2023', '2024']
    )

    expected_data = [
        ['holiday1', 'Saturday 1 January &  Monday 3 January', 'Sunday 1 January & Monday 2 January'],
        ['holiday2', 'Saturday 1 January', 'Sunday 1 January'],
        ['holiday3', 'Saturday 1 January', 'Sunday 1 January'],
        ['holiday4', 'Saturday 1 January', 'Sunday 1 January'],
        ['holiday5', 'Saturday 1 January', 'Sunday 1 January']
    ]
    expected_df = pd.DataFrame(
        expected_data, columns=['Holiday Name', '2022', '2023']
    )

    parser = HolidayParser()
    assert parser.clean_table(test_df).equals(expected_df)


def test_clean_data_without_special_chars():
    test_data = [
        ['holiday1', 'Saturday 1 January &  Monday 3 January', 'Sunday 1 January & Monday 2 January', 'Monday 1 January & Tuesday 2 January'],
        ['holiday2', 'Saturday 1 January', 'Sunday 1 January', 'Monday 1 January'],
        ['holiday3', 'Saturday 1 January', 'Sunday 1 January', 'Monday 1 January'],
        ['holiday4', 'Saturday 1 January', 'Sunday 1 January', 'Monday 1 January'],
        ['holiday5', 'Saturday 1 January', 'Sunday 1 January', 'Monday 1 January']
    ]
    test_df = pd.DataFrame(
        test_data, columns=['Unnamed', '2022', '2023', '2024']
    )

    expected_data = [
        ['holiday1', 'Saturday 1 January &  Monday 3 January', 'Sunday 1 January & Monday 2 January'],
        ['holiday2', 'Saturday 1 January', 'Sunday 1 January'],
        ['holiday3', 'Saturday 1 January', 'Sunday 1 January'],
        ['holiday4', 'Saturday 1 January', 'Sunday 1 January'],
        ['holiday5', 'Saturday 1 January', 'Sunday 1 January']
    ]
    expected_df = pd.DataFrame(
        expected_data, columns=['Holiday Name', '2022', '2023']
    )

    parser = HolidayParser()
    assert parser.clean_table(test_df).equals(expected_df)


def test_clean_data_with_nan_values():
    test_data = [
        ['holiday1*', 'Saturday 1 January &  Monday 3 January', 'Sunday 1 January & Monday 2 January', 'Monday 1 January & Tuesday 2 January'],
        ['holiday2#', None, 'Sunday 1 January', 'Monday 1 January'],
        ['holiday3**', 'Saturday 1 January**', None, 'Monday 1 January**'],
        ['holiday4 #', 'Saturday 1 January#', 'Sunday 1 January ', None],
        ['holiday5 ***', None, 'Sunday 1 January ***', 'Monday 1 January ***'],
        ['holiday6 ***', None, None]
    ]
    test_df = pd.DataFrame(
        test_data, columns=['Unnamed', '2022', '2023', '2024']
    )

    expected_data = [
        ['holiday1', 'Saturday 1 January &  Monday 3 January', 'Sunday 1 January & Monday 2 January'],
        ['holiday2', None, 'Sunday 1 January'],
        ['holiday3', 'Saturday 1 January', None],
        ['holiday4', 'Saturday 1 January', 'Sunday 1 January'],
        ['holiday5', None, 'Sunday 1 January'],
        ['holiday6', None, None]
    ]
    expected_df = pd.DataFrame(
        expected_data, columns=['Holiday Name', '2022', '2023']
    )

    parser = HolidayParser()
    assert parser.clean_table(test_df).equals(expected_df)
