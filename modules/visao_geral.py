import plotly.express as px
import pandas as pd
import streamlit as st

from utils.metricas import (
    calcular_kpis,
    calcular_variacao,
    filtrar_intervalo_meses,
    filtrar_mes_unico,
    nome_mes,
    periodo_anterior_intervalo,
    periodo_anterior_mes_unico,
)


def _formatar_moeda(valor: float) -> str:
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _formatar_percentual(valor: float) -> str:
    return f"{valor * 100:,.2f}%".replace(",", "X").replace(".", ",").replace("X", ".")


def _aplicar_filtros_secundarios(df: pd.DataFrame, fabricantes: list[str], linhas: list[str]) -> pd.DataFrame:
    df_filtrado = df.copy()

    if fabricantes:
        df_filtrado = df_filtrado[df_filtrado["fabricante"].isin(fabricantes)]

    if linhas:
        df_filtrado = df_filtrado[df_filtrado["linha"].isin(linhas)]

    return df_filtrado


def _render_kpi(titulo: str, valor_atual: str, delta_abs: str, delta_pct: str):
    st.metric(
        label=titulo,
        value=valor_atual,
        delta=f"{delta_abs} | {delta_pct}",
    )


def render_visao_geral(df_vendas: pd.DataFrame):
    st.header("Visão Geral")

    anos_disponiveis = sorted(df_vendas["ano"].dropna().unique().tolist())
    fabricantes_disponiveis = sorted(df_vendas["fabricante"].dropna().unique().tolist())
    linhas_disponiveis = sorted(df_vendas["linha"].dropna().unique().tolist())

    col_filtro_1, col_filtro_2, col_filtro_3 = st.columns([1, 1, 2])

    with col_filtro_1:
        modo_periodo = st.radio(
            "Modo de período",
            options=["Mês único", "Intervalo de meses"],
            horizontal=False,
        )

    with col_filtro_2:
        fabricantes_selecionados = st.multiselect(
            "Fabricante",
            options=fabricantes_disponiveis,
        )

    with col_filtro_3:
        linhas_selecionadas = st.multiselect(
            "Categoria",
            options=linhas_disponiveis,
        )

    df_periodo_atual = pd.DataFrame()
    df_periodo_anterior = pd.DataFrame()
    titulo_periodo = ""

    if modo_periodo == "Mês único":
        col1, col2 = st.columns(2)
        with col1:
            ano_sel = st.selectbox("Ano", options=anos_disponiveis, index=len(anos_disponiveis) - 1)
        with col2:
            meses_do_ano = sorted(df_vendas[df_vendas["ano"] == ano_sel]["mes"].dropna().unique().tolist())
            mes_sel = st.selectbox(
                "Mês",
                options=meses_do_ano,
                format_func=nome_mes,
                index=len(meses_do_ano) - 1,
            )

        df_periodo_atual = filtrar_mes_unico(df_vendas, ano_sel, mes_sel)
        ano_ant, mes_ant = periodo_anterior_mes_unico(ano_sel, mes_sel)
        df_periodo_anterior = filtrar_mes_unico(df_vendas, ano_ant, mes_ant)

        titulo_periodo = f"{nome_mes(mes_sel)}/{ano_sel}"

    else:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            ano_inicio = st.selectbox("Ano inicial", options=anos_disponiveis, index=max(len(anos_disponiveis) - 1, 0))
        with col2:
            meses_inicio = sorted(df_vendas[df_vendas["ano"] == ano_inicio]["mes"].dropna().unique().tolist())
            mes_inicio = st.selectbox("Mês inicial", options=meses_inicio, format_func=nome_mes)

        with col3:
            ano_fim = st.selectbox("Ano final", options=anos_disponiveis, index=len(anos_disponiveis) - 1)
        with col4:
            meses_fim = sorted(df_vendas[df_vendas["ano"] == ano_fim]["mes"].dropna().unique().tolist())
            mes_fim = st.selectbox(
                "Mês final",
                options=meses_fim,
                format_func=nome_mes,
                index=len(meses_fim) - 1,
            )

        if (ano_fim, mes_fim) < (ano_inicio, mes_inicio):
            st.warning("O período final não pode ser anterior ao período inicial.")
            st.stop()

        df_periodo_atual = filtrar_intervalo_meses(df_vendas, ano_inicio, mes_inicio, ano_fim, mes_fim)

        ai, mi, af, mf = periodo_anterior_intervalo(ano_inicio, mes_inicio, ano_fim, mes_fim)
        df_periodo_anterior = filtrar_intervalo_meses(df_vendas, ai, mi, af, mf)

        titulo_periodo = f"{nome_mes(mes_inicio)}/{ano_inicio} até {nome_mes(mes_fim)}/{ano_fim}"

    df_periodo_atual = _aplicar_filtros_secundarios(df_periodo_atual, fabricantes_selecionados, linhas_selecionadas)
    df_periodo_anterior = _aplicar_filtros_secundarios(df_periodo_anterior, fabricantes_selecionados, linhas_selecionadas)

    st.caption(f"Período selecionado: {titulo_periodo}")

    if df_periodo_atual.empty:
        st.warning("Não há dados para os filtros selecionados.")
        return

    kpis_atual = calcular_kpis(df_periodo_atual)
    kpis_anterior = calcular_kpis(df_periodo_anterior)

    delta_fat = calcular_variacao(kpis_atual["faturamento"], kpis_anterior["faturamento"])
    delta_lucro = calcular_variacao(kpis_atual["lucro"], kpis_anterior["lucro"])
    delta_margem = calcular_variacao(kpis_atual["margem"], kpis_anterior["margem"])
    delta_pedidos = calcular_variacao(kpis_atual["pedidos"], kpis_anterior["pedidos"])
    delta_clientes = calcular_variacao(kpis_atual["clientes"], kpis_anterior["clientes"])
    delta_skus = calcular_variacao(kpis_atual["skus"], kpis_anterior["skus"])

    c1, c2, c3 = st.columns(3)
    c4, c5, c6 = st.columns(3)

    with c1:
        _render_kpi(
            "Faturamento Bruto",
            _formatar_moeda(kpis_atual["faturamento"]),
            _formatar_moeda(delta_fat[0]),
            _formatar_percentual(delta_fat[1]),
        )

    with c2:
        _render_kpi(
            "Lucro",
            _formatar_moeda(kpis_atual["lucro"]),
            _formatar_moeda(delta_lucro[0]),
            _formatar_percentual(delta_lucro[1]),
        )

    with c3:
        _render_kpi(
            "Margem Final",
            _formatar_percentual(kpis_atual["margem"]),
            _formatar_percentual(delta_margem[0]),
            _formatar_percentual(delta_margem[1]),
        )

    with c4:
        _render_kpi(
            "Pedidos",
            f"{kpis_atual['pedidos']:,}".replace(",", "."),
            f"{delta_pedidos[0]:,.0f}".replace(",", "."),
            _formatar_percentual(delta_pedidos[1]),
        )

    with c5:
        _render_kpi(
            "Clientes",
            f"{kpis_atual['clientes']:,}".replace(",", "."),
            f"{delta_clientes[0]:,.0f}".replace(",", "."),
            _formatar_percentual(delta_clientes[1]),
        )

    with c6:
        _render_kpi(
            "SKUs Vendidos",
            f"{kpis_atual['skus']:,}".replace(",", "."),
            f"{delta_skus[0]:,.0f}".replace(",", "."),
            _formatar_percentual(delta_skus[1]),
        )

    st.divider()

    st.subheader("Tendência de vendas")

    if modo_periodo == "Mês único":
        tendencia = (
            df_periodo_atual.groupby("dia", as_index=False)["venda_bruta"]
            .sum()
            .sort_values("dia")
        )
        fig_tendencia = px.line(
            tendencia,
            x="dia",
            y="venda_bruta",
            markers=True,
            labels={"dia": "Dia", "venda_bruta": "Faturamento"},
        )
    else:
        tendencia = (
            df_periodo_atual.groupby("ano_mes", as_index=False)["venda_bruta"]
            .sum()
            .sort_values("ano_mes")
        )
        fig_tendencia = px.line(
            tendencia,
            x="ano_mes",
            y="venda_bruta",
            markers=True,
            labels={"ano_mes": "Mês", "venda_bruta": "Faturamento"},
        )

    fig_tendencia.update_layout(height=420)
    st.plotly_chart(fig_tendencia, use_container_width=True)

    col_graf_1, col_graf_2 = st.columns(2)

    with col_graf_1:
        st.subheader("Faturamento por fabricante")
        por_fabricante = (
            df_periodo_atual.groupby("fabricante", as_index=False)["venda_bruta"]
            .sum()
            .sort_values("venda_bruta", ascending=True)
        )

        fig_fabricante = px.bar(
            por_fabricante,
            x="venda_bruta",
            y="fabricante",
            orientation="h",
            labels={"venda_bruta": "Faturamento", "fabricante": "Fabricante"},
        )
        fig_fabricante.update_layout(height=450)
        st.plotly_chart(fig_fabricante, use_container_width=True)

    with col_graf_2:
        st.subheader("Faturamento por categoria")
        modo_categoria = st.radio(
            "Exibir categoria em",
            options=["Valor absoluto", "Percentual"],
            horizontal=True,
        )

        por_categoria = (
            df_periodo_atual.groupby("linha", as_index=False)["venda_bruta"]
            .sum()
            .sort_values("venda_bruta", ascending=True)
        )

        if modo_categoria == "Percentual":
            total = por_categoria["venda_bruta"].sum()
            if total != 0:
                por_categoria["participacao"] = por_categoria["venda_bruta"] / total
            else:
                por_categoria["participacao"] = 0

            fig_categoria = px.bar(
                por_categoria,
                x="participacao",
                y="linha",
                orientation="h",
                labels={"participacao": "Participação", "linha": "Categoria"},
            )
        else:
            fig_categoria = px.bar(
                por_categoria,
                x="venda_bruta",
                y="linha",
                orientation="h",
                labels={"venda_bruta": "Faturamento", "linha": "Categoria"},
            )

        fig_categoria.update_layout(height=450)
        st.plotly_chart(fig_categoria, use_container_width=True)
