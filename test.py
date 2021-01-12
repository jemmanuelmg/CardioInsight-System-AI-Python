from tkinter import *

root=Tk()
Label(root,text="hello").grid(row=1,column=1)
Label(root,text="world").grid(row=2,column=3)
Label(root,relief=SUNKEN,borderwidth=1,bg="red").grid(row=2,column=2)
Label(root).grid(row=2,column=1)
root.mainloop()