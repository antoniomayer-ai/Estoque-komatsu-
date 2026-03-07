import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import urllib.parse

# 1. ESTILO CORPORATIVO LIMPO (ALTO CONTRASTE)
st.set_page_config(page_title="KOMATSU PANELTRACK", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #f4f4f9 !important; }
    * { color: #000000 !important; font-family: 'Segoe UI', sans-serif; }
    h1, h2, h3 { color: #004a99 !important; }
    .stDataFrame { background-color: white; border-radius: 10px; }
    button { background-color: #004a99 !important; color: white !important; font-weight: bold !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. BANCO DE DADOS COMPLETO (22 FAMÍLIAS)
if 'estoque' not in st.session_state:
    st.session_state.estoque = [
        {"code": "GA035", "name": "Assoalho Diant LE", "cat": "COMMON", "per": 100, "racks": 9, "ideal": 24},
        {"code": "GA036", "name": "Assoalho Diant LD", "cat": "COMMON", "per": 100, "racks": 12, "ideal": 24},
        {"code": "GA037", "name": "Painel Dash", "cat": "COMMON", "per": 100, "racks": 12, "ideal": 24},
        {"code": "GA038", "name": "Assoalho Interm", "cat": "COMMON", "per": 20, "racks": 57, "ideal": 119},
        {"code": "GA039", "name": "Assoalho Trás NB4", "cat": "NB", "per": 40, "racks": 15, "ideal": 20},
        {"code": "GA040", "name": "Assoalho Trás HB5", "cat": "HB", "per": 50, "racks": 45, "ideal": 32},
        {"code": "GA042", "name": "Cofre Externo", "cat": "COMMON", "per": 23, "racks": 40, "ideal": 104},
        {"code": "GA041", "name": "Cofre Interno", "cat": "COMMON", "per": 46, "racks": 70, "ideal": 52},
        {"code": "GA051", "name": "Lateral Int LE", "cat": "HB", "per": 50, "racks": 19, "ideal": 32},
        {"code": "GA052", "name": "Lateral Int LD", "cat": "HB", "per": 50, "racks": 21, "ideal": 32},
        {"code": "GA055", "name": "Porta Ext Diant LE", "cat": "COMMON", "per": 24, "racks": 100, "ideal": 100},
        {"code": "GA056", "name": "Porta Ext Diant LD", "cat": "COMMON", "per": 24, "racks": 110, "ideal": 100},
        {"code": "GA057", "name": "Porta Int Diant LE", "cat": "COMMON", "per": 40, "racks": 24, "ideal": 60},
        {"code": "GA058", "name": "Porta Int Diant LD", "cat": "COMMON", "per": 40, "racks": 29, "ideal": 60},
        {"code": "GA059", "name": "Porta Ext Trás LE NB4", "cat": "NB", "per": 24, "racks": 35, "ideal": 33},
        {"code": "GA060", "name": "Porta Ext Trás LD NB4", "cat": "NB", "per": 24, "racks": 46, "ideal": 33},
        {"code": "GA061", "name": "Porta Int Trás LE NB4", "cat": "NB", "per": 40, "racks": 14, "ideal": 20},
        {"code": "GA062", "name": "Porta Int Trás LD NB4", "cat": "NB", "per": 40, "racks": 14, "ideal": 20},
        {"code": "GA063", "name": "Porta Ext Trás LE HB5", "cat": "HB", "per": 24, "racks": 52, "ideal": 67},
        {"code": "GA064", "name": "Porta Ext Trás LD HB5", "cat": "HB", "per": 24, "racks": 63, "ideal": 67},
        {"code": "GA065", "name": "Porta Int Trás LE HB5", "cat": "HB", "per": 40, "racks": 30, "ideal": 40},
        {"code": "GA066", "name": "Porta Int Trás LD HB5", "cat": "HB", "per": 40, "racks": 35, "ideal": 40},
    ]

# 3. LÓGICA DE TEMPO (CORREÇÃO GMT-3)
fuso = timedelta(hours=-3)
agora_br = datetime.now() + fuso
data_formatada = agora_br.strftime("%d/%m %H:%M")

# 4. CONFIGURAÇÃO DE JPH E ORDENAÇÃO
st.title("🚜 Painel Track Komatsu")
col_j1, col_j2 = st.columns([2, 1])
j_total = col_j1.number_input("JPH Geral", value=61)
ordem = col_j2.selectbox("Ordenar por:", ["Código", "Menor Cobertura"])

# 5. CÁLCULOS E RELATÓRIO WHATSAPP
df = pd.DataFrame(st.session_state.estoque)
df['Peças'] = df['racks'] * df['per']
df['Horas'] = df.apply(lambda x: x['Peças'] / (24 if x['cat'] == 'NB' else 37 if x['cat'] == 'HB' else j_total), axis=1)

# Gerar Mensagem WhatsApp
msg = f"RELATÓRIO Komatsu 📅 {data_formatada}\n\n"
for _, row in df.sort_values(by='Horas').iterrows():
    status = "🔴" if row['Horas'] < 8 else "⚠️" if row['Horas'] <= 15 else "✅"
    msg += f"{status} {row['code']}: {row['Horas']:.1f}h\n"

url_zap = "https://wa.me/?text=" + urllib.parse.quote(msg)

# 6. INTERFACE (WHATSAPP E TABELA)
st.markdown(f'<a href="{url_zap}" target="_blank" style="text-decoration:none;"><div style="background-color:#25d366; color:white; padding:10px; border-radius:5px; text-align:center; font-weight:bold; margin-bottom:10px;">📲 EXPORTAR PARA WHATSAPP</div></a>', unsafe_allow_html=True)

with st.expander("📝 LANÇAR RACKS"):
    escolha = st.selectbox("Peça:", [f"{i['code']} - {i['name']}" for i in st.session_state.estoque])
    valor = st.number_input("Quantidade:", min_value=0, step=1)
    if st.button("SALVAR"):
        for i in st.session_state.estoque:
            if i['code'] == escolha.split(" - ")[0]: i['racks'] = valor
        st.rerun()

# 7. EXIBIÇÃO FINAL
if ordem == "Menor Cobertura":
    df = df.sort_values(by='Horas')

st.subheader(f"Situação em {data_formatada}")
st.dataframe(df[['code', 'name', 'racks', 'Horas']], hide_index=True, use_container_width=True)
