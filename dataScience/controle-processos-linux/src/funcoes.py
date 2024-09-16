#!/usr/bin/python3
import json
import os
import pandas as pd

def ler_json(caminho_arquivo):
    # Verifica se o arquivo existe
    if not os.path.exists(caminho_arquivo):
        # Arquivo não existe, retorna um DataFrame vazio
        return pd.DataFrame()
    
    # Tenta abrir e ler o arquivo
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
    except json.JSONDecodeError:
        # Arquivo vazio ou corrompido, retorna um DataFrame vazio
        return pd.DataFrame()
    
    # Verifica se dados é uma lista (múltiplos registros) ou um dicionário (único registro)
    if isinstance(dados, list):
        # Se for uma lista, retorna todos os registros como DataFrame
        return pd.DataFrame(dados)
    else:
        # Se for um único registro, transforma em lista de um item para criar DataFrame
        return pd.DataFrame([dados])

def lerDados():
    # Exemplo de uso
    caminho_arquivo = '/opt/processos/dados/dados.json'
    df = ler_json(caminho_arquivo)
    return df

def salvarDados(df):
    # Converte o DataFrame para JSON com a orientação correta
    dados_json = df.to_json(orient='records', indent=4)
    with open('/opt/processos/dados/dados.json', 'w', encoding='utf-8') as f:
        f.write(dados_json)

# Função para apagar um dado com base no ID e atualizar o JSON
def apagarDado(id):
    df = lerDados()
    df = df[df['id'] != id]  # Remove a linha com o ID especificado
    salvarDados(df)
    print(f"Dado com ID {id} apagado com sucesso.")

def ultimoID(dados):
    if dados.empty:
        maior_id = 0
    else:
        maior_id = dados['id'].max()

    informacoes = {
        'id': maior_id + 1,
        'cpf': '',
        'nome': '',
        'telefone': '',
        'whatsapp': False,
        'meu_inss': False,
        'senha_meu_inss': '',
        'numero_processo': '',
        'tipo_processo': '',
        'vara_processo': '',
        'distribuicao': '',
        'autor': '',
        'reu': '',
        'movimentacao': ''
    }
    return informacoes

