import streamlit as st
import pandas as pd

# 1. CONFIGURAÇÃO DE CORES "ANTIFANTASMA" (FORÇANDO CONTRASTE)
st.set_page_config(page_title="KOMATSU PANELTRACK", layout="wide")

st.markdown("""
    <style>
    /* Fundo cinza claro para não cansar a vista */
    .main { background-color: #e5e7eb !important; }
    
    /* Blocos Brancos com Letras PRETAS (Forçado) */
    div[data-testid="stMetric"] {
        background-color: #ffffff !important;
        border: 2px solid #004a99 !important;
        padding: 15px !important;
        border-radius: 10px !important;
    }
    /* Forçando a cor do número e do título a ser PRETA */
    div[data-testid="stMetricValue"] > div { color: #000000 !important; font-weight: bold !important; }
    div[data-testid="stMetricLabel"] > div > p { color: #004a99 !important; font-weight: bold !important; }
    
    /* Tabelas e Textos */
    .stTable, p, span, h1, h2, h3 { color: #000000 !important; }
    
    /* Botão Azul Grande */
    button { 
        background-color: #004a99 !important; 
        color: white !important; 
        font-weight: bold !important; 
        height: 3.5em !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. BANCO DE DADOS COM AS 22 FAMÍLIAS (Mascado)
if 'estoque' not in st.session_state:
    st.session_state.estoque = [
        {"code": "GA042", "name": "cofre externo", "per": 23, "racks": 59},
        {"code": "GA041", "name": "cofre interno", "per": 46, "racks": 29},
        {"code": "GA037", "name": "painel dash", "per": 100, "racks": 12},
        {"code": "GA038", "name": "assoalho intermediário", "per": 20, "racks": 55},
        {"code": "GA059", "name": "Porta ext Traseira LE NB4", "per": 24, "racks": 13},
        {"code": "GA060", "name": "Porta ext Traseira LD NB4", "per": 24, "racks": 27},
        {"code": "GA057", "name": "Porta int Dianteira LE", "per": 40, "racks": 31},
        {"code": "GA058", "name": "Porta int Dianteira LD", "per": 40, "racks": 36},
        {"code": "GA065", "name": "Porta int Traseira LE HB5", "per": 40, "racks": 28},
        {"code": "GA066", "name": "Porta int traseira LD HB5", "per": 40, "racks": 29},
        {"code": "GA051", "name": "Lateral interna LE", "per": 50, "racks": 23},
        {"code": "GA052", "name": "Lateral interna LD", "per": 50, "racks": 27},
        {"code": "GA063", "name": "Porta ext Traseira LE HB5", "per": 24, "racks": 64},
        {"code": "GA064", "name": "Porta ext Traseira LD HB5", "per": 24, "racks": 76},
        {"code": "GA055", "name": "Porta ext Dianteira LE", "per": 24, "racks": 90},
        {"code": "GA056", "name": "Porta ext Dianteira LD", "per": 24, "racks": 103},
        {"code": "GA061", "name": "Porta int traseira LE NB4", "per": 40, "racks": 14},
        {"code": "GA062", "name": "Porta int traseira LD NB4", "per": 40, "racks": 15},
        {"code": "GA035", "name": "assoalho dianteiro LE", "per": 100, "racks": 36},
        {"code": "GA036", "name": "assoalho dianteiro LD", "per": 100, "racks": 38},
        {"code": "GA040", "name": "assoalho traseiro HB5", "per": 50, "racks": 65},
        {"code": "GA039", "name": "assoalho traseiro NB4", "per": 40, "racks": 33}
    ]

# 3. INTERFACE E CÁLCULOS
st.title("📊 Painel Track - Komatsu")

df = pd.DataFrame(st.session_state.estoque)
total_pecas = (df['racks'] * df['per']).sum()
cobertura = total_pecas / 63 

c1, c2 = st.columns(2)
c1.metric("ESTOQUE TOTAL (PEÇAS)", f"{int(total_pecas):,}")
c2.metric("COBERTURA MÉDIA (HORAS)", f"{cobertura:.1f}h")

st.markdown("---")

# 4. ATUALIZAR RACKS (Onde você edita)
st.subheader("📝 Atualizar Contagem")
lista_pecas = [f"{i['code']} - {i['name']}" for i in st.session_state.estoque]
escolha = st.selectbox("Selecione o Item:", lista_pecas)
novo_valor = st.number_input("Nova Qtd de Racks:", min_value=0, step=1)

if st.button("SALVAR ATUALIZAÇÃO"):
    codigo = escolha.split(" - ")[0]
    for item in st.session_state.estoque:
        if item['code'] == codigo:
            item['racks'] = novo_valor
    st.success("✅ Estoque Atualizado!")
    st.rerun()

# 5. TABELA FINAL
st.subheader("📋 Relatório por Família")
df_vis = pd.DataFrame(st.session_state.estoque)
df_vis['Total Peças'] = df_vis['racks'] * df_vis['per']
st.table(df_vis[['code', 'name', 'racks', 'Total Peças']])
