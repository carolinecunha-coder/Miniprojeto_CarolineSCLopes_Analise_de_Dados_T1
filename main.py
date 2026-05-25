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

# Produto
if "PR_NOME" in df.columns:

    df["PR_NOME"] = (
        df["PR_NOME"]
        .astype(str)
        .str.strip()
        .str.title()
    )

# Categoria
if "PR_CAT" in df.columns:

    df["PR_CAT"] = (
        df["PR_CAT"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

# =========================
# TRATAMENTO DE DATAS
# =========================

if "DATA" in df.columns:

    df["DATA"] = pd.to_datetime(
        df["DATA"],
        dayfirst=True,
        errors="coerce"
    )

    print("\nDatas convertidas!")

# =========================
# TRATAMENTO DE VALORES NULOS
# =========================

# Número de filhos
if "CL_FHL" in df.columns:

    mediana_filhos = df["CL_FHL"].median()

    df["CL_FHL"] = df["CL_FHL"].fillna(mediana_filhos)

    print("\nValores nulos tratados!")

# =========================
# ESTATÍSTICA DESCRITIVA
# =========================

print("\n========== ESTATÍSTICA DESCRITIVA ==========")

if "CL_FHL" in df.columns:

    print(f"\nContagem Total: {df['CL_FHL'].count()}")

    print(f"Média: {df['CL_FHL'].mean():.2f}")

    print(f"Mediana: {df['CL_FHL'].median():.2f}")

    print(f"Desvio Padrão: {df['CL_FHL'].std():.2f}")

    print(f"Moda: {df['CL_FHL'].mode()[0]}")

    print(f"Mínimo: {df['CL_FHL'].min()}")

    print(f"Máximo: {df['CL_FHL'].max()}")

    print(f"Quartil 1 (25%): {df['CL_FHL'].quantile(0.25)}")

    print(f"Quartil 2 (50%): {df['CL_FHL'].quantile(0.50)}")

    print(f"Quartil 3 (75%): {df['CL_FHL'].quantile(0.75)}")

# =========================
# AGRUPAMENTOS
# =========================

print("\n========== AGRUPAMENTOS ==========")

# Compras por gênero
if "CL_GENERO" in df.columns:

    compras_genero = (
        df.groupby("CL_GENERO")
        .size()
        .reset_index(name="Qtd_Compras")
    )

    print("\nCompras por Gênero:")

    print(compras_genero)

# Volume por categoria
if "PR_CAT" in df.columns:

    categorias = (
        df.groupby("PR_CAT")
        .size()
        .reset_index(name="Total_Registros")
    )

    print("\nVolume por Categoria:")

    print(categorias)

# =========================
# CRIAÇÃO DOS GRÁFICOS
# =========================

# -------------------------
# GRÁFICO 1 - CATEGORIAS
# -------------------------

if "PR_CAT" in df.columns:

    categorias_grafico = df["PR_CAT"].value_counts()

    plt.figure(figsize=(10, 5))

    categorias_grafico.plot(kind="bar")

    plt.title("Quantidade por Categoria")

    plt.ylabel("Quantidade")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig("imagens/grafico_categoria.png")

    plt.show()

    print("\nGráfico de categorias salvo!")

# -------------------------
# GRÁFICO 2 - PRODUTOS
# -------------------------

if "PR_NOME" in df.columns:

    produtos_grafico = df["PR_NOME"].value_counts().head(10)

    plt.figure(figsize=(12, 5))

    produtos_grafico.plot(kind="bar")

    plt.title("Top 10 Produtos")

    plt.ylabel("Quantidade")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig("imagens/grafico_produtos.png")

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
