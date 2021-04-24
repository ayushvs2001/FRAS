from datetime import datetime
import sqlite3 as sql
import xlsxwriter


def add_attendance(name):
    """
    It add the name, current date and current time into the database

    :param name: name of person
    """

    now = datetime.now()
    current_date = now.date()
    current_time = now.strftime("%H:%M:%S")

    # make in format of h*10000 + m*100 + s
    current_time = (str(current_time)).split(":")
    hour, minute, second = current_time[0], current_time[1], current_time[2]
    current_time = int(hour) * 10000 + int(minute) * 100 + int(second)

    # make in specific format as we did for current time
    current_date = (str(current_date)).split("-")
    date, month, year = current_date[2], current_date[1], current_date[0][-2:]
    current_date = int(year) * 10000 + int(month) * 100 + int(date)

    conn = sql.connect("attendance.bd")
    c = conn.cursor()

    c.execute("INSERT INTO attendance VALUES(:name, :date, :time)",
              {
                  "name": name.title(),
                  "date": current_date,
                  "time": current_time
              })

    conn.commit()
    conn.close()


def build_query(input_values):
    col = ""

    # query for name
    name = "%" + input_values[0].title() + "%"

    # query for date
    start_date = input_values[1].split("/")
    start_date = int(start_date[2]) * 10000 + int(start_date[0]) * 100 + int(start_date[1])

    end_date = input_values[2].split("/")
    end_date = int(end_date[2]) * 10000 + int(end_date[0]) * 100 + int(end_date[1])

    date = f"date >= {start_date} and date <= {end_date}"

    # query for time
    start_time = int(input_values[3]) * 10000 + int(input_values[4]) * 100

    end_time = int(input_values[5]) * 10000 + int(input_values[6]) * 100

    time = f"time >= {start_time} and time <= {end_time}"

    col = f"name like '{name}' and {date} and {time}"
    return col


def check_attendance_data(input_values):
    """
    It used to check the data in database

    :param input_values: list of data contain name of person, start and end date, start and end time
    :return:  list containing data of person
    """

    quality_list = []

    conn = sql.connect("attendance.bd")
    c = conn.cursor()

    # build_query function return query
    col = build_query(input_values)
    c.execute("SELECT * FROM attendance where " + col)
    records = c.fetchall()

    for record in records:
        record1 = str(record[1])
        record2 = str(record[2])
        temp_record1 = record1[-2:] + "/" + record1[-4:-2] + "/" + record1[:-4]
        temp_record2 = record2[:-4] + ":" + record2[-4:-2] + ":" + record2[-2:]

        quality_list.append(str(record[0]) + " " + temp_record1 + " " + temp_record2)

    conn.commit()
    conn.close()

    return quality_list


def delete_attendance(input_values):
    """
    It is used to delete attendance of person
    :param input_values: list of data contain name of person, start and end date, start and end time
    """
    conn = sql.connect("attendance.bd")
    c = conn.cursor()

    # build_query function return query
    col = build_query(input_values)

    # delete all the data which satisfy the condition of name or date
    c.execute("delete FROM attendance where " + col)

    conn.commit()
    conn.close()


def make_attendace_file(input_list):
    """
    It is used to add data in attendance database
    """

    file_name = "Attendance.xlsx"

    # create a file object
    workbook = xlsxwriter.Workbook(file_name)

    # used to add work shit using worksheet object
    worksheet = workbook.add_worksheet()

    # add data
    data = check_attendance_data(input_list)

    worksheet.write(0, 0, "NAME")
    worksheet.write(0, 1, "DATE")
    worksheet.write(0, 2, "TIME")
    row = 1
    column = 0
    for i in data:
        i = i.rsplit(" ")
        worksheet.write(row, column, i[0])
        worksheet.write(row, column + 1, i[1])
        worksheet.write(row, column + 2, i[2])
        row += 1

    workbook.close()


