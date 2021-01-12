import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#from tkinter import Tk, Frame, Label, Entry, Radiobutton
from tkinter import *
from sklearn.svm import SVC
from sklearn import svm
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

'''
data = pd.read_csv('data/heart.csv')

x = data.drop('target', axis = 1) 
y = data.target

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4, random_state=109)

clf = make_pipeline(StandardScaler(), SVC(kernel='rbf', gamma=0.1, C=1.0))
clf.fit(x_train, y_train)

print('The score')
print(clf.score(x_test, y_test))

print('The first prediction')
print(clf.predict([[52,1,0,125,212,0,1,168,0,1,2,2,3]])) #No
print(clf.predict([[34,0,1,118,210,0,1,192,0,0.7,2,0,2]])) #Si
'''

root = Tk()

gender = StringVar(root, '1') 

root.title('Predictor de Enfermedades del Corazon')
#root.resizable(False, False)

window_height = 600
window_width = 1100

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

root.geometry('{}x{}+{}+{}'.format(window_width, window_height, x_cordinate, y_cordinate))

main_frame = Frame(root, bg='red')
main_frame.pack(fill='both', expand=True)

container_frame = Frame(main_frame, bg='yellow')





left_frame = Frame(container_frame, bg='green', width=550, height=400, padx=15, pady=15)

age_subframe = Frame(left_frame)

label_age = Label(age_subframe, text="Edad:", anchor='w')
label_age.grid(row=0, column=0, sticky="we", padx=(0, 8))

entry_age = Entry(age_subframe)
entry_age.grid(row=0, column=1, sticky='we')

age_subframe.grid_columnconfigure(0, weight=1)
age_subframe.grid_columnconfigure(1, weight=1)
age_subframe.pack(fill='x', expand=True, pady=(0, 10))

left_frame.grid(row=0, column=0, sticky='nsew')





right_frame = Frame(container_frame, bg='blue', width=550, height=400, padx=15, pady=15)

gender_subframe = Frame(right_frame)

label_gender = Label(gender_subframe, text="Género: ", anchor='w')
label_gender.grid(row=0, column=0, sticky="we", padx=(0, 8))

radiobtn_subframe1 = Frame(gender_subframe)

radiobtn_masculin = Radiobutton(radiobtn_subframe1, text='Masculino', value='1', variable=gender)
radiobtn_femenin = Radiobutton(radiobtn_subframe1, text='Femenino', value='2', variable=gender)

radiobtn_masculin.pack(side='left')
radiobtn_femenin.pack(side='left')

radiobtn_subframe1.grid(row=0, column=1, sticky='we')

gender_subframe.grid_columnconfigure(0, weight=1)
gender_subframe.grid_columnconfigure(1, weight=1)
gender_subframe.pack(fill='x', expand=True, pady=(0, 10))

right_frame.grid(row=0, column=1, sticky='nsew')






container_frame.grid_columnconfigure(0, weight=1)
container_frame.grid_columnconfigure(1, weight=1)

container_frame.pack(fill="x")



root.mainloop()





