import time
import io
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter.font import Font
from sklearn.svm import SVC
from sklearn import svm
from sklearn import metrics
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix
from PIL import ImageTk, Image
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from datetime import datetime

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

gender_map = {
	'1': 'Masculino',
	'0': 'Femenino'
}

angina_pain_map = {
	'1': 'Sí',
	'0': 'No'
}

# Fuentes del programa
normal_font = Font(family='Raleway Medium', size=11)
normal_font_bold = Font(family='Raleway Medium', weight='bold', size=14)
medium_font = Font(family='Raleway Medium', size=14)
large_font = Font(family='Raleway Medium', size=16)










# Leer el dataset
data = pd.read_csv('data/heart.csv')

# Dividir el dataset entre: X son los registros y Y es la etiqueta
x = data.drop('target', axis=1)
y = data.target

# Dividir otra vez X e Y entre datos de entrenamiento y datos de prueba
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=109)

#Crear la SVM e ingresarle los datos X e Y de prueba
clf = make_pipeline(StandardScaler(), SVC(kernel='rbf', gamma=0.1, C=1.0))
clf.fit(x_train, y_train)

# Guardar en esta variable todas las predicciones hechas sobre datos de prueba
y_pred = clf.predict(x_train)

# Crear matriz de confusion para obtener precision de la clasificación de cada etiqueta
cm = confusion_matrix(y_train, y_pred)
cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

confusion_matrix = np.array(cm);
accuracy_positive = round(confusion_matrix[0][0], 4) * 100
accuracy_negative = round(confusion_matrix[1][1], 4) * 100

print('*** Matriz de confusion con scores')
print(cm)
print('*** Precision diagnostico positivo')
print(accuracy_positive)
print('*** Precision diagnostico negativo')
print(accuracy_negative)

'''
print('*** El contenido de x_train')
print(x_train)

print(' ')

print('*** El contenido de y_train')
print(y_train)

print(' ')

print('*** La prediccion de todo el x_train')
print(clf.predict(x_train))
'''

'''
print('The score')
print(clf.score(x_test, y_test))

print('The first prediction')
print(clf.predict([[52,1,0,125,212,0,1,168,0,1,2,2,3]])) #No
print(clf.predict([[34,0,1,118,210,0,1,192,0,0.7,2,0,2]])) #Si
'''

def predict_result():

	# Obtener los valores a enviar a la SVM
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

	# Obtener la clasificación usando clf.predict() y enviando los datos en orden
	final_prediction = clf.predict([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]])
	#prediction_accuracy = clf.score(x_test, y_test) * 100
	#accuracy_value['text'] = str(prediction_accuracy)[:5] + '%'

	# Si el resultado final es 0 (Negativo, no tiene la enfermedad)
	if final_prediction == 0:

		prediction_value['text'] = 'Negativo'
		accuracy_value['text'] = accuracy_negative

		prediction_value['fg'] = '#4BCA81'
		accuracy_value['fg'] = '#4BCA81'

	# Si el resultado final es 1 (Positivo, tiene la enfermedad)	
	else:

		prediction_value['text'] = 'Positivo'
		accuracy_value['text'] = accuracy_positive

		prediction_value['fg'] = '#C23934'
		accuracy_value['fg'] = '#C23934'

	# Habilitar el boton para exportar resultados a pdf
	export_pdf_button['state'] = 'normal'


def validate_inputs():

	is_valid = True
	errors = ''

	patient_name = entry_patientname.get()
	patient_id = entry_patientid.get()
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

	#Validación nombre del paciente
	if not patient_name:
		errors += "- Por favor complete el campo 'Nombres del Paciente' \n\n"
		is_valid = False
		label_patientname['fg'] = 'red'
	else:
		label_patientname['fg'] = 'black'

	# Validacion identificación del paciente
	if not patient_id:
		errors += "- Por favor complete el campo 'Identificación del Paciente' \n\n"
		is_valid = False
		label_patientid['fg'] = 'red'
	else:
		label_patientid['fg'] = 'black'

	# Validacion edad
	if age is None:
		errors += "- Por favor complete el campo Edad \n\n"
		is_valid = False
		label_age['fg'] = 'red'
	else:
		try:
			int(age)
			label_age['fg'] = 'black'
		except ValueError:
			is_valid = False
			errors += "- El valor del campo Edad no es válido. Por favor ingrese un numero entero \n\n"
			label_age['fg'] = 'red'
			entry_age.delete(0, 'end')

	# Validacion angina
	if angina_val is None:
		errors += "- Por favor complete el campo 'Tipo de Dolor Pectoral' \n\n"
		is_valid = False
		label_angina['fg'] = 'red'
	else:
		label_angina['fg'] = 'black'

	#Validacion Presión Arterial en Reposo
	if bloodp is None:
		errors += "- Por favor complete el campo 'Presión Arterial en Reposo' \n\n"
		is_valid = False
		label_bloodp['fg'] = 'red'
	else:
		try:
			int(bloodp)
			label_bloodp['fg'] = 'black'
		except ValueError:
			is_valid = False
			errors += "- El valor del campo 'Presión Arterial en Reposo' no es válido. Por favor ingrese un numero entero \n\n"
			label_bloodp['fg'] = 'red'
			entry_bloodp.delete(0, 'end')

	# Validacion Colesterol Sérico
	if cholesterol is None:
		errors += "- Por favor complete el campo 'Colesterol Sérico' \n\n"
		is_valid = False
		label_cholesterol['fg'] = 'red'
	else:
		try:
			int(cholesterol)
			label_cholesterol['fg'] = 'black'
		except ValueError:
			is_valid = False
			errors += "- El valor del campo 'Colesterol Sérico' no es válido. Por favor ingrese un numero entero \n\n"
			label_cholesterol['fg'] = 'red'
			entry_cholesterol.delete(0, 'end')

	#Validación Nivel de Azúcar en Ayunas
	if sugar is None:
		errors += "- Por favor complete el campo 'Nivel de Azúcar en Ayunas' \n\n"
		is_valid = False
		label_sugar['fg'] = 'red'
	else:
		try:
			float(sugar)
			label_sugar['fg'] = 'black'
		except ValueError:
			is_valid = False
			errors += "- El valor del campo 'Nivel de Azúcar en Ayunas' no es válido. Por favor ingrese un numero entero o decimal con punto \n\n"
			label_sugar['fg'] = 'red'
			entry_sugar.delete(0, 'end')

	#Valicación Resultados Electrocardiográficos en Reposo
	if electrocardio_val is None or electrocardio_val == '':
		errors += "- Por favor complete el campo 'Resultados Electrocardiográficos en Reposo' \n\n"
		is_valid = False
		label_electrocardio['fg'] = 'red'
	else:
		label_electrocardio['fg'] = 'black'

	#Validación Frecuencia Cardíaca Máxima
	if heartrate is None:
		errors += "- Por favor complete el campo 'Frecuencia Cardíaca Máxima' \n\n"
		is_valid = False
		label_heartrate['fg'] = 'red'
	else:
		try:
			int(heartrate)
			label_heartrate['fg'] = 'black'
		except ValueError:
			is_valid = False
			errors += "- El valor del campo 'Frecuencia Cardíaca Máxima' no es válido. Por favor ingrese un numero entero \n\n"
			label_heartrate['fg'] = 'red'
			entry_heartrate.delete(0, 'end')

	#Validación ¿Angina Inducida por el Ejercicio?
	if anginapain_val is None:
		errors += "- Por favor complete el campo '¿Angina Inducida por el Ejercicio?' \n\n"
		is_valid = False
		label_anginapain['fg'] = 'red'
	else:
		label_anginapain['fg'] = 'black'

	#Validación Depresión de Onda ST Inducida por Ejercicio
	if st_depression is None:
		errors += "- Por favor complete el campo 'Depresión de Onda ST Inducida por Ejercicio' \n\n"
		is_valid = False
		label_st_depression['fg'] = 'red'
	else:
		try:
			float(st_depression)
			label_st_depression['fg'] = 'black'
		except ValueError:
			is_valid = False
			errors += "- El valor del campo 'Depresión de Onda ST Inducida por Ejercicio' no es válido. Por favor ingrese un numero entero o decimal con punto \n\n"
			label_st_depression['fg'] = 'red'
			entry_st_depression.delete(0, 'end')

	#Validación Pendiente del Segmento ST Durante Pico de Ejercicio
	if slope is None:
		errors += "- Por favor complete el campo 'Pendiente del Segmento ST Durante Pico de Ejercicio' \n\n"
		is_valid = False
		label_slope['fg'] = 'red'
	else:
		label_slope['fg'] = 'black'

	#Validación Número de Vasos Principales Coloreados por la Floración
	if not flourosopy_val:
		errors += "- Por favor complete el campo 'Número de Vasos Principales Coloreados por la Floración' \n\n"
		is_valid = False
		label_flourosopy['fg'] = 'red'
	else:
		label_flourosopy['fg'] = 'black'
	
	#Validación Resultado Prueba de Estrés con Talio
	try:
		int(thalium_val)
		label_thalium['fg'] = 'black'
	except ValueError:
		is_valid = False
		errors += "- Por favor complete el campo 'Resultado Prueba de Estrés con Talio' \n\n"
		label_thalium['fg'] = 'red'

	#Retornar validez final de todos los inputs
	if not is_valid:
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

	prediction_value['text'] = '-'
	accuracy_value['text'] = '-'

	if form_valid:

		progress_bar.pack()

		for _ in range(25):
			progress_bar['value'] += 10
			root.update_idletasks()
			time.sleep(0.1)

		progress_bar['value'] = 0
		progress_bar.pack_forget()

		predict_result()

def save_as_pdf():

	is_form_valid = validate_inputs()

	# Verificar que todos los campos son validos antes de proceder
	if is_form_valid:

		# Obtener la ruta del directorio donde se guardará el archivo
		directory_route = filedialog.askdirectory()

		# Si la ruta escogida no esta vacía, entonces
		if directory_route != '':

			# Resutado final y precision para escribir a pdf
			result_val = prediction_value['text']
			accuracy_val = accuracy_value['text']

			# Datos principales del paciente para escribir a pdf
			patient_name = entry_patientname.get()
			patient_id = entry_patientid.get()
			current_date = str(datetime.date(datetime.now()))

			#Datos medicos del paciente para escribir a pdf
			age = entry_age.get()
			gender_val = gender_map.get(gender.get())
			angina_val = angina.get()
			bloodp = entry_bloodp.get()
			cholesterol = entry_cholesterol.get()
			sugar = entry_sugar.get()
			electrocardio_val = electrocardio.get()
			heartrate = entry_heartrate.get()
			anginapain_val = angina_pain_map.get(anginapain.get())
			st_depression = entry_st_depression.get()
			slope = slope_val.get()
			flourosopy_val = flourosopy.get()
			thalium_val = thalium.get()

			packet = io.BytesIO()

			# Crear un nuevo PDF con reportlab
			can = canvas.Canvas(packet, pagesize=letter)

			# Poner tipo de letra Times tamaño 12 y escribir datos
			# El punto se ubica por defecto en la esquina inferior izq
			can.setFont('Times-Roman', 12)
			can.drawString(6*cm, 22*cm, patient_name)
			can.drawString(6*cm, 21*cm, patient_id)
			can.drawString(17.3*cm, 22*cm, current_date)

			can.setFont('Times-Bold', 12)
			can.drawString(4.587*cm, 19.569*cm, result_val)
			can.drawString(4.587*cm, 18.412*cm, accuracy_val)

			can.setFont('Times-Roman', 12)
			can.drawString(11.25*cm, 16*cm, age)
			can.drawString(11.25*cm, 15.3*cm, gender_val)
			can.drawString(11.25*cm, 14.6*cm, angina_val)
			can.drawString(11.25*cm, 13.9*cm, cholesterol)
			can.drawString(11.25*cm, 13.11*cm, electrocardio_val)
			can.drawString(11.25*cm, 12.32*cm, anginapain_val)
			can.drawString(11.25*cm, 11.52*cm, slope)
			can.drawString(11.25*cm, 10.16*cm, thalium_val)
			can.drawString(11.25*cm, 9.37*cm, bloodp)
			can.drawString(11.25*cm, 8.58*cm, sugar)
			can.drawString(11.25*cm, 7.79*cm, heartrate)
			can.drawString(11.25*cm, 7*cm, st_depression)
			can.drawString(11.25*cm, 5.68*cm, flourosopy_val)

			can.save()

			packet.seek(0)
			new_pdf = PdfFileReader(packet)

			# Leer el PDF plantilla
			existing_pdf = PdfFileReader(open("docs/PDF_Base.pdf", "rb"))
			output = PdfFileWriter()

			page = existing_pdf.getPage(0)
			#page2 = existing_pdf.getPage(1)
			page.mergePage(new_pdf.getPage(0))
			output.addPage(page)
			#output.addPage(page2)

			# Guardar el archivo en la ruta seleccionada con el nombre e ID del paciente
			outputStream = open(directory_route + '/Resultados ' + patient_name + ' ' + patient_id + '.pdf', "wb")
			output.write(outputStream)
			outputStream.close()

			messagebox.showinfo(title='Información', message='Los resultados fueron exportados correctamente')

		else:

			# Si no se seleccionó ninguna ruta, mostrar mensaje de error
			messagebox.showerror(title='Datos no exportados', message='No se ha seleccionado ninguna carpeta, porfavor seleccione un directorio válido')

		








# Configuración del elemento raíz de la ventana y menús superiores
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

# Configurar ventana para aparezca como pantalla completa
root.state('zoomed')








#Frame principal (contenedor de todos los elementos)
main_frame = Frame(root)
main_frame.pack(fill='both', expand=True)

container_frame = LabelFrame(main_frame, text='Datos del Paciente', relief=RIDGE, font=normal_font)








# Frame header del título e imágenes
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

header_frame.pack(fill="x", padx=15, pady=9)








# Panel de inputs lado izquierdo
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

label_slope = Label(slope_subframe, text="Pendiente del Segmento ST Durante Pico de Ejercicio:", anchor='w', justify='left', font=normal_font)
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








# Panel de inputs lado derecho
right_frame = Frame(container_frame, width=550, height=400, padx=15, pady=15)

##
patientname_subframe = Frame(right_frame)

label_patientname = Label(patientname_subframe, text="Nombres del Paciente:", anchor='w', font=normal_font)
label_patientname.grid(row=0, column=0, sticky="we", padx=(0, 8))

entry_patientname = Entry(patientname_subframe)
entry_patientname.grid(row=0, column=1, sticky='we')

patientname_subframe.grid_columnconfigure(0, weight=1)
patientname_subframe.grid_columnconfigure(1, weight=1)
patientname_subframe.pack(fill='x', expand=True, pady=(0, 10))
##

##
patientid_subframe = Frame(right_frame)

label_patientid = Label(patientid_subframe, text="Identificación del Paciente:", anchor='w', font=normal_font)
label_patientid.grid(row=0, column=0, sticky="we", padx=(0, 8))

entry_patientid = Entry(patientid_subframe)
entry_patientid.grid(row=0, column=1, sticky='we')

patientid_subframe.grid_columnconfigure(0, weight=1)
patientid_subframe.grid_columnconfigure(1, weight=1)
patientid_subframe.pack(fill='x', expand=True, pady=(0, 10))
##

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

label_flourosopy = Label(flourosopy_subframe, text="Número de Vasos Principales Coloreados por la Floración:", anchor='w', justify='left', font=normal_font)
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










# Botones, barra de progreso y panel de resultados (zona inferior)
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


prediction_value = Label(results_frame, text='-', font=normal_font_bold)
prediction_value.grid(row=1, column=0, sticky="we")

accuracy_value = Label(results_frame, text='-', font=normal_font_bold)
accuracy_value.grid(row=1, column=1, sticky="we")

export_pdf_button = Button(results_frame, text='Exportar Pronóstico a PDF', font=normal_font, command=save_as_pdf, state='disabled')
#export_pdf_button = Button(results_frame, text='Exportar Pronóstico a PDF', font=normal_font, command=save_as_pdf)
export_pdf_button.grid(row=1, column=2, sticky="we")

results_frame.grid_columnconfigure(0, weight=1)
results_frame.grid_columnconfigure(1, weight=1)
results_frame.grid_columnconfigure(2, weight=1)

results_frame.pack(fill="x", pady=10, padx=10)








# Ejecutar la ventana en un ciclo infinito
root.mainloop()





