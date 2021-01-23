from Face_Recognition_And_Attendance_Project.person_database import *
from Face_Recognition_And_Attendance_Project.checkAttendance import check_attendance_data, delete_attendance, make_attendace_file
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import cv2
import face_recognition

root = Tk()
root.configure(background='black')
root.title("FACE RECOGNITION + ATTENDANCE PROJECT")
root.iconbitmap("photos/FACE_RECO.ico")

# set image in window
file = PhotoImage(file='photos/face_reco_.png')
headingIcon = Label(root, image=file)
headingIcon.pack(side=TOP, pady=10)


# create new window for person database
def open_person_database():
    """ second window for person database"""
    try:
        root.withdraw()
        top = Toplevel()
        top.title("PERSON DATABASE")
        top.configure(background='black')

        variable = StringVar(top)
        quality_combo = ttk.Combobox(top, width=27, font="arial", textvariable=variable)

        # label at the top of person database name
        my_label = Label(top, text="person database", font="arial", fg="White", bg="black")
        my_label.grid(row=0, column=1, padx=(0, 90), pady=(10, 0))

        # label and input field for name && Add button
        name_label = Label(top, text="NAME :", font="arial")
        name_label.grid(row=1, column=0, padx=(0, 10), pady=(10, 0))

        name = Entry(top, width=25, font="arial")
        name.grid(row=1, column=1, padx=20, pady=(10, 0))

        # label and input field for path and button right to input field for browsing to img
        path_name_label = Label(top, text="PATH :", font="arial")
        path_name_label.grid(row=2, column=0, padx=(0, 10), pady=(10, 0))

        path_name = Entry(top, width=25, font="arial")
        path_name.grid(row=2, column=1, padx=(13, 10), pady=(10, 0))

        def path_of_image():
            root.filename = filedialog.askopenfilename(initialdir="/", title="select a image",
                                                       filetypes=(("jpeg images", "*.jpg"), ("png images", "*.png")))
            path_name.insert(0, root.filename)

        path_btn = Button(top, text="->", fg="black", bg="white", command=path_of_image)
        path_btn.grid(row=2, column=2, columnspan=2, pady=(15, 0), padx=(0, 0), ipady=1, ipadx=6)

        def add_data():
            if name.get() == "" or path_name.get() == "":
                messagebox.showerror("Message", "Please Fill All Required DATA")
            else:
                # read img
                img = cv2.imread(path_name.get())

                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                # find encoding
                encoding = face_recognition.face_encodings(img)[0]

                # pass to add function in person database.py
                add(name.get(), encoding)
                messagebox.showinfo("Message", "Data ADDED Successfully")
                name.delete(0, len(name.get()))   # delete the name in name input filled after hitting the add button
                path_name.delete(0, len(path_name.get()))

        add_btn = Button(top, text="ADD Data", font="arial", fg="red", bg="pink", command=add_data)
        add_btn.grid(row=3, column=0, columnspan=2, pady=10, padx=10, ipadx=47)

        # label and input field for oid and delete button
        oid_label = Label(top, text="O-ID : ", font="arial")
        oid_label.grid(row=4, column=0, pady=(10, 0))

        oid = Entry(top, width=25, font="arial")
        oid.grid(row=4, column=1, padx=10, pady=(10, 0))

        def delete_data():  # this function is used to delete data from the person_info table
            if oid.get() == "":
                messagebox.showerror("Message", "Please select record \n you want to DELETE")
            else:
                delete(oid.get())
                messagebox.showinfo("Message", "Data Deleted Successfully")
                oid.delete(0)

        delete_btn = Button(top, text="DELETE Data", font="arial", fg="white", bg="purple", command=delete_data)
        delete_btn.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=30)

        def callbackFunc(event):  # this function used to get selected item from the combo box and load into oid i/p box
            """when the item choose from the combobox it load to choice"""
            choice = quality_combo.get()
            choice = int((choice.strip())[0])

            # put the data choose into oid input field
            oid.insert(0, choice)

        def show_data():  # this function used to show data in combo box whenever show button hit
            quality_combo['values'] = ()
            quality_combo['values'] = tuple(show())

            quality_combo.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=30)
            quality_combo.bind("<<ComboboxSelected>>", callbackFunc)  # call callback function when record selected

        # show and exit button
        show_btn = Button(top, text="SHOW DATA", font="arial", fg="red", bg="yellow", command=show_data)
        show_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=(0, 200), ipadx=22)

        def hide_open2():
            root.deiconify()
            top.destroy()

        exit2_btn = Button(top, text="EXIT", font="arial", fg="red", bg="yellow", command=hide_open2)
        exit2_btn.grid(row=6, column=1, columnspan=2, pady=10, padx=(100, 0), ipadx=50)

    except:
        messagebox.showerror("Message", "Error in the open_person database")


