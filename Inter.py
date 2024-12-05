import tkinter as tk
from tkinter import messagebox
from pymongo import MongoClient


# Conexión con MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Cambia si tu conexión es diferente
db = client["mi_base_datos"]
collection = db["mi_coleccion"]


# Función para insertar datos
def insertar_datos():
    try:
        datos = {
            "cedula": entry_cedula.get(),
            "nombre": entry_nombre.get(),
            "apellidos": entry_apellidos.get(),
            "sexo": entry_sexo.get(),
            "ecivil": entry_ecivil.get(),
            "fecnac": entry_fecnac.get()
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
        cedula_valor = entry_id.get()
        if not cedula_valor:
            messagebox.showerror("Error", "El campo Cédula no puede estar vacío.")
            return

        # Busca el documento por el campo 'cedula'
        dato = collection.find_one({"cedula": cedula_valor})  # O usa int(cedula_valor) si 'cedula' es un número
        if dato:
            resultado = (
                f"ID: {dato['_id']}\n"
                f"Cédula: {dato['cedula']}\n"
                f"Nombre: {dato['nombre']}\n"
                f"Apellidos: {dato['apellidos']}\n"
                f"Sexo: {dato['sexo']}\n"
                f"Estado Civil: {dato['ecivil']}\n"
                f"Fecha Nac.: {dato['fecnac']}"
            )
            messagebox.showinfo("Datos Encontrados", resultado)
        else:
            messagebox.showinfo("Sin Resultados", "No se encontró un documento con esa cédula.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo extraer: {e}")



# Función para limpiar campos
def limpiar_campos():
    entry_cedula.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_apellidos.delete(0, tk.END)
    entry_sexo.delete(0, tk.END)
    entry_ecivil.delete(0, tk.END)
    entry_fecnac.delete(0, tk.END)
    entry_id.delete(0, tk.END)


# Interfaz Gráfica
root = tk.Tk()
root.title("Gestión de MongoDB")

# Campos para insertar datos
tk.Label(root, text="Cédula:").grid(row=0, column=0, sticky="e")
entry_cedula = tk.Entry(root)
entry_cedula.grid(row=0, column=1)

tk.Label(root, text="Nombre:").grid(row=1, column=0, sticky="e")
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=1, column=1)

tk.Label(root, text="Apellidos:").grid(row=2, column=0, sticky="e")
entry_apellidos = tk.Entry(root)
entry_apellidos.grid(row=2, column=1)

tk.Label(root, text="Sexo:").grid(row=3, column=0, sticky="e")
entry_sexo = tk.Entry(root)
entry_sexo.grid(row=3, column=1)

tk.Label(root, text="Estado Civil:").grid(row=4, column=0, sticky="e")
entry_ecivil = tk.Entry(root)
entry_ecivil.grid(row=4, column=1)

tk.Label(root, text="Fecha Nacimiento (DD/MM/AAAA):").grid(row=5, column=0, sticky="e")
entry_fecnac = tk.Entry(root)
entry_fecnac.grid(row=5, column=1)

# Botón para insertar datos
btn_insertar = tk.Button(root, text="Insertar Datos", command=insertar_datos)
btn_insertar.grid(row=6, column=0, columnspan=2, pady=10)

# Campo para buscar por ID
tk.Label(root, text="Buscar por cedula:").grid(row=7, column=0, sticky="e")
entry_id = tk.Entry(root)
entry_id.grid(row=7, column=1)

# Botón para extraer datos
btn_extraer = tk.Button(root, text="Extraer Datos", command=extraer_datos)
btn_extraer.grid(row=8, column=0, columnspan=2, pady=10)

root.mainloop()
