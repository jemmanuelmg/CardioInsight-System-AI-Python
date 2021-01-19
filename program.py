import time
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.font import Font
from sklearn.svm import SVC
from sklearn import svm
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from PIL import ImageTk, Image

root = Tk()
gender = StringVar(root, '1')
angina = StringVar(root)
electrocardio = StringVar(root)
anginapain = StringVar(root, '1')
slope_val = StringVar(root)
flourosopy = StringVar(root)
thalium = StringVar(root)
final_prediction = "-"
prediction_accuracy = "-"

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

normal_font = Font(family='Raleway Medium', size=11)
normal_font_bold = Font(family='Raleway Medium', weight='bold', size=14)
medium_font = Font(family='Raleway Medium', size=14)
large_font = Font(family='Raleway Medium', size=16)

data = pd.read_csv('data/heart.csv')

x = data.drop('target', axis=1)
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

def predict_result():

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
	prediction_accuracy = clf.score(x_test, y_test) * 100
	accuracy_value['text'] = str(prediction_accuracy)[:5] + '%'

	if final_prediction == 0:
		prediction_value['text'] = 'Negativo'
		prediction_value['fg'] = '#4BCA81'
		accuracy_value['fg'] = '#4BCA81'
	else:
		prediction_value['text'] = 'Positivo'
		prediction_value['fg'] = '#C23934'
		accuracy_value['fg'] = '#C23934'


def validate_inputs():

	is_valid = True
	errors = ''

	age = entry_age.get()
	angina_val = angina_map.get(angina.get())
	bloodp = entry_bloodp.get()
	cholesterol = entry_cholesterol.get()
	sugar = entry_sugar.get()
	electrocardio_val = electrocardio_map.get(electrocardio.get())
	heartrate = entry_heartrate.get()
	anginapain_val = anginapain.get()
	st_depression = entry_st_depression.get()
	slope = slope_map.get(slope_val.get())
	flourosopy_val = flourosopy.get()
	thalium_val = thalium.get()

	if age is None:
		errors += "- Por favor complete el campo Edad \n\n"
		is_valid = False
	else:
		try:
			int(age)
		except ValueError:
			is_valid = False
			errors += "- El valor del campo Edad no es válido. Por favor ingrese un numero entero \n\n"

	if angina_val is None:
		errors += "- Por favor complete el campo 'Tipo de Dolor Pectoral' \n\n"
		is_valid = False

	if bloodp is None:
		errors += "- Por favor complete el campo 'Presión Arterial en Reposo' \n\n"
		is_valid = False
	else:
		try:
			int(bloodp)
		except ValueError:
			is_valid = False
			errors += "- El valor del campo 'Presión Arterial en Reposo' no es válido. Por favor ingrese un numero entero \n\n"

	if cholesterol is None:
		errors += "- Por favor complete el campo 'Colesterol Sérico' \n\n"
		is_valid = False
	else:
		try:
			int(cholesterol)
		except ValueError:
			is_valid = False
			errors += "- El valor del campo 'Colesterol Sérico' no es válido. Por favor ingrese un numero entero \n\n"

	if sugar is None:
		errors += "- Por favor complete el campo 'Nivel de Azúcar en Ayunas' \n\n"
		is_valid = False
	else:
		try:
			float(sugar)
		except ValueError:
			is_valid = False
			errors += "- El valor del campo 'Nivel de Azúcar en Ayunas' no es válido. Por favor ingrese un numero entero o decimal con punto \n\n"

	if electrocardio_val is None:
		errors += "- Por favor complete el campo 'Resultados Electrocardiográficos en Reposo' \n\n"
		is_valid = False

	if heartrate is None:
		errors += "- Por favor complete el campo 'Frecuencia Cardíaca Máxima' \n\n"
		is_valid = False
	else:
		try:
			int(heartrate)
		except ValueError:
			is_valid = False
			errors += "- El valor del campo 'Frecuencia Cardíaca Máxima' no es válido. Por favor ingrese un numero entero \n\n"

	if anginapain_val is None:
		errors += "- Por favor complete el campo '¿Angina Inducida por el Ejercicio?' \n\n"
		is_valid = False

	if st_depression is None:
		errors += "- Por favor complete el campo 'Depresión de Onda ST Inducida por Ejercicio' \n\n"
		is_valid = False
	else:
		try:
			float(st_depression)
		except ValueError:
			is_valid = False
			errors += "- El valor del campo 'Depresión de Onda ST Inducida por Ejercicio' no es válido. Por favor ingrese un numero entero o decimal con punto \n\n"

	if slope is None:
		errors += "- Por favor complete el campo 'Pendiente del Segmento ST Durante Pico de Ejercicio' \n\n"
		is_valid = False

	try:
		int(flourosopy_val)
	except ValueError:
		is_valid = False
		errors += "- Por favor complete el campo 'Número de Vasos Principales Coloreados por la Floración' \n\n"

	try:
		int(thalium_val)
	except ValueError:
		is_valid = False
		errors += "- Por favor complete el campo 'Resultado Prueba de Estrés con Talio' \n\n"

	if not is_valid:
		#label_validation['text'] = errors
		messagebox.showerror(message=errors, title="Información Suministrada No Valida")
		return False
	else:
		return True