person_btn = Button(root, text="Person's Database", font="arial", fg="white", bg="green", padx=80, pady=10,
                     command=open_person_database)
person_btn.pack(pady=10)


# function for attendance from camera
def take_attendance():
    # root.withdraw()
    try:
        mark_attendance()
    except cv2.error:
        messagebox.showerror("Message", "Please check web cam is attached or not \n And try again")


take_attendance_btn = Button(root, text="Take Attendance", font="arial", fg="white", bg="blue", padx=80, pady=10,
                        command=take_attendance)
take_attendance_btn.pack(padx=50, pady=10)


# create new window for person database
def check_attendance_window():
    """ second window for check attendance"""
    try:
        root.withdraw()
        top = Toplevel()
        top.title("Check Attendance")
        top.configure(background='black')

        variable = StringVar(top)
        quality_combo = ttk.Combobox(top, width=27, font="arial", textvariable=variable)

        # label at the top of person database name
        my_label = Label(top, text="person database", font="arial", fg="White", bg="black")
        my_label.grid(row=0, column=1, padx=(0, 90), pady=(10, 0))

        # label and input field for name && Add button
        name_label = Label(top, text="NAME :", font="arial")
        name_label.grid(row=1, column=0, padx=(0, 10), pady=(10, 0))

        name = Entry(top, width=25, font="arial")
        name.grid(row=1, column=1, padx=20, pady=(10, 0))

        # label and input field for path and button right to input field for browsing to img
        date_label = Label(top, text="DATE :", font="arial")
        date_label.grid(row=3, column=0, padx=(0, 10), pady=(10, 0))

        date = Entry(top, width=25, font="arial")
        date.grid(row=3, column=1, padx=(13, 10), pady=(10, 0))

        # show and exit button
        delete_btn = Button(top, text="DELETE DATA", font="arial", fg="black", bg="violet", padx=54,
                            command=lambda: delete_attendance(name.get(), date.get()))
        delete_btn.grid(row=6, column=0, columnspan=2, pady=10)

        def callbackFunc(event):  # this function used to get selected item from the combo box and load into oid i/p box
            """when the item choose from the combobox it load to choice"""
            choice = quality_combo.get()
            choice = int((choice.strip())[0])

            # put the data choose into oid input field
            date.insert(0, choice)
            name.insert(0, choice)

        def check_data():  # this function used to show data in combo box whenever show button hit
            quality_combo['values'] = ()
            if name.get() != "" or date.get() != "":
                quality_combo['values'] = tuple(check_attendance_data(name.get(), date.get()))

                quality_combo.grid(row=5, column=0, columnspan=2, pady=10, padx=10, ipadx=30)
                quality_combo.bind("<<ComboboxSelected>>", callbackFunc)  # call callback function when record selected
            else:
                messagebox.showerror("Message", "PLEASE ENTER THE DATA \n EITHER NAME OR DATE OR BOTH")


        # show and exit button
        show_btn = Button(top, text="SHOW DATA", font="arial", fg="white", bg="blue", padx=60, command=check_data)
        show_btn.grid(row=4, column=0, columnspan=2, pady=10)

        def hide_open2():
            root.deiconify()
            top.destroy()

        # show and exit button
        generate_btn = Button(top, text="GENERATE EXCEL FILE", font="arial", fg="white", bg="blue", padx=5,
                              command=lambda: make_attendace_file(name.get(), date.get()))
        generate_btn.grid(row=7, column=0, columnspan=2, pady=10)

        exit2_btn = Button(top, text="EXIT", font="arial", fg="white", bg="red", padx=97, command=hide_open2)
        exit2_btn.grid(row=8, column=0, columnspan=2, pady=10)

    except:
        messagebox.showerror("Message", "Error in the open_person database")


check_attendance_btn = Button(root, text="Check Attendance", font="arial", fg="white", bg="violet", padx=76, pady=10,
                             command=check_attendance_window)
check_attendance_btn.pack(padx=50, pady=10)

exit_btn = Button(root, text="Exit", command=root.quit, font="arial", fg="white", bg="red", padx=140, pady=10)
exit_btn.pack(padx=50, pady=10)


root.mainloop()

