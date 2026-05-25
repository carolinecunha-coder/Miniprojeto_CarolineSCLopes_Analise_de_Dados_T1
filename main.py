import csv
import datetime
import numpy as np
import pandas as pd

# =========================================================================
# SPRINT 1: IMPORTAÇÃO E RECONHECIMENTO DOS DADOS
# =========================================================================
print("--- SPRINT 1: Carregando a Base de Dados Real ---")

nome_arquivo = "Base Varejo.csv/Base Varejo.csv"

try:
    # Diagnóstico estrutural rápido usando Pandas
    df_diagnostico = pd.read_csv(nome_arquivo, sep=';', on_bad_lines='skip')
    
    print(f"✅ Arquivo '{nome_arquivo}' mapeado com sucesso!")
    print(f"• Total de registros originais: {df_diagnostico.shape[0]}")
    print(f"• Colunas identificadas na base: {list(df_diagnostico.columns.values)[:10]}\n")
    
except FileNotFoundError:
    # Fallback caso o arquivo esteja solto na raiz
    nome_arquivo = "Base Varejo.csv"
    try:
        df_diagnostico = pd.read_csv(nome_arquivo, sep=';', on_bad_lines='skip')
        print(f"✅ Arquivo '{nome_arquivo}' mapeado com sucesso na raiz!")
        print(f"• Total de registros originais: {df_diagnostico.shape[0]}\n")
    except FileNotFoundError:
        print(f"❌ Erro: O arquivo '{nome_arquivo}' não foi encontrado.")


# =========================================================================
# SPRINT 2 & 3: TRATAMENTO DE NULOS E DATAS (Módulo Datetime + csv.DictReader)
# =========================================================================
print("--- SPRINT 2 & 3: Iniciando Limpeza Estruturada ---")

dados_limpos = []

# Critério 3: Leitura estruturada e nativa usando csv.DictReader
with open(nome_arquivo, mode="r", encoding="utf-8") as arquivo:
    leitor = csv.DictReader(arquivo, delimiter=';')
    
    for linha in leitor:
        # Critério 4: Lógica if/else para preencher categorias vazias (PR_CAT)
        if not linha.get("PR_CAT") or linha["PR_CAT"].strip() == "":
            linha["PR_CAT"] = "Sem Categoria"
            
        # Tratamento de nulos na coluna de número de filhos (CL_FHL)
        if not linha.get("CL_FHL") or linha["CL_FHL"].strip() == "" or linha["CL_FHL"] == "NaN":
            linha["CL_FHL"] = None  # Será tratado com a mediana logo abaixo
            
        # Critério 5: Converter a string de data utilizando o módulo datetime nativo
        data_original = linha.get("DATA")
        if data_original:
            try:
                linha["DATA"] = datetime.datetime.strptime(data_original, "%d/%m/%Y").date()
            except ValueError:
                linha["DATA"] = None

        dados_limpos.append(linha)

# Transforma a lista limpa em DataFrame para aplicar validações de negócio e regras estatísticas
df_varejo = pd.DataFrame(dados_limpos)

# Ajustando tipos numéricos
if 'PR_ID' in df_varejo.columns:
    df_varejo["Valor_Venda"] = pd.to_numeric(df_varejo["PR_ID"], errors='coerce').fillna(10.0)

df_varejo["CL_FHL"] = pd.to_numeric(df_varejo["CL_FHL"], errors='coerce')

# Preenchendo os filhos nulos com a mediana
mediana_filhos = df_varejo["CL_FHL"].median()
if pd.isna(mediana_filhos):
    mediana_filhos = 0
df_varejo["CL_FHL"] = df_varejo["CL_FHL"].fillna(mediana_filhos)

# Critério 5: Validar a regra do identificador de compra (remover duplicatas de CO_ID)
df_varejo = df_varejo.drop_duplicates(subset=["CO_ID"], keep="first")

print("✅ Processamento, limpeza e tratamento de tipos concluídos!\n")


# =========================================================================
# SPRINT 4: ESTATÍSTICA DESCRITIVA (Coluna: CL_FHL - Número de Filhos)
# =========================================================================
print("--- SPRINT 4: Estatística Descritiva (Número de Filhos) ---")

contagem = df_varejo["CL_FHL"].count()
media = df_varejo["CL_FHL"].mean()
mediana = df_varejo["CL_FHL"].median()
desvio_padrao = df_varejo["CL_FHL"].std()
minimo = df_varejo["CL_FHL"].min()
maximo = df_varejo["CL_FHL"].max()

moda_series = df_varejo["CL_FHL"].mode()
moda = moda_series[0] if not moda_series.empty else np.nan

q1 = df_varejo["CL_FHL"].quantile(0.25)
q2 = df_varejo["CL_FHL"].quantile(0.50)
q3 = df_varejo["CL_FHL"].quantile(0.75)

print(f"• Contagem Total: {contagem}")
print(f"• Média: {media:.2f}")
print(f"• Mediana: {mediana:.2f}")
print(f"• Desvio Padrão: {desvio_padrao:.2f}" if not pd.isna(desvio_padrao) else "• Desvio Padrão: 0.00")
print(f"• Moda: {moda}")
print(f"• Mínimo: {minimo}")
print(f"• Máximo: {maximo}")
print(f"• Quartil 1 (25%): {q1}")
print(f"• Quartil 2 (50%/Mediana): {q2}")
print(f"• Quartil 3 (75%): {q3}\n")


# =========================================================================
# SPRINT 5: PADRÕES DE AGRUPAMENTO (Relatório no Terminal)
# =========================================================================
print("--- SPRINT 5: Padrões de Agrupamento ---")

print("\n[Agrupamento 1] Total de Compras por Gênero do Cliente:")
agrup_genero = df_varejo.groupby("CL_GENERO").agg(
    Qtd_Compras=("CO_ID", "count")
).reset_index()
print(agrup_genero)

print("\n[Agrupamento 2] Volume de Movimentações por Categoria de Produto:")
agrup_cat = df_varejo.groupby("PR_CAT").agg(
    Total_Registros=("CO_ID", "count")
).reset_index()
print(agrup_cat)

# Salvando a base final tratada
df_varejo.to_csv("df_limpo.csv", index=False, sep=';')
print("\n✅ Script finalizado! O arquivo 'df_limpo.csv' foi gerado com sucesso.")
