import streamlit as st
import pandas as pd

# 1. ESTILO CORPORATIVO (AZUL E BRANCO - LIMPO)
st.set_page_config(page_title="KOMATSU PANELTRACK", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6 !important; }
    h1, h2, h3 { color: #004a99 !important; font-family: 'Segoe UI', sans-serif; }
    .stMetric { background-color: #ffffff; border-radius: 10px; padding: 15px; border: 1px solid #d1d5db; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    div[data-testid="stMetricValue"] { color: #004a99 !important; font-weight: bold; }
    label { color: #374151 !important; font-weight: bold !important; }
    button { background-color: #004a99 !important; color: white !important; font-weight: bold !important; border-radius: 5px !important; height: 3em; }
    .stTable { background-color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. BANCO DE DADOS (22 FAMÍLIAS) - COM MEMÓRIA
if 'estoque' not in st.session_state:
    st.session_state.estoque = [
        {"code": "GA042", "name": "cofre externo", "cat": "COMMON", "per": 23, "racks": 59},
        {"code": "GA041", "name": "cofre interno", "cat": "COMMON", "per": 46, "racks": 29},
        {"code": "GA037", "name": "painel dash", "cat": "COMMON", "per": 100, "racks": 12},
        {"code": "GA038", "name": "assoalho intermediário", "cat": "COMMON", "per": 20, "racks": 55},
        {"code": "GA059", "name": "Porta ext Traseira LE NB4", "cat": "NB", "per": 24, "racks": 13},
        {"code": "GA060", "name": "Porta ext Traseira LD NB4", "cat": "NB", "per": 24, "racks": 27},
        {"code": "GA057", "name": "Porta int Dianteira LE", "cat": "COMMON", "per": 40, "racks": 31},
        {"code": "GA058", "name": "Porta int Dianteira LD", "cat": "COMMON", "per": 40, "racks": 36},
        {"code": "GA065", "name": "Porta int Traseira LE HB5", "cat": "HB", "per": 40, "racks": 28},
        {"code": "GA066", "name": "Porta int traseira LD HB5", "cat": "HB", "per": 40, "racks": 29},
        {"code": "GA051", "name": "Lateral interna LE", "cat": "HB", "per": 50, "racks": 23},
        {"code": "GA052", "name": "Lateral interna LD", "cat": "HB", "per": 50, "racks": 27},
        {"code": "GA063", "name": "Porta ext Traseira LE HB5", "cat": "HB", "per": 24, "racks": 64},
        {"code": "GA064", "name": "Porta ext Traseira LD HB5", "cat": "HB", "per": 24, "racks": 76},
        {"code": "GA055", "name": "Porta ext Dianteira LE", "cat": "COMMON", "per": 24, "racks": 90},
        {"code": "GA056", "name": "Porta ext Dianteira LD", "cat": "COMMON", "per": 24, "racks": 103},
        {"code": "GA061", "name": "Porta int traseira LE NB4", "cat": "NB", "per": 40, "racks": 14},
        {"code": "GA062", "name": "Porta int traseira LD NB4", "cat": "NB", "per": 40, "racks": 15},
        {"code": "GA035", "name": "assoalho dianteiro LE", "cat": "COMMON", "per": 100, "racks": 36},
        {"code": "GA036", "name": "assoalho dianteiro LD", "cat": "COMMON", "per": 100, "racks": 38},
        {"code": "GA040", "name": "assoalho traseiro HB5", "cat": "HB", "per": 50, "racks": 65},
        {"code": "GA039", "name": "assoalho traseiro NB4", "cat": "NB", "per": 40, "racks": 33}
    ]

# 3. INTERFACE
st.title("📊 Painel Track - Inventário Komatsu")

df = pd.DataFrame(st.session_state.estoque)
total_pecas = (df['racks'] * df['per']).sum()
cobertura = total_pecas / 63 

c1, c2 = st.columns(2)
c1.metric("Estoque Total (Peças)", f"{int(total_pecas):,}")
c2.metric("Cobertura Média", f"{cobertura:.1f} Horas")

st.markdown("---")

# 4. ATUALIZAÇÃO RÁPIDA
st.subheader("📝 Atualizar Contagem de Racks")
with st.container():
    opcoes = [f"{i['code']} - {i['name']}" for i in st.session_state.estoque]
    escolha = st.selectbox("Selecione o Item:", opcoes)
    novo_rack = st.number_input("Quantidade Atual de Racks:", min_value=0, step=1)
    
    if st.button("CONFIRMAR ATUALIZAÇÃO"):
        cod_ref = escolha.split(" - ")[0]
        for item in st.session_state.estoque:
            if item['code'] == cod_ref:
                item['racks'] = novo_rack
        st.success(f"Estoque de {escolha} atualizado!")
        st.rerun()

# 5. TABELA GERAL
st.subheader("📋 Relatório Completo")
df_vis = pd.DataFrame(st.session_state.estoque)
df_vis['Total Peças'] = df_vis['racks'] * df_vis['per']
st.table(df_vis[['code', 'name', 'racks', 'Total Peças']])
