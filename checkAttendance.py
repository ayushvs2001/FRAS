from datetime import datetime
import sqlite3 as sql
import xlsxwriter


# conn = sql.connect("attendance.bd")
# c = conn.cursor()
# # c.execute("""CREATE TABLE person_info(
# #              name text,
# #              encoding tinyblob
# # )
# #         """)
# # c.execute("""CREATE TABLE person_attendance(
# #              name text,
# #              date text,
# #              time text
# # )
# #         """)
# c.execute("""select name from sqlite_master where type='table'""")
# # c.execute("select * from person_info")
# print(c.fetchall())
# # c.execute("drop table student_attendance")
# conn.commit()
# conn.close()

def add_attedance(name):
    """
    It add the name, current date and current time into the database

    :param name: name of person
    """

    now = datetime.now()
    current_date = now.date()
    current_time = now.strftime("%H:%M:%S")
    conn = sql.connect("attendance.bd")
    c = conn.cursor()

    c.execute("INSERT INTO person_attendance VALUES(:name, :date, :time)",
                              {
                                  "name": name.title(),
                                  "date": str(current_date),
                                  "time": str(current_time)
                              })

    conn.commit()
    conn.close()


def check_attendance_data(name, date):
    """
    It used to check the data into database

    :param name: name of person
    :param date: current date
    :return:  list containing data of person
    """

    quality_list = []

    conn = sql.connect("attendance.bd")
    c = conn.cursor()

    col = ""



    # retrive all data from the person_attendance
    if name != "" and date == "":
        col = f"name = '{name.title()}'"
    elif name == "" and date != "":
        col = f"date = '{date}'"
    else:
        col = f"name = '{name.title()}' and date='{date}'"

    c.execute("SELECT * FROM person_attendance where "+col)
    records = c.fetchall()

    conn.commit()
    conn.close()

    for record in records:
        quality_list.append(str(record[0]) + " " + str(record[1]) + " " + str(record[2]))

    return quality_list

def delete_attendance(name, date):
    """
    It is used to delete attendance of person
    """
    conn = sql.connect("attendance.bd")
    c = conn.cursor()

    col = ""

    if name != "" and date == "":
        col = f"name = '{name.title()}'"
    elif name == "" and date != "":
        col = f"date = '{date}'"
    else:
        col = f"name = '{name.title()}' and date='{date}'"

    c.execute("delete FROM person_attendance where "+col)
    records = c.fetchall()

    conn.commit()
    conn.close()


def make_attendace_file(name, date):
    """
    It is used to add data into attendance database

    """

    file_name = "Attendance.xlsx"

    # create a file object
    workbook = xlsxwriter.Workbook(file_name)

    # used to addwork shit using worksheet object
    worksheet = workbook.add_worksheet()

    # add data
    data = check_attendance_data(name.title(), date)

    worksheet.write(0, 0, "NAME")
    worksheet.write(0, 1, "DATE")
    worksheet.write(0, 2, "TIME")
    row = 1
    column = 0
    for i in data:
        i = i.rsplit(" ")
        worksheet.write(row, column, i[0])
        worksheet.write(row, column+1, i[1])
        worksheet.write(row, column+2, i[2])
        row += 1

    workbook.close()




