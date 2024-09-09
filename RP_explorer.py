from tkinter import filedialog as fd 
from tkinter import *
import customtkinter as ct
import tkinter as tk
from tkinter import ttk
from customtkinter import *
import pandas as pd
from PIL import Image
import mysql.connector
import csv
import base64
from io import BytesIO
import os
from images import logo_source
from images import logo2_source

window = ct.CTk()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f"{screen_width}x{screen_height}+0+0")
window.configure(fg_color='#FFFFFF') 
window.title("Elevator")

logo_frame = ct.CTkFrame(window,fg_color="#FFFFFF")
logo_frame.pack(side='top', fill='x')

logo_deco = base64.b64decode(logo_source)
logo2_deco = base64.b64decode(logo2_source)

logo_fin = Image.open(BytesIO(logo_deco))
logo2_fin = Image.open(BytesIO(logo2_deco))

logo = ct.CTkImage(light_image=logo2_fin, size=(320, 80))
display = ct.CTkLabel(logo_frame, text="", image=logo)
display.pack(side='left', pady=1)

logo2 = ct.CTkImage(light_image=logo_fin, size=(320, 80))
display2 = ct.CTkLabel(logo_frame, text="", image=logo2)
display2.pack(side='right', pady=1)

tabview = ct.CTkTabview(window)
tabview.pack()

tab1 = tabview.add("File Converter")
tab2 = tabview.add("CSV Explorer")
tab3 = tabview.add("Data Insertion")

frame = ct.CTkFrame(master=tab1, width=650, height=20, fg_color="#FFFFFF", border_color="#000000", border_width=3)
frame.pack(fill='both',expand=False, padx=10, pady=10)

framex = ct.CTkFrame(master=tab3, width=650, height=20, fg_color="#FFFFFF", border_color="#000000", border_width=3)
framex.pack(fill='both',expand=False, padx=10, pady=10)

vframe = tk.LabelFrame(master=tab2,text="", width=200, height=650)
vframe.pack(fill="both",expand=True,padx=10, pady=10)

butframe = ct.CTkFrame(vframe,fg_color="#FFFFFF")
butframe.pack(padx=5,pady=5)

tree = ttk.Treeview(vframe)
tree.pack(fill="both", expand=True)

treey = tk.Scrollbar(vframe,orient="vertical",command=tree.yview)
treex = tk.Scrollbar(vframe,orient="horizontal",command=tree.xview)
tree.configure(xscrollcommand=treex.set,yscrollcommand=treey.set)

treey.pack(side="right",fill="y")
treex.pack(side="bottom",fill="x")

Title = ct.CTkLabel(frame,text="To convert, select a Excel Type file",text_color="black")
Title.pack(anchor='center',padx=5, pady=5)

excel_button = ct.CTkButton(frame, text="Select File")
excel_button.pack(anchor='center',padx=5, pady=5)

nombre_label = ct.CTkLabel(frame, text="New File Name: ",text_color="black")
nombre_label.pack(anchor='center',padx=5, pady=5)

nombre_entry = ct.CTkEntry(frame)
nombre_entry.pack(anchor='center',padx=10, pady=10)

save_button = ct.CTkButton(frame, text="Save")
save_button.pack(anchor='center',padx=10, pady=10)

data_connection = ct.CTkButton(framex,text="Connect To Database")
data_connection.pack(anchor='center',padx=10, pady=10)

select_csv_file = ct.CTkButton(framex,text="Select CSV File To Insert")
select_csv_file.pack(anchor='center',padx=10, pady=10)

other_file_viewer = ct.CTkButton(butframe,text="Review CSV")
other_file_viewer.pack(anchor='c')

close_viewer = ct.CTkButton(butframe,text="Clean CSV Viewer")
close_viewer.pack(anchor='c')

inserter = ct.CTkButton(framex,text="Insert Files ")
inserter.pack(anchor='center',padx=10, pady=10)

sys_label = ct.CTkLabel(master=frame, text="System Log", font=("Arial", 16),text_color="black")
sys_label.pack(anchor='center',fill='both',expand=True,pady=5,padx=5)

clear = ct.CTkButton(frame, text="Clear Conversion Log and Release Resources")
clear.pack(anchor='center',padx=10, pady=10)

clear_db = ct.CTkButton(framex, text="Clear Database Log and Release Resources")
clear_db.pack(anchor='center',padx=10, pady=10)

inner_frame = ct.CTkScrollableFrame(
    master=frame,
    width=740,
    height=280,
    fg_color="#000000",
    border_color="#FFFFFF",
    border_width=3
)
inner_frame.pack(fill='both', padx=5, pady=5, expand=True)

inner_frame2 = ct.CTkScrollableFrame(
    master=framex,
    width=740,
    height=280,
    fg_color="#000000",
    border_color="#FFFFFF",
    border_width=3
)
inner_frame2.pack(fill='both', padx=5, pady=5, expand=True)

inner_frame3 = ct.CTkFrame(
    master=butframe,
    width=780,
    height=100,
    fg_color="#000000",
    border_color="#FFFFFF",
    border_width=3
)
inner_frame3.pack(fill='both', padx=1, pady=1, expand=True)

usname = ct.CTkLabel(window,text="Welcome "+os.getlogin(),text_color="black")
usname.pack(anchor='center',padx=5, pady=5)

def create_label(parent, text):
    label = ct.CTkLabel(parent, text=text, anchor='w', fg_color="#000000", text_color="#FFFFFF")
    label.pack(fill='x', padx=0, pady=0)
    return label