def show_help():
	pass


def show_about_info():
	pass


def start_progress_bar():

	form_valid = validate_inputs()
	if form_valid:

		progress_bar.pack()

		for x in range(25):
			progress_bar['value'] += 10
			root.update_idletasks()
			time.sleep(0.5)

		#predict_result()

		progress_bar['value'] = 0
		progress_bar.pack_forget()

		predict_result()









root.title('Pronóstico Enfermedad del Corazon')
root.iconbitmap('img/program-icon.ico')

main_menu = Menu(root)
root.config(menu=main_menu)

file_menu = Menu(main_menu, tearoff=0)
file_menu.add_command(label='Salir', command=root.quit)
main_menu.add_cascade(label='Archivo', menu=file_menu)

help_menu = Menu(main_menu, tearoff=0)
help_menu.add_command(label='Mostrar Ayuda', command=show_help)
main_menu.add_cascade(label='Ayuda', menu=help_menu)


about_menu = Menu(main_menu, tearoff=0)
about_menu.add_command(label='Acerca De...', command=show_about_info)
main_menu.add_cascade(label='Información', menu=about_menu)

# root.resizable(False, False)

window_height = 670
window_width = 1300

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))

root.geometry('{}x{}+{}+{}'.format(window_width, window_height, x_cordinate, y_cordinate))

main_frame = Frame(root)
main_frame.pack(fill='both', expand=True)

container_frame = LabelFrame(main_frame, text='Datos del Paciente', relief=RIDGE, font=normal_font)









header_frame = Frame(main_frame)

medicine_logo_canvas = Canvas(header_frame, width=95, height=95)
medicine_logo_img = ImageTk.PhotoImage(Image.open('img/heart-1.png'))
medicine_logo_canvas.create_image(0, 0, anchor='nw', image=medicine_logo_img)
medicine_logo_canvas.grid(row=0, column=0, sticky='nw')

title_label = Label(header_frame, text='Inteligencia Artificial \n Pronóstico de Enfermedad del Corazón', justify='center', font=medium_font)
title_label.grid(row=0, column=1, sticky='we')

heart_img_canvas = Canvas(header_frame, width=95, height=95)
heart_img = ImageTk.PhotoImage(Image.open('img/medicine-logo.png'))
heart_img_canvas.create_image(0, 0, anchor='nw', image=heart_img)
heart_img_canvas.grid(row=0, column=2, sticky='ne')

header_frame.grid_columnconfigure(0, weight=1)
header_frame.grid_columnconfigure(1, weight=1)
header_frame.grid_columnconfigure(2, weight=1)

header_frame.pack(fill="x", padx=15, pady=15)









left_frame = Frame(container_frame, width=550, height=400, padx=15, pady=15)
##
age_subframe = Frame(left_frame)

label_age = Label(age_subframe, text="Edad:", anchor='w', font=normal_font)
label_age.grid(row=0, column=0, sticky="we", padx=(0, 8))

entry_age = Entry(age_subframe)
entry_age.grid(row=0, column=1, sticky='we')

