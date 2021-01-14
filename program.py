import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from tkinter import ttk
from sklearn.svm import SVC
from sklearn import svm
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

root = Tk()

gender = StringVar(root, '1') 
angina = StringVar(root)
electrocardio = StringVar(root)
anginapain = StringVar(root, '1')
slope_val = StringVar(root)
flourosopy = StringVar(root)
thalium = StringVar(root)
final_prediction = 0

angina_map = { 
	'Angina Típica': 0, 
	'Angina Atípica': 1, 
	'Dolor No-Anginal': 2, 
	'Asintomático': 3 
}

electrocardio_map = {
	'Sin resultados reelevantes': 0,
	'Anormalidad en onda ST-T': 1,
	'Hipertrofia ventricular izquierda posible o definitiva': 2
}

slope_map = {
	'Ascendente (Rito cardíaco mejora con el ejercicio)': 0,
	'Plana (Cambio mínimo)': 1,
	'Descendete (Signos de corazón enfermo)': 2
}


data = pd.read_csv('data/heart.csv')

x = data.drop('target', axis = 1) 
y = data.target

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4, random_state=109)

clf = make_pipeline(StandardScaler(), SVC(kernel='rbf', gamma=0.1, C=1.0))
clf.fit(x_train, y_train)

'''
print('The score')
print(clf.score(x_test, y_test))

print('The first prediction')
print(clf.predict([[52,1,0,125,212,0,1,168,0,1,2,2,3]])) #No
print(clf.predict([[34,0,1,118,210,0,1,192,0,0.7,2,0,2]])) #Si
'''

def validate_inputs():
	is_valid = True
	errors = ''

	age = entry_age.get()
	gender = gender.get()
	angina = angina_map.get(angina.get()) ##
	bloodp = entry_bloodp.get()
	cholesterol = entry_cholesterol.get()
	sugar = entry_sugar.get()
	electrocardio = electrocardio_map.get(electrocardio.get())
	heartrate = entry_heartrate.get()
	anginapain = anginapain.get()
	st_depression = entry_st_depression.get()
	slope = slope_map.get(slope_val.get())
	flourosopy = flourosopy.get()
	thalium = thalium.get()

	if age == null:
		errors += "Por favor complete el campo Edad \n"
		is_valid = False
	else:
		try:
	    	int(age)
	    except ValueError:
	        is_valid = False
	        errors += "El valor del campo Edad no es válido. Por favor ingrese un numero entero \n"

	if angina == null:
		errors += "Por favor complete el campo 'Tipo de Dolor Pectoral' \n"
		is_valid = False

	if bloodp == null:
		errors += "Por favor complete el campo 'Presión Arterial en Reposo' \n"
		is_valid = False
	else:
		try:
	    	int(bloodp)
	    except ValueError:
	        is_valid = False
	        errors += "El valor del campo 'Presión Arterial en Reposo' no es válido. Por favor ingrese un numero entero \n"

    if cholesterol == null:
		errors += "Por favor complete el campo 'Colesterol Sérico' \n"
		is_valid = False
	else:
		try:
	    	int(cholesterol)
	    except ValueError:
	        is_valid = False
	        errors += "El valor del campo 'Colesterol Sérico' no es válido. Por favor ingrese un numero entero \n"

    if sugar == null:
		errors += "Por favor complete el campo 'Nivel de Azúcar en Ayunas' \n"
		is_valid = False
	else:
		try:
	    	float(sugar)
	    except ValueError:
	        is_valid = False
	        errors += "El valor del campo 'Nivel de Azúcar en Ayunas' no es válido. Por favor ingrese un numero entero o decimal con punto \n"

	if electrocardio == null:
		errors += "Por favor complete el campo 'Resultados Electrocardiográficos en Reposo' \n"
		is_valid = False

	if heartrate == null:
		errors += "Por favor complete el campo 'Frecuencia Cardíaca Máxima' \n"
		is_valid = False
	else:
		try:
	    	int(electrocardio)
	    except ValueError:
	        is_valid = False
	        errors += "El valor del campo 'Frecuencia Cardíaca Máxima' no es válido. Por favor ingrese un numero entero \n"

    if anginapain == null:
		errors += "Por favor complete el campo '¿Angina Inducida por el Ejercicio?' \n"
		is_valid = False

	if st_depression == null:
		errors += "Por favor complete el campo 'Depresión de Onda ST Inducida por Ejercicio' \n"
		is_valid = False
	else:
		try:
	    	float(st_depression)
	    except ValueError:
	        is_valid = False
	        errors += "El valor del campo 'Depresión de Onda ST Inducida por Ejercicio' no es válido. Por favor ingrese un numero entero o decimal con punto \n"

    if slope == null:
		errors += "Por favor complete el campo 'Pendiente del Segmento ST Durante Pico de Ejercicio' \n"
		is_valid = False

	if flourosopy == null:
		errors += "Por favor complete el campo 'Número de Vasos Principales Coloreados por la Floración' \n"
		is_valid = False

	if thalium == null:
		errors += "Por favor complete el campo 'Resultado Prueba de Estrés con Talio' \n"
		is_valid = False

	if !is_valid:
		label_validation['text'] = errors
	else:
		predict_result()



