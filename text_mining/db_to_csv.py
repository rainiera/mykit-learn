import sys
import sqlite3 as lite
import json
import csv
import pprint
from collections import defaultdict


"""Example usage:

$ python db_to_csv.py participants.db participants.csv

Should work fine as long as `turkdemo` in the `table_name` field of config.txt is unaltered,
because that table is being accessed via sqlite in the code.
"""


DB_FILENAME = 'participants.db' if sys.argv[1] is None else sys.argv[1]
CSV_FILENAME = 'participants.csv' if sys.argv[2] is None else sys.argv[2]
COL_NAME = 'datastring'


def get_column_data(col_name=COL_NAME):
    """Returns the data from a column as a list of strings.
    In this case, we are getting a list of the strings from the `datastring` column.
    """
    con = lite.connect(DB_FILENAME)
    data = []
    with con:
        con.row_factory = lite.Row
        cur = con.cursor()
        # the table name is hard-coded into the SQL command
        cur.execute('SELECT * FROM turkdemo')
        rows = cur.fetchall()
        for row in rows:
            data.append(row[col_name])
        return data
    return None


def convert_data_to_dicts(json_strs):
    """Accepts a list of strings representing JSON, and returns a list of dictionaries.
    Skips the string if it cannot be converted into JSON and prints it.
    """
    json_dicts = []
    failed = 0
    total = len(json_strs)
    for i in range(total):
        try:
            json_dict = json.loads(json_strs[i])
            json_dicts.append(json_dict)
        except:
            failed += 1
            print "\nWarning: the record at zero-indexed row {}:".format(i)
            print json_strs[i]
            print "could not be converted into JSON.\n"
            pass
    print "Rows failed: {} / {} \n".format(failed, total)
    return json_dicts


def convert_dicts_to_csv(json_dicts, col_names=['ID', 'phase', 'trial', 'word', 'condition', 'response_word', 'RT_ms']):
    with open('results.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=col_names)
        writer.writeheader()
        for i in range(len(json_dicts)):
            curr = json_dicts[i] # The current json dict/object
            # for debugging
            pretty_print = pprint.PrettyPrinter(indent=4)
            # pretty_print.pprint(curr)
            hitId = curr['hitId']
            data = curr['data']
            for datum in data:
                trial = datum['current_trial']
                phase = datum['trialdata']['phase']
                is_test = (phase == 'TEST')
                word = datum['trialdata']['word'] if is_test else ''
                # print is_test
                pretty_print.pprint(datum)
                condition = datum['trialdata']['relation'] if is_test else ''
                response_word = datum['trialdata']['response'] if is_test else ''
                rt_ms = datum['trialdata']['rt'] if is_test else ''
                writer.writerow({
                                  'ID': hitId,
                                  'trial': trial,
                                  'phase': phase,
                                  'word': word,
                                  'condition': condition,
                                  'response_word': response_word,
                                  'RT_ms': rt_ms,
                                })


if __name__ == "__main__":
    datastrings = get_column_data()
    dicts = convert_data_to_dicts(datastrings)
    convert_dicts_to_csv(dicts)
