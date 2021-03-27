# tkButtonArrayv0.py
#
# Modular style tkinter implementation of button array
#
# BH - 13/10/20

from tkinter import *

def buttonSelected(row,col):
    global count
    global buttons
    global instruction

    print(row,col)
    count += 1

    # relief does not do anything on a MAC but works fine on Windows 10
    if buttons[row][col]["relief"] == "sunken":
        buttons[row][col].config(relief = "raised",bg='#009f00')
    else:
        buttons[row][col].config(relief = "sunken")

    if count % 2 == 0:
        instruction.config(text = "a nice even number")
        buttons[row][col].config(fg = "green")
    else:
        buttons[row][col].config(fg = "red")
        instruction.config(text = "a pesky odd number")

    buttons[row][col].config(text = str(count))

# main
buttons = []
count = 0

window = Tk() # create the window
window.wm_title("Tkinter Array")
window.geometry("175x130")

# create buttons, store pointers to them in an array and link them to buttonSelected()
for r in range(2):
    buttonRow = []
    for c in range(3):
        aButton = Button(window, width=6, height=3, text=' ', command=lambda row=r, column=c : buttonSelected(row, column))
        aButton.grid(row=r, column=c)
        buttonRow.append(aButton)
    buttons.append(buttonRow)

instruction = Label(window, text = "Here is some text")
instruction.grid(row=r+1, columnspan = 3)  # span 3 columns

window.mainloop() # set the main loop running for the window
