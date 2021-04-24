from tkinter import messagebox
import cv2
import face_recognition
from check_attendance import add_attendance
import sqlite3
import numpy
import io


def mark_attendance():
    """
    It used to send data of student which encounter in camera
    """
    conn = sqlite3.connect("person_database.bd")
    c = conn.cursor()

    c.execute("SELECT *, oid FROM person_info")
    records = c.fetchall()

    class_names = []
    encode_list_known = []

    for record in records:
        class_names.append(record[0])
        out = io.BytesIO(record[1])
        out.seek(0)
        data = numpy.load(out)
        encode_list_known.append(data)

    messagebox.showinfo("Message", "PLEASE \n WAIT A MINUTE")

    conn.commit()
    conn.close()

    cap = cv2.VideoCapture(0)

    thres = 0.45  # Threshold to detect object
    config_path = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'  # for object detection such as cellphone
    weights_path = 'frozen_inference_graph.pb'

    net = cv2.dnn_DetectionModel(weights_path, config_path)
    net.setInputSize(320, 320)
    net.setInputScale(1.0 / 127.5)
    net.setInputMean((127.5, 127.5, 127.5))
    net.setInputSwapRB(True)

    while class_names:
        success, img = cap.read()

        # for object detection
        class_ids, confs, bbox = net.detect(img, confThreshold=thres)
        list_of_object = {77: "cell phone", 73: "laptop"}
        temp = img
        confidence_of_required_object = 0

        if len(class_ids) != 0:
            for classId, confidence, box in zip(class_ids.flatten(), confs.flatten(), bbox):
                if classId in list_of_object.keys():
                    cv2.rectangle(temp, box, color=(0, 255, 0), thickness=2)
                    confidence_of_required_object = int(confidence * 100)

        # if object not detected then process go on for face recognition
        if confidence_of_required_object < 48:

            imgs = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgs = cv2.cvtColor(imgs, cv2.COLOR_BGR2RGB)

            faces_cur_frame = face_recognition.face_locations(imgs)  # sending only first img
            encode_cur_frame = face_recognition.face_encodings(imgs, faces_cur_frame)

            for encodeFace, faceLoc in zip(encode_cur_frame, faces_cur_frame):
                matches = face_recognition.compare_faces(encode_list_known, encodeFace)
                face_dis = face_recognition.face_distance(encode_list_known, encodeFace)
                match_index = numpy.argmin(face_dis)

                if matches[match_index] and face_dis[0] < 0.5:
                    name = class_names[match_index].title()
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

                    # remove the record from encode_list_known
                    class_names.pop(match_index)
                    encode_list_known.pop(match_index)

                    # add the data of person into attendance database
                    add_attendance(name)

        cv2.imshow('webcam', img)

        if cv2.waitKey(1) & 0xff == ord(" "):  # if d is press the break the while loop
            break

    cv2.destroyWindow(winname="webcam")
