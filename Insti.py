import tkinter as tk
from random import randint
from tkinter import messagebox
from pymongo import MongoClient
import random


presupuesto_total = 800000000
presupuesto_juntas = presupuesto_total/2
presupuesto_hogares = presupuesto_juntas*0.15
presupuesto_Institu = presupuesto_juntas*0.35
población = 2140


# Conexión con MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Cambia si tu conexión es diferente
db = client["mi_base_datos"]
collection = db["Juntas"]

#Juntas:    Nombre, cantidad alumn, fecha actual, cedula juridica, distrito al que pertenecen, ubicación, telefono contacto
#


def random_solicitud():
 solicitado = random.randint(1000000,20000000)



# Función para insertar datos
def insertar_datos_juntas():
    try:
        datos = {
            "cedula_juridica": entry_cedJuridica.get(),
            "nombre": entry_nombre.get(),
            "cantidad_alumn": entry_cantidad_alumn.get(),
            "fecha": entry_fecha.get(),
            "distrito": entry_distrito.get(),
            "ubicación": entry_ubicación.get(),
            "telefono": entry_telefono.get(),
            "solicitado": randint(1000000,20000000),
            "otorgado": entry_otorgado.get()
        }

        if not all(datos.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        result = collection.insert_one(datos)
        messagebox.showinfo("Éxito", f"Datos insertados con _id: {result.inserted_id}")
        limpiar_campos()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo insertar: {e}")


# Función para extraer datos
def extraer_datos():
    try:
        cedula_juridica = entry_id.get()
        if not cedula_juridica:
            messagebox.showerror("Error", "El campo Cédula no puede estar vacío.")
            return

        # Busca el documento por el campo 'cedula'
        dato = collection.find_one({"cedula_juridica": cedula_juridica})  # O usa int(cedula_juridica) si 'cedula' es un número
        otorgado = dato.get('otorgado', 0)
        flotarizado = float(otorgado)
        porcentaje = (flotarizado / presupuesto_juntas) * 100
        if dato:
            resultado = (
                f"ID: {dato['_id']}\n"
                f"Cédula Juridica: {dato['cedula_juridica']}\n"
                f"Nombre: {dato['nombre']}\n"
                f"Cant_Alumnos: {dato['cantidad_alumn']}\n"
                f"Fecha: {dato['fecha']}\n"
                f"Distrito: {dato['distrito']}\n"
                f"Ubicación: {dato['ubicación']}\n"
                f"Telefono: {dato['telefono']}\n"
                f"Porcentaje: {porcentaje:.4f}%\n"
            )
            messagebox.showinfo("Datos Encontrados", resultado)
        else:
            messagebox.showinfo("Sin Resultados", "No se encontró un documento con esa cédula.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo extraer: {e}")



# Función para limpiar campos
def limpiar_campos():
    entry_cedJuridica.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_cantidad_alumn.delete(0, tk.END)
    entry_fecha.delete(0, tk.END)
    entry_distrito.delete(0, tk.END)
    entry_ubicación.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    entry_id.delete(0, tk.END)


# Interfaz Gráfica
root = tk.Tk()
root.title("Gestión de MongoDB")

# Campos para insertar datos
tk.Label(root, text="Cédula Juridica:").grid(row=0, column=0, sticky="e")
entry_cedJuridica = tk.Entry(root)
entry_cedJuridica.grid(row=0, column=1)

tk.Label(root, text="Nombre:").grid(row=1, column=0, sticky="e")
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=1, column=1)

tk.Label(root, text="Cantidad Alumnos:").grid(row=2, column=0, sticky="e")
entry_cantidad_alumn = tk.Entry(root)
entry_cantidad_alumn.grid(row=2, column=1)

tk.Label(root, text="Fecha:").grid(row=3, column=0, sticky="e")
entry_fecha = tk.Entry(root)
entry_fecha.grid(row=3, column=1)

tk.Label(root, text="Distrito:").grid(row=4, column=0, sticky="e")
entry_distrito = tk.Entry(root)
entry_distrito.grid(row=4, column=1)

tk.Label(root, text="ubicación").grid(row=5, column=0, sticky="e")
entry_ubicación = tk.Entry(root)
entry_ubicación.grid(row=5, column=1)

tk.Label(root, text="Telefono").grid(row=6, column=0, sticky="e")
entry_telefono = tk.Entry(root)
entry_telefono.grid(row=6, column=1)

tk.Label(root, text="Dinero Otorgado").grid(row=7, column=0, sticky="e")
entry_otorgado = tk.Entry(root)
entry_otorgado.grid(row=7, column=1)

# Botón para insertar datos
btn_insertar = tk.Button(root, text="Insertar Datos", command=insertar_datos_juntas)
btn_insertar.grid(row=8, column=0, columnspan=2, pady=10)

# Campo para buscar por ID
tk.Label(root, text="Buscar por cedula:").grid(row=9, column=0, sticky="e")
entry_id = tk.Entry(root)
entry_id.grid(row=9, column=1)

# Botón para extraer datos
btn_extraer = tk.Button(root, text="Datos", command=extraer_datos)
btn_extraer.grid(row=11, column=0, columnspan=2, pady=10)

root.mainloop()
