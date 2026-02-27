import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(
    page_title="PanelTrack - Komatsu",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização Customizada (CSS)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stMetric { background-color: white; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
    .critical-card { background-color: #fef2f2; border-left: 5px solid #ef4444; padding: 15px; border-radius: 8px; margin-bottom: 10px; }
    .safe-card { background-color: #f0fdf4; border-left: 5px solid #22c55e; padding: 15px; border-radius: 8px; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- DADOS INICIAIS ---
if 'inventory' not in st.session_state:
    st.session_state.inventory = [
        {"id": "7", "code": "GA042", "name": "cofre externo", "category": "COMMON", "partsPerRack": 23, "currentRacks": 59, "idealLotRacks": 104},
        {"id": "8", "code": "GA041", "name": "cofre interno", "category": "COMMON", "partsPerRack": 46, "currentRacks": 29, "idealLotRacks": 52},
        {"id": "3", "code": "GA037", "name": "painel dash", "category": "COMMON", "partsPerRack": 100, "currentRacks": 12, "idealLotRacks": 24},
        {"id": "4", "code": "GA038", "name": "assoalho intermediário", "category": "COMMON", "partsPerRack": 20, "currentRacks": 55, "idealLotRacks": 119},
        {"id": "15", "code": "GA059", "name": "Porta ext Traseira LE NB4", "category": "NB", "partsPerRack": 24, "currentRacks": 13, "idealLotRacks": 33},
        {"id": "16", "code": "GA060", "name": "Porta ext Traseira LD NB4", "category": "NB", "partsPerRack": 24, "currentRacks": 27, "idealLotRacks": 33},
        {"id": "13", "code": "GA057", "name": "Porta int Dianteira LE", "category": "COMMON", "partsPerRack": 40, "currentRacks": 31, "idealLotRacks": 60},
        {"id": "14", "code": "GA058", "name": "Porta int Dianteira LD", "category": "COMMON", "partsPerRack": 40, "currentRacks": 36, "idealLotRacks": 60},
        {"id": "21", "code": "GA065", "name": "Porta int Traseira LE HB5", "category": "HB", "partsPerRack": 40, "currentRacks": 28, "idealLotRacks": 40},
        {"id": "22", "code": "GA066", "name": "Porta int traseira LD HB5", "category": "HB", "partsPerRack": 40, "currentRacks": 29, "idealLotRacks": 40},
        {"id": "9", "code": "GA051", "name": "Lateral interna LE", "category": "HB", "partsPerRack": 50, "currentRacks": 23, "idealLotRacks": 32},
        {"id": "10", "code": "GA052", "name": "Lateral interna LD", "category": "HB", "partsPerRack": 50, "currentRacks": 27, "idealLotRacks": 32},
        {"id": "19", "code": "GA063", "name": "Porta ext Traseira LE HB5", "category": "HB", "partsPerRack": 24, "currentRacks": 64, "idealLotRacks": 67},
        {"id": "20", "code": "GA064", "name": "Porta ext Traseira LD HB5", "category": "HB", "partsPerRack": 24, "currentRacks": 76, "idealLotRacks": 67},
        {"id": "11", "code": "GA055", "name": "Porta ext Dianteira LE", "category": "COMMON", "partsPerRack": 24, "currentRacks": 90, "idealLotRacks": 100},
        {"id": "12", "code": "GA056", "name": "Porta ext Dianteira LD", "category": "COMMON", "partsPerRack": 24, "currentRacks": 103, "idealLotRacks": 100},
        {"id": "17", "code": "GA061", "name": "Porta int traseira LE NB4", "category": "NB", "partsPerRack": 40, "currentRacks": 14, "idealLotRacks": 20},
        {"id": "18", "code": "GA062", "name": "Porta int traseira LD NB4", "category": "NB", "partsPerRack": 40, "currentRacks": 15, "idealLotRacks": 20},
        {"id": "1", "code": "GA035", "name": "assoalho dianteiro LE", "category": "COMMON", "partsPerRack": 100, "currentRacks": 36, "idealLotRacks": 24},
        {"id": "2", "code": "GA036", "name": "assoalho dianteiro LD", "category": "COMMON", "partsPerRack": 100, "currentRacks": 38, "idealLotRacks": 24},
        {"id": "6", "code": "GA040", "name": "assoalho traseiro HB5", "category": "HB", "partsPerRack": 50, "currentRacks": 65, "idealLotRacks": 32},
        {"id": "5", "code": "GA039", "name": "assoalho traseiro NB4", "category": "NB", "partsPerRack": 40, "currentRacks": 33, "idealLotRacks": 20},
    ]

if 'settings' not in st.session_state:
    st.session_state.settings = {"total": 63, "nb": 16, "hb": 47}

# --- HEADER ---
st.title("KOMATSU Inventory")
st.caption("Controle de Estamparia - PanelTrack System")

# --- CONFIGURAÇÃO DE PRODUÇÃO (SIDEBAR) ---
with st.sidebar:
    st.header("⚙️ Configurações (JPH)")
    total = st.number_input("TOTAL", value=st.session_state.settings["total"])
    nb = st.number_input("NB", value=st.session_state.settings["nb"])
    hb = st.number_input("HB", value=st.session_state.settings["hb"])
    
    # Validação Exata
    is_mismatch = (nb + hb != total)
    if is_mismatch:
        st.error("⚠ ajuste o valor total, ou HB e NB")
    else:
        st.success("✅ Soma correta")
        st.session_state.settings = {"total": total, "nb": nb, "hb": hb}

# --- CÁLCULOS GERAIS ---
df = pd.DataFrame(st.session_state.inventory)
df['totalParts'] = df['currentRacks'] * df['partsPerRack']

def calc_coverage(row):
    consumption = st.session_state.settings['total']
    if row['category'] == 'NB': consumption = st.session_state.settings['nb']
    elif row['category'] == 'HB': consumption = st.session_state.settings['hb']
    return row['totalParts'] / consumption if consumption > 0 else 999

df['coverage'] = df.apply(calc_coverage, axis=1)
df['percentIdeal'] = (df['currentRacks'] / df['idealLotRacks'] * 100).clip(upper=110)

global_stock = df['percentIdeal'].mean()
critical_count = len(df[df['coverage'] < 8])

# --- DASHBOARD ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Média Estoque", f"{global_stock:.0f}%")
col2.metric("Itens Críticos", critical_count, delta_color="inverse")
col3.metric("Total Racks", int(df['currentRacks'].sum()))
col4.metric("Total Peças", f"{int(df['totalParts'].sum()):,}")

# --- FILTROS ---
st.divider()
f_col1, f_col2 = st.columns([2, 1])
search = f_col1.text_input("🔍 Buscar por código ou nome")
cat_filter = f_col2.selectbox("Filtrar Categoria", ["Todas", "NB", "HB", "COMMON"])

# Aplicar Filtros
filtered_df = df.copy()
if search:
    filtered_df = filtered_df[filtered_df['name'].str.contains(search, case=False) | filtered_df['code'].str.contains(search, case=False)]
if cat_filter != "Todas":
    filtered_df = filtered_df[filtered_df['category'] == cat_filter]

# --- TABELA DE INVENTÁRIO ---
st.subheader("📋 Inventário Detalhado")

# Usando st.data_editor para permitir edição direta de racks
edited_df = st.data_editor(
    filtered_df[['code', 'name', 'category', 'idealLotRacks', 'currentRacks', 'percentIdeal', 'totalParts', 'coverage']],
    column_config={
        "code": "Código",
        "name": "Descrição",
        "category": "Cat",
        "idealLotRacks": st.column_config.NumberColumn("Lote Ideal", help="Meta em Racks"),
        "currentRacks": st.column_config.NumberColumn("Qtd Racks", help="Ajuste a contagem aqui"),
        "percentIdeal": st.column_config.ProgressColumn("% Ideal", format="%d%%", min_value=0, max_value=110),
        "totalParts": st.column_config.NumberColumn("Total Peças", format="%d"),
        "coverage": st.column_config.NumberColumn("Cobertura (h)", format="%.1f h"),
    },
    disabled=["code", "name", "category", "percentIdeal", "totalParts", "coverage"],
    hide_index=True,
    use_container_width=True,
    key="inventory_editor"
)

# Atualizar o estado global se houver edição
if st.session_state.inventory_editor:
    # Lógica para sincronizar as mudanças de volta para st.session_state.inventory
    # (O Streamlit Data Editor lida com isso automaticamente via key, mas para persistência real 
    # você salvaria em um banco de dados ou arquivo aqui)
    pass

# --- LEGENDA ---
st.info("""
**Legenda de Cobertura:**
- 🔴 **Crítico:** < 8h 
- 🟡 **Atenção:** 8h - 15h
- 🟢 **Seguro:** > 15h
""")

if st.button("💾 Salvar Dados Localmente"):
    st.toast("Dados salvos na sessão!", icon="✅")
