import streamlit as st
import pandas as pd
from datetime import datetime

# 1. ESTILO "GESTÃO À VISTA" (Cópia fiel da sua imagem)
st.set_page_config(page_title="ESTAMPARIA KOMATSU", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #1a1c24 !important; }
    h1, h2, h3, p, span, div { color: #ffffff !important; font-family: 'Segoe UI', sans-serif; }
    
    /* Estilo dos Cards */
    .card {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        border-left: 8px solid #22c55e;
        min-height: 180px;
    }
    .card-red { border-left-color: #ef4444 !important; }
    .card-yellow { border-left-color: #facc15 !important; }
    .card-green { border-left-color: #22c55e !important; }
    
    .card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; }
    .card-code { color: #1a1c24; font-weight: bold; font-size: 1.1rem; }
    .card-desc { color: #1a1c24; font-size: 0.8rem; text-transform: uppercase; }
    .card-racks { color: #1a1c24; font-size: 1.4rem; font-weight: 900; }
    .card-pct { color: #22c55e; font-weight: bold; float: right; }
    .card-pieces { color: #9ca3af; font-size: 0.8rem; text-align: center; margin: 10px 0; }
    
    /* Faixa de Horas Colorida */
    .hours-box {
        border-radius: 4px;
        padding: 5px;
        text-align: center;
        font-weight: bold;
        font-size: 1.2rem;
    }
    .bg-red { background-color: #fef2f2; color: #ef4444 !important; }
    .bg-yellow { background-color: #fefce8; color: #ca8a04 !important; }
    .bg-green { background-color: #f0fdf4; color: #166534 !important; }
    
    /* Legenda no rodapé */
    .legend { display: flex; justify-content: center; gap: 20px; margin-top: 20px; font-size: 0.8rem; }
    .dot { height: 10px; width: 10px; border-radius: 50%; display: inline-block; margin-right: 5px; }
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

# 3. HEADER (Data, Título e Percentual Global)
now = datetime.now().strftime("%d/%m - %H:%M")
df = pd.DataFrame(st.session_state.inventory)
total_racks = df['racks'].sum()
ideal_racks = df['ideal'].sum()
global_pct = (total_racks / ideal_racks) * 100

st.write(f"### ESTAMPARIA KOMATSU <span style='float:right; color:#22c55e;'>{global_pct:.0f}% ESTOQUE</span>", unsafe_allow_html=True)
st.caption(f"{now}")

# 4. BARRA DE CONFIGURAÇÃO JPH
col_j1, col_j2, col_j3 = st.columns([2, 1, 1])
j_total = col_j1.number_input("⏱ JPH TOTAL", value=61)
j_nb = col_j2.number_input("📈 NB", value=24)
j_hb = col_j3.number_input("📉 HB", value=37)

st.divider()

# 5. ATUALIZAÇÃO RÁPIDA (PARA O ANTÔNIO NÃO SOFRER)
with st.expander("📝 LANÇAR NOVA CONTAGEM"):
    escolha = st.selectbox("Peça:", [f"{i['code']} - {i['name']}" for i in st.session_state.inventory])
    valor = st.number_input("Qtd Racks:", min_value=0, step=1)
    if st.button("SALVAR DADOS"):
        cod = escolha.split(" - ")[0]
        for item in st.session_state.inventory:
            if item['code'] == cod: item['racks'] = valor
        st.success("Salvo!")
        st.rerun()

# 6. GRID DE CARDS (4 colunas como na imagem)
cols = st.columns(4)
for i, item in enumerate(st.session_state.inventory):
    # Cálculos Individuais
    pecas = item['racks'] * item['per']
    if item['cat'] == 'NB': h = pecas / j_nb if j_nb > 0 else 0
    elif item['cat'] == 'HB': h = pecas / j_hb if j_hb > 0 else 0
    else: h = pecas / j_total if j_total > 0 else 0
    
    pct = (item['racks'] / item['ideal']) * 100
    
    # Lógica de Cores
    status_class = "card-green"
    bg_class = "bg-green"
    if h < 8: status_class, bg_class = "card-red", "bg-red"
    elif h <= 15: status_class, bg_class = "card-yellow", "bg-yellow"

    with cols[i % 4]:
        st.markdown(f"""
            <div class="card {status_class}">
                <div class="card-header">
                    <span class="card-code">{item['code']}</span>
                    <span class="card-pct">{pct:.0f}%</span>
                </div>
                <div class="card-desc">{item['name']}</div>
                <div class="card-racks">{item['racks']}R</div>
                <div class="card-pieces">{pecas:,} PÇS</div>
                <div class="hours-box {bg_class}">{h:.1f}h</div>
            </div>
        """, unsafe_allow_html=True)

# 7. LEGENDA
st.markdown("""
    <div class="legend">
        <span><span class="dot" style="background-color: #ef4444;"></span>CRÍTICO (&lt; 8H)</span>
        <span><span class="dot" style="background-color: #facc15;"></span>ATENÇÃO (8H - 15H)</span>
        <span><span class="dot" style="background-color: #22c55e;"></span>SEGURO (&gt; 15H)</span>
    </div>
""", unsafe_allow_html=True)