def predict_result():
	print('>>> Los valores para la prediccion')
	
	

	age = entry_age.get()
	sex = gender.get()
	cp = angina_map.get(angina.get())
	trestbps = entry_bloodp.get()
	chol = entry_cholesterol.get()

	fbs = entry_sugar.get()

	if float(fbs) > 120:
		fbs = 1
	else:
		fbs = 0

	restecg = electrocardio_map.get(electrocardio.get())
	thalach = entry_heartrate.get()
	exang = anginapain.get()
	oldpeak = entry_st_depression.get()
	slope = slope_map.get(slope_val.get())
	ca = flourosopy.get()
	thal = thalium.get()

	final_prediction = clf.predict([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])

	print('>>> Resultado final: ', final_prediction)

	
	
	
	



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

validation_frame = Frame(main_frame)
label_validation = Label(text='Hello', anchor=w)
validation_frame.pack(fill='x', expand=True, padx=15, pady=15)

container_frame = Frame(main_frame, bg='yellow')





left_frame = Frame(container_frame, bg='green', width=550, height=400, padx=15, pady=15)
##
age_subframe = Frame(left_frame)

label_age = Label(age_subframe, text="Edad:", anchor='w')
label_age.grid(row=0, column=0, sticky="we", padx=(0, 8))

entry_age = Entry(age_subframe)
entry_age.grid(row=0, column=1, sticky='we')

age_subframe.grid_columnconfigure(0, weight=1)
age_subframe.grid_columnconfigure(1, weight=1)
age_subframe.pack(fill='x', expand=True, pady=(0, 10))
##

##
angina_subframe = Frame(left_frame)

label_angina = Label(angina_subframe, text="Tipo de Dolor Pectoral:", anchor='w', justify='left')
label_angina.grid(row=0, column=0, sticky="we", padx=(0, 8))

combobox_angina = ttk.Combobox(angina_subframe, width = 32, textvariable = angina, state="readonly")

combobox_angina['values'] = tuple(angina_map.keys())

combobox_angina.grid(row=0, column=1, sticky='we')

angina_subframe.grid_columnconfigure(0, weight=1)
angina_subframe.grid_columnconfigure(1, weight=1)
angina_subframe.pack(fill='x', expand=True, pady=(0, 10))
##

##
cholesterol_subframe = Frame(left_frame)

label_cholesterol = Label(cholesterol_subframe, text="Colesterol Sérico (mg/dl):", anchor='w')
label_cholesterol.grid(row=0, column=0, sticky="we", padx=(0, 8))

entry_cholesterol = Entry(cholesterol_subframe)
entry_cholesterol.grid(row=0, column=1, sticky='we')

cholesterol_subframe.grid_columnconfigure(0, weight=1)
cholesterol_subframe.grid_columnconfigure(1, weight=1)
cholesterol_subframe.pack(fill='x', expand=True, pady=(0, 10))
##

##
electrocardio_subframe = Frame(left_frame)

label_electrocardio = Label(electrocardio_subframe, text="Resultados Electrocariográficos En Reposo:", anchor='w', justify='left')
label_electrocardio.grid(row=0, column=0, sticky="we", padx=(0, 8))

combobox_electrocardio = ttk.Combobox(electrocardio_subframe, width = 32, textvariable = electrocardio, state="readonly")

combobox_electrocardio['values'] = tuple(electrocardio_map.keys())

combobox_electrocardio.grid(row=0, column=1, sticky='we')

electrocardio_subframe.grid_columnconfigure(0, weight=1)
electrocardio_subframe.grid_columnconfigure(1, weight=1)
electrocardio_subframe.pack(fill='x', expand=True, pady=(0, 10))
##

##
anginapain_subframe = Frame(left_frame)

label_anginapain = Label(anginapain_subframe, text="¿Angina Inducida Por El Ejercicio?: ", anchor='w')
label_anginapain.grid(row=0, column=0, sticky="we", padx=(0, 8))

anginapain_subframe1 = Frame(anginapain_subframe)

radiobtn_pain_yes = Radiobutton(anginapain_subframe1, text='Sí', value='1', variable=anginapain)
radiobtn_pain_no = Radiobutton(anginapain_subframe1, text='No', value='2', variable=anginapain)

radiobtn_pain_yes.pack(side='left')
radiobtn_pain_no.pack(side='left')

anginapain_subframe1.grid(row=0, column=1, sticky='we')

anginapain_subframe.grid_columnconfigure(0, weight=1)
anginapain_subframe.grid_columnconfigure(1, weight=1)
anginapain_subframe.pack(fill='x', expand=True, pady=(0, 10))
##

##
slope_subframe = Frame(left_frame)

label_slope = Label(slope_subframe, text="Pendiente Del Segmento ST Durante Pico De Ejercicio:", anchor='w', justify='left')
label_slope.grid(row=0, column=0, sticky="we", padx=(0, 8))

