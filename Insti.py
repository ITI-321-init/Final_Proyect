import tkinter as tk
from random import randint
from tkinter import messagebox
from pymongo import MongoClient
import random
import pandas as pd  # Importa pandas para manejar archivos Excel
import openpyxl


presupuesto_total = 800000000
presupuesto_Institu = presupuesto_total*0.35
presupuesto_Equitativo = 10800000


# Conexión con MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Cambia si tu conexión es diferente
db = client["mi_base_datos"]
collection = db["Instituciones"]

#Juntas:    Nombre, cantidad alumn, fecha actual, cedula juridica, distrito al que pertenecen, ubicación, telefono contacto
#


def random_solicitud():
 solicitado = random.randint(1000000,20000000)



# Función para insertar datos
# Función para insertar datos
def insertar_datos():
    try:
        # Obtener el valor ingresado para el dinero otorgado
        otorgado = entry_otorgado.get()

        # Verificar si el campo 'Dinero Otorgado' está vacío
        if not otorgado:
            messagebox.showerror("Error", "El campo 'Dinero Otorgado' es obligatorio.")
            return

        # Convertir el valor ingresado a float (si no lo es)
        otorgado = float(otorgado)
        otorgado = presupuesto_Institu * (otorgado/100)

        #
        Ejemplo = 5
        # Agregar el valor de 'presupuesto_Equitativo' al monto otorgado
        otorgado_final = otorgado + presupuesto_Equitativo
        usado = random.uniform(0,otorgado_final)

        #Total multiplicado por el porcentaje

        # Recoger el resto de los datos
        datos = {
            "cedula_juridica": entry_cedJuridica.get(),
            "nombre": entry_nombre.get(),
            "correo": entry_correo.get(),
            "distrito": entry_distrito.get(),
            "ubicación": entry_ubicación.get(),
            "telefono": entry_telefono.get(),
            "solicitado": randint(1000000, 20000000),
            "otorgado": otorgado_final,  # Guardar el monto final después de añadir el presupuesto equitativo
            "Usado": usado,
            "Restante": otorgado_final - usado
        }

        # Verificar que todos los campos están llenos
        if not all(datos.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Insertar los datos en la base de datos
        result = collection.insert_one(datos)
        messagebox.showinfo("Éxito", f"Datos insertados con _id: {result.inserted_id}")

        # Limpiar los campos después de insertar
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
        usado = dato.get('Usado', 0)
        restante = dato.get('Restante', 0)
        equitativo = flotarizado + presupuesto_Equitativo
        porcentaje = (flotarizado / presupuesto_Institu) * 100

        #CedJur,Distrito,Ubicacion,Telefono,ccorreo

        if dato:
            resultado = (
                f"ID: {dato['_id']}\n"
                f"Cédula Juridica: {dato['cedula_juridica']}\n"
                f"Nombre: {dato['nombre']}\n"
                f"correo: {dato['correo']}\n"
                f"Distrito: {dato['distrito']}\n"
                f"Ubicación: {dato['ubicación']}\n"
                f"Telefono: {dato['telefono']}\n"
                f"Dinero solicitado: {dato['solicitado']}\n"
                f"Dinero dado: {otorgado:.1f}\n"
                f"Dinero usado: {usado:.1f}\n"
                f"Dinero restante: {restante:.1f}\n"
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
    entry_correo.delete(0, tk.END)
    entry_distrito.delete(0, tk.END)
    entry_ubicación.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)
    entry_id.delete(0, tk.END)
    entry_otorgado.delete(0, tk.END)


# Función para exportar los datos a un archivo Excel
def exportar_datos_excel():
    try:
        # Extrae todos los documentos de la colección
        datos = collection.find()

        # Crea una lista para almacenar los datos formateados
        lista_datos = []
        for doc in datos:
            lista_datos.append({
                "Cédula Jurídica": doc.get("cedula_juridica", ""),
                "Nombre": doc.get("nombre", ""),
                "Solicitado": doc.get("solicitado", ""),
                "Otorgado": doc.get("otorgado", ""),
                "Usado": doc.get("Usado", ""),
                "Restante": doc.get("Restante", "")
            })

        # Crea un DataFrame de pandas
        df = pd.DataFrame(lista_datos)

        # Exporta el DataFrame a un archivo Excel
        df.to_excel("Institutos.xlsx", index=False)

        messagebox.showinfo("Éxito", "Datos exportados a 'Institutos.xlsx' con éxito.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar los datos: {e}")








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

tk.Label(root, text="Correo:").grid(row=2, column=0, sticky="e")
entry_correo = tk.Entry(root)
entry_correo.grid(row=2, column=1)

tk.Label(root, text="Distrito:").grid(row=3, column=0, sticky="e")
entry_distrito = tk.Entry(root)
entry_distrito.grid(row=3, column=1)

tk.Label(root, text="ubicación").grid(row=4, column=0, sticky="e")
entry_ubicación = tk.Entry(root)
entry_ubicación.grid(row=4, column=1)

tk.Label(root, text="Telefono").grid(row=5, column=0, sticky="e")
entry_telefono = tk.Entry(root)
entry_telefono.grid(row=5, column=1)

tk.Label(root, text="Dinero Otorgado").grid(row=6, column=0, sticky="e")
entry_otorgado = tk.Entry(root)
entry_otorgado.grid(row=6, column=1)

# Botón para insertar datos
btn_insertar = tk.Button(root, text="Insertar Datos", command=insertar_datos)
btn_insertar.grid(row=7, column=0, columnspan=2, pady=10)

# Campo para buscar por ID
tk.Label(root, text="Buscar por cedula:").grid(row=8, column=0, sticky="e")
entry_id = tk.Entry(root)
entry_id.grid(row=8, column=1)

# Botón para extraer datos
btn_extraer = tk.Button(root, text="Datos", command=extraer_datos)
btn_extraer.grid(row=9, column=0, columnspan=2, pady=10)

# Botón para exportar a Excel
btn_exportar_excel = tk.Button(root, text="Exportar a Excel", command=exportar_datos_excel)
btn_exportar_excel.grid(row=12, column=0, columnspan=2, pady=10)

root.mainloop()
