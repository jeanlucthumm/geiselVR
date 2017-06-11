import csv
import sys
import sqlite3

# Positions in CSV file
ITEM_NUM = 0
BIB_NUM = 1
TITLE = 2
AUTHOR = 3
O_AUTHOR = 4
PUBLISHER = 5
YEAR = 6
ISBN = 7
EXT_OR_DESC = 8
DIM_OR_DESC = 9
SUBJECT = 10
GENRE = 11
SUMMARY = 12
TOC = 13
CALL_NUM = 14
COPY_NUM = 15
VOL = 16
LOCATION = 17

SIZE = 18  # number of entries per line


def process_line(line):
    if (len(line) != SIZE):
        return None

    return (line[CALL_NUM], line[TITLE])


def store_data(data: tuple, db: sqlite3.Cursor):
    db.execute('INSERT INTO main VALUES (?,?)', data)

def main(argv):
    with open(argv[1], newline='') as csvfile:
        csvfile.readline()  # skip header
        reader = csv.reader(csvfile, delimiter='\t')
        conn = sqlite3.connect('call-only.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM main')


        # Populate dat
        count = 0
        for row in reader:
            dataTuple = process_line(row)
            store_data(dataTuple, cursor)
            if (count % 100000 == 0):
                print(count)
            count += 1
        conn.commit()
        conn.close()


if __name__ == '__main__':
    main(sys.argv)