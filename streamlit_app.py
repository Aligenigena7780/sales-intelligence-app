import streamlit as st

from utils.carregar_dados import carregar_arquivo
from utils.preprocessamento import preprocessar_vendas, preprocessar_giro
from modules.visao_geral import render_visao_geral
from modules.clientes import render_clientes
from modules.produtos import render_produtos
from modules.oportunidades import render_oportunidades

st.set_page_config(
    page_title="Plataforma de Inteligência Comercial",
    layout="wide",
    page_icon="📊",
)

st.title("📊 Plataforma de Inteligência Comercial")

if "df_vendas" not in st.session_state:
    st.session_state.df_vendas = None

if "df_giro" not in st.session_state:
    st.session_state.df_giro = None

with st.sidebar:
    st.header("Dados")

    arquivo_vendas = st.file_uploader(
        "Upload - Relatório de Vendas",
        type=["xlsx", "xls", "csv"],
        key="upload_vendas",
    )

    arquivo_giro = st.file_uploader(
        "Upload - Relatório de Giro",
        type=["xlsx", "xls", "csv"],
        key="upload_giro",
    )

    if arquivo_vendas is not None:
        try:
            vendas_raw = carregar_arquivo(arquivo_vendas)
            st.session_state.df_vendas = preprocessar_vendas(vendas_raw)
            st.success("Relatório de vendas carregado com sucesso.")
        except Exception as e:
            st.session_state.df_vendas = None
            st.error(f"Erro ao carregar vendas: {e}")

    if arquivo_giro is not None:
        try:
            giro_raw = carregar_arquivo(arquivo_giro)
            st.session_state.df_giro = preprocessar_giro(giro_raw)
            st.success("Relatório de giro carregado com sucesso.")
        except Exception as e:
            st.session_state.df_giro = None
            st.error(f"Erro ao carregar giro: {e}")

    st.divider()
    st.header("Navegação")

    modulo = st.radio(
        "Selecione o módulo",
        options=["Visão Geral", "Clientes", "Produtos", "Oportunidades"],
        index=0,
    )

df_vendas = st.session_state.df_vendas
df_giro = st.session_state.df_giro

if df_vendas is None:
    st.info(
        "Envie o relatório de vendas na barra lateral para iniciar a análise. "
        "O relatório de giro pode ser enviado agora ou depois."
    )
    st.stop()

if modulo == "Visão Geral":
    render_visao_geral(df_vendas)

elif modulo == "Clientes":
    render_clientes(df_vendas)

elif modulo == "Produtos":
    render_produtos(df_vendas, df_giro)

elif modulo == "Oportunidades":
    render_oportunidades(df_vendas, df_giro)
