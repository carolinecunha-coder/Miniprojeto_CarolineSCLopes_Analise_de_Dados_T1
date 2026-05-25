# Mini-Projeto Avaliativo: Análise Exploratória de Dados (Varejo)
**Módulo 1 - Semana 07 — Análise de Dados com Python** **Aluna:** Caroline de Souza Cunha Lopes  
**Turma:** T1  

---

## 1. Instruções de Execução

O projeto foi totalmente desenvolvido e testado no ecossistema local utilizando o **VS Code**. Para reproduzir a análise e gerar os relatórios:

1. Certifique-se de possuir o Python 3.x instalado em sua máquina, juntamente com as bibliotecas `pandas` e `numpy`.
2. Garanta que o arquivo bruto `Base Varejo.csv` esteja localizado exatamente na raiz da pasta do projeto.
3. Abra o terminal do VS Code e execute o comando:
```bash
python main.py

## 2. Reflexão Teórica: O Papel Crítico do ETL e da Qualidade de Dados

O acrônimo **ETL (Extract, Transform, Load)** representa a espinha dorsal da Engenharia e da Análise de Dados moderna. Em ambientes corporativos reais, os dados brutos extraídos diretamente de sistemas de transação (como PDVs e e-commerces) são inerentemente "sujos" e instáveis, contendo ruídos operacionais, falhas de sincronismo de rede, registros duplicados por reenvio de pacotes e ausência de preenchimento em campos cadastrais.

A fase de **Transformação (Transform)** desempenha um papel científico e estratégico essencial antes de qualquer tomada de decisão:

* **Manipulação Estruturada Nativa:** A utilização do módulo `csv.DictReader` permite ler e isolar cada linha do arquivo como um dicionário estruturado de chaves e valores. Isso garante o controle granular do dado em baixo nível antes de submetê-lo a estruturas mais pesadas de memória.
* **Tipagem Temporal Rigorosa:** A conversão de strings brutas contendo formatos de data inconsistentes para objetos reais `datetime.date` padroniza a cronologia dos eventos, viabilizando análises de cohort, sazonalidade e séries temporais legítimas.
* **A Ciência do Tratamento de Nulos:** Na dimensão física `CL_FHL` (Número de Filhos), a escolha técnica de imputar a **mediana** em substituição aos valores nulos (`NaN`) mitiga as distorções causadas por possíveis *outliers* (valores extremos). Excluir as linhas reduziria o tamanho amostral de forma severa, enquanto usar a média poderia enviesar a distribuição populacional. A mediana preserva a tendência central de forma matematicamente segura.

Garantir a integridade dos dados nesta etapa evita o fenômeno conhecido como *Garbage In, Garbage Out* (Entrada de Lixo, Saída de Lixo), certificando que os dashboards de Business Intelligence reflitam fielmente a realidade da operação.

---

## 3. Relatório de Conclusões e Insights Operacionais

A execução do pipeline de dados gerou os seguintes indicadores estruturais e de negócios:

* **Insight 1 (Dominância de Portfólio):** A categoria **Alimentos** é o principal motor volumétrico do varejo analisado, acumulando expressivas **9.672 movimentações**. Em contrapartida, a categoria **Acessórios** detém a menor participação de gôndola, registrando apenas **327 operações**. Campanhas de cross-selling podem usar a alta tração de alimentos para alavancar categorias menores.
* **Insight 2 (Saneamento de Cadastro):** Foram detectadas e treated diversas linhas onde a categoria do produto encontrava-se vazia. Ao aplicar a regra de negócio condicional `if/else`, esses registros foram mapeados como **"Sem Categoria"**. Isso indica um gargalo técnico no ERP de origem, evidenciando que o campo de categoria não está configurado como obrigatório no momento do cadastro do item.
* **Insight 3 (Comportamento de Compra por Gênero):** O primeiro agrupamento estatístico automatizado isolou a volumetria de compras por gênero (`CL_GENERO`), revelando a exata distribuição de transações comerciais na base e oferecendo insumos para a personalização de jornadas de marketing.
* **Problema Remanescente 1 (Qualidade do Extrator):** A presença de delimitadores sobressalentes (como `;;;` no final de cada registro observado no arquivo bruto) aponta que o script de exportação do banco de dados relacional de origem necessita de manutenção em suas configurações de fim de linha (*End of Line*).
* **Problema Remanescente 2 (Inconsistência de IDs):** Foram identificados registros com inconsistências de caracteres em colunas identificadoras, o que exigiu blindagem de código com o argumento `errors='coerce'` para evitar a interrupção abrupta (*crash*) da aplicação durante a conversão em lote.