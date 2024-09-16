#!/usr/bin/python3
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import json
import os
import pandas as pd

from funcoes import lerDados, ultimoID, salvarDados, apagarDado

pad5 = 5
pad10 = 10
pad42 = 42

def focus_next_widget(event):
  event.widget.tk_focusNext().focus_set()
  return "break"

def buscar(root, criterio, valor_busca):
  # Lê os dados do DataFrame
  df = lerDados()

  # Filtra os dados com base no critério de busca
  if not df.empty:
    if criterio and valor_busca:
      df = df[df[criterio].astype(str).str.contains(valor_busca, na=False, case=False)]

  tabela_janela = tk.Toplevel(root)
  tabela_janela.title("Resultado da Busca")

  cols = ("ID", "CPF", "Nome", "Número do Processo", "Tipo do Processo")
  tree = ttk.Treeview(tabela_janela, columns=cols, show='headings')

  for col in cols:
    tree.heading(col, text=col)
    tree.column(col, width=100)

  # Adiciona os dados filtrados na Treeview
  for index, row in df.iterrows():
    tree.insert("", "end", values=(row["id"], row["cpf"], row["nome"], row["numero_processo"], row["tipo_processo"]))

  tree.pack(expand=True, fill='both')

  def on_select(event):
    item = tree.selection()[0]
    values = tree.item(item, "values")
    # Encontra a linha completa no DataFrame correspondente ao ID selecionado
    dados_completos = df[df["id"] == int(values[0])].iloc[0].to_dict()
    
    # Preenche os campos na tela principal com os dados selecionados
    preencherCampos(dados_completos)

  tree.bind("<Double-1>", on_select)

  btn_fechar = tk.Button(tabela_janela, text="Fechar", command=tabela_janela.destroy)
  btn_fechar.pack(pady=pad10)

# Funções para os botões
def novo():
  dados = lerDados()
  novoDado = ultimoID(dados)
  preencherCampos(novoDado)

def salvar():
  # Lógica para salvar os dados
  dados = lerDados()
  id = int(entry_id.get())
  # Verifica se o ID já existe no DataFrame
  if id in dados['id'].values:
    # Atualiza o registro existente
    dados.loc[dados['id'] == id, 'cpf'] = entry_cpf.get()
    dados.loc[dados['id'] == id, 'nome'] = entry_nome.get()
    dados.loc[dados['id'] == id, 'telefone'] = entry_telefone.get()
    dados.loc[dados['id'] == id, 'whatsapp'] = whatsapp_var.get()
    dados.loc[dados['id'] == id, 'meu_inss'] = meu_inss_var.get()
    dados.loc[dados['id'] == id, 'senha_meu_inss'] = entry_senha_meu_inss.get()
    dados.loc[dados['id'] == id, 'numero_processo'] = entry_numero_processo.get()
    dados.loc[dados['id'] == id, 'tipo_processo'] = entry_tipo_processo.get()
    dados.loc[dados['id'] == id, 'vara_processo'] = entry_vara_processo.get()
    dados.loc[dados['id'] == id, 'distribuicao'] = entry_distribuicao.get()
    dados.loc[dados['id'] == id, 'autor'] = entry_autor.get()
    dados.loc[dados['id'] == id, 'reu'] = entry_reu.get()
    dados.loc[dados['id'] == id, 'movimentacao'] = text_movimentacao.get(1.0, tk.END)
  else:
    # Adiciona um novo registro caso o ID não exista
    novo_registro = pd.DataFrame([{
      'id': id,
      'cpf': entry_cpf.get(),
      'nome': entry_nome.get(),
      'telefone': entry_telefone.get(),
      'whatsapp': whatsapp_var.get(),
      'meu_inss': meu_inss_var.get(),
      'senha_meu_inss': entry_senha_meu_inss.get(),
      'numero_processo': entry_numero_processo.get(),
      'tipo_processo': entry_tipo_processo.get(),
      'vara_processo': entry_vara_processo.get(),
      'distribuicao': entry_distribuicao.get(),
      'autor': entry_autor.get(),
      'reu': entry_reu.get(),
      'movimentacao': text_movimentacao.get(1.0, tk.END)
    }])
    
    dados = pd.concat([dados, novo_registro], ignore_index=True)
  
  # Valida e salva os dados
  salvarDados(dados)
  messagebox.showinfo("Sucesso", "Dados salvos com sucesso.")
  limparCampos()  # Limpa os campos após excluir

def excluir():
  # Função para excluir um dado com confirmação
  id_dado = int(entry_id.get())
  if id_dado:
    if messagebox.askyesno("Confirmação", f"Deseja realmente excluir o registro com ID {id_dado}?"):
      apagarDado(id_dado)
      messagebox.showinfo("Sucesso", f"Registro com ID {id_dado} excluído com sucesso.")
      limparCampos()  # Limpa os campos após excluir

