import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plataforma de Inteligência de Vendas", layout="wide")

st.title("📊 Plataforma de Inteligência de Vendas")

st.write("Faça o upload do seu relatório de vendas para iniciar a análise.")

arquivo = st.file_uploader(
    "Envie um arquivo de vendas (Excel ou CSV)", 
    type=["xlsx", "csv"]
)

if arquivo:

    if arquivo.name.endswith(".csv"):
        df = pd.read_csv(arquivo)
    else:
        df = pd.read_excel(arquivo)

    st.subheader("Pré-visualização dos dados")
    st.dataframe(df)

    st.subheader("Informações básicas do relatório")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Quantidade de linhas", df.shape[0])

    with col2:
        st.metric("Quantidade de colunas", df.shape[1])

    colunas_numericas = df.select_dtypes(include=["number"]).columns

    if len(colunas_numericas) > 0:
        coluna = st.selectbox(
            "Selecione uma coluna numérica para visualizar",
            colunas_numericas
        )

        st.subheader("Visualização dos dados")
        st.bar_chart(df[coluna])
