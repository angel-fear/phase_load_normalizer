from lib import *
from tkinter import *
from tkinter import messagebox
import xlsxwriter
import time

# ---------------------------- GLOBAL & CONSTANTS --------------------------- #
list_1 = []
list_3 = []
BACKGROUND_COLOR = "#c6ebc9"


# ------------------------- EXPORT REPORT TO .XLSX -------------------------- #
def save_report(a_list, b_list, c_list, uneven_value):
    global list_3

    # Generate file name for .xlsx report
    timestamp = time.localtime()
    time_string = time.strftime("%d%m%Y_%H%M%S", timestamp)
    filename = f'reports/report_{time_string}.xlsx'

    # Open workbook and worksheet
    save_fl = True
    try:
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
    except:
        messagebox.showinfo("Error", "Cannot create report file")
        save_fl = False

    # Formatting list
    a_header = workbook.add_format({'bold': True, 'align': 'center', 'border': True, 'fg_color': 'yellow'})
    b_header = workbook.add_format({'bold': True, 'align': 'center', 'border': True, 'fg_color': 'green'})
    c_header = workbook.add_format({'bold': True, 'align': 'center', 'border': True, 'fg_color': 'red'})
    data = workbook.add_format({'bold': False, 'align': 'center', 'border': True})
    merge_format = workbook.add_format({
        'bold': True, 'border': True,
        'align': 'center', 'valign': 'vcenter',
        'fg_color': 'silver'})
    percent_format = workbook.add_format({
        'bold': True, 'border': True,
        'align': 'center', 'valign': 'vcenter',
        'fg_color': 'silver', 'num_format': '0.000%'})

    # Output headers of table
    worksheet.write('A1', 'A', a_header)
    worksheet.write('B1', 'B', b_header)
    worksheet.write('C1', 'C', c_header)
    worksheet.set_column('A:C', 15)

    # Output three-phases loads if exist
    row_after = len(list_3)
    if row_after > 0:
        for r in range(row_after):
            if a_list[r] != 0:
                worksheet.merge_range(f'A{r + 2}:C{r + 2}', a_list[r], merge_format)

    # Output A-phase column
    row, col = row_after + 1, 0
    for i in range(len(a_list) - row_after):
        if a_list[i + row_after] != 0:
            worksheet.write(row, col, a_list[i + row_after], data)
            row += 1
    a_row = row

    # Output B-phase column
    row, col = row_after + 1, 1
    for i in range(len(b_list) - row_after):
        if b_list[i + row_after] != 0:
            worksheet.write(row, col, b_list[i + row_after], data)
            row += 1
    b_row = row

    # Output C-phase column
    row, col = row_after + 1, 2
    for i in range(len(c_list) - row_after):
        if c_list[i + row_after] != 0:
            worksheet.write(row, col, c_list[i + row_after], data)
            row += 1
    c_row = row

    # Calculate bottom line number
    uneven_row = max(a_row, b_row, c_row) + 2
    worksheet.merge_range(f'A{uneven_row}:B{uneven_row}', 'Max uneven of phases loading', merge_format)
    worksheet.write(f'C{uneven_row}', uneven_value, percent_format)

    # Close .xlsx file
    try:
        workbook.close()
    except:
        messagebox.showinfo("Error", "Cannot create report file")
        save_fl = False
    if save_fl:
        messagebox.showinfo("Report export", f"Report saved to {filename}")


# ------------------------- CREATE A REPORT COMMAND ------------------------- #
def create_report():
    global list_1, list_3
    fl = True

    try:
        list_1 = [float(value) for value in entry_input_list_1.get().split()]
    except ValueError:
        messagebox.showinfo("Error", "Invalid value in single phase loads data")
        fl = False
    try:
        list_3 = [float(value) for value in entry_input_list_3.get().split()]
    except ValueError:
        messagebox.showinfo("Error", "Invalid value in three phase loads data")
        fl = False
    if len(list_1) == 0 and len(list_3) == 0:
        fl = False
    if fl:
        start_calc()