def limparCampos():
  entry_id.delete(0, tk.END)
  entry_cpf.delete(0, tk.END)
  entry_nome.delete(0, tk.END)
  entry_telefone.delete(0, tk.END)
  whatsapp_var.set(False)
  meu_inss_var.set(False)
  entry_senha_meu_inss.delete(0, tk.END)
  entry_numero_processo.delete(0, tk.END)
  entry_tipo_processo.delete(0, tk.END)
  entry_vara_processo.delete(0, tk.END)
  entry_distribuicao.delete(0, tk.END)
  entry_autor.delete(0, tk.END)
  entry_reu.delete(0, tk.END)
  text_movimentacao.delete(1.0, tk.END)

def preencherCampos(dados):
  limparCampos()
  entry_id.insert(0, dados['id'])
  entry_cpf.insert(0, dados['cpf'])
  entry_nome.insert(0, dados['nome'])
  entry_telefone.insert(0, dados['telefone'])
  whatsapp_var.set(dados['whatsapp'])
  meu_inss_var.set(dados['meu_inss'])
  entry_senha_meu_inss.insert(0, dados['senha_meu_inss'])
  entry_numero_processo.insert(0, dados['numero_processo'])
  entry_tipo_processo.insert(0, dados['tipo_processo'])
  entry_vara_processo.insert(0, dados['vara_processo'])
  entry_distribuicao.insert(0, dados['distribuicao'])
  entry_autor.insert(0, dados['autor'])
  entry_reu.insert(0, dados['reu'])
  text_movimentacao.insert(tk.END, dados['movimentacao'])

