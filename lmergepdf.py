# pdf_concatenador.py
import os
import sys
import platform
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2

# ------------------------------------------------------------------
# Utilidades
# ------------------------------------------------------------------
def resource_path(relative_path: str) -> str:
    """
    Devuelve la ruta absoluta del recurso tanto si se ejecuta el script
    normalmente como si está congelado con PyInstaller.
    """
    if getattr(sys, "frozen", False):          # Ejecutable PyInstaller
        base_path = sys._MEIPASS              # pylint: disable=protected-access
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def centrar_ventana(ventana: tk.Tk | tk.Toplevel, ancho: int, alto: int) -> None:
    """Centra la ventana en la pantalla según las dimensiones dadas."""
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


# ------------------------------------------------------------------
# Ventana principal
# ------------------------------------------------------------------
app = tk.Tk()
app.title("Concatenar PDFs")

ICONO = resource_path("icono_personalizado.ico")
try:
    app.iconbitmap(ICONO)
except tk.TclError:
    # Si algo va mal con el ícono, continuamos sin interrumpir la app
    pass

# Centrar la ventana principal (tamaño adaptable)
VENTANA_ANCHO, VENTANA_ALTO = 750, 520
centrar_ventana(app, VENTANA_ANCHO, VENTANA_ALTO)

archivos_seleccionados: list[str] = []

# ------------------------------------------------------------------
# Callbacks
# ------------------------------------------------------------------
def seleccionar_archivos():
    archivos = filedialog.askopenfilenames(
        title="Seleccionar archivos PDF", filetypes=[("PDF files", "*.pdf")]
    )
    for archivo in archivos:
        if archivo not in archivos_seleccionados:
            archivos_seleccionados.append(archivo)
            lista_archivos.insert(tk.END, archivo)


def eliminar_archivo():
    seleccion = lista_archivos.curselection()
    if seleccion:
        indice = seleccion[0]
        archivos_seleccionados.pop(indice)
        lista_archivos.delete(indice)


def mover_arriba():
    seleccion = lista_archivos.curselection()
    if seleccion:
        idx = seleccion[0]
        if idx > 0:
            archivos_seleccionados[idx - 1], archivos_seleccionados[idx] = (
                archivos_seleccionados[idx],
                archivos_seleccionados[idx - 1],
            )
            actualizar_lista()
            lista_archivos.select_set(idx - 1)


def mover_abajo():
    seleccion = lista_archivos.curselection()
    if seleccion:
        idx = seleccion[0]
        if idx < len(archivos_seleccionados) - 1:
            archivos_seleccionados[idx + 1], archivos_seleccionados[idx] = (
                archivos_seleccionados[idx],
                archivos_seleccionados[idx + 1],
            )
            actualizar_lista()
            lista_archivos.select_set(idx + 1)


def actualizar_lista():
    lista_archivos.delete(0, tk.END)
    for archivo in archivos_seleccionados:
        lista_archivos.insert(tk.END, archivo)


def abrir_pdf():
    seleccion = lista_archivos.curselection()
    if not seleccion:
        messagebox.showwarning("Advertencia", "Selecciona un archivo de la lista.")
        return

    archivo = archivos_seleccionados[seleccion[0]]
    try:
        if platform.system() == "Windows":
            os.startfile(archivo)  # type: ignore[attr-defined]
        elif platform.system() == "Darwin":  # macOS
            subprocess.call(["open", archivo])
        else:  # Linux, etc.
            subprocess.call(["xdg-open", archivo])
    except Exception as exc:  # noqa: BLE001
        messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{exc}")


def concatenar_archivos():
    if not archivos_seleccionados:
        messagebox.showwarning("Advertencia", "No hay archivos en la lista.")
        return

    salida = filedialog.asksaveasfilename(
        title="Guardar PDF concatenado como", defaultextension=".pdf"
    )
    if not salida:
        return

    try:
        pdf_merger = PyPDF2.PdfMerger()
        for archivo in archivos_seleccionados:
            pdf_merger.append(archivo)
        pdf_merger.write(salida)
        pdf_merger.close()
        messagebox.showinfo("Éxito", f"PDF guardado como:\n{salida}")
        app.destroy()
    except Exception as exc:  # noqa: BLE001
        messagebox.showerror("Error", f"Ocurrió un error:\n{exc}")


def mostrar_about():
    ventana_about = tk.Toplevel(app)
    ventana_about.title("Acerca de")
    try:
        ventana_about.iconbitmap(ICONO)
    except tk.TclError:
        pass

    ANCHO, ALTO = 500, 300
    centrar_ventana(ventana_about, ANCHO, ALTO)

    texto = (
        "Desarrollado por Manuel Alvaro Pacheco Hoyo\n"
        "Utilizando ChatGPT\n"
        "Fecha: 26 de mayo de 2025\n\n"
        "Cita:\n"
        "OpenAI. (2024). ChatGPT (GPT-4). https://chat.openai.com/"
    )

    label_about = tk.Label(
        ventana_about,
        text=texto,
        justify="left",
        wraplength=ANCHO - 40,
        padx=20,
        pady=20,
        font=("Arial", 11),
    )
    label_about.pack(expand=True, fill="both")

    boton_cerrar = tk.Button(
        ventana_about, text="Cerrar", command=ventana_about.destroy
    )
    boton_cerrar.pack(pady=10)


# ------------------------------------------------------------------
# Widgets
# ------------------------------------------------------------------
frame_botones = tk.Frame(app)
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="Seleccionar archivos PDF", command=seleccionar_archivos).grid(row=0, column=0, padx=5)
tk.Button(frame_botones, text="Eliminar seleccionado", command=eliminar_archivo).grid(row=0, column=1, padx=5)
tk.Button(frame_botones, text="Subir", command=mover_arriba).grid(row=0, column=2, padx=5)
tk.Button(frame_botones, text="Bajar", command=mover_abajo).grid(row=0, column=3, padx=5)
tk.Button(frame_botones, text="Abrir PDF seleccionado", command=abrir_pdf).grid(row=0, column=4, padx=5)
tk.Button(frame_botones, text="About", command=mostrar_about).grid(row=0, column=5, padx=5)

lista_archivos = tk.Listbox(app, width=100, height=15)
lista_archivos.pack(pady=10)

tk.Button(app, text="Concatenar PDFs en el orden mostrado", command=concatenar_archivos).pack(pady=10)

# ------------------------------------------------------------------
# ¡A ejecutar!
# ------------------------------------------------------------------
app.mainloop()
