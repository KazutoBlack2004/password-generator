import string
import random
import tkinter as tk
from tkinter import messagebox, ttk
import json
import base64

CONFIG_FILE = "config.json"

def cargar_configuracion():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "longitud": 8,
            "usar_letras": True,
            "usar_digitos": True,
            "usar_especiales": True,
            "guardar_cifrado": False,
        }

def guardar_configuracion(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

def generar_contraseña(longitud, usar_letras, usar_digitos, usar_especiales):
    caracteres = ""
    seleccion = []

    if usar_letras:
        caracteres += string.ascii_letters
        seleccion.append(random.choice(string.ascii_letters))
    if usar_digitos:
        caracteres += string.digits
        seleccion.append(random.choice(string.digits))
    if usar_especiales:
        caracteres += string.punctuation
        seleccion.append(random.choice(string.punctuation))

    if not caracteres:
        raise ValueError("Debe seleccionar al menos un tipo de carácter.")

    longitud = max(longitud, len(seleccion))
    contraseña = seleccion + [random.choice(caracteres) for _ in range(longitud - len(seleccion))]
    random.shuffle(contraseña)
    return "".join(contraseña)

def guardar_contraseña(contraseña, cifrar=False):
    archivo = "contraseña_generada.txt"
    with open(archivo, "wb" if cifrar else "w") as f:
        if cifrar:
            codificada = base64.b64encode(contraseña.encode())
            f.write(codificada + b"\n")
        else:
            f.write("Contraseña generada: " + contraseña + "\n")
    mensaje = f"Contraseña {'codificada ' if cifrar else ''}guardada en '{archivo}'"
    messagebox.showinfo("Guardado", mensaje)

def copiar_portapapeles(contraseña):
    root.clipboard_clear()
    root.clipboard_append(contraseña)
    root.update()
    messagebox.showinfo("Copiado", "Contraseña copiada al portapapeles.")

def generar():
    try:
        longitud = int(entry_longitud.get())
        usar_letras = var_letras.get()
        usar_digitos = var_digitos.get()
        usar_especiales = var_especiales.get()
        cifrar = guardar_cifrado_var.get()

        if not (usar_letras or usar_digitos or usar_especiales):
            raise ValueError("Debe seleccionar al menos un tipo de carácter.")

        contraseña = generar_contraseña(longitud, usar_letras, usar_digitos, usar_especiales)
        entry_resultado.config(state="normal")
        entry_resultado.delete(0, tk.END)
        entry_resultado.insert(0, contraseña)
        entry_resultado.config(state="readonly")

        if guardar_var.get():
            guardar_contraseña(contraseña, cifrar)

        btn_copiar.config(state="normal", command=lambda: copiar_portapapeles(contraseña))

        config = {
            "longitud": longitud,
            "usar_letras": usar_letras,
            "usar_digitos": usar_digitos,
            "usar_especiales": usar_especiales,
            "guardar_cifrado": cifrar,
        }
        guardar_configuracion(config)

    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Configurar ventana principal
root = tk.Tk()
root.title("Generador de Contraseñas")
root.geometry("400x300")
root.configure(bg="#000000")  # Fondo oscuro
root.resizable(False, False)

# Configuración inicial
config = cargar_configuracion()

# Tema oscuro para estilos
style = ttk.Style()
style.theme_use("default")
style.configure(
    "TButton",# boton crear
    background="#2e2e2e",  # Color de fondo del botón
    foreground="#ffffff",   # Color del texto del botón
    borderwidth=1,
    focusthickness=3,
    focuscolor="#444444",
)
style.map(
    "TButton", #boton copiar
    background=[("active", "#383838")],
    foreground=[("active", "#ffffff")],
)
style.map(
    "TCheckbutton",
    background=[("active", "#000000")],  # Mantener el fondo igual cuando está activo (sin hover)
    foreground=[("active", "#ffffff")],   # Mantener el color del texto igual cuando está activo
)
style.configure(
    "TCheckbutton",
    background="#000000",
    foreground="#ffffff",
    highlightthickness=0, 
)
style.configure(
    "TLabel", # Etiqueta
    background="#000000",
    foreground="#ffffff",
    highlightthickness=0, 
)

style.configure(
    "TFrame",
    background="#000000",  # Fondo oscuro para el frame
)

# (El resto de tu código permanece igual)





frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=True)
frame.configure(style="TFrame")  # Aplica el estilo al frame


ttk.Label(frame, text="Tamaño de la contraseña:").grid(row=0, column=0, sticky="w", pady=5)
entry_longitud = ttk.Entry(frame, width=10)
entry_longitud.insert(0, config["longitud"])
entry_longitud.grid(row=0, column=1, pady=5)

var_letras = tk.BooleanVar(value=config["usar_letras"])
var_digitos = tk.BooleanVar(value=config["usar_digitos"])
var_especiales = tk.BooleanVar(value=config["usar_especiales"])
guardar_cifrado_var = tk.BooleanVar(value=config["guardar_cifrado"])

ttk.Checkbutton(frame, text="Incluir letras", variable=var_letras).grid(row=1, column=0, sticky="w", pady=5)
ttk.Checkbutton(frame, text="Incluir dígitos", variable=var_digitos).grid(row=2, column=0, sticky="w", pady=5)
ttk.Checkbutton(frame, text="Incluir caracteres especiales", variable=var_especiales).grid(row=3, column=0, sticky="w", pady=5)

btn_generar = ttk.Button(frame, text="Generar", command=generar)
btn_generar.grid(row=5, column=0, pady=10)

btn_copiar = ttk.Button(frame, text="Copiar", state="disabled")
btn_copiar.grid(row=5, column=1, pady=10)

ttk.Label(frame, text="Contraseña generada:").grid(row=6, column=0, sticky="w", pady=5)
entry_resultado = ttk.Entry(frame, state="readonly", width=30)
entry_resultado.grid(row=6, column=1, pady=5)

guardar_var = tk.BooleanVar(value=False)
ttk.Checkbutton(frame, text="Guardar en archivo", variable=guardar_var).grid(row=7, column=0, sticky="w", pady=5)
ttk.Checkbutton(frame, text="Codificar al guardar", variable=guardar_cifrado_var).grid(row=8, column=0, sticky="w", pady=5)


root.mainloop()
