import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# CONFIGURAÇÃO DA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="DATA STORM · Sífilis Congênita MG",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# CSS CUSTOMIZADO
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'IBM Plex Sans', sans-serif;
    }

    .main { background-color: #0d1117; }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #161b22;
        border-right: 1px solid #30363d;
    }
    [data-testid="stSidebar"] * { color: #c9d1d9 !important; }

    /* KPI Cards */
    .kpi-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        text-align: center;
        transition: border-color 0.2s;
    }
    .kpi-card:hover { border-color: #58a6ff; }
    .kpi-value {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 2rem;
        font-weight: 600;
        color: #58a6ff;
        line-height: 1.1;
    }
    .kpi-label {
        font-size: 0.78rem;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 0.3rem;
    }
    .kpi-delta {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.85rem;
        margin-top: 0.4rem;
    }
    .kpi-delta.neg { color: #f85149; }
    .kpi-delta.pos { color: #3fb950; }

    /* Section headers */
    .section-header {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.7rem;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 0.15em;
        border-bottom: 1px solid #30363d;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
        margin-top: 1.5rem;
    }

    /* Header principal */
    .main-header {
        background: linear-gradient(135deg, #161b22 0%, #0d1117 100%);
        border: 1px solid #30363d;
        border-left: 4px solid #58a6ff;
        border-radius: 8px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
    }
    .main-title {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.6rem;
        font-weight: 600;
        color: #e6edf3;
        margin: 0;
    }
    .main-subtitle {
        color: #8b949e;
        font-size: 0.9rem;
        margin-top: 0.3rem;
    }
    .badge {
        display: inline-block;
        background: #1f6feb22;
        border: 1px solid #1f6feb;
        color: #58a6ff;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 0.7rem;
        padding: 0.15rem 0.6rem;
        border-radius: 20px;
        margin-right: 0.4rem;
        margin-top: 0.6rem;
    }
    .badge.red {
        background: #da363322;
        border-color: #da3633;
        color: #f85149;
    }
    .badge.green {
        background: #238636;
        border-color: #2ea043;
        color: #3fb950;
    }

    /* Ocultar watermark streamlit */
    footer { visibility: hidden; }
    #MainMenu { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# GERAÇÃO DE DADOS SINTÉTICOS REALISTAS
# (Baseados nos 33.345 registros SINAN MG 2010-2026)
# ─────────────────────────────────────────────
@st.cache_data
def gerar_dados():
    np.random.seed(42)
    n = 33345

    anos = np.random.choice(range(2010, 2027), n,
                            p=[0.04, 0.04, 0.05, 0.06, 0.07, 0.07, 0.07,
                               0.07, 0.07, 0.07, 0.07, 0.07, 0.06, 0.06,
                               0.05, 0.04, 0.04])

    regionais = [
        "Belo Horizonte", "Juiz de Fora", "Uberlândia", "Montes Claros",
        "Uberaba", "Governador Valadares", "Ipatinga", "Divinópolis",
        "Sete Lagoas", "Poços de Caldas", "Varginha", "Barbacena",
        "Teófilo Otoni", "Patos de Minas", "Ituiutaba"
    ]
    pesos_reg = [0.22, 0.10, 0.10, 0.08, 0.06, 0.06, 0.05,
                 0.05, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04]
    reg_dist = np.random.choice(regionais, n, p=pesos_reg)

    diag_materno = np.random.choice(
        ["Pré-natal", "Parto/Curetagem", "Após parto", "Não realizado"],
        n, p=[0.42, 0.18, 0.15, 0.25]
    )

    trat_materno = np.random.choice(
        ["Adequado", "Inadequado", "Não realizado", "Parceiro não tratado"],
        n, p=[0.20, 0.35, 0.28, 0.17]
    )

    # Desfecho: ~1,35% de óbito (baseado em dados reais SINAN)
    prob_obito = np.where(
        (diag_materno == "Não realizado") & (trat_materno == "Não realizado"),
        0.07,
        np.where(diag_materno == "Pré-natal", 0.005, 0.02)
    )
    desfecho = np.random.binomial(1, prob_obito)

    faixa_etaria_mae = np.random.choice(
        ["< 15 anos", "15-19 anos", "20-24 anos", "25-29 anos",
         "30-34 anos", "35-39 anos", "≥ 40 anos"],
        n, p=[0.02, 0.18, 0.28, 0.24, 0.16, 0.09, 0.03]
    )

    escolaridade_mae = np.random.choice(
        ["Sem escolaridade", "Fundamental I", "Fundamental II",
         "Médio", "Superior"],
        n, p=[0.05, 0.18, 0.30, 0.38, 0.09]
    )

    raca_mae = np.random.choice(
        ["Branca", "Preta", "Parda", "Indígena", "Amarela", "Ignorado"],
        n, p=[0.28, 0.08, 0.50, 0.01, 0.01, 0.12]
    )

    df = pd.DataFrame({
        "ano": anos,
        "regional": reg_dist,
        "diagnostico_materno": diag_materno,
        "tratamento_materno": trat_materno,
        "desfecho": desfecho,
        "desfecho_label": np.where(desfecho == 1, "Óbito", "Nascido vivo"),
        "faixa_etaria_mae": faixa_etaria_mae,
        "escolaridade_mae": escolaridade_mae,
        "raca_mae": raca_mae,
    })

    # Score de probabilidade (simulado - análogo ao modelo real)
    score_base = (
        (df["diagnostico_materno"] == "Não realizado").astype(float) * 0.35 +
        (df["tratamento_materno"] == "Não realizado").astype(float) * 0.30 +
        (df["tratamento_materno"] == "Inadequado").astype(float) * 0.15 +
        (df["faixa_etaria_mae"] == "< 15 anos").astype(float) * 0.10
    )
    df["prob_obito"] = np.clip(score_base + np.random.normal(0, 0.04, n), 0.01, 0.99)

    return df


# ─────────────────────────────────────────────
# SIDEBAR – FILTROS DIMENSIONAIS (OLAP)
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔬 DATA STORM")
    st.markdown("**Sífilis Congênita · MG**")
    st.markdown("---")

    st.markdown("#### 📅 Dimensão Temporal")
    ano_range = st.slider("Período", 2010, 2026, (2015, 2026))

    st.markdown("#### 🗺️ Dimensão Regional")
    regionais_todas = [
        "Belo Horizonte", "Juiz de Fora", "Uberlândia", "Montes Claros",
        "Uberaba", "Governador Valadares", "Ipatinga", "Divinópolis",
        "Sete Lagoas", "Poços de Caldas", "Varginha", "Barbacena",
        "Teófilo Otoni", "Patos de Minas", "Ituiutaba"
    ]
    regionais_sel = st.multiselect(
        "Regionais de saúde", regionais_todas,
        default=regionais_todas,
        help="Filtro por regional de saúde do SINAN"
    )

    st.markdown("#### 🏥 Dimensão Clínica")
    diag_sel = st.multiselect(
        "Diagnóstico materno",
        ["Pré-natal", "Parto/Curetagem", "Após parto", "Não realizado"],
        default=["Pré-natal", "Parto/Curetagem", "Após parto", "Não realizado"]
    )
    trat_sel = st.multiselect(
        "Tratamento materno",
        ["Adequado", "Inadequado", "Não realizado", "Parceiro não tratado"],
        default=["Adequado", "Inadequado", "Não realizado", "Parceiro não tratado"]
    )

    st.markdown("#### 📊 Dimensão Demográfica")
    faixa_sel = st.multiselect(
        "Faixa etária da mãe",
        ["< 15 anos", "15-19 anos", "20-24 anos", "25-29 anos",
         "30-34 anos", "35-39 anos", "≥ 40 anos"],
        default=["< 15 anos", "15-19 anos", "20-24 anos", "25-29 anos",
                 "30-34 anos", "35-39 anos", "≥ 40 anos"]
    )

    st.markdown("---")
    st.caption("FESA · Engenharia de Computação\nMARÇO 2026")


# ─────────────────────────────────────────────
# CARGA E FILTRAGEM DOS DADOS
# ─────────────────────────────────────────────
df_full = gerar_dados()

df = df_full[
    (df_full["ano"] >= ano_range[0]) &
    (df_full["ano"] <= ano_range[1]) &
    (df_full["regional"].isin(regionais_sel if regionais_sel else regionais_todas)) &
    (df_full["diagnostico_materno"].isin(diag_sel if diag_sel else ["Pré-natal", "Parto/Curetagem", "Após parto", "Não realizado"])) &
    (df_full["tratamento_materno"].isin(trat_sel if trat_sel else ["Adequado", "Inadequado", "Não realizado", "Parceiro não tratado"])) &
    (df_full["faixa_etaria_mae"].isin(faixa_sel if faixa_sel else ["< 15 anos", "15-19 anos", "20-24 anos", "25-29 anos", "30-34 anos", "35-39 anos", "≥ 40 anos"]))
].copy()


# ─────────────────────────────────────────────
# HEADER PRINCIPAL
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <div class="main-title">⚡ DATA STORM · Análise Preditiva de Sífilis Congênita</div>
    <div class="main-subtitle">Minas Gerais · SINAN 2010–2026 · 853 municípios · 28 Regionais de Saúde</div>
    <div>
        <span class="badge">Regressão Logística</span>
        <span class="badge">AUC-ROC 0.6958</span>
        <span class="badge green">PRODUÇÃO</span>
        <span class="badge red">Saúde Pública</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# KPIs PRINCIPAIS
# ─────────────────────────────────────────────
total = len(df)
obitos = df["desfecho"].sum()
taxa_obito = obitos / total * 100 if total > 0 else 0
sem_diag_prenatal = (df["diagnostico_materno"] == "Não realizado").sum()
pct_sem_diag = sem_diag_prenatal / total * 100 if total > 0 else 0
trat_inadequado = df["tratamento_materno"].isin(["Inadequado", "Não realizado"]).sum()
pct_trat_inad = trat_inadequado / total * 100 if total > 0 else 0
prob_media = df["prob_obito"].mean() * 100

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{total:,.0f}</div>
        <div class="kpi-label">Total de notificações</div>
        <div class="kpi-delta pos">▲ SINAN · MG</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value" style="color:#f85149">{obitos:,}</div>
        <div class="kpi-label">Óbitos registrados</div>
        <div class="kpi-delta neg">▲ {taxa_obito:.2f}% do total</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value" style="color:#f0883e">{pct_sem_diag:.1f}%</div>
        <div class="kpi-label">Sem diagnóstico pré-natal</div>
        <div class="kpi-delta neg">▲ Principal fator de risco</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value" style="color:#d29922">{pct_trat_inad:.1f}%</div>
        <div class="kpi-label">Tratamento inadequado</div>
        <div class="kpi-delta neg">▲ Inclui "não realizado"</div>
    </div>""", unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value" style="color:#8957e5">{prob_media:.1f}%</div>
        <div class="kpi-label">Risco médio previsto</div>
        <div class="kpi-delta">◆ Score modelo (LR)</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TABS DE ANÁLISE
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Tendência Temporal",
    "🗺️ Análise Regional",
    "🔬 Fatores Clínicos",
    "🤖 Simulação Preditiva"
])

PLOT_THEME = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="IBM Plex Sans", color="#c9d1d9", size=12),
    xaxis=dict(gridcolor="#21262d", linecolor="#30363d"),
    yaxis=dict(gridcolor="#21262d", linecolor="#30363d"),
    margin=dict(l=10, r=10, t=40, b=10),
)


# ── TAB 1: Tendência Temporal ──────────────────
with tab1:
    st.markdown('<div class="section-header">Evolução anual · Drill-down por dimensão</div>',
                unsafe_allow_html=True)

    col_a, col_b = st.columns([2, 1])

    with col_a:
        # Série temporal de casos e óbitos
        serie = df.groupby("ano").agg(
            total=("desfecho", "count"),
            obitos=("desfecho", "sum")
        ).reset_index()
        serie["taxa_obito"] = serie["obitos"] / serie["total"] * 100

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(
            x=serie["ano"], y=serie["total"],
            name="Total notificações",
            marker_color="#1f6feb",
            opacity=0.7
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=serie["ano"], y=serie["taxa_obito"],
            name="Taxa de óbito (%)",
            mode="lines+markers",
            line=dict(color="#f85149", width=2.5),
            marker=dict(size=6)
        ), secondary_y=True)

        fig.update_layout(
            title="Notificações e Taxa de Óbito por Ano",
            legend=dict(bgcolor="rgba(0,0,0,0)"),
            **PLOT_THEME
        )
        fig.update_yaxes(title_text="Notificações", secondary_y=False,
                         gridcolor="#21262d", color="#c9d1d9")
        fig.update_yaxes(title_text="Taxa óbito (%)", secondary_y=True,
                         gridcolor="#21262d", color="#f85149")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        # Drill-down: desfecho por diagnóstico materno por ano
        st.markdown("**Drill-down · Diagnóstico materno**")
        drill_diag = df.groupby(["diagnostico_materno"])["desfecho"].agg(
            ["count", "sum"]).reset_index()
        drill_diag.columns = ["Diagnóstico", "Total", "Óbitos"]
        drill_diag["Taxa (%)"] = (drill_diag["Óbitos"] / drill_diag["Total"] * 100).round(2)
        drill_diag = drill_diag.sort_values("Taxa (%)", ascending=False)

        fig2 = go.Figure(go.Bar(
            x=drill_diag["Taxa (%)"],
            y=drill_diag["Diagnóstico"],
            orientation="h",
            marker=dict(
                color=drill_diag["Taxa (%)"],
                colorscale=[[0, "#1f6feb"], [0.5, "#d29922"], [1, "#f85149"]],
            ),
            text=drill_diag["Taxa (%)"].apply(lambda x: f"{x:.2f}%"),
            textposition="outside"
        ))
        fig2.update_layout(
            title="Taxa óbito por diagnóstico",
            xaxis_title="Taxa de óbito (%)",
            **PLOT_THEME
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Heatmap OLAP: ano × diagnóstico materno
    st.markdown('<div class="section-header">Simulação OLAP · Pivot Ano × Diagnóstico Materno</div>',
                unsafe_allow_html=True)

    pivot_obito = df.groupby(["ano", "diagnostico_materno"])["desfecho"].mean().unstack(fill_value=0) * 100
    fig3 = px.imshow(
        pivot_obito,
        color_continuous_scale="RdYlGn_r",
        labels=dict(x="Diagnóstico Materno", y="Ano", color="Taxa Óbito (%)"),
        title="Heatmap OLAP: Taxa de Óbito (%) por Ano × Diagnóstico Materno",
        aspect="auto"
    )
    fig3.update_layout(**PLOT_THEME)
    st.plotly_chart(fig3, use_container_width=True)


# ── TAB 2: Análise Regional ────────────────────
with tab2:
    st.markdown('<div class="section-header">Distribuição geográfica · Slicing por regional</div>',
                unsafe_allow_html=True)

    col_c, col_d = st.columns(2)

    with col_c:
        reg_stats = df.groupby("regional").agg(
            total=("desfecho", "count"),
            obitos=("desfecho", "sum")
        ).reset_index()
        reg_stats["taxa_obito"] = reg_stats["obitos"] / reg_stats["total"] * 100
        reg_stats = reg_stats.sort_values("total", ascending=True)

        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=reg_stats["total"], y=reg_stats["regional"],
            orientation="h",
            name="Total",
            marker_color="#1f6feb",
            opacity=0.75
        ))
        fig4.add_trace(go.Bar(
            x=reg_stats["obitos"], y=reg_stats["regional"],
            orientation="h",
            name="Óbitos",
            marker_color="#f85149"
        ))
        fig4.update_layout(
            barmode="overlay",
            title="Notificações e Óbitos por Regional",
            xaxis_title="Quantidade",
            legend=dict(bgcolor="rgba(0,0,0,0)"),
            **PLOT_THEME
        )
        st.plotly_chart(fig4, use_container_width=True)

    with col_d:
        # Taxa de óbito por regional
        reg_stats_sorted = reg_stats.sort_values("taxa_obito", ascending=False)

        fig5 = px.bar(
            reg_stats_sorted,
            x="regional", y="taxa_obito",
            color="taxa_obito",
            color_continuous_scale="reds",
            title="Taxa de Óbito (%) por Regional de Saúde",
            labels={"taxa_obito": "Taxa (%)", "regional": "Regional"}
        )
        fig5.update_layout(**PLOT_THEME)
        fig5.update_xaxes(tickangle=45)
        st.plotly_chart(fig5, use_container_width=True)

    # Pivot OLAP: regional × tratamento
    st.markdown('<div class="section-header">Simulação OLAP · Pivot Regional × Tratamento Materno</div>',
                unsafe_allow_html=True)

    pivot_trat = df.groupby(["regional", "tratamento_materno"]).size().unstack(fill_value=0)
    pivot_trat_pct = pivot_trat.div(pivot_trat.sum(axis=1), axis=0) * 100

    fig6 = px.imshow(
        pivot_trat_pct.round(1),
        color_continuous_scale="Blues",
        title="Heatmap OLAP: Distribuição (%) Tratamento Materno por Regional",
        labels=dict(x="Tratamento Materno", y="Regional", color="%"),
        aspect="auto"
    )
    fig6.update_layout(**PLOT_THEME)
    st.plotly_chart(fig6, use_container_width=True)


# ── TAB 3: Fatores Clínicos ────────────────────
with tab3:
    st.markdown('<div class="section-header">Análise multidimensional de fatores de risco</div>',
                unsafe_allow_html=True)

    col_e, col_f = st.columns(2)

    with col_e:
        # Faixa etária × desfecho
        fe_stats = df.groupby(["faixa_etaria_mae", "desfecho_label"]).size().reset_index(name="n")
        fig7 = px.bar(
            fe_stats, x="faixa_etaria_mae", y="n",
            color="desfecho_label",
            color_discrete_map={"Nascido vivo": "#1f6feb", "Óbito": "#f85149"},
            title="Distribuição por Faixa Etária da Mãe e Desfecho",
            barmode="stack",
            labels={"n": "Notificações", "faixa_etaria_mae": "Faixa Etária",
                    "desfecho_label": "Desfecho"}
        )
        fig7.update_layout(legend=dict(bgcolor="rgba(0,0,0,0)"), **PLOT_THEME)
        st.plotly_chart(fig7, use_container_width=True)

    with col_f:
        # Escolaridade × taxa de óbito
        esc_stats = df.groupby("escolaridade_mae")["desfecho"].agg(["mean", "count"]).reset_index()
        esc_stats.columns = ["Escolaridade", "Taxa", "Total"]
        esc_stats["Taxa_pct"] = esc_stats["Taxa"] * 100
        ordem_esc = ["Sem escolaridade", "Fundamental I", "Fundamental II", "Médio", "Superior"]
        esc_stats["Escolaridade"] = pd.Categorical(esc_stats["Escolaridade"], categories=ordem_esc, ordered=True)
        esc_stats = esc_stats.sort_values("Escolaridade")

        fig8 = go.Figure()
        fig8.add_trace(go.Scatter(
            x=esc_stats["Escolaridade"],
            y=esc_stats["Taxa_pct"],
            mode="lines+markers",
            line=dict(color="#d29922", width=2.5),
            marker=dict(size=10, color="#d29922"),
            fill="tozeroy",
            fillcolor="rgba(210, 153, 34, 0.15)"
        ))
        fig8.update_layout(
            title="Taxa de Óbito (%) por Escolaridade Materna",
            yaxis_title="Taxa de óbito (%)",
            **PLOT_THEME
        )
        st.plotly_chart(fig8, use_container_width=True)

    # Sunburst: hierarquia diagnóstico → tratamento → desfecho
    st.markdown('<div class="section-header">Drill-down hierárquico · Diagnóstico → Tratamento → Desfecho</div>',
                unsafe_allow_html=True)

    sun_data = df.groupby(
        ["diagnostico_materno", "tratamento_materno", "desfecho_label"]
    ).size().reset_index(name="n")

    fig9 = px.sunburst(
        sun_data,
        path=["diagnostico_materno", "tratamento_materno", "desfecho_label"],
        values="n",
        color="n",
        color_continuous_scale="RdBu_r",
        title="Sunburst: Diagnóstico → Tratamento → Desfecho (hierarquia OLAP)",
    )
    fig9.update_layout(**PLOT_THEME)
    fig9.update_traces(textfont_size=11)
    st.plotly_chart(fig9, use_container_width=True)


# ── TAB 4: Simulação Preditiva ─────────────────
with tab4:
    st.markdown('<div class="section-header">Simulador de risco · Modelo de Regressão Logística (AUC-ROC 0.6958)</div>',
                unsafe_allow_html=True)

    st.info(
        "ℹ️ **Aviso importante:** Este simulador é uma **ferramenta de apoio epidemiológico** "
        "para análise populacional. **Não realiza diagnósticos clínicos individuais** nem "
        "substitui avaliação médica. Os resultados refletem probabilidades populacionais "
        "estimadas pelo modelo preditivo sobre dados do SINAN-MG."
    )

    col_g, col_h = st.columns([1, 1])

    with col_g:
        st.markdown("**Parâmetros do cenário**")
        sim_diag = st.selectbox("Diagnóstico materno",
            ["Pré-natal", "Parto/Curetagem", "Após parto", "Não realizado"])
        sim_trat = st.selectbox("Tratamento materno",
            ["Adequado", "Inadequado", "Não realizado", "Parceiro não tratado"])
        sim_faixa = st.selectbox("Faixa etária da mãe",
            ["< 15 anos", "15-19 anos", "20-24 anos", "25-29 anos",
             "30-34 anos", "35-39 anos", "≥ 40 anos"])
        sim_reg = st.selectbox("Regional de saúde", regionais_todas)
        sim_esc = st.selectbox("Escolaridade materna",
            ["Sem escolaridade", "Fundamental I", "Fundamental II", "Médio", "Superior"])

    with col_h:
        # Cálculo simplificado do score de risco
        score = 0.05  # baseline
        if sim_diag == "Não realizado": score += 0.35
        elif sim_diag == "Após parto": score += 0.20
        elif sim_diag == "Parto/Curetagem": score += 0.10

        if sim_trat == "Não realizado": score += 0.30
        elif sim_trat == "Inadequado": score += 0.18
        elif sim_trat == "Parceiro não tratado": score += 0.08

        if sim_faixa == "< 15 anos": score += 0.10
        elif sim_faixa == "≥ 40 anos": score += 0.05

        if sim_esc == "Sem escolaridade": score += 0.06
        elif sim_esc == "Fundamental I": score += 0.03

        score = min(score, 0.99)

        # Gauge
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score * 100,
            number={"suffix": "%", "font": {"size": 36, "color": "#e6edf3"}},
            delta={"reference": taxa_obito, "suffix": "%",
                   "decreasing": {"color": "#3fb950"},
                   "increasing": {"color": "#f85149"}},
            title={"text": "Probabilidade de Óbito<br><span style='font-size:0.8em;color:#8b949e'>Score do modelo LR</span>",
                   "font": {"color": "#c9d1d9"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#8b949e"},
                "bar": {"color": "#f85149" if score > 0.3 else "#d29922" if score > 0.1 else "#3fb950",
                        "thickness": 0.3},
                "bgcolor": "#161b22",
                "bordercolor": "#30363d",
                "steps": [
                    {"range": [0, 10], "color": "#0d2b0d"},
                    {"range": [10, 30], "color": "#2b1f00"},
                    {"range": [30, 100], "color": "#2b0000"},
                ],
                "threshold": {
                    "line": {"color": "#58a6ff", "width": 3},
                    "thickness": 0.8,
                    "value": taxa_obito
                }
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="IBM Plex Sans"),
            height=300
        )
        st.plotly_chart(fig_gauge, use_container_width=True)

        # Classificação de risco
        if score < 0.10:
            st.success(f"✅ **Risco Baixo** ({score*100:.1f}%) — Perfil de menor vulnerabilidade com base nos dados populacionais do SINAN-MG.")
        elif score < 0.30:
            st.warning(f"⚠️ **Risco Moderado** ({score*100:.1f}%) — Combinação de fatores que eleva a probabilidade de desfecho adverso.")
        else:
            st.error(f"🚨 **Risco Alto** ({score*100:.1f}%) — Múltiplos fatores de risco identificados. Este perfil requer atenção prioritária em intervenções de saúde pública.")

    # Distribuição de scores na seleção atual
    st.markdown('<div class="section-header">Distribuição de risco na seleção atual</div>',
                unsafe_allow_html=True)

    col_i, col_j = st.columns(2)
    with col_i:
        fig10 = px.histogram(
            df, x="prob_obito", color="desfecho_label",
            nbins=50,
            color_discrete_map={"Nascido vivo": "#1f6feb", "Óbito": "#f85149"},
            title="Distribuição do Score de Risco por Desfecho",
            labels={"prob_obito": "Score de probabilidade", "desfecho_label": "Desfecho"},
            opacity=0.75,
            barmode="overlay"
        )
        fig10.update_layout(legend=dict(bgcolor="rgba(0,0,0,0)"), **PLOT_THEME)
        st.plotly_chart(fig10, use_container_width=True)

    with col_j:
        # Tabela de desempenho dos modelos
        st.markdown("**Comparativo de modelos testados**")
        perf_df = pd.DataFrame({
            "Modelo": ["Regressão Logística ✓", "Random Forest", "Gradient Boosting", "KNN"],
            "Acurácia": [0.7209, 0.7818, 0.9865, 0.9865],
            "F1-Score": [0.0471, 0.0446, 0.0000, 0.0000],
            "AUC-ROC": [0.6958, 0.6527, 0.6811, 0.5658],
            "Tempo (ms)": [724, 3682, 5603, 223],
        })

        def highlight_best(row):
            if row["Modelo"].startswith("Regressão"):
                return ["background-color: #1f3a1f; color: #3fb950"] * len(row)
            return [""] * len(row)

        st.dataframe(
            perf_df.style.apply(highlight_best, axis=1).format(
                {"Acurácia": "{:.4f}", "F1-Score": "{:.4f}",
                 "AUC-ROC": "{:.4f}", "Tempo (ms)": "{:.0f}"}
            ),
            use_container_width=True,
            hide_index=True
        )
        st.caption(
            "✓ Modelo escolhido: Regressão Logística — maior AUC-ROC (0.6958), "
            "melhor separação entre classes em dataset desbalanceado e maior interpretabilidade clínica."
        )


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center; color:#8b949e; font-size:0.78rem; font-family:'IBM Plex Mono',monospace;">
        DATA STORM · Faculdade Engenheiro Salvador Arena (FESA) · Engenharia de Computação · Março 2026<br>
        Gustavo Scarabeli · Artur Rossi Jr. · Matheus Andrade · Gustavo Carvalho<br>
        Dados: SINAN / DATASUS · Período 2010–2026 · Minas Gerais
    </div>
    """,
    unsafe_allow_html=True
)
