from tkinter import *
from Project import *

root = Tk()

root.title("Boarding")

canvas = Canvas(root, width=1350, height=950, bg='sky blue')
canvas.pack()

for i in range(8):
    x = 550 + (i * 30)
    canvas.create_line(x, 932, x, -850, width=4)

for i in range(32):
    y = - (i * 30)
    canvas.create_line(760, -y, 550, -y, width=4)

img = PhotoImage(file='/home/jordan/Documents/PersonalStuff/Airplane-Boarding-Simulation/man.png')
img = img.subsample(22, 22)

#30 spaces down for moving down a row
canvas.create_image(
    648,
    2, 
    anchor=NW, 
    image=img
    )    
canvas.create_image(
    648,
    32, 
    anchor=NW, 
    image=img
    )     

#root.mainloop()

simulation("Random", 0, 1, False)