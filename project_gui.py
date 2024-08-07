import tkinter as tk
from tkinter import *
import project
import re

def data_validation(x):
    reee = re.compile(r'100|\d{1,2}')
    print(reee.match(x).group())
    if reee.match(x).group()==x :
        print('Valid Input')
        return True
    else:
        print('Invalid input, write a percentage between 1 and 100')
        return False

def on_submit(event=None):
    scale_value = scale_entry.get()
    print(f"Entered Scale:{scale_value}")
    if data_validation(scale_value):
        project.gui_f = int(scale_value)/100
        # print(project.gui_f)
        project.core_func(project.gui_f)
    else:
        scale_entry.delete(0, tk.END)

#Main window + title
root = tk.Tk()
root.title("Veikk Screen Area Changer")
root.geometry('350x75+800+440')
root.iconbitmap('icon.ico')

#Adding a frame with padding
theme = '#cef564'
mainframe = tk.Frame(root, padx=10, pady=20)
mainframe.configure(background=theme)

#makr frame/grid expand, can't see green colour without this.
mainframe.grid(column=0, row=0, sticky=(W,E,N,S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#Creating the scale Entry (widget)
label = tk.Label(mainframe,text='Scale:',background=theme,font=('Impact',14))
label.grid(column=0,row=1,sticky=(E),padx=5)
#---------------------------------------------------------------------------
#Entry Text Box
scale = StringVar()
scale_entry = tk.Entry(mainframe,width=4, textvariable=scale, bg='white', fg='black')
scale_entry.grid(column=1,row=1,padx=25)
# Percentage Label
percentage = tk.Label(mainframe, text='%', background=theme)
percentage.grid(column=1,row=1,sticky=(E))
#---------------------------------------------------------------------------

#Submit button
submit = tk.Button(mainframe,text='OK',padx=10, command=on_submit, background=theme, font=('SansSerif',10))
submit.grid(column=2,row=1, sticky=(E,N,S))

#'Return' key Event Listener
scale_entry.bind("<Return>", on_submit)

#MainFrame Column Weights
mainframe.columnconfigure(0,weight=0)
mainframe.columnconfigure(2,weight=1)

# -------------------------------------

print('Program launched.')

root.mainloop()

print('Program closed.')