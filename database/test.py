import sqlite3

# Crear conexion con BD, si no existe se crea
conn = sqlite3.connect('CardioInsight.db')

# Crear un nuevo objeto cursor para interactuar con BD
c = conn.cursor()

# Crear tabla Diagnosticos
c.execute(
'''
CREATE TABLE IF NOT EXISTS Diagnosticos (
    id_diagnostico INTEGER PRIMARY KEY,
    documento_paciente TEXT,
    nombre_paciente TEXT,
    edad INTEGER,
    genero TEXT,
    dolor_toracico TEXT,
    colesterol_serico INTEGER,
    angina_ejercicio INTEGER,
    st_pico_ejercicio TEXT,
    estres_talio INTEGER,
    presion_reposo INTEGER,
    azucar_ayunas INTEGER,
    frecuencia_maxima INTEGER,
    depresion_st NUMERIC,
    vasos_fluoracion INTEGER
)'''
)

# Guardar cambios y generar archivo .db
conn.commit()


