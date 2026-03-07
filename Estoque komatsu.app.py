import streamlit as st
import pandas as pd
from datetime import datetime

# 1. ESTILO "ESTAMPARIA" - FORÇANDO BRANCO E PRETO
st.set_page_config(page_title="KOMATSU PANELTRACK", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; }
    * { color: #000000 !important; font-family: sans-serif; }
    
    /* Estilo dos Cartões */
    .card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid #d1d5db;
        border-left: 8px solid #22c55e;
        height: 160px;
    }
    .card-red { border-left-color: #ef4444 !important; }
    .card-yellow { border-left-color: #facc15 !important; }
    .card-green { border-left-color: #22c55e !important; }
    
    .card-code { color: #004a99 !important; font-weight: bold; font-size: 1.1rem; display: block; }
    .card-name { color: #374151 !important; font-size: 0.75rem; font-weight: bold; text-transform: uppercase; margin-bottom: 5px; display: block; }
    .card-racks { color: #000000 !important; font-size: 1.3rem; font-weight: 900; }
    .card-hours { background-color: #ffffff; border-radius: 4px; padding: 3px; text-align: center; font-weight: bold; font-size: 1.1rem; margin-top: 5px; border: 1px solid #e5e7eb; }
    
    .text-red { color: #ef4444 !important; }
    .text-yellow { color: #ca8a04 !important; }
    .text-green { color: #166534 !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. BANCO DE DADOS (22 ITENS)
if 'inventory' not in st.session_state:
    st.session_state.inventory = [
        {"code": "GA035", "name": "LE", "cat": "COMMON", "per": 100, "racks": 9, "ideal": 24},
        {"code": "GA057", "name": "LE", "cat": "COMMON", "per": 40, "racks": 24, "ideal": 60},
        {"code": "GA038", "name": "INT", "cat": "COMMON", "per": 20, "racks": 57, "ideal": 119},
        {"code": "GA058", "name": "LD", "cat": "COMMON", "per": 40, "racks": 29, "ideal": 60},
        {"code": "GA037", "name": "DASH", "cat": "COMMON", "per": 100, "racks": 12, "ideal": 24},
        {"code": "GA036", "name": "LD", "cat": "COMMON", "per": 100, "racks": 12, "ideal": 24},
        {"code": "GA061", "name": "LE", "cat": "NB", "per": 40, "racks": 14, "ideal": 20},
        {"code": "GA062", "name": "LD", "cat": "NB", "per": 40, "racks": 14, "ideal": 20},
        {"code": "GA039", "name": "NB4", "cat": "NB", "per": 40, "racks": 15, "ideal": 20},
        {"code": "GA051", "name": "LE", "cat": "HB", "per": 50, "racks": 19, "ideal": 32},
        {"code": "GA041", "name": "EXT", "cat": "COMMON", "per": 46, "racks": 70, "ideal": 52},
        {"code": "GA052", "name": "LD", "cat": "HB", "per": 50, "racks": 21, "ideal": 32},
        {"code": "GA042", "name": "INT", "cat": "COMMON", "per": 23, "racks": 40, "ideal": 104},
        {"code": "GA065", "name": "LE", "cat": "HB", "per": 40, "racks": 30, "ideal": 40},
        {"code": "GA063", "name": "LE", "cat": "HB", "per": 24, "racks": 52, "ideal": 67},
        {"code": "GA059", "name": "LE", "cat": "NB", "per": 24, "racks": 35, "ideal": 33},
        {"code": "GA066", "name": "LD", "cat": "HB", "per": 40, "racks": 35, "ideal": 40},
        {"code": "GA055", "name": "LE", "cat": "COMMON", "per": 24, "racks": 100, "ideal": 100},
        {"code": "GA064", "name": "LD", "cat": "HB", "per": 24, "racks": 63, "ideal": 67},
        {"code": "GA056", "name": "LD", "cat": "COMMON", "per": 24, "racks": 110, "ideal": 100},
        {"code": "GA060", "name": "LD", "cat": "NB", "per": 24, "racks": 46, "ideal": 33},
        {"code": "GA040", "name": "HB5", "cat": "HB", "per": 50, "racks": 45, "ideal": 32},
    ]

# 3. SIDEBAR JPH
with st.sidebar:
    st.header("⚙️ Produção JPH")
    j_total = st.number_input("TOTAL", value=61)
    j_nb = st.number_input("NB", value=24)
    j_hb = st.number_input("HB", value=37)

# 4. LÓGICA DE RELATÓRIO WHATSAPP
agora = datetime.now().strftime("%d/%m %H:%M")
status_ok = []
status_atencao = []
status_critico = []

for item in st.session_state.inventory:
    pecas = item['racks'] * item['per']
    if item['cat'] == 'NB': h = pecas / j_nb if j_nb > 0 else 0
    elif item['cat'] == 'HB': h = pecas / j_hb if j_hb > 0 else 0
    else: h = pecas / j_total if j_total > 0 else 0
    
    info = f"* {item['code']} {item['name']}: {h:.1f}h"
    if h < 8: status_critico.append(info)
    elif h <= 15: status_atencao.append(info)
    else: status_ok.append(info)

msg_zap = f"RELATÓRIO Komatsu 📅 {agora}\n📊 Nível Geral: {(sum([i['racks'] for i in st.session_state.inventory])/sum([i['ideal'] for i in st.session_state.inventory])*100):.0f}%\n⚡ JPH: {j_total} (NB: {j_nb} / HB: {j_hb})\n\n"
if status_critico: msg_zap += "🔴 CRÍTICO (<8h)\n" + "\n".join(status_critico) + "\n\n"
if status_atencao: msg_zap += "⚠️ ATENÇÃO (8h-15h)\n" + "\n".join(status_atencao) + "\n\n"
if status_ok: msg_zap += "✅ OK (>15h)\n" + "\n".join(status_ok)

# 5. HEADER E RELATÓRIO
st.title("🚜 KOMATSU - PAINEL TRACK")

with st.expander("📲 GERAR RELATÓRIO WHATSAPP"):
    st.code(msg_zap, language=None)
    st.caption("Copia o texto acima e cola no WhatsApp")

with st.expander("📝 ATUALIZAR RACKS"):
    escolha = st.selectbox("Peça:", [f"{i['code']} - {i['name']}" for i in st.session_state.inventory])
    valor = st.number_input("Qtd Racks:", min_value=0, step=1)
    if st.button("SALVAR"):
        for item in st.session_state.inventory:
            if item['code'] == escolha.split(" - ")[0]: item['racks'] = valor
        st.rerun()

st.divider()

# 6. GRID DE CARDS
cols = st.columns(4)
for i, item in enumerate(st.session_state.inventory):
    pecas = item['racks'] * item['per']
    if item['cat'] == 'NB': h = pecas / j_nb if j_nb > 0 else 0
    elif item['cat'] == 'HB': h = pecas / j_hb if j_hb > 0 else 0
    else: h = pecas / j_total if j_total > 0 else 0
    
    color_class = "card-green"
    text_class = "text-green"
    if h < 8: color_class, text_class = "card-red", "text-red"
    elif h <= 15: color_class, text_class = "card-yellow", "text-yellow"

    with cols[i % 4]:
        st.markdown(f"""
            <div class="card {color_class}">
                <span class="card-code">{item['code']}</span>
                <span class="card-name">{item['name']}</span>
                <span class="card-racks">{item['racks']}R</span>
                <div class="card-hours {text_class}">{h:.1f}h</div>
            </div>
        """, unsafe_allow_html=True)
