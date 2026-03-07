import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. ESTILO "LUZ TOTAL" - COMPACTO PARA CELULAR
st.set_page_config(page_title="KOMATSU PANELTRACK", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #ffffff !important; }
    * { color: #000000 !important; font-family: sans-serif; font-size: 14px; }
    h1, h2, h3 { color: #004a99 !important; margin: 0; padding: 0; }
    /* Tabela compacta */
    .compact-table { width: 100%; border-collapse: collapse; margin-top: 10px; }
    .compact-table td, .compact-table th { border: 1px solid #ddd; padding: 4px; text-align: center; }
    .bg-red { background-color: #ffcccc; color: #cc0000 !important; font-weight: bold; }
    .bg-yellow { background-color: #ffffcc; color: #886600 !important; font-weight: bold; }
    .bg-green { background-color: #ccffcc; color: #006600 !important; font-weight: bold; }
    /* Botão WhatsApp */
    .btn-zap { background-color: #25d366; color: white !important; padding: 10px; border-radius: 5px; text-decoration: none; font-weight: bold; display: block; text-align: center; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. BANCO DE DADOS (TODOS OS 22 ITENS)
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

# 3. HEADER E CONFIGURAÇÃO JPH
st.title("🚜 KOMATSU - PAINEL")
col_j1, col_j2, col_j3 = st.columns(3)
j_total = col_j1.number_input("JPH", value=61)
j_nb = col_j2.number_input("NB", value=24)
j_hb = col_j3.number_input("HB", value=37)

# 4. LÓGICA DO RELATÓRIO WHATSAPP
agora = datetime.now().strftime("%d/%m %H:%M")
total_r = sum([i['racks'] for i in st.session_state.inventory])
ideal_r = sum([i['ideal'] for i in st.session_state.inventory])
pct_geral = (total_r / ideal_r * 100)

msg_whatsapp = f"RELATÓRIO Komatsu 📅 {agora}\n📊 Nível Geral: {pct_geral:.0f}%\n⚡ JPH: {j_total} (NB: {j_nb} / HB: {j_hb})\n\n"
lista_ok, lista_at, lista_cr = [], [], []

for item in st.session_state.inventory:
    pecas = item['racks'] * item['per']
    if item['cat'] == 'NB': h = pecas / j_nb if j_nb > 0 else 0
    elif item['cat'] == 'HB': h = pecas / j_hb if j_hb > 0 else 0
    else: h = pecas / j_total if j_total > 0 else 0
    
    txt = f"* {item['code']} {item['name']}: {h:.1f}h"
    if h < 8: lista_cr.append(txt)
    elif h <= 15: lista_at.append(txt)
    else: lista_ok.append(txt)

if lista_cr: msg_whatsapp += "🔴 CRÍTICO (<8h)\n" + "\n".join(lista_cr) + "\n\n"
if lista_at: msg_whatsapp += "⚠️ ATENÇÃO (8h-15h)\n" + "\n".join(lista_at) + "\n\n"
if lista_ok: msg_whatsapp += "✅ OK (>15h)\n" + "\n".join(lista_ok)

# 5. BOTÃO WHATSAPP E EDIÇÃO
url_zap = "https://wa.me/?text=" + urllib.parse.quote(msg_whatsapp)
st.markdown(f'<a href="{url_zap}" target="_blank" class="btn-zap">📲 ENVIAR PARA WHATSAPP</a>', unsafe_allow_html=True)

with st.expander("📝 LANÇAR RACKS"):
    escolha = st.selectbox("Peça:", [f"{i['code']} - {i['name']}" for i in st.session_state.inventory])
    valor = st.number_input("Nova Qtd:", min_value=0, step=1)
    if st.button("SALVAR"):
        for item in st.session_state.inventory:
            if item['code'] == escolha.split(" - ")[0]: item['racks'] = valor
        st.rerun()

# 6. RELATÓRIO COMPACTO (CABEM TODOS NA TELA)
html_table = '<table class="compact-table"><tr><th>Cód</th><th>Peça</th><th>R</th><th>Horas</th></tr>'
for item in st.session_state.inventory:
    pecas = item['racks'] * item['per']
    if item['cat'] == 'NB': h = pecas / j_nb if j_nb > 0 else 0
    elif item['cat'] == 'HB': h = pecas / j_hb if j_hb > 0 else 0
    else: h = pecas / j_total if j_total > 0 else 0
    
    cor = "bg-green"
    if h < 8: cor = "bg-red"
    elif h <= 15: cor = "bg-yellow"
    
    html_table += f'<tr><td>{item["code"]}</td><td>{item["name"]}</td><td>{item["racks"]}</td><td class="{cor}">{h:.1f}h</td></tr>'
html_table += '</table>'

st.markdown(html_table, unsafe_allow_html=True)