def gerarTela(root):
  root.title("Interface de Dados")
  root.geometry("800x600")  # Define o tamanho inicial da janela
  root.attributes('-fullscreen', True)  # Define a janela para ocupar 100% da altura da tela

  # Primeira linha: Botões
  frame_buttons_1 = tk.Frame(root)
  frame_buttons_1.pack(fill=tk.X, padx=pad10, pady=pad5)

  btn_novo = tk.Button(frame_buttons_1, text="Novo", command=lambda: novo())
  btn_novo.pack(side=tk.LEFT, padx=pad5)
  btn_novo.bind("<Tab>", focus_next_widget)

  global criterio_var, entry_busca
  criterio_var = tk.StringVar()
  criterios = [("ID", "id"), ("CPF", "cpf"), ("Nome", "nome"), ("Número Processo", "numero_processo")]

  for text, value in criterios:
    tk.Radiobutton(frame_buttons_1, text=text, variable=criterio_var, value=value).pack(side=tk.LEFT, padx=pad5)

  entry_busca = tk.Entry(frame_buttons_1, width=pad42)
  entry_busca.pack(side=tk.LEFT, padx=pad10)
  entry_busca.bind("<Tab>", focus_next_widget)

  btn_buscar = tk.Button(frame_buttons_1, text="Buscar", command=lambda: buscar(root, criterio_var.get(), entry_busca.get()))
  btn_buscar.pack(side=tk.LEFT, padx=pad5)
  btn_buscar.bind("<Tab>", focus_next_widget)

  # Segunda linha: Campos de entrada
  frame_fields_1 = tk.Frame(root)
  frame_fields_1.pack(fill=tk.X, padx=pad10, pady=pad5)

  global entry_id, entry_cpf, entry_nome, entry_telefone, whatsapp_var, meu_inss_var, entry_senha_meu_inss
  tk.Label(frame_fields_1, text="ID:").pack(side=tk.LEFT)
  entry_id = tk.Entry(frame_fields_1, width=pad5)
  entry_id.pack(side=tk.LEFT, padx=pad5)
  entry_id.bind("<Tab>", focus_next_widget)
  def txtEvent(event):
    if(event.state==12 and event.keysym=='c' ):
      return
    else:
      return "break"
  entry_id.bind("<Key>", lambda e: txtEvent(e))

  tk.Label(frame_fields_1, text="CPF:").pack(side=tk.LEFT)
  entry_cpf = tk.Entry(frame_fields_1)
  entry_cpf.pack(side=tk.LEFT, padx=pad5)
  entry_cpf.bind("<Tab>", focus_next_widget)

  tk.Label(frame_fields_1, text="Nome:").pack(side=tk.LEFT)
  entry_nome = tk.Entry(frame_fields_1, width=pad42)
  entry_nome.pack(side=tk.LEFT, padx=pad5)
  entry_nome.bind("<Tab>", focus_next_widget)

  tk.Label(frame_fields_1, text="Telefone:").pack(side=tk.LEFT)
  entry_telefone = tk.Entry(frame_fields_1)
  entry_telefone.pack(side=tk.LEFT, padx=pad5)
  entry_telefone.bind("<Tab>", focus_next_widget)

  # Terceira linha: Campos de entrada
  frame_fields_2 = tk.Frame(root)
  frame_fields_2.pack(fill=tk.X, padx=pad10, pady=pad5)

  tk.Label(frame_fields_2, text="WhatsApp:").pack(side=tk.LEFT)
  whatsapp_var = tk.BooleanVar()
  checkbox_whatsapp = tk.Checkbutton(frame_fields_2, variable=whatsapp_var)
  checkbox_whatsapp.pack(side=tk.LEFT, padx=pad5)
  checkbox_whatsapp.bind("<Tab>", focus_next_widget)

  tk.Label(frame_fields_2, text="Meu INSS:").pack(side=tk.LEFT)
  meu_inss_var = tk.BooleanVar()
  checkbox_meu_inss = tk.Checkbutton(frame_fields_2, variable=meu_inss_var)
  checkbox_meu_inss.pack(side=tk.LEFT, padx=pad5)
  checkbox_meu_inss.bind("<Tab>", focus_next_widget)

  tk.Label(frame_fields_2, text="Senha Meu INSS:").pack(side=tk.LEFT)
  entry_senha_meu_inss = tk.Entry(frame_fields_2)
  entry_senha_meu_inss.pack(side=tk.LEFT, padx=pad5)
  entry_senha_meu_inss.bind("<Tab>", focus_next_widget)

  # Quinta linha: Campos de entrada
  frame_fields_3 = tk.Frame(root)
  frame_fields_3.pack(fill=tk.X, padx=pad10, pady=pad5)

  global entry_numero_processo, entry_tipo_processo, entry_vara_processo, entry_distribuicao, entry_autor, entry_reu
  tk.Label(frame_fields_3, text="Número Processo:").pack(side=tk.LEFT)
  entry_numero_processo = tk.Entry(frame_fields_3, width=pad42)
  entry_numero_processo.pack(side=tk.LEFT, padx=pad5)
  entry_numero_processo.bind("<Tab>", focus_next_widget)

  tk.Label(frame_fields_3, text="Tipo Processo:").pack(side=tk.LEFT)
  entry_tipo_processo = tk.Entry(frame_fields_3, width=pad42)
  entry_tipo_processo.pack(side=tk.LEFT, padx=pad5)
  entry_tipo_processo.bind("<Tab>", focus_next_widget)

  tk.Label(frame_fields_3, text="Vara Processo:").pack(side=tk.LEFT)
  entry_vara_processo = tk.Entry(frame_fields_3, width=pad42)
  entry_vara_processo.pack(side=tk.LEFT, padx=pad5)
  entry_vara_processo.bind("<Tab>", focus_next_widget)

  # Sexta linha: Campos de entrada
  frame_fields_4 = tk.Frame(root)
  frame_fields_4.pack(fill=tk.X, padx=pad10, pady=pad5)

  tk.Label(frame_fields_4, text="Distribuição:").pack(side=tk.LEFT)
  entry_distribuicao = tk.Entry(frame_fields_4)
  entry_distribuicao.pack(side=tk.LEFT, padx=pad5)
  entry_distribuicao.bind("<Tab>", focus_next_widget)

  tk.Label(frame_fields_4, text="Autor:").pack(side=tk.LEFT)
  entry_autor = tk.Entry(frame_fields_4, width=pad42)
  entry_autor.pack(side=tk.LEFT, padx=pad5)
  entry_autor.bind("<Tab>", focus_next_widget)

  tk.Label(frame_fields_4, text="Réu:").pack(side=tk.LEFT)
  entry_reu = tk.Entry(frame_fields_4, width=pad42)
  entry_reu.pack(side=tk.LEFT, padx=pad5)
  entry_reu.bind("<Tab>", focus_next_widget)

  # Setima linha: Campo de movimentação
  frame_movimentacao = tk.Frame(root)
  frame_movimentacao.pack(fill=tk.BOTH, expand=True, padx=pad10, pady=pad5)

  tk.Label(frame_movimentacao, text="Movimentação:").pack(anchor='nw')
  global text_movimentacao
  text_movimentacao = tk.Text(frame_movimentacao)
  text_movimentacao.pack(fill=tk.BOTH, expand=True)
  text_movimentacao.bind("<Tab>", focus_next_widget)

  # Quinta linha: Botões
  frame_buttons_2 = tk.Frame(root)
  frame_buttons_2.pack(fill=tk.X, padx=pad10, pady=pad5)

  btn_salvar = tk.Button(frame_buttons_2, text="Salvar", command=lambda: salvar())
  btn_salvar.pack(side=tk.RIGHT, padx=pad5)

  btn_excluir = tk.Button(frame_buttons_2, text="Excluir", command=lambda: excluir())
  btn_excluir.pack(side=tk.RIGHT, padx=pad5)
