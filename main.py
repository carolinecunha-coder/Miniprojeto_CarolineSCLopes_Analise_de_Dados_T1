# ==========================================
# MINI-PROJETO - ANÁLISE EXPLORATÓRIA DE DADOS
# Aluna: Caroline de Souza Cunha Lopes
# ==========================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Garantir que a pasta de imagens exista
if not os.path.exists('imagens'):
    os.makedirs('imagens')

# =========================
# LEITURA DA BASE DE DADOS
# =========================

print("Lendo base de dados...")
df = pd.read_csv("Base_Varejo.csv", sep=";", encoding="latin1")

# Remove colunas 'Unnamed' extras
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

print("\nBase carregada com sucesso!")

# =========================
# REMOÇÃO DE DUPLICIDADES
# =========================

df = df.drop_duplicates()
print("\nDuplicidades removidas!")

# =========================
# LIMPEZA DE COLUNAS E NULOS
# =========================

# Produto: Padronização
if "PR_NOME" in df.columns:
    df["PR_NOME"] = df["PR_NOME"].astype(str).str.strip().str.title()

# Categoria: Tratamento com "Sem Categoria"
if "PR_CAT" in df.columns:
    df["PR_CAT"] = df["PR_CAT"].fillna("Sem Categoria").astype(str).str.strip().str.upper()

# Tratamento de Datas
if "DATA" in df.columns:
    df["DATA"] = pd.to_datetime(df["DATA"], dayfirst=True, errors="coerce")
    print("Datas convertidas.")

# Número de filhos: Imputação pela mediana
if "CL_FHL" in df.columns:
    mediana_filhos = df["CL_FHL"].median()
    df["CL_FHL"] = df["CL_FHL"].fillna(mediana_filhos)

# =========================
# ESTATÍSTICA DESCRITIVA
# =========================

print("\n========== ESTATÍSTICA DESCRITIVA ==========")
if "CL_FHL" in df.columns:
    print(f"Média: {df['CL_FHL'].mean():.2f} | Mediana: {df['CL_FHL'].median():.2f}")
    print(f"Moda: {df['CL_FHL'].mode()[0]} | Mínimo: {df['CL_FHL'].min()} | Máximo: {df['CL_FHL'].max()}")

# =========================
# AGRUPAMENTOS
# =========================

print("\n========== AGRUPAMENTOS ==========")

if "CL_GENERO" in df.columns:
    compras_genero = df.groupby("CL_GENERO").size().reset_index(name="Qtd_Compras")
    print("\nCompras por Gênero:\n", compras_genero)

if "PR_CAT" in df.columns:
    categorias = df.groupby("PR_CAT").size().reset_index(name="Total_Registros")
    print("\nVolume por Categoria:\n", categorias)

# Análise de Recorrência (Mesmo Dia)
print("\n========== ANÁLISE DE RECORRÊNCIA (MESMO DIA) ==========")
if "CL_ID" in df.columns and "PR_NOME" in df.columns and "DATA" in df.columns:
    recorrencia_diaria = df.groupby(['CL_ID', 'PR_NOME', 'DATA']).size().reset_index(name='Frequencia_No_Dia')
    mesmo_dia = recorrencia_diaria[recorrencia_diaria['Frequencia_No_Dia'] > 1]
    
    print(f"Total de registros com compra repetida do mesmo item no mesmo dia: {len(mesmo_dia)}")
    print(mesmo_dia.head())

# =========================
# CRIAÇÃO DOS GRÁFICOS
# =========================

if "PR_CAT" in df.columns:
    plt.figure(figsize=(10, 5))
    df["PR_CAT"].value_counts().plot(kind="bar")
    plt.title("Quantidade por Categoria")
    plt.savefig("imagens/grafico_categoria.png")

if "PR_NOME" in df.columns:
    plt.figure(figsize=(12, 5))
    df["PR_NOME"].value_counts().head(10).plot(kind="bar")
    plt.title("Top 10 Produtos")
    plt.savefig("imagens/grafico_produtos.png")

# =========================
# EXPORTAÇÃO
# =========================

df.to_csv("df_limpo.csv", index=False)
print("\nProjeto finalizado e base limpa exportada para 'df_limpo.csv'!")
