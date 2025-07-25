import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "processed" / "all_coins.parquet"


@st.cache_data
def load_data():
    df = pd.read_parquet(DATA_PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df


st.set_page_config(page_title="Crypto ETL Dashboard", layout="wide")
st.title("📊 Criptomoedas – Análise Técnica com Dados Históricos")

df = load_data()

coin_options = df["coin"].unique().tolist()
selected_coin = st.sidebar.selectbox("🪙 Selecione a moeda", coin_options)
selected_window = st.sidebar.selectbox("📈 Janela de Tempo da Volatilidade", [
                                       "7", "14", "30", "90", "180", "365"])
coin_df = df[df["coin"] == selected_coin].copy()

# ───────── KPIs ─────────
if len(coin_df) < 30:
    st.warning("⛔ Dados insuficientes para exibir métricas dessa moeda.")
else:
    last_row = coin_df.iloc[-1]
    price = last_row["price"]
    return_pct = last_row["return_from_start"] * 100
    max_drawdown = coin_df["drawdown"].min() * 100
    vol_avg = coin_df[f"volatility_{selected_window}d"].mean()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Preço atual", f"R$ {price:,.2f}")
    col1.caption("Último preço registrado da moeda no período analisado.")

    col2.metric("📈 Retorno total", f"{return_pct:.2f} %")
    col2.caption("Variação percentual do preço desde o início do período.")

    col3.metric("🔻 Máx. Drawdown", f"{max_drawdown:.2f} %")
    col3.caption("Maior queda percentual desde o topo. Mede o pior tombo.")

    col4.metric("📊 Volatilidade média", f"{vol_avg:.2f}")
    col4.caption("Oscilação média do preço nos últimos dias selecionados.")

# ───────── GRÁFICO DE PREÇO COM MÉDIAS ─────────
st.markdown("---")
st.subheader("📈 Preço e Médias Móveis")

if coin_df["price"].notna().sum() < 10:
    st.warning("📉 Sem dados suficientes para exibir gráfico de preço.")
else:
    fig_price = go.Figure()
    fig_price.add_trace(go.Scatter(x=coin_df["timestamp"], y=coin_df["price"],
                                   mode="lines", name="Preço", line=dict(color="blue")))
    for w in [7, 14, 30, 90, 180, 365]:
        colname = f"ma_{w}d"
        if colname in coin_df.columns and coin_df[colname].notna().sum() > 5:
            fig_price.add_trace(go.Scatter(
                x=coin_df["timestamp"],
                y=coin_df[colname],
                mode="lines",
                name=f"Média {w}d",
                line=dict(dash="dot")
            ))
    fig_price.update_layout(
        title="Variação do preço da moeda ao longo do tempo, com médias móveis suavizando a tendência.",
        height=400
    )
    st.plotly_chart(fig_price, use_container_width=True)

# ───────── VOLATILIDADE ─────────
st.markdown("---")
st.subheader("📉 Volatilidade")

vol_col = f"volatility_{selected_window}d"
if vol_col not in coin_df or coin_df[vol_col].notna().sum() < 10:
    st.warning("📊 Sem dados suficientes para exibir gráfico de volatilidade.")
else:
    fig_vol = go.Figure()
    fig_vol.add_trace(go.Scatter(x=coin_df["timestamp"], y=coin_df[vol_col],
                                 mode="lines", name="Volatilidade", line=dict(color="orange")))
    fig_vol.update_layout(
        title="Oscilação do preço em torno da média. Quanto maior, mais instável é a moeda.",
        height=300
    )
    st.plotly_chart(fig_vol, use_container_width=True)

# ───────── RETORNO ACUMULADO ─────────
st.markdown("---")
st.subheader("📈 Retorno Acumulado (%)")

if "cumulative_return" not in coin_df or coin_df["cumulative_return"].notna().sum() < 10:
    st.warning("📈 Sem dados suficientes para exibir gráfico de retorno.")
else:
    fig_ret = go.Figure()
    fig_ret.add_trace(go.Scatter(x=coin_df["timestamp"], y=coin_df["cumulative_return"] * 100,
                                 mode="lines", name="Retorno Acumulado", line=dict(color="green")))
    fig_ret.update_layout(
        title="Quanto teria rendido um investimento de R$1 desde o início do período.",
        height=300
    )
    st.plotly_chart(fig_ret, use_container_width=True)

# ───────── RETORNO DIÁRIO ─────────
st.markdown("---")
st.subheader("📊 Retorno Diário (%)")

if "daily_return" in coin_df and coin_df["daily_return"].notna().sum() > 10:
    fig_daily = go.Figure()
    fig_daily.add_trace(go.Scatter(
        x=coin_df["timestamp"],
        y=coin_df["daily_return"] * 100,
        mode="lines",
        name="Retorno Diário (%)",
        line=dict(color="purple")
    ))
    fig_daily.update_layout(
        title="Variação percentual diária. Revela instabilidade e momentos críticos.",
        height=300
    )
    st.plotly_chart(fig_daily, use_container_width=True)
else:
    st.warning("📊 Sem dados suficientes para retorno diário.")

# ───────── HEATMAP DE CORRELAÇÃO ─────────
st.markdown("---")
st.subheader("📊 Correlação entre Moedas")

df_corr = df.pivot(index="timestamp", columns="coin", values="daily_return")
df_corr = df_corr.dropna(axis=0, how="any")
correlation_matrix = df_corr.corr()

if correlation_matrix.shape[0] < 2:
    st.warning("📉 Dados insuficientes para gerar correlação.")
else:
    fig_heatmap = px.imshow(
        correlation_matrix,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale="RdBu",
        title="Correlação de Pearson entre os retornos diários. 1 = movimento idêntico, -1 = oposto.",
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
