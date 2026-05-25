# ==========================================
# MINI-PROJETO - ANÁLISE EXPLORATÓRIA DE DADOS
# Aluna: Caroline de Souza Cunha Lopes
# ==========================================

# =========================
# IMPORTAÇÃO DAS BIBLIOTECAS
# =========================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =========================
# LEITURA DA BASE DE DADOS
# =========================

print("Lendo base de dados...")

df = pd.read_csv("Base_Varejo.csv", sep=";", encoding="latin1")

print("\nBase carregada com sucesso!")

# =========================
# VISUALIZAÇÃO INICIAL
# =========================

print("\nPrimeiras linhas da base:")
print(df.head())

print("\nInformações gerais:")
print(df.info())

print("\nValores nulos:")
print(df.isnull().sum())

# =========================
# REMOÇÃO DE DUPLICIDADES
# =========================

df = df.drop_duplicates()

print("\nDuplicidades removidas!")

# =========================
# LIMPEZA DE COLUNAS TEXTUAIS
# =========================

# Exemplo para coluna Produto
if "Produto" in df.columns:
    df["Produto"] = df["Produto"].str.strip().str.title()

# Exemplo para coluna Categoria
if "Categoria" in df.columns:
    df["Categoria"] = df["Categoria"].str.strip().str.title()

# =========================
# TRATAMENTO DE VALORES MONETÁRIOS
# =========================

# Verifica se a coluna Valor existe
if "Valor" in df.columns:

    # Remove R$, pontos e ajusta vírgula
    df["Valor"] = (
        df["Valor"]
        .astype(str)
        .str.replace("R$", "", regex=False)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.strip()
    )

    # Converte para número
    df["Valor"] = pd.to_numeric(df["Valor"], errors="coerce")

    print("\nColuna Valor convertida com sucesso!")

# =========================
# TRATAMENTO DE DATAS
# =========================

# Verifica se existe coluna Data
if "Data" in df.columns:

    df["Data"] = pd.to_datetime(
        df["Data"],
        dayfirst=True,
        errors="coerce"
    )

    print("\nDatas convertidas!")

# =========================
# TRATAMENTO DE VALORES NULOS
# =========================

# Preenchimento da mediana para Valor
if "Valor" in df.columns:

    mediana_valor = df["Valor"].median()

    df["Valor"] = df["Valor"].fillna(mediana_valor)

    print("\nValores nulos preenchidos com mediana!")

# =========================
# ANÁLISES EXPLORATÓRIAS
# =========================

print("\n========== ANÁLISES ==========")

# Faturamento total
if "Valor" in df.columns:

    faturamento_total = df["Valor"].sum()

    print(f"\nFaturamento Total: R$ {faturamento_total:,.2f}")

# Produtos mais vendidos
if "Produto" in df.columns:

    print("\nTop 10 Produtos Mais Vendidos:")

    print(df["Produto"].value_counts().head(10))

# Faturamento por categoria
if "Categoria" in df.columns and "Valor" in df.columns:

    print("\nFaturamento por Categoria:")

    print(
        df.groupby("Categoria")["Valor"]
        .sum()
        .sort_values(ascending=False)
    )

# =========================
# CRIAÇÃO DOS GRÁFICOS
# =========================

# Gráfico 1 - Faturamento por Categoria
if "Categoria" in df.columns and "Valor" in df.columns:

    faturamento_categoria = (
        df.groupby("Categoria")["Valor"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(10, 5))

    faturamento_categoria.plot(kind="bar")

    plt.title("Faturamento por Categoria")

    plt.ylabel("Valor Total")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig("grafico_categoria.png")

    plt.show()

    print("\nGráfico de faturamento salvo!")

# Gráfico 2 - Produtos Mais Vendidos
if "Produto" in df.columns:

    top_produtos = df["Produto"].value_counts().head(10)

    plt.figure(figsize=(10, 5))

    top_produtos.plot(kind="bar")

    plt.title("Top 10 Produtos Mais Vendidos")

    plt.ylabel("Quantidade")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig("grafico_produtos.png")

    plt.show()

    print("\nGráfico de produtos salvo!")

# =========================
# EXPORTAÇÃO DA BASE LIMPA
# =========================

df.to_csv("df_limpo.csv", index=False)

print("\nBase limpa exportada com sucesso!")

# =========================
# FINALIZAÇÃO
# =========================

print("\nProjeto executado com sucesso!")
