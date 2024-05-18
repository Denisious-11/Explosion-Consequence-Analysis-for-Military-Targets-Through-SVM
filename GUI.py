from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter.filedialog import askopenfilename
import cv2 as cv
import numpy as np
a = Tk()
a.title("Damage Level Predict")
a.geometry("1000x650")


def prediction(var, e_var1, e_var2, e_var3):

    import pandas as pd
    import joblib
    load_model = joblib.load(
        "Project_Saved_Models/pipeline_svm_model_85acc.sav")

    info = []
    parameters = ['Target Type',
                  'TNT Equivalent(Kg)', 'Range(m)', 'Blast Overpressure']
    Target_Type = var.get()
    TNT_Equivalent = e_var1.get()
    Range = e_var2.get()
    Blast_Overpressure = e_var3.get()

    if Target_Type == 'Select' or TNT_Equivalent == '' or Range == '' or Blast_Overpressure == '':
        message.set("fill the empty field!!!")
    else:
        list_box.insert(1, "Loading Values")
        list_box.insert(2, "")
        list_box.insert(3, "Loading Model")
        list_box.insert(4, "")
        list_box.insert(5, "Prediction")
        message.set("")
        print(Target_Type)
        print(type(Target_Type))
        if Target_Type == 'Light Armour':
            my_Target_Type = 1
        elif Target_Type == 'Heavy Armour':
            my_Target_Type = 2
        elif Target_Type == 'Troops in Open Field':
            my_Target_Type = 3
        elif Target_Type == 'Troops in Bunkers':
            my_Target_Type = 4
        elif Target_Type == 'Parked Aircraft':
            my_Target_Type = 5
        print(my_Target_Type)
        info.append(my_Target_Type)

        TNT_Equivalent = int(TNT_Equivalent)
        print(TNT_Equivalent)
        print(type(TNT_Equivalent))
        info.append(TNT_Equivalent)

        Range = int(Range)
        print(Range)
        print(type(Range))
        info.append(Range)

        Blast_Overpressure = float(Blast_Overpressure)
        print(Blast_Overpressure)
        print(type(Blast_Overpressure))
        info.append(Blast_Overpressure)

        my_dict = dict(zip(parameters, info))

        # convert dict into dataframe
        my_data = pd.DataFrame(my_dict, index=[0])

        # dataframe is putting into the MODEL to make PREDICTION
        my_pred = load_model.predict(my_data)
        print(my_pred)

        my_pred = my_pred[0]
        print(my_pred)

        print("\n")
        print("RESULT:")
        if my_pred == 0:
            a = "LOW"
            print("LOW")
        if my_pred == 1:
            a = "MODERATE"
            print("MODERATE")
        if my_pred == 2:
            a = "HEAVY"
            print("HEAVY")
        out_label.config(text="Output : "+a)


def Check():
    global f
    f.pack_forget()

    f = Frame(a, bg="white")
    f.pack(side="top", fill="both", expand=True)

    global f1
    f1 = Frame(f, bg="light blue")
    f1.place(x=0, y=0, width=760, height=400)
    f1.config()

    input_label = Label(f1, text="Input", font="arial 16", bg="light blue")
    input_label.pack(padx=0, pady=10)

    label1 = Label(f1, text="Target Type :", font="arial 12", bg="light blue")
    label1.place(x=130, y=80)
    label2 = Label(f1, text="TNT Equivalent(Kg) :",
                   font="arial 12", bg="light blue")
    label2.place(x=130, y=130)
    label3 = Label(f1, text="Range(m) :", font="arial 12", bg="light blue")
    label3.place(x=130, y=170)
    label4 = Label(f1, text="Blast Overpressure Value :",
                   font="arial 12", bg="light blue")
    label4.place(x=130, y=210)

    var = StringVar()
    var.set("Select")
    options = ["Light Armour", "Heavy Armour",
               "Troops in Open Field", "Troops in Bunkers", "Parked Aircraft"]
    op1 = OptionMenu(f1, var, *options)
    op1.place(x=330, y=80)

    global message
    e_var1 = StringVar()
    e_var2 = StringVar()
    e_var3 = StringVar()
    message = StringVar()

    entry1 = Entry(f1, textvariable=e_var1, bd=2, width=25)
    entry1.place(x=330, y=130)
    entry2 = Entry(f1, textvariable=e_var2, bd=2, width=25)
    entry2.place(x=330, y=170)
    entry3 = Entry(f1, textvariable=e_var3, bd=2, width=25)
    entry3.place(x=330, y=210)

    msg_label = Label(f1, text="", textvariable=message,
                      bg='light blue').place(x=330, y=240)

    predict_button = Button(
        f1, text="Predict", command=lambda: prediction(var, e_var1, e_var2, e_var3), bg="deepskyblue")
    predict_button.pack(side="bottom", pady=100)
    global f2
    f2 = Frame(f, bg="light green")
    f2.place(x=0, y=400, width=760, height=250)
    f2.config(pady=20)

    result_label = Label(f2, text="RESULT", font="arial 16", bg="light green")
    result_label.pack(padx=0, pady=0)

    global out_label
    out_label = Label(f2, text="", bg="light green", font="arial 16")
    out_label.pack(pady=30)

    f3 = Frame(f, bg="mistyrose")
    f3.place(x=760, y=0, width=240, height=690)
    f3.config()

    name_label = Label(f3, text="Process", font="arial 14", bg="mistyrose")
    name_label.pack(pady=20)

    global list_box
    list_box = Listbox(f3, height=12, width=31)
    list_box.pack()


def Home():
    global f
    f.pack_forget()

    f = Frame(a, bg="light sky blue")
    f.pack(side="top", fill="both", expand=True)

    home_label = Label(f, text="Damage Level Predictor",
                       font="arial 35", bg="light sky blue")
    home_label.place(x=250, y=250)


f = Frame(a, bg="light sky blue")
f.pack(side="top", fill="both", expand=True)

home_label = Label(f, text="Damage Level Predictor",
                   font="arial 35", bg="light sky blue")
home_label.place(x=250, y=250)

m = Menu(a)
m.add_command(label="Home", command=Home)
checkmenu = Menu(m)
m.add_command(label="Check", command=Check)
a.config(menu=m)


a.mainloop()
