from tkinter import filedialog as fd 
from tkinter import *
import customtkinter as ct
from customtkinter import *
import pandas as pd
from PIL import Image
import mysql.connector
import csv

window = ct.CTk()
window.geometry("1000x1000")
window.configure(fg_color='#FFFFFF') 
window.title("Elevator")

logo = ct.CTkImage(light_image=Image.open(r"C:\Users\sebas\Downloads\rplogo1.png"), size=(190, 80))
display = ct.CTkLabel(window, text="", image=logo)
display.pack(pady=5) 

nam = ct.CTkLabel(window,text="Ruhrpumpen Elevator Data Engine",text_color="black", font=("Arial", 20))
nam.pack()

frame = ct.CTkFrame(master=window, width=650, height=550, fg_color="#4A90E2", border_color="#000000", border_width=3)
frame.pack(fill='both',expand=True, padx=10, pady=10)

vframe = ct.CTkScrollableFrame(master=frame, width=450, height=200, fg_color="#FFFFFF", border_color="#000000", border_width=3)
vframe.pack(side="right",expand=True, padx=8,pady=6, fill="both")

Title = ct.CTkLabel(frame,text="To convert, select a .xslm file")
Title.pack(anchor='center',padx=5, pady=5)

excel_button = ct.CTkButton(frame, text="Select File")
excel_button.pack(anchor='center',padx=5, pady=5)

nombre_label = ct.CTkLabel(frame, text="File Name: ")
nombre_label.pack(anchor='center',padx=5, pady=5)

nombre_entry = ct.CTkEntry(frame)
nombre_entry.pack(anchor='center',padx=10, pady=10)

save_button = ct.CTkButton(frame, text="Save")
save_button.pack(anchor='center',padx=10, pady=10)

data_connection = ct.CTkButton(frame,text="Connect To Database")
data_connection.pack(anchor='center',padx=10, pady=10)

select_csv_file = ct.CTkButton(frame,text="Select CSV File To Insert")
select_csv_file.pack(anchor='center',padx=10, pady=10)

file_viewers = ct.CTkButton(frame,text="Review other CSVs")
file_viewers.pack(anchor='center',padx=10, pady=10)

file_viewer = ct.CTkButton(frame,text="Review Selected CSV")
file_viewer.pack(anchor='center',padx=10, pady=10)

close_viewer = ct.CTkButton(frame,text="Clean CSV Viewer")
close_viewer.pack(anchor='center',padx=10, pady=10)

inserter = ct.CTkButton(frame,text="Insert Files ")
inserter.pack(anchor='center',padx=10, pady=10)

sys_label = ct.CTkLabel(master=frame, text="System Log", font=("Arial", 16))
sys_label.pack(anchor='center',fill='both',expand=True,pady=5,padx=5)

inner_frame = ct.CTkScrollableFrame(
    master=frame,
    width=280,
    height=280,
    fg_color="#000000",
    border_color="#FFFFFF",
    border_width=3
)
inner_frame.pack(fill='both', padx=5, pady=5, expand=True)

def create_label(parent, text):
    label = ct.CTkLabel(parent, text=text, anchor='w', fg_color="#000000", text_color="#FFFFFF")
    label.pack(fill='x', padx=0, pady=0)
    return label

chosen_file_label = create_label(inner_frame, "")
saved_file_label = create_label(inner_frame, "")
conn_stat = create_label(inner_frame, "")
conn_fail = create_label(inner_frame, "")
chosen_csv = create_label(inner_frame, "")
dbinsert_stat = create_label(inner_frame, "")
dbinsert_fail = create_label(inner_frame, "")
dbwarn = create_label(inner_frame, "")
falpath_lable = create_label(inner_frame, "")
ok_label = create_label(inner_frame, "")
true = create_label(inner_frame, "")
false = create_label(inner_frame, "")
csvstat = create_label(inner_frame, "")

def clear_view():
    global file_select,file_selects
    for widget in vframe.winfo_children():
        widget.destroy()
    file_select = None
    file_selects = None

def select_csv():
    global file_select
    file_select = fd.askopenfilename(
            title="Select an CSV File",
            filetypes=[("CSV Files", "*.csv")], 
    )
    
    chosen_csv.configure(text="Selected File: " + file_select)

def csv_viewer():
    global file_select
    if 'file_select' not in globals() or file_select is None:
        csvstat.configure(text="Cant start Reader Engine, File not Selected")
        return   
    if file_select:
        with open(file_select,mode='r') as file:
            reader = csv.reader(file)
            data = list(reader)
        if data:
            headers = data[0]
        for j, header in enumerate(headers):
            header_label = ct.CTkLabel(vframe, text=header, font=("Arial", 12, "bold"),text_color="black")
            header_label.grid(row=0, column=j, padx=10, pady=5, sticky='nsew')

    # Mostrar los datos de la tabla
        for i, fila in enumerate(data[1:], start=1):
            for j, valor in enumerate(fila):
                cell_label = ct.CTkLabel(vframe, text=valor,text_color="black",)
                cell_label.grid(row=i, column=j, padx=5, pady=5, sticky='nsew')

    # Ajustar el tamaño de las columnas
        for j in range(len(data[0])):
            vframe.grid_columnconfigure(len(headers), weight=2)
    else:
        csvstat.configure(text="Cant start Reader Engine, File not Selected")


def csv_viewers():
    global file_selects

    file_selects = fd.askopenfilename(
            title="Select an CSV File",
            filetypes=[("CSV Files", "*.csv")], 
    )

    if file_selects:
            with open(file_selects,mode='r') as file:
                reader = csv.reader(file)
                data = list(reader)

    if data:
        headers = data[0]
    for j, header in enumerate(headers):
        header_label = ct.CTkLabel(vframe, text=header, font=("Arial", 12, "bold"),text_color="black")
        header_label.grid(row=0, column=j, padx=10, pady=5, sticky='nsew')

    # Mostrar los datos de la tabla
    for i, fila in enumerate(data[1:], start=1):
        for j, valor in enumerate(fila):
            cell_label = ct.CTkLabel(vframe, text=valor,text_color="black",)
            cell_label.grid(row=i, column=j, padx=5, pady=5, sticky='nsew')

    # Ajustar el tamaño de las columnas
    for j in range(len(data[0])):
        vframe.grid_columnconfigure(len(headers), weight=2)
    else:
        csvstat.configure(text="Cant start Reader Engine, File not Selected")

def choose_excel():
    global excel
    excel = fd.askopenfilename(
            title="Select an Excel File",
            filetypes=[("Excel Files", "*.xlsx")],
            
    )
    chosen_file_label.configure(text="Selected File: " + excel)


def dbconn():
    global cursor,connector
    connector = mysql.connector.connect(user='root', password='Focus2009',
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

    # Actualizar el estado de la inserción
    def insertstatus():
        if cursor.rowcount > 0:
            return "Successfully inserted Data"
        else:
            return "Failed to Insert Data"

    dbinsert_stat.configure(text=f"Insertion Status: {insertstatus()}")

def save():
        global nombre, destino
        nombre = nombre_entry.get() + ".csv"
        destino = fd.asksaveasfilename(
            title="Save file as ",
            initialfile=nombre,
        )
        df = pd.read_excel(excel, engine='openpyxl')
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
file_viewer.configure(command=csv_viewer)
file_viewers.configure(command=csv_viewers)
close_viewer.configure(command=clear_view)
inserter.configure(command=insert)

window.mainloop()