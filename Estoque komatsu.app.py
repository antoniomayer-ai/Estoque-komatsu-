import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. FUNILARIA E PINTURA (Design Premium)
st.set_page_config(page_title="KOMATSU PANELTRACK", layout="wide")

st.markdown("""
    <style>
    /* Fundo Dark Profissional */
    .stApp { background-color: #0e1117 !important; }
    
    /* Títulos e Textos */
    h1, h2, h3, p, span { color: #ffffff !important; font-family: 'Inter', sans-serif; }
    
    /* Cards de Gestão à Vista */
    .metric-card {
        background-color: #1d2129;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        border-top: 5px solid #238636; /* Verde por padrão */
    }
    .critico { border-top-color: #da3633 !important; }
    .atencao { border-top-color: #d29922 !important; }
    
    .card-code { font-weight: bold; font-size: 1.1rem; color: #58a6ff; }
    .card-name { font-size: 0.8rem; color: #8b949e; text-transform: uppercase; }
    .card-racks { font-size: 1.8rem; font-weight: bold; margin: 5px 0; }
    .card-hours { font-size: 1.1rem; font-weight: bold; }
    
    /* Botão WhatsApp Estilo Premium */
    .btn-whatsapp {
        background-color: #238636;
        color: white !important;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        text-decoration: none;
        display: block;
        font-weight: bold;
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .btn-whatsapp:hover { background-color: #2ea043; }
    </style>
    """, unsafe_allow_html=True)

# 2. DADOS COMPLETOS (AS 22 PEÇAS)
if 'estoque' not in st.session_state:
    st.session_state.estoque = [
        {"id": "1", "code": "GA035", "name": "Assoalho Diant LE", "cat": "COMMON", "per": 100, "racks": 9, "ideal": 24},
        {"id": "2", "code": "GA036", "name": "Assoalho Diant LD", "cat": "COMMON", "per": 100, "racks": 12, "ideal": 24},
        {"id": "3", "code": "GA037", "name": "Painel Dash", "cat": "COMMON", "per": 100, "racks": 12, "ideal": 24},
        {"id": "4", "code": "GA038", "name": "Assoalho Interm", "cat": "COMMON", "per": 20, "racks": 57, "ideal": 119},
        {"id": "5", "code": "GA039", "name": "Assoalho Trás NB4", "cat": "NB", "per": 40, "racks": 15, "ideal": 20},
        {"id": "6", "code": "GA040", "name": "Assoalho Trás HB5", "cat": "HB", "per": 50, "racks": 45, "ideal": 32},
        {"id": "7", "code": "GA042", "name": "Cofre Externo", "cat": "COMMON", "per": 23, "racks": 40, "ideal": 104},
        {"id": "8", "code": "GA041", "name": "Cofre Interno", "cat": "COMMON", "per": 46, "racks": 70, "ideal": 52},
        {"id": "9", "code": "GA051", "name": "Lateral Int LE", "cat": "HB", "per": 50, "racks": 19, "ideal": 32},
        {"id": "10", "code": "GA052", "name": "Lateral Int LD", "cat": "HB", "per": 50, "racks": 21, "ideal": 32},
        {"id": "11", "code": "GA055", "name": "Porta Ext Diant LE", "cat": "COMMON", "per": 24, "racks": 100, "ideal": 100},
        {"id": "12", "code": "GA056", "name": "Porta Ext Diant LD", "cat": "COMMON", "per": 24, "racks": 110, "ideal": 100},
        {"id": "13", "code": "GA057", "name": "Porta Int Diant LE", "cat": "COMMON", "per": 40, "racks": 24, "ideal": 60},
        {"id": "14", "code": "GA058", "name": "Porta Int Diant LD", "cat": "COMMON", "per": 40, "racks": 29, "ideal": 60},
        {"id": "15", "code": "GA059", "name": "Porta Ext Trás LE NB4", "cat": "NB", "per": 24, "racks": 35, "ideal": 33},
        {"id": "16", "code": "GA060", "name": "Porta Ext Trás LD NB4", "cat": "NB", "per": 24, "racks": 46, "ideal": 33},
        {"id": "17", "code": "GA061", "name": "Porta Int Trás LE NB4", "cat": "NB", "per": 40, "racks": 14, "ideal": 20},
        {"id": "18", "code": "GA062", "name": "Porta Int Trás LD NB4", "cat": "NB", "per": 40, "racks": 14, "ideal": 20},
        {"id": "19", "code": "GA063", "name": "Porta Ext Trás LE HB5", "cat": "HB", "per": 24, "racks": 52, "ideal": 67},
        {"id": "20", "code": "GA064", "name": "Porta Ext Trás LD HB5", "cat": "HB", "per": 24, "racks": 63, "ideal": 67},
        {"id": "21", "code": "GA065", "name": "Porta Int Trás LE HB5", "cat": "HB", "per": 40, "racks": 30, "ideal": 40},
        {"id": "22", "code": "GA066", "name": "Porta Int Trás LD HB5", "cat": "HB", "per": 40, "racks": 35, "ideal": 40},
    ]

# 3. LÓGICA DE PRODUÇÃO
j_total, j_nb, j_hb = 61, 24, 37 # Valores que você usa

st.title("🚜 KOMATSU - PANELTRACK")

# Gerar Relatório WhatsApp
agora = datetime.now().strftime("%d/%m %H:%M")
msg = f"RELATÓRIO Komatsu 📅 {agora}\n\n"
for i in st.session_state.estoque:
    p = i['racks'] * i['per']
    h = p / (j_nb if i['cat'] == 'NB' else j_hb if i['cat'] == 'HB' else j_total)
    status = "🔴" if h < 8 else "⚠️" if h <= 15 else "✅"
    msg += f"{status} {i['code']}: {h:.1f}h\n"

url_zap = "https://wa.me/?text=" + urllib.parse.quote(msg)
st.markdown(f'<a href="{url_zap}" target="_blank" class="btn-whatsapp">📲 EXPORTAR PARA WHATSAPP</a>', unsafe_allow_html=True)

# 4. LANÇAMENTO DE DADOS
with st.expander("📝 ATUALIZAR ESTOQUE"):
    escolha = st.selectbox("Peça:", [f"{i['code']} - {i['name']}" for i in st.session_state.estoque])
    valor = st.number_input("Racks:", min_value=0, step=1)
    if st.button("SALVAR"):
        for i in st.session_state.estoque:
            if i['code'] == escolha.split(" - ")[0]: i['racks'] = valor
        st.rerun()

st.divider()

# 5. GRID DE CARDS (O Porsche)
cols = st.columns(2) # 2 por linha no celular fica perfeito
for i, item in enumerate(st.session_state.estoque):
    pecas = item['racks'] * item['per']
    h = pecas / (j_nb if item['cat'] == 'NB' else j_hb if item['cat'] == 'HB' else j_total)
    
    status_color = ""
    if h < 8: status_color = "critico"
    elif h <= 15: status_color = "atencao"

    with cols[i % 2]:
        st.markdown(f"""
            <div class="metric-card {status_color}">
                <div class="card-code">{item['code']}</div>
                <div class="card-name">{item['name']}</div>
                <div class="card-racks">{item['racks']} Racks</div>
                <div class="card-hours">{h:.1f} horas</div>
            </div>
        """, unsafe_allow_html=True)
