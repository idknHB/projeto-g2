
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==================================================
# CONFIGURAÇÃO DA PÁGINA
# ==================================================

st.set_page_config(
    page_title="Dashboard Climático do Brasil",
    page_icon="🌎",
    layout="wide"
)

# ==================================================
# CARREGAMENTO DOS DADOS
# ==================================================

@st.cache_data
def carregar_dados():
    df = pd.read_csv("simulacao_clima_brasil.csv")

    df["data"] = pd.to_datetime(df["data"])

    return df

df = carregar_dados()

# ==================================================
# TÍTULO
# ==================================================

st.title("🌎 Dashboard Climático Brasileiro")

st.markdown("""
Análise de dados climáticos das regiões brasileiras entre 2015 e 2025.

O objetivo deste projeto é identificar padrões de temperatura,
chuvas, umidade e eventos extremos ao longo do tempo.
""")

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header("Filtros")

anos = sorted(df["ano"].unique())
regioes = sorted(df["regiao"].unique())
ufs = sorted(df["uf"].unique())

ano = st.sidebar.multiselect(
    "Ano",
    anos,
    default=anos
)

regiao = st.sidebar.multiselect(
    "Região",
    regioes,
    default=regioes
)

uf = st.sidebar.multiselect(
    "UF",
    ufs,
    default=ufs
)

# ==================================================
# FILTRO
# ==================================================

df_filtrado = df[
    (df["ano"].isin(ano)) &
    (df["regiao"].isin(regiao)) &
    (df["uf"].isin(uf))
]

# ==================================================
# KPIs
# ==================================================

st.subheader("📈 Indicadores Principais")

col1, col2, col3, col4 = st.columns(4)

temp_media = df_filtrado["temperatura_media"].mean()
chuva_total = df_filtrado["chuva_mm"].sum()
umidade_media = df_filtrado["umidade"].mean()
eventos = df_filtrado["eventos_extremos"].sum()

col1.metric(
    "🌡 Temperatura Média",
    f"{temp_media:.1f} °C"
)

col2.metric(
    "🌧 Chuva Total",
    f"{chuva_total:,.0f} mm"
)

col3.metric(
    "💧 Umidade Média",
    f"{umidade_media:.1f}%"
)

col4.metric(
    "⚠ Eventos Extremos",
    f"{eventos}"
)

st.divider()

# ==================================================
# ABAS
# ==================================================

aba1, aba2, aba3, aba4 = st.tabs([
    "Temperatura",
    "Chuvas",
    "Eventos",
    "Dados"
])

# ==================================================
# ABA TEMPERATURA
# ==================================================

with aba1:

    st.subheader("Temperatura Média por Ano")

    temp_ano = (
        df_filtrado
        .groupby("ano")["temperatura_media"]
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10,5))

    sns.lineplot(
        data=temp_ano,
        x="ano",
        y="temperatura_media",
        marker="o",
        ax=ax
    )

    ax.set_ylabel("Temperatura (°C)")
    ax.set_xlabel("Ano")

    st.pyplot(fig)

    st.subheader("Distribuição por Região")

    fig, ax = plt.subplots(figsize=(10,5))

    sns.boxplot(
        data=df_filtrado,
        x="regiao",
        y="temperatura_media",
        ax=ax
    )

    st.pyplot(fig)

# ==================================================
# ABA CHUVAS
# ==================================================

with aba2:

    st.subheader("Média de Chuva por Região")

    chuva_regiao = (
        df_filtrado
        .groupby("regiao")["chuva_mm"]
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10,5))

    sns.barplot(
        data=chuva_regiao,
        x="regiao",
        y="chuva_mm",
        ax=ax
    )

    st.pyplot(fig)

    st.subheader("Chuva ao Longo do Tempo")

    chuva_ano = (
        df_filtrado
        .groupby("ano")["chuva_mm"]
        .mean()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10,5))

    sns.lineplot(
        data=chuva_ano,
        x="ano",
        y="chuva_mm",
        marker="o",
        ax=ax
    )

    st.pyplot(fig)

# ==================================================
# ABA EVENTOS
# ==================================================

with aba3:

    st.subheader("Eventos Extremos por Região")

    eventos_regiao = (
        df_filtrado
        .groupby("regiao")["eventos_extremos"]
        .sum()
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(10,5))

    sns.barplot(
        data=eventos_regiao,
        x="regiao",
        y="eventos_extremos",
        ax=ax
    )

    st.pyplot(fig)

    st.subheader("Mapa de Correlação")

    corr = (
        df_filtrado
        .select_dtypes(include="number")
        .corr()
    )

    fig, ax = plt.subplots(figsize=(10,6))

    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm",
        ax=ax
    )

    st.pyplot(fig)

# ==================================================
# ABA DADOS
# ==================================================

with aba4:

    st.subheader("Base Filtrada")

    st.dataframe(
        df_filtrado,
        use_container_width=True
    )

    st.download_button(
        "⬇ Baixar CSV filtrado",
        df_filtrado.to_csv(index=False),
        "dados_filtrados.csv",
        "text/csv"
    )

# ==================================================
# CONCLUSÃO
# ==================================================

st.divider()

st.subheader("📋 Conclusão Executiva")

st.markdown("""
Os dados climáticos analisados permitem identificar padrões
de temperatura, chuva e ocorrência de eventos extremos nas
diferentes regiões do Brasil.

A utilização de filtros interativos possibilita explorar os
dados por região, estado e período, auxiliando na tomada de
decisão e na compreensão das tendências climáticas.
""")