age_subframe.grid_columnconfigure(0, weight=1)
age_subframe.grid_columnconfigure(1, weight=1)
age_subframe.pack(fill='x', expand=True, pady=(0, 10))
##

##
angina_subframe = Frame(left_frame)

label_angina = Label(angina_subframe, text="Tipo de Dolor Pectoral:", anchor='w', justify='left', font=normal_font)
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

label_cholesterol = Label(cholesterol_subframe, text="Colesterol Sérico (mg/dl):", anchor='w', font=normal_font)
label_cholesterol.grid(row=0, column=0, sticky="we", padx=(0, 8))

entry_cholesterol = Entry(cholesterol_subframe)
entry_cholesterol.grid(row=0, column=1, sticky='we')

cholesterol_subframe.grid_columnconfigure(0, weight=1)
cholesterol_subframe.grid_columnconfigure(1, weight=1)
cholesterol_subframe.pack(fill='x', expand=True, pady=(0, 10))
##

##
electrocardio_subframe = Frame(left_frame)

label_electrocardio = Label(electrocardio_subframe, text="Resultados Electrocariográficos en Reposo:", anchor='w', justify='left', font=normal_font)
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

label_anginapain = Label(anginapain_subframe, text="¿Angina Inducida por el Ejercicio?: ", anchor='w', font=normal_font)
label_anginapain.grid(row=0, column=0, sticky="we", padx=(0, 8))

anginapain_subframe1 = Frame(anginapain_subframe)

radiobtn_pain_yes = Radiobutton(anginapain_subframe1, text='Sí', value='1', variable=anginapain, font=normal_font)
radiobtn_pain_no = Radiobutton(anginapain_subframe1, text='No', value='2', variable=anginapain, font=normal_font)

radiobtn_pain_yes.pack(side='left')
radiobtn_pain_no.pack(side='left')

anginapain_subframe1.grid(row=0, column=1, sticky='we')

anginapain_subframe.grid_columnconfigure(0, weight=1)
anginapain_subframe.grid_columnconfigure(1, weight=1)
anginapain_subframe.pack(fill='x', expand=True, pady=(0, 10))
##

##
slope_subframe = Frame(left_frame)

label_slope = Label(slope_subframe, text="Pendiente Del Segmento ST Durante Pico De Ejercicio:", anchor='w', justify='left', font=normal_font)
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

label_thalium = Label(thalium_subframe, text="Resultado Prueba de Estrés con Talio:", anchor='w', justify='left', font=normal_font)
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









right_frame = Frame(container_frame, width=550, height=400, padx=15, pady=15)

##
gender_subframe = Frame(right_frame)

label_gender = Label(gender_subframe, text="Género: ", anchor='w', font=normal_font)
label_gender.grid(row=0, column=0, sticky="we", padx=(0, 8))

radiobtn_subframe1 = Frame(gender_subframe)

radiobtn_masculin = Radiobutton(radiobtn_subframe1, text='Masculino', value='1', variable=gender, font=normal_font)
radiobtn_femenin = Radiobutton(radiobtn_subframe1, text='Femenino', value='2', variable=gender, font=normal_font)

radiobtn_masculin.pack(side='left')
radiobtn_femenin.pack(side='left')

radiobtn_subframe1.grid(row=0, column=1, sticky='we')

gender_subframe.grid_columnconfigure(0, weight=1)
gender_subframe.grid_columnconfigure(1, weight=1)
gender_subframe.pack(fill='x', expand=True, pady=(0, 10))
##

##
blood_pressure_subframe = Frame(right_frame)

label_bloodp = Label(blood_pressure_subframe, text="Presión Arterial en Reposo (mm Hg):", anchor='w', font=normal_font)
label_bloodp.grid(row=0, column=0, sticky="we", padx=(0, 8))

entry_bloodp = Entry(blood_pressure_subframe)
entry_bloodp.grid(row=0, column=1, sticky='we')

blood_pressure_subframe.grid_columnconfigure(0, weight=1)
blood_pressure_subframe.grid_columnconfigure(1, weight=1)
blood_pressure_subframe.pack(fill='x', expand=True, pady=(0, 10))
##