def create_label2(parent, text):
    label = ct.CTkLabel(parent, text=text, anchor='w', fg_color="#FFFFFF", text_color="#000000")
    label.pack(fill='x', padx=0, pady=0)
    return label

chosen_file_label = create_label(inner_frame, "")
saved_file_label = create_label(inner_frame, "")

#Database State
chosen_csv = create_label(inner_frame2, "")
dbinsert_stat = create_label(inner_frame2, "")
dbinsert_fail = create_label(inner_frame2, "")
conn_stat = create_label(inner_frame2, "")
conn_fail = create_label(inner_frame2, "")
dbwarn = create_label(inner_frame2, "")

#Conversor State
true = create_label(inner_frame, "")
false = create_label(inner_frame, "")

#CSV Reader
csvstat = create_label2(inner_frame3, "")

def clear_csv_view():
    global file_selects
    file_selects = None
    tree.delete(*tree.get_children())
    tree["columns"] = ()
    tree["show"] = ""
    csvstat.configure(text="")

    for widget in inner_frame3.winfo_children():
        widget.configure(text="")

def clear_conv_log():
    global excel        
    excel = None
    chosen_file_label.configure(text="")
    true.configure(text="")
    false.configure(text="")
    saved_file_label.configure(text="") 

def clear_db_details():
    global file_select
    file_select = None
    for widget in inner_frame2.winfo_children():
        widget.configure(text="")
    

def select_csv(): #Elegit CSV para Insertar a Base de Datos
    global file_select
    file_select = fd.askopenfilename(
            title="Select a CSV File To Insert",
            filetypes=[("CSV Files", "*.csv")], 
    )
    
    if file_select != "":
        chosen_csv.configure(text="Selected File: " + file_select)
    elif file_select == "":
        chosen_csv.configure(text="No File Selected")
    

def other_csv_viewers(): #Abrir cualquier Otro CSV en el visor construido
    global file_selects

    file_selects = fd.askopenfilename(
            title="Select an CSV File",
            filetypes=[("CSV Files", "*.csv")], 
    )
    filename = os.path.basename(file_selects)

    if file_selects:
        path = file_selects
        try:
            df = pd.read_csv(path)
            csvstat.configure(text="Now viewing: "+filename)
        except ValueError:
            tk.messagebox.showerror("Warning, wrong file type")
            return None
        except FileNotFoundError:
            tk.messagebox.showerror("Warning, file does not exist")
            return None

        tree["column"] = list(df.columns)
        tree["show"] = "headings"
        for column in tree["columns"]:
            tree.heading(column, text=column)

        df_row = df.to_numpy().tolist()

        for row in df_row:
            tree.insert("","end",values=row)
        return None
    else:
        csvstat.configure(text="Cant start Reader Engine, File not Selected")

def choose_excel():
    global excel
    excel = fd.askopenfilename(
            title="Select an Excel File",
            filetypes=[("Excel Files", "*.xlsx")],
    )
    filename = os.path.basename(excel)
    if excel != "":
        chosen_file_label.configure(text="Selected File: " + filename)
    elif excel == "":
        chosen_file_label.configure(text="No File Selected")
        excel = None

def dbconn():
    global cursor,connector
    connector = mysql.connector.connect(user='root', password='FireSystems25',
                                 host='127.0.0.1',
                                 database='rp',
                                 use_pure=True,
                                 allow_local_infile=True,
                                 ssl_disabled=True)
    def status():
        if connector.is_connected() == True:
            return "Connection established"
        elif connector.is_connected() == False:
            return "Connection attempt failed"
    cursor = connector.cursor()
    conn_stat.configure(text=f"Connection Status: {status()}")

def insert():
    global cursor, connector, file_select
    if 'connector' not in globals() or connector is None:
        conn_fail.configure(text="Not connected to Database, connect to continue")
        return   
    if 'file_select' not in globals() or file_select is None:
        dbinsert_fail.configure(text="File not selected, unable to insert data")
        return
    else:
        csv_file_path2 = file_select
        with open(csv_file_path2, mode='r') as csvfile:
                reader = csv.reader(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                next(reader) 
                for row in reader:
                    cursor.execute("INSERT INTO pumps (Company,Flow,Head,Pump_Speed_in_RPM,Max_BHP,Pump_Model,Line,Stages,Pump_Size) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s)", (row[0], row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8]))
        connector.commit()

    def insertstatus():
        if cursor.rowcount > 0:
            return "Successfully inserted Data"
        else:
            return "No Data Was Inserted"

    dbinsert_stat.configure(text=f"Insertion Status: {insertstatus()}")

def save():
        global nombre, destino
        nombre = nombre_entry.get()
        destino = fd.asksaveasfilename(
            title="Save file as ",
            initialfile=nombre,
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")] 
        )
        df = pd.read_excel(excel, engine='openpyxl')

        if not destino.lower().endswith('.csv'):
            destino += '.csv'
        try:
            df.to_csv(destino, index=False)
        except FileNotFoundError:
            false.configure(text="Error, Could not convert file, please try again")
        else:
            true.configure(text="Success, File was converted successfully, the saved path is on screen")

        saved_file_label.configure(text="Saved File at: " + destino) 

excel_button.configure(command=choose_excel)
save_button.configure(command=save)
data_connection.configure(command=dbconn)
select_csv_file.configure(command=select_csv)
other_file_viewer.configure(command=other_csv_viewers)
close_viewer.configure(command=clear_csv_view)
clear.configure(command=clear_conv_log)
clear_db.configure(command=clear_db_details)
inserter.configure(command=insert)

window.mainloop()