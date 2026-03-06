import streamlit as st
import pandas as pd

# 1. Configuração de Visibilidade Total (Preto e Amarelo - Alto Contraste)
st.set_page_config(page_title="KOMATSU PANELTRACK", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #000 !important; }
    h1, h2, h3, p, b, label, .stMetric { color: #FFFF00 !important; font-family: sans-serif; }
    div[data-testid="stMetricValue"] { color: white !important; font-size: 3rem !important; }
    input { background-color: #222 !important; color: white !important; border: 2px solid #FF0 !important; }
    button { background-color: #FF0 !important; color: #000 !important; font-weight: bold !important; width: 100%; height: 3em; }
    </style>
    """, unsafe_allow_html=True)

# 2. Banco de Dados COMPLETO (Todas as 22 famílias)
if 'dados' not in st.session_state:
    st.session_state.dados = [
        {"id": "7", "code": "GA042", "name": "cofre externo", "cat": "COMMON", "per": 23, "racks": 59},
        {"id": "8", "code": "GA041", "name": "cofre interno", "cat": "COMMON", "per": 46, "racks": 29},
        {"id": "3", "code": "GA037", "name": "painel dash", "cat": "COMMON", "per": 100, "racks": 12},
        {"id": "4", "code": "GA038", "name": "assoalho intermediário", "cat": "COMMON", "per": 20, "racks": 55},
        {"id": "15", "code": "GA059", "name": "Porta ext Traseira LE NB4", "cat": "NB", "per": 24, "racks": 13},
        {"id": "16", "code": "GA060", "name": "Porta ext Traseira LD NB4", "cat": "NB", "per": 24, "racks": 27},
        {"id": "13", "code": "GA057", "name": "Porta int Dianteira LE", "cat": "COMMON", "per": 40, "racks": 31},
        {"id": "14", "code": "GA058", "name": "Porta int Dianteira LD", "cat": "COMMON", "per": 40, "racks": 36},
        {"id": "21", "code": "GA065", "name": "Porta int Traseira LE HB5", "cat": "HB", "per": 40, "racks": 28},
        {"id": "22", "code": "GA066", "name": "Porta int traseira LD HB5", "cat": "HB", "per": 40, "racks": 29},
        {"id": "9", "code": "GA051", "name": "Lateral interna LE", "cat": "HB", "per": 50, "racks": 23},
        {"id": "10", "code": "GA052", "name": "Lateral interna LD", "cat": "HB", "per": 50, "racks": 27},
        {"id": "19", "code": "GA063", "name": "Porta ext Traseira LE HB5", "cat": "HB", "per": 24, "racks": 64},
        {"id": "20", "code": "GA064", "name": "Porta ext Traseira LD HB5", "cat": "HB", "per": 24, "racks": 76},
        {"id": "11", "code": "GA055", "name": "Porta ext Dianteira LE", "cat": "COMMON", "per": 24, "racks": 90},
        {"id": "12", "code": "GA056", "name": "Porta ext Dianteira LD", "cat": "COMMON", "per": 24, "racks": 103},
        {"id": "17", "code": "GA061", "name": "Porta int traseira LE NB4", "cat": "NB", "per": 40, "racks": 14},
        {"id": "18", "code": "GA062", "name": "Porta int traseira LD NB4", "cat": "NB", "per": 40, "racks": 15},
        {"id": "1", "code": "GA035", "name": "assoalho dianteiro LE", "cat": "COMMON", "per": 100, "racks": 36},
        {"id": "2", "code": "GA036", "name": "assoalho dianteiro LD", "cat": "COMMON", "per": 100, "racks": 38},
        {"id": "6", "code": "GA040", "name": "assoalho traseiro HB5", "cat": "HB", "per": 50, "racks": 65},
        {"id": "5", "code": "GA039", "name": "assoalho traseiro NB4", "cat": "NB", "per": 40, "racks": 33}
    ]

# 3. Cabeçalho e Cálculos
st.title("🚜 KOMATSU - PAINEL DE ESTOQUE")

df = pd.DataFrame(st.session_state.dados)
total_pecas = (df['racks'] * df['per']).sum()
cobertura = total_pecas / 63 # JPH Médio

c1, c2 = st.columns(2)
c1.metric("TOTAL PEÇAS", f"{int(total_pecas):,}")
c2.metric("COBERTURA MÉDIA", f"{cobertura:.1f}h")

st.divider()

# 4. Área de Edição (SIMPLIFICADA PARA CELULAR)
st.subheader("📝 ATUALIZAR RACKS")
lista_nomes = [f"{i['code']} - {i['name']}" for i in st.session_state.dados]
escolha = st.selectbox("Selecione a Peça:", lista_nomes)
novo_valor = st.number_input("Quantidade de Racks:", min_value=0, step=1)

if st.button("SALVAR AGORA"):
    codigo = escolha.split(" - ")[0]
    for item in st.session_state.dados:
        if item['code'] == codigo:
            item['racks'] = novo_valor
    st.success("✅ Atualizado com sucesso!")
    st.rerun()

# 5. Relatório Geral (Visão de todas as famílias)
st.subheader("📋 RELATÓRIO COMPLETO")
df_rep = pd.DataFrame(st.session_state.dados)
df_rep['Peças'] = df_rep['racks'] * df_rep['per']
st.table(df_rep[['code', 'name', 'racks', 'Peças']])