combobox_slope = ttk.Combobox(slope_subframe, width = 32, textvariable = slope_val, state="readonly")

combobox_slope['values'] = tuple(slope_map.keys())

combobox_slope.grid(row=0, column=1, sticky='we')

slope_subframe.grid_columnconfigure(0, weight=1)
slope_subframe.grid_columnconfigure(1, weight=1)
slope_subframe.pack(fill='x', expand=True, pady=(0, 10))
##

##
thalium_subframe = Frame(left_frame)

label_thalium = Label(thalium_subframe, text="Resultado Prueba De Estrés Con Talio:", anchor='w', justify='left')
label_thalium.grid(row=0, column=0, sticky="we", padx=(0, 8))

combobox_thalium = ttk.Combobox(thalium_subframe, width = 32, textvariable = thalium, state="readonly")

combobox_thalium['values'] = ('0',  
	                          '1', 
	                          '2',
	                          '3')

combobox_thalium.grid(row=0, column=1, sticky='we')

thalium_subframe.grid_columnconfigure(0, weight=1)
thalium_subframe.grid_columnconfigure(1, weight=1)
thalium_subframe.pack(fill='x', expand=True, pady=(0, 10))
##

left_frame.grid(row=0, column=0, sticky='nsew')









right_frame = Frame(container_frame, bg='blue', width=550, height=400, padx=15, pady=15)

##
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
##

##
blood_pressure_subframe = Frame(right_frame)

label_bloodp = Label(blood_pressure_subframe, text="Presión Arterial En Reposo (mm Hg):", anchor='w')
label_bloodp.grid(row=0, column=0, sticky="we", padx=(0, 8))

entry_bloodp = Entry(blood_pressure_subframe)
entry_bloodp.grid(row=0, column=1, sticky='we')

blood_pressure_subframe.grid_columnconfigure(0, weight=1)
blood_pressure_subframe.grid_columnconfigure(1, weight=1)
blood_pressure_subframe.pack(fill='x', expand=True, pady=(0, 10))
##

##
sugar_subframe = Frame(right_frame)

label_sugar = Label(sugar_subframe, text="Nivel De Azúcar En Ayunas (mg/dl):", anchor='w')
label_sugar.grid(row=0, column=0, sticky="we", padx=(0, 8))

entry_sugar = Entry(sugar_subframe)
entry_sugar.grid(row=0, column=1, sticky='we')

sugar_subframe.grid_columnconfigure(0, weight=1)
sugar_subframe.grid_columnconfigure(1, weight=1)
sugar_subframe.pack(fill='x', expand=True, pady=(0, 10))
##

##
heartrate_subframe = Frame(right_frame)

label_heartrate = Label(heartrate_subframe, text="Frecuencia Cardíaca Máxima Alcanzada:", anchor='w')
label_heartrate.grid(row=0, column=0, sticky="we", padx=(0, 8))

entry_heartrate = Entry(heartrate_subframe)
entry_heartrate.grid(row=0, column=1, sticky='we')

heartrate_subframe.grid_columnconfigure(0, weight=1)
heartrate_subframe.grid_columnconfigure(1, weight=1)
heartrate_subframe.pack(fill='x', expand=True, pady=(0, 10))
##

##
st_depression_subframe = Frame(right_frame)

label_st_depression = Label(st_depression_subframe, text="Depresión De Onda ST Inducida Por Ejercicio (En Relación Al Reposo):", anchor='w')
label_st_depression.grid(row=0, column=0, sticky="we", padx=(0, 8))

entry_st_depression = Entry(st_depression_subframe)
entry_st_depression.grid(row=0, column=1, sticky='we')

st_depression_subframe.grid_columnconfigure(0, weight=1)
st_depression_subframe.grid_columnconfigure(1, weight=1)
st_depression_subframe.pack(fill='x', expand=True, pady=(0, 10))
##

##
flourosopy_subframe = Frame(right_frame)

label_flourosopy = Label(flourosopy_subframe, text="Número De Vasos Principales Coloreados Por La Floración:", anchor='w', justify='left')
label_flourosopy.grid(row=0, column=0, sticky="we", padx=(0, 8))

combobox_flourosopy = ttk.Combobox(flourosopy_subframe, width = 32, textvariable = flourosopy, state="readonly")

combobox_flourosopy['values'] = ('1',  
		                         '2', 
		                         '3')

combobox_flourosopy.grid(row=0, column=1, sticky='we')

flourosopy_subframe.grid_columnconfigure(0, weight=1)
flourosopy_subframe.grid_columnconfigure(1, weight=1)
flourosopy_subframe.pack(fill='x', expand=True, pady=(0, 10))
##

right_frame.grid(row=0, column=1, sticky='nsew')

container_frame.grid_columnconfigure(0, weight=1)
container_frame.grid_columnconfigure(1, weight=1)
container_frame.pack(fill="x")

main_button = Button(main_frame, text='Calcular Predicción', width=20, command=validate_inputs)
main_button.pack(pady=(30, 10))



root.mainloop()





