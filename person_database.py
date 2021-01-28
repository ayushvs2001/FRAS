import sqlite3
import io
import numpy
import cv2, face_recognition
from tkinter import messagebox
from Face_Recognition_And_Attendance_Project.checkAttendance import add_attedance

def add(name, encoding):
    """

    :param name: name of person
    :param encoding: data of there image
    :return:
    """

    # create a database or connect to one
    conn = sqlite3.connect("person_database.bd",detect_types=sqlite3.PARSE_DECLTYPES)
    # create cursor
    c = conn.cursor()

    out = io.BytesIO()
    numpy.save(out, encoding)
    out.seek(0)

    c.execute("INSERT INTO person_info VALUES (:name, :encoding)",
              {
                  "name": name,
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


def mark_attendance():
    """
    It used to send data of student which encounter in camera
    """
    conn = sqlite3.connect("person_database.bd")
    c = conn.cursor()

    c.execute("SELECT *, oid FROM person_info")
    records = c.fetchall()

    classNames = []
    encodeListKnown = []
    list_of_names = set()

    for record in records:
        classNames.append(record[0])
        out = io.BytesIO(record[1])
        out.seek(0)
        data = numpy.load(out)
        encodeListKnown.append(data)

    messagebox.showinfo("Message", "PLEASE \n WAIT A MINUTE")

    conn.commit()
    conn.close()

    cap = cv2.VideoCapture(0)

    thres = 0.45  # Threshold to detect object
    configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'  # for object detection such as cellphone
    weightsPath = 'frozen_inference_graph.pb'

    net = cv2.dnn_DetectionModel(weightsPath, configPath)
    net.setInputSize(320, 320)
    net.setInputScale(1.0 / 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)

    while True:
        success, img = cap.read()

        # for object detection
        classIds, confs, bbox = net.detect(img, confThreshold=thres)
        list_of_object = {77: "cell phone", 73: "laptop"}
        temp = img
        confidence_of_required_object = 0

        if len(classIds) != 0:
            for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                if classId in list_of_object.keys():
                    cv2.rectangle(temp, box, color=(0, 255, 0), thickness=2)
                    confidence_of_required_object = int(confidence * 100)

       # if object not detected then process go on for face recognition
        if confidence_of_required_object < 48:

            imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgs)  # sending only first img
            encodeCurFrame = face_recognition.face_encodings(imgs, facesCurFrame)

            for encodeFace, faceLoc in zip(encodeCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                # print(faceDis)
                matchIndex = numpy.argmin(faceDis)

                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    # print(name)
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                    if name not in list_of_names:
                       list_of_names.add(name)
                       add_attedance(name)

        cv2.imshow('webcam', img)

        if cv2.waitKey(1) & 0xff == ord(" "):  # if d is press the break the while loop
            break

    cv2.destroyWindow(winname="webcam")