# ---------------------------- BASIC CALCULATION ---------------------------- #
def start_calc():
    global list_1, list_3
    num_of_loads = len(list_1)
    init_input = list_1.copy()
    loads_ph_a = [0] * num_of_loads
    loads_ph_b = [0] * num_of_loads
    loads_ph_c = [0] * num_of_loads

    # Sorting Input Data by descending
    sorted_input = sorted(init_input, reverse=True)

    # Put Max value in minimum loaded phase
    while sum(sorted_input):
        move_load_to_min_loaded_phase(loads_ph_a, loads_ph_b, loads_ph_c, sorted_input)
        move_load_to_min_loaded_phase(loads_ph_b, loads_ph_a, loads_ph_c, sorted_input)
        move_load_to_min_loaded_phase(loads_ph_c, loads_ph_a, loads_ph_b, sorted_input)

    # Try achieve better results by flip near values
    for i in range(3, num_of_loads - 1):
        sum_ph_a, sum_ph_b, sum_ph_c = get_sum_per_phase(loads_ph_a, loads_ph_b, loads_ph_c)
        max_in, min_in = get_max_and_min_per_phase(sum_ph_a, sum_ph_b, sum_ph_c)
        delta1 = max_in - min_in
        flip_near_phase(loads_ph_a, loads_ph_b, loads_ph_c, i)
        sum_ph_a, sum_ph_b, sum_ph_c = get_sum_per_phase(loads_ph_a, loads_ph_b, loads_ph_c)
        max_in, min_in = get_max_and_min_per_phase(sum_ph_a, sum_ph_b, sum_ph_c)
        delta2 = max_in - min_in
        if delta2 < delta1:
            continue
        else:
            flip_near_phase(loads_ph_a, loads_ph_b, loads_ph_c, i)

    # Restore original sequence of elements (not sorted)
    restore(loads_ph_a, init_input, num_of_loads)
    restore(loads_ph_b, init_input, num_of_loads)
    restore(loads_ph_c, init_input, num_of_loads)

    # Add three-phase loads to the calculation
    loads_ph_a = list_3 + loads_ph_a
    loads_ph_b = list_3 + loads_ph_b
    loads_ph_c = list_3 + loads_ph_c
    sum_ph_a, sum_ph_b, sum_ph_c = get_sum_per_phase(loads_ph_a, loads_ph_b, loads_ph_c)
    max_in, min_in = get_max_and_min_per_phase(sum_ph_a, sum_ph_b, sum_ph_c)

    # Calculate uneven of phases and save report to .xlsx file
    uneven_value = (max_in - min_in) / max_in
    save_report(loads_ph_a, loads_ph_b, loads_ph_c, uneven_value)


# --------------------------------- UI SETUP -------------------------------- #
window = Tk()
window.title("Phase load normalizer")
window.iconbitmap("images/PLN.ico")
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR, highlightthickness=0)

canvas = Canvas(width=600, height=400, bg=BACKGROUND_COLOR, highlightthickness=0)

background_img = PhotoImage(file="images/background.png")
canvas.create_image(300, 200, image=background_img)
canvas.grid(row=0, column=0, columnspan=2)

label_input_list_1 = Label(text="Digits, space and dot allowed.", font=('Arial', 9, 'bold'), bg=BACKGROUND_COLOR)
label_input_list_1.grid(column=0, row=1, columnspan=2)

label_input_list_1 = Label(text="Input single phase loads here: ", font=('Arial', 11, 'normal'), bg=BACKGROUND_COLOR)
label_input_list_1.grid(column=0, row=2, columnspan=2)

label_input_list_3 = Label(text="Input three phase loads here: ", font=('Arial', 11, 'normal'), bg=BACKGROUND_COLOR)
label_input_list_3.grid(column=0, row=4, columnspan=2)

entry_input_list_1 = Entry(window, width=90, bd=3)
val_command = (entry_input_list_1.register(callback))
entry_input_list_1.config(validate='all', validatecommand=(val_command, '%P'))
entry_input_list_1.grid(column=0, row=3, columnspan=2)

entry_input_list_3 = Entry(window, width=90, bd=3)
val_command = (entry_input_list_3.register(callback))
entry_input_list_3.config(validate='all', validatecommand=(val_command, '%P'))
entry_input_list_3.grid(column=0, row=5, columnspan=2)

button_img = PhotoImage(file='images/button.png')
report_button = Button(image=button_img, highlightthickness=0, command=create_report,
                       bd=0, bg=BACKGROUND_COLOR, activebackground=BACKGROUND_COLOR)
report_button.grid(column=0, row=6, columnspan=2)

entry_input_list_1.focus()

window.mainloop()
