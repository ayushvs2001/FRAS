from person_database import *
from mark_attendance import mark_attendance
from check_attendance import check_attendance_data, delete_attendance, make_attendace_file
from tkinter import *
from tkinter import ttk
from tkcalendar import DateEntry
from tkinter import messagebox
from tkinter import filedialog
import cv2
import face_recognition
import re

# We creating the tkinter object, So that root window appear, when we execute this program
root = Tk()
root.configure(background='black')
root.title("FACE RECOGNITION + ATTENDANCE PROJECT-")
root.iconbitmap("photos/FACE_RECO.ico")

# set image in window
file = PhotoImage(file='photos/face_reco_.png')
headingIcon = Label(root, image=file)
headingIcon.pack(side=TOP, pady=10)


# create new window for person database
def open_person_database():
    """ second window for person database """
    try:
        root.withdraw()
        top = Toplevel()
        top.title("PERSON DATABASE")
        top.configure(background='black')

        variable = StringVar(top)
        quality_combo = ttk.Combobox(top, width=27, font="arial", textvariable=variable)

        # label at the top of person database name
        my_label = Label(top, text="PERSON DATABASE", font="arial", fg="blue", bg="cyan")
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
                name.delete(0, len(name.get()))  # delete the name in name input filled after hitting the add button
                path_name.delete(0, len(path_name.get()))

        add_btn = Button(top, text="ADD Data", font="arial", fg="red", bg="pink", command=add_data)
        add_btn.grid(row=3, column=0, columnspan=2, pady=10, padx=10, ipadx=47)

        # label and input field for oid and delete button
        oid_label = Label(top, text="P-ID : ", font="arial")
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

        def callback_func(event):  # this function get selected item from the combo box and load into oid i/p box
            """when the item choose from the combobox it load to choice"""
            choice = quality_combo.get()
            choice = int((choice.strip())[0])

            # put the data choose into oid input field
            oid.insert(0, choice)

        def show_data():  # this function used to show data in combo box whenever show button hit
            quality_combo['values'] = ()
            quality_combo['values'] = tuple(show())

            quality_combo.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=30)
            quality_combo.bind("<<ComboboxSelected>>", callback_func)  # call callback function when record selected

        # show and exit button
        show_btn = Button(top, text="SHOW DATA", font="arial", fg="red", bg="yellow", command=show_data)
        show_btn.grid(row=6, column=0, columnspan=2, pady=10, padx=(0, 200), ipadx=22)

        def hide_open2():
            root.deiconify()
            top.destroy()

        exit2_btn = Button(top, text="EXIT", font="arial", fg="blue", bg="red", command=hide_open2)
        exit2_btn.grid(row=6, column=1, columnspan=2, pady=10, padx=(100, 0), ipadx=50)

    except:
        messagebox.showerror("Message", "Error in the open_person database")


file_database = PhotoImage(file="photos/database.png")
person_btn = Button(root, text="Person's Database", image=file_database, compound=LEFT, font=("arial", 15, "bold"),
                    fg="white", bg="green",
                    command=open_person_database)
person_btn.pack(padx=40, pady=10, ipady=3, ipadx=36)


# function for attendance from camera
def take_attendance():
    # root.withdraw()
    try:
        mark_attendance()
    except cv2.error:
        messagebox.showerror("Message", "Please check web cam is attached or not \n And try again")


file_web_camera = PhotoImage(file="photos/web_camera.png")
take_attendance_btn = Button(root, text="Take Attendance", image=file_web_camera, compound=LEFT,
                             font=("arial", 15, "bold"), fg="white", bg="blue",
                             command=take_attendance)
