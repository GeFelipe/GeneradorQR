# ===============================
# Generador de Códigos QR NWTA
# ===============================
# Descripción:
#   Esta aplicación gráfica permite al usuario seleccionar una tarea,
#   ingresar códigos asociados (orden, mu, dirección), y genera una
#   cadena estandarizada separada por pipes (|), con la cual se crea
#   una imagen QR personalizada con pie de página.
# Librerías usadas:
#   tkinter  → interfaz gráfica
#   qrcode   → generación del código QR
#   Pillow   → creación y edición de imágenes (texto, tamaño, etc.)
# ===============================

import tkinter as tk                     # Librería base para interfaz gráfica
from tkinter import ttk, messagebox       # ttk para widgets modernos y messagebox para alertas
from PIL import Image, ImageDraw, ImageFont  # Librerías de Pillow para manejar imágenes
import qrcode                            # Librería para generar códigos QR

# --- CONFIGURACIÓN INICIAL ---
# Diccionario que relaciona:
#   codtarea → (descripcion, codtrabajo)
# Esto permite configurar fácilmente qué código de trabajo corresponde a cada tarea.
TAREAS_CONFIG = {
    "01": ("Inspección de red baja tensión", "01"),
    "02": ("Mantenimiento de transformador", "01"),
    "03": ("Cambio de poste", "01"),
    "04": ("Revisión de conexión", "02"),
    "05": ("Instalación de medidor", "02"),
    "06": ("Reparación de línea secundaria", "03"),
    "07": ("Sustitución de fusible", "03"),
    "08": ("Ajuste de acometida", "03"),
    "09": ("Verificación de tensión", "02"),
    "10": ("Reinstalación de suministro", "03"),
    "14": ("Reparación principal", "03"),
}


# --- FUNCIÓN PRINCIPAL: GENERAR EL CÓDIGO QR ---
def generar_qr():
    """Obtiene los datos del usuario, construye la cadena y genera la imagen QR."""

    # Obtener la tarea seleccionada (ejemplo: "14 - Reparación principal")
    seleccion = combo_codtarea.get().strip()
    if not seleccion:
        messagebox.showerror("Error", "Debe seleccionar una tarea.")
        return

    # Extraer solo el código (antes del guion)
    codtarea = seleccion.split(" - ")[0]

    # Obtener los demás campos ingresados por el usuario
    codord = entry_codord.get().strip()
    codmu = entry_codmu.get().strip()
    coddir = entry_coddir.get().strip()

    # Validar que los campos no estén vacíos
    if not codord or not codmu or not coddir:
        messagebox.showerror("Error", "Por favor complete todos los campos obligatorios.")
        return

    # Buscar descripción y codtrabajo en el diccionario
    descripcion, codtrabajo = TAREAS_CONFIG.get(codtarea, ("", "03"))

    # Valores constantes definidos por el estándar
    NWTA = "NWTA"   # texto fijo al inicio
    final = "I"     # texto fijo al final

    # Construir la estructura con 13 valores separados por '|'
    partes = [
        NWTA,              # 1. Prefijo fijo
        codtrabajo,        # 2. Código de trabajo (oculto al usuario)
        codtarea,          # 3. Código de la tarea seleccionada
        codord,            # 4. Código de orden
        codmu,             # 5. Código MU
        "",                # 6. Vacío
        coddir,            # 7. Dirección
        "", "", "", "", "", final  # 8–13. Campos vacíos + "I"
    ]

    # Unir los elementos con pipe (|)
    cadena_final = "|".join(partes)

    # --- GENERAR EL CÓDIGO QR ---
    qr = qrcode.make(cadena_final)  # Crear el código QR con la cadena final
    qr = qr.convert("RGB")          # Convertir a formato de imagen RGB

    # --- CREAR IMAGEN FINAL CON PIE DE PÁGINA ---
    ancho, alto = qr.size
    alto_total = alto + 100         # Se agrega espacio para dos líneas de texto
    img_final = Image.new("RGB", (ancho, alto_total), "white")  # Crear lienzo blanco
    img_final.paste(qr, (0, 0))     # Pegar el QR en la parte superior

    # Preparar para dibujar texto sobre la imagen
    draw = ImageDraw.Draw(img_final)
    fuente = ImageFont.load_default()  # Fuente simple por defecto

    # Texto del pie de página (dos líneas)
    linea1 = f"{codord} - {coddir}"                  # Línea superior
    linea2 = f"Tarea {codtarea}: {descripcion}"      # Línea inferior

    # Calcular tamaños de texto usando textbbox (nuevo método Pillow)
    bbox1 = draw.textbbox((0, 0), linea1, font=fuente)
    text_w1 = bbox1[2] - bbox1[0]
    text_h1 = bbox1[3] - bbox1[1]

    bbox2 = draw.textbbox((0, 0), linea2, font=fuente)
    text_w2 = bbox2[2] - bbox2[0]
    text_h2 = bbox2[3] - bbox2[1]

    # Escribir las dos líneas centradas horizontalmente
    draw.text(((ancho - text_w1) / 2, alto + 15), linea1, fill="black", font=fuente)
    draw.text(((ancho - text_w2) / 2, alto + 35), linea2, fill="black", font=fuente)

    # Guardar la imagen con un nombre único
    nombre_archivo = f"QR_{codtarea}_{codord}.png"
    img_final.save(nombre_archivo)

    # Mostrar mensaje de éxito y vista previa
    messagebox.showinfo("Éxito", f"QR generado correctamente:\n\n{cadena_final}\n\nGuardado como {nombre_archivo}")
    img_final.show()


# --- INTERFAZ GRÁFICA (Tkinter) ---
# Crear la ventana principal
root = tk.Tk()
root.title("Generador de QR")

# --- Campos de entrada ---
# Combobox de tareas (muestra descripción al usuario)
tk.Label(root, text="Código de Tarea:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
combo_codtarea = ttk.Combobox(
    root,
    values=[f"{k} - {v[0]}" for k, v in TAREAS_CONFIG.items()],
    width=40
)
combo_codtarea.grid(row=0, column=1, padx=10, pady=5)

# Campo de código de orden
tk.Label(root, text="Código de Orden (codord):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_codord = tk.Entry(root, width=43)
entry_codord.grid(row=1, column=1, padx=10, pady=5)

# Campo de código MU
tk.Label(root, text="Código MU (codmu):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_codmu = tk.Entry(root, width=43)
entry_codmu.grid(row=2, column=1, padx=10, pady=5)

# Campo de dirección
tk.Label(root, text="Dirección (coddir):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_coddir = tk.Entry(root, width=43)
entry_coddir.grid(row=3, column=1, padx=10, pady=5)

# Botón principal
tk.Button(
    root,
    text="Generar QR",
    command=generar_qr,
    bg="#007ACC",
    fg="white",
    width=30
).grid(row=4, column=0, columnspan=2, pady=20)

# Ejecutar el bucle principal de la ventana
root.mainloop()