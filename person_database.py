import io
import sqlite3
import numpy


def add(name, encoding):
    """

    :param name: name of person
    :param encoding: data of there image
    :return:
    """

    # create a database or connect to one
    conn = sqlite3.connect("person_database.bd", detect_types=sqlite3.PARSE_DECLTYPES)
    # create cursor
    c = conn.cursor()

    # we are saving encoding of image using BytesIO object
    out = io.BytesIO()
    numpy.save(out, encoding)
    out.seek(0)

    c.execute("INSERT INTO person_info VALUES (:name, :encoding)",
              {
                  "name": name.title(),
                  "encoding": sqlite3.Binary(out.read())
              })

    conn.commit()
    conn.close()


def delete(no):
    """
    This fuction delete data from the person_database database
    :param no:
    :return:
    """

    conn = sqlite3.connect("person_database.bd")
    c = conn.cursor()

    # delete a record
    c.execute(f"DELETE from person_info WHERE oid= " + str(no))

    conn.commit()
    conn.close()


def show():
    """
    It is used to show return data of person
    """

    quality_list = []

    conn = sqlite3.connect("person_database.bd")
    c = conn.cursor()

    c.execute("SELECT *, oid FROM person_info")
    records = c.fetchall()

    conn.commit()
    conn.close()

    for record in records:
        quality_list.append(str(record[2]) + " " + str(record[0]))

    return quality_list