##
sugar_subframe = Frame(right_frame)

label_sugar = Label(sugar_subframe, text="Nivel de Azúcar en Ayunas (mg/dl):", anchor='w', font=normal_font)
label_sugar.grid(row=0, column=0, sticky="we", padx=(0, 8))

entry_sugar = Entry(sugar_subframe)
entry_sugar.grid(row=0, column=1, sticky='we')

sugar_subframe.grid_columnconfigure(0, weight=1)
sugar_subframe.grid_columnconfigure(1, weight=1)
sugar_subframe.pack(fill='x', expand=True, pady=(0, 10))
##

##
heartrate_subframe = Frame(right_frame)

label_heartrate = Label(heartrate_subframe, text="Frecuencia Cardíaca Máxima Alcanzada:", anchor='w', font=normal_font)
label_heartrate.grid(row=0, column=0, sticky="we", padx=(0, 8))

entry_heartrate = Entry(heartrate_subframe)
entry_heartrate.grid(row=0, column=1, sticky='we')

heartrate_subframe.grid_columnconfigure(0, weight=1)
heartrate_subframe.grid_columnconfigure(1, weight=1)
heartrate_subframe.pack(fill='x', expand=True, pady=(0, 10))
##

##
st_depression_subframe = Frame(right_frame)

label_st_depression = Label(st_depression_subframe, text="Depresión de Onda ST Inducida por Ejercicio (En Relación al Reposo):", anchor='w', font=normal_font)
label_st_depression.grid(row=0, column=0, sticky="we", padx=(0, 8))

entry_st_depression = Entry(st_depression_subframe)
entry_st_depression.grid(row=0, column=1, sticky='we')

st_depression_subframe.grid_columnconfigure(0, weight=1)
st_depression_subframe.grid_columnconfigure(1, weight=1)
st_depression_subframe.pack(fill='x', expand=True, pady=(0, 10))
##

##
flourosopy_subframe = Frame(right_frame)

label_flourosopy = Label(flourosopy_subframe, text="Número De Vasos Principales Coloreados Por La Floración:", anchor='w', justify='left', font=normal_font)
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
container_frame.pack(fill="x", pady=(10, 7), padx=10)










#main_button = Button(main_frame, text='Calcular Pronóstico', width=20, command=validate_inputs, font=normal_font)
main_button = Button(main_frame, text='Calcular Pronóstico', width=20, command=start_progress_bar, font=normal_font)
main_button.pack()

progress_bar = ttk.Progressbar(main_frame, orient=HORIZONTAL, length=300, mode='indeterminate')

results_frame = LabelFrame(main_frame, text='Resultados del Pronóstico', relief=RIDGE, padx=15, pady=7, font=normal_font)

prediction_label = Label(results_frame, text='¿Paciente Presenta Enfermedad del Corazón?', font=normal_font)
prediction_label.grid(row=0, column=0, sticky="we")

accuracy_label = Label(results_frame, text='Precisión del Pronóstico', font=normal_font)
accuracy_label.grid(row=0, column=1, sticky="we")

actions_label = Label(results_frame, text='Acciónes', font=normal_font)
actions_label.grid(row=0, column=2, sticky="we")


#prediction_value = Label(results_frame, text=final_prediction, bg='#4BCA81')
prediction_value = Label(results_frame, text='-', font=normal_font_bold)
prediction_value.grid(row=1, column=0, sticky="we")

#accuracy_value = Label(results_frame, text=str(prediction_accuracy), bg='#4BCA81')
accuracy_value = Label(results_frame, text='-', font=normal_font_bold)
accuracy_value.grid(row=1, column=1, sticky="we")

export_pdf_button = Button(results_frame, text='Exportar Pronóstico a PDF', font=normal_font)
export_pdf_button.grid(row=1, column=2, sticky="we")

results_frame.grid_columnconfigure(0, weight=1)
results_frame.grid_columnconfigure(1, weight=1)
results_frame.grid_columnconfigure(2, weight=1)

results_frame.pack(fill="x", pady=10, padx=10)









root.mainloop()





