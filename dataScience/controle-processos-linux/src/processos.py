#!/usr/bin/python3
import tkinter as tk

from gerarTela import gerarTela

def minimizar():
  root.iconify()  # Minimiza a janela

def sair():
  root.quit()  # Fecha a janela

# Cria a janela principal
root = tk.Tk()

frame_buttons = tk.Frame(root)
frame_buttons.pack(fill=tk.X, padx=10, pady=5)

btn_sair = tk.Button(frame_buttons, text="X", command=sair)
btn_sair.pack(side=tk.RIGHT, padx=5)

btn_minimizar = tk.Button(frame_buttons, text="_", command=minimizar)
btn_minimizar.pack(side=tk.RIGHT, padx=5)

gerarTela(root)

# Inicia o loop principal da interface
root.mainloop()
