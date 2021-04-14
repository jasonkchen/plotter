# This code creates a GUI that allows a user to plot data quickly and on
# more than one y-axis if needed.

# PRE-REQUISITES:
# (1) Need XLSX file that can be read by the Pandas Python library

# RELEASE NOTES
#
# Rev A: 04/2021: Initial Release

# To Do:
# (1) Allow for 3 y axis
# (2) If primary y axis is checked, deselected secondary y axis checkbox

import tkinter as tk
import csv
import pandas as pd
import matplotlib.pyplot as plt

# Create GUI Window
window = tk.Tk()
window.title("Data Plotter")

#---User Entries----------------------------------------------------------------
headers = ["Data File", "Plot Title", "X-Axis Label", "Primary Y-Axis Label",\
           "Secondary Y-Axis Label"]
for a in range(len(headers)):
    dataFile_lbl = tk.Label(window,
                            text=headers[a])
    dataFile_lbl.grid(column=0, row=a)

dataFile_entry = tk.Entry(window,width=20)
dataFile_entry.grid(column=1, row=0)

title_entry = tk.Entry(window)
title_entry.grid(column=1, row=1)

x_label_entry = tk.Entry(window)
x_label_entry.grid(column=1, row=2)

y_pri_label_entry = tk.Entry(window)
y_pri_label_entry.grid(column=1, row=3)

y_sec_label_entry = tk.Entry(window)
y_sec_label_entry.grid(column=1, row=4)

#---Load Data-------------------------------------------------------------------
headers = ["#", "Name", "X-Axis", "Primary Y-Axis", "Secondary Y-Axis"]
for a in range(len(headers)):
    header_lbl = tk.Label(window,
                          text = headers[a],
                          width=15,
                          font=("Segoe UI",9, "bold"))
    header_lbl.grid(column=a, row=5)

# Load button
def load():
    # Assign global variables to be used outside of this function
    global x_var_list, pri_y_var_list, sec_y_var_list, datafile_df, col_names_list

    # Find XLSX file
    try:
        datafile_df = pd.read_excel(dataFile_entry.get())
    except FileNotFoundError:
        notfound_lbl = tk.Label(window,
                                text = "File Not Found")
        notfound_lbl.grid(column=2, row=0)
    except AssertionError:
        notfound_lbl = tk.Label(window,
                                text = "File Not Found")
        notfound_lbl.grid(column=2, row=0)    

    # Set up table of numbering, names, and checkboxes
    col_names_list = list(datafile_df.columns)
    dataRows = len(col_names_list)
    x_var_list = [0] * dataRows
    pri_y_var_list = [0] * dataRows
    sec_y_var_list = [0] * dataRows

    for a in range(dataRows):
        # Numbering
        number_lbl = tk.Label(window,
                              text=a+1)
        number_lbl.grid(column=0, row=a+6)                                
        
        # Names
        name_lbl = tk.Label(window,
                            text=col_names_list[a])
        name_lbl.grid(column=1, row=a+6)
        
        # X-axis checkboxes
        x_var_list[a] = tk.IntVar()
        x_chkbx = tk.Checkbutton(window,
                                    variable=x_var_list[a],
                                    onvalue=1,
                                    offvalue=0,
                                    width=5)
        x_chkbx.grid(column=2, row=a+6)    

        # Primary y-axis checkboxes
        pri_y_var_list[a] = tk.IntVar()
        primary_chkbx = tk.Checkbutton(window,
                                    variable=pri_y_var_list[a],
                                    onvalue=1,
                                    offvalue=0,
                                    width=5)
        primary_chkbx.grid(column=3, row=a+6)

        # Secondary y-axis checkboxes
        sec_y_var_list[a] = tk.IntVar()
        secondary_chkbx = tk.Checkbutton(window,
                                    variable=sec_y_var_list[a],
                                    onvalue=1,
                                    offvalue=0,
                                    width=5)
        secondary_chkbx.grid(column=4, row=a+6)

plot_btn = tk.Button(window, text = "Load Data", command = load)
plot_btn.grid(column=3, row=0, ipadx=10)

#---Plot------------------------------------------------------------------------
def plot():
    # Get lists of the checkboxes where 0 = unchecked, 1 = checked
    x_list = []
    y_pri_list = []
    y_sec_list = []
    for a in range(len(x_var_list)):
        x_list.append(x_var_list[a].get())
        y_pri_list.append(pri_y_var_list[a].get())
        y_sec_list.append(sec_y_var_list[a].get())

    x_plot_list = []
    y_pri_plot_list = []
    y_sec_plot_list = []
    
    for a in range(len(x_list)):
        # Find name of x values to plot
        if x_list[a] == 1:
            x_plot_list = col_names_list[a]

        # Find names of y values to plot on primary y axis:
        if y_pri_list[a] == 1:
            y_pri_plot_list.append(col_names_list[a]) 

        # Find names of y values to plot on secondary y axis:
        if y_sec_list[a] == 1:
            y_sec_plot_list.append(col_names_list[a])

    print(f"X names to plot: {x_plot_list}")
    print(f"Y names to plot on primary y: {y_pri_plot_list}")
    print(f"Y names to plot on secondary y: {y_sec_plot_list}")

    # Plot data
    ax = datafile_df.plot(x = x_plot_list, y = y_pri_plot_list)

    if 1 in y_sec_list:
        # If no secondary y-axis is checked, skip this
        ax2 = datafile_df.plot(x = x_plot_list, y = y_sec_plot_list, secondary_y = True, ax=ax)
        ax2.set_ylabel(y_sec_label_entry.get())      

    plt.title(title_entry.get())
    ax.set_xlabel(x_label_entry.get())
    ax.set_ylabel(y_pri_label_entry.get())

    plt.show()
    
plot_btn = tk.Button(window, text = "Plot Data", command = plot)
plot_btn.grid(column=4, row=0, ipadx=15)

#---Quit------------------------------------------------------------------------
def quit():
    window.destroy()

exit_btn = tk.Button(window, text = "Exit GUI", command = quit)
exit_btn.grid(column=5, row=0, ipadx=20)


# Must include this or nothing will be displayed
window.mainloop()