take_attendance_btn.pack(padx=30, pady=(10, 10), ipady=3, ipadx=40)


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
        my_label = Label(top, text="CHECK DATABASE", font="arial", fg="blue", bg="cyan")
        my_label.grid(row=0, column=1, columnspan=3, padx=(0, 90), pady=(10, 0))

        # label and input field for name && Add button
        name_label = Label(top, text="Name :", font="arial")
        name_label.grid(row=1, column=0, padx=(0, 10), pady=(10, 0))

        name = Entry(top, width=25, font="arial")
        name.grid(row=1, column=1, padx=20, pady=(10, 0))

        start_date_label = Label(top, text="Start Date :", font="arial")
        start_date_label.grid(row=3, column=0, padx=(0, 10), pady=(10, 0))

        start_date = DateEntry(top, width=15, bg="darkblue", fg="white", font="arial", year=2021)
        start_date.grid(row=3, column=1, padx=(13, 10), pady=(10, 0))

        end_date_label = Label(top, text="End Date :", font="arial")
        end_date_label.grid(row=3, column=3, padx=(0, 10), pady=(10, 0))

        end_date = DateEntry(top, width=15, bg="darkblue", fg="white", font="arial", year=2021)
        end_date.grid(row=3, column=4, padx=(13, 10), pady=(10, 0))

        start_time_label = Label(top, text="Start Time :", font="arial")
        start_time_label.grid(row=4, column=0, padx=(0, 10), pady=(10, 0))

        hour_option = [x for x in range(0, 24)]
        minute_option = [x for x in range(0, 60)]

        # Setup for starting hour and starting minute
        start_hour_default = StringVar(top)
        start_hour_default.set(0)

        start_hour_label = Label(top, text="Choose Hour :", font="arial")
        start_hour_label.grid(row=4, column=1, padx=(0, 10), pady=(10, 0))

        start_hour = OptionMenu(top, start_hour_default, *hour_option)
        start_hour.grid(row=4, column=2, padx=(13, 10), pady=(10, 0))

        start_min_default = StringVar(top)
        start_min_default.set(0)

        start_minute_label = Label(top, text="Choose Minute :", font="arial")
        start_minute_label.grid(row=5, column=1, padx=(0, 10), pady=(10, 0))

        start_min = OptionMenu(top, start_min_default, *minute_option)
        start_min.grid(row=5, column=2, padx=(13, 10), pady=(10, 0))

        # Setup for ending hour and minute

        end_time_label = Label(top, text="End Time :", font="arial")
        end_time_label.grid(row=6, column=0, padx=(0, 10), pady=(10, 0))

        end_hour_default = StringVar(top)
        end_hour_default.set(23)

        end_hour_label = Label(top, text="Choose Hour :", font="arial")
        end_hour_label.grid(row=6, column=1, padx=(0, 10), pady=(10, 0))

        end_hour = OptionMenu(top, end_hour_default, *hour_option)
        end_hour.grid(row=6, column=2, padx=(13, 10), pady=(10, 0))

        end_min_default = StringVar(top)
        end_min_default.set(59)

        end_minute_label = Label(top, text="Choose Minute :", font="arial")
        end_minute_label.grid(row=7, column=1, padx=(0, 10), pady=(10, 0))

        end_min = OptionMenu(top, end_min_default, *minute_option)
        end_min.grid(row=7, column=2, padx=(13, 10), pady=(10, 0))

        ######## input list ########
        input_values = []

        def refresh():
            flag = bool(re.search(r"^\d{1,2}[-/]\d{1,2}[-/]\d{2,4}$", start_date.get())) and \
                   bool(re.search(r"^\d{1,2}[-/]\d{1,2}[-/]\d{2,4}$", end_date.get()))

            if flag:
                return True
            else:
                return False

        # show and exit button
        delete_btn = Button(top, text="DELETE DATA", font="arial", fg="black", bg="violet", padx=54,
                            command=lambda: refresh() and delete_attendance(
                                [name.get(), start_date.get(), end_date.get(), start_hour_default.get(),
                                 start_min_default.get(), end_hour_default.get(), end_min_default.get()]))
        delete_btn.grid(row=10, column=2, columnspan=3)

        def callback_func(event):  # this function give the all entries satisfies the conditions
            """ when the item choose from the combobox it load to choice"""
            choice = quality_combo.get()
            choice = choice.split()

            # put the data choose into oid input field
            name.delete(0, "end")
            name.insert(0, choice[0])

        def check_data():  # this function used to show data in combo box whenever show button hit
            quality_combo['values'] = ()

            if refresh():
                quality_combo['values'] = tuple(check_attendance_data([name.get(), start_date.get(),
                                                                       end_date.get(), start_hour_default.get(),
                                                                       start_min_default.get(), end_hour_default.get(),
                                                                       end_min_default.get()]))
                quality_combo.grid(row=9, column=0, columnspan=2, pady=10, padx=10, ipadx=30)
                quality_combo.bind("<<ComboboxSelected>>", callback_func)  # call callback function when record selected

            else:
                messagebox.showerror("Message", "PLEASE ENTER THE DATA PROPERLY")

        # show and exit button
        show_btn = Button(top, text="SHOW DATA", font="arial", fg="white", bg="blue", padx=60, command=check_data)
        show_btn.grid(row=10, column=0, columnspan=2, pady=10)

        def hide_open2():
            root.deiconify()
            top.destroy()

        # data generator button
        generate_btn = Button(top, text="GENERATE EXCEL FILE", font="arial", fg="blue", bg="cyan", padx=5,
                              command=lambda: refresh() and make_attendace_file([name.get(), start_date.get(),
                                                                                 end_date.get(),
                                                                                 start_hour_default.get(),
                                                                                 start_min_default.get(),
                                                                                 end_hour_default.get(),
                                                                                 end_min_default.get()]))
        generate_btn.grid(row=11, column=0, columnspan=2, pady=10)

        exit2_btn = Button(top, text="EXIT", font="arial", fg="white", bg="red", padx=97, command=hide_open2)
        exit2_btn.grid(row=11, column=2, columnspan=3, pady=10)

    except Exception as e:
        messagebox.showerror("Message", f"Error in the open person database \n {e}")


file_camera = PhotoImage(file="photos/attendance.png")
check_attendance_btn = Button(root, text="Check Attendance", image=file_camera, compound=LEFT,
                              font=("arial", 15, "bold"), fg="blue", bg="violet",
                              command=check_attendance_window)
check_attendance_btn.pack(padx=30, pady=10, ipadx=40, ipady=3)

file_delete = PhotoImage(file="photos/delete.png")
exit_btn = Button(root, text="Exit", image=file_delete, compound=LEFT, command=root.quit, font=("arial", 15, "bold"),
                  fg="white", bg="red")
exit_btn.pack(padx=50, pady=(10, 10), ipadx=105, ipady=3)

root.mainloop()
