import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import random
import time

# Configuração da página
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS PROFISSIONAL - Compatível com Streamlit Cloud
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Background principal com gradiente animado */
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e293b, #6d28d9, #1e293b, #0f172a);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        font-family: 'Inter', sans-serif;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Header principal com glassmorphism */
    .main-header {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.9), rgba(6, 182, 212, 0.9));
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        margin: 2rem 0;
        color: white;
        box-shadow: 0 8px 32px rgba(139, 92, 246, 0.37);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        font-weight: 900;
        margin: 0;
        background: linear-gradient(135deg, #ffffff, #f8fafc, #e2e8f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 30px rgba(255,255,255,0.5);
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        font-size: 1.3rem;
        margin: 1rem 0 0.5rem 0;
        opacity: 0.95;
        position: relative;
        z-index: 1;
    }
    
    .main-header .subtitle {
        font-size: 1rem;
        opacity: 0.8;
        position: relative;
        z-index: 1;
    }
    
    /* Cards de métricas com glassmorphism e animações */
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 16px;
        padding: 2rem 1.5rem;
        text-align: center;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .metric-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(139, 92, 246, 0.4);
        border-color: rgba(255, 255, 255, 0.3);
    }
    
    .metric-card:hover::before {
        left: 100%;
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        margin: 1rem 0;
        background: linear-gradient(135deg, #ffffff, #f8fafc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 20px rgba(255,255,255,0.3);
        animation: countUp 2s ease-out;
    }
    
    @keyframes countUp {
        from { transform: scale(0.5); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .metric-trend {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.7);
        margin-top: 0.5rem;
    }
    
    /* Insight cards com diferentes cores */
    .insight-card {
        background: rgba(139, 92, 246, 0.15);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: white;
        border-left: 4px solid #8b5cf6;
        box-shadow: 0 4px 16px rgba(139, 92, 246, 0.2);
        transition: all 0.3s ease;
    }
    
    .insight-card:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3);
    }
    
    .success-card {
        background: rgba(16, 185, 129, 0.15);
        border-color: rgba(16, 185, 129, 0.3);
        border-left-color: #10b981;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.2);
    }
    
    .success-card:hover {
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
    }
    
    .warning-card {
        background: rgba(245, 158, 11, 0.15);
        border-color: rgba(245, 158, 11, 0.3);
        border-left-color: #f59e0b;
        box-shadow: 0 4px 16px rgba(245, 158, 11, 0.2);
    }
    
    .warning-card:hover {
        box-shadow: 0 8px 25px rgba(245, 158, 11, 0.3);
    }
    
    .critical-card {
        background: rgba(239, 68, 68, 0.15);
        border-color: rgba(239, 68, 68, 0.3);
        border-left-color: #ef4444;
        box-shadow: 0 4px 16px rgba(239, 68, 68, 0.2);
    }
    
    .critical-card:hover {
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.3);
    }
    
    /* Títulos de seção */
    .section-title {
        color: white;
        font-size: 2rem;
        font-weight: 700;
        text-align: center;
        margin: 3rem 0 2rem 0;
        background: linear-gradient(135deg, #ffffff, #e2e8f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        position: relative;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 3px;
        background: linear-gradient(135deg, #8b5cf6, #06b6d4);
        border-radius: 2px;
    }
    
    .subsection-title {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.4rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        text-align: center;
    }
    
    /* Container de conteúdo */
    .content-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }
    
    /* Botões personalizados */
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6, #06b6d4) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1) !important;
        box-shadow: 0 4px 16px rgba(139, 92, 246, 0.3) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.4) !important;
        background: linear-gradient(135deg, #7c3aed, #0891b2) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(0.98) !important;
    }
    
    /* Sidebar personalizada */
    .css-1d391kg {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.95), rgba(30, 41, 59, 0.95));
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Elementos de formulário */
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 8px !important;
        color: white !important;
    }
    
    /* DataFrame personalizado */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }
    
    /* Loading animation */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
    }
    
    .loading-spinner {
        width: 50px;
        height: 50px;
        border: 3px solid rgba(139, 92, 246, 0.3);
        border-top: 3px solid #8b5cf6;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Status indicators */
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-online {
        background: #10b981;
        animation: pulse 2s infinite;
    }
    
    .status-warning {
        background: #f59e0b;
        animation: pulse 2s infinite;
    }
    
    .status-offline {
        background: #ef4444;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    
    /* Footer elegante */
    .footer-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 3rem 2rem;
        margin-top: 4rem;
        text-align: center;
        color: rgba(255, 255, 255, 0.8);
    }
    
    .footer-container h3 {
        color: white;
        margin-bottom: 1rem;
    }
    
    /* Responsividade */
    @media (max-width: 768px) {
        .main-header h1 {
            font-size: 2.5rem;
        }
        
        .metric-value {
            font-size: 2rem;
        }
        
        .metric-card {
            padding: 1.5rem 1rem;
        }
        
        .content-container {
            padding: 1rem;
        }
    }
    
    /* Remover elementos do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Esconder indicador de running */
    .stAppViewContainer > .main > div > div > div > div.stMarkdown > div {
        display: none;
    }
    
    /* Tabs personalizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 600;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8b5cf6, #06b6d4);
        color: white;
        box-shadow: 0 4px 16px rgba(139, 92, 246, 0.3);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def generate_realistic_data():
    """Gera dados realistas e variados para o dashboard"""
    random.seed(42)
    np.random.seed(42)
    
    # Dados mais realistas
    departamentos = ['RH', 'TI', 'Operações', 'Financeiro', 'Marketing', 'Comercial', 'Logística']
    estados = ['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'PE', 'GO', 'DF']
    motivos = ['Família', 'Doença', 'Pessoal', 'Médico', 'Falta de transporte', 'Sem justificativa']
    justificadas = ['Sim', 'Não']
    generos = ['M', 'F']
    cargos = ['Analista Jr', 'Analista Pl', 'Analista Sr', 'Coordenador', 'Supervisor', 'Gerente', 'Diretor']
    
    data = []
    for i in range(250):  # Mais dados para análises robustas
        # Distribuição mais realista por departamento
        if i < 50:  # TI tem mais faltas (burnout)
            dept = 'TI'
            motivo_weights = [0.2, 0.3, 0.25, 0.15, 0.05, 0.05]
        elif i < 90:  # Operações (trabalho físico)
            dept = 'Operações'
            motivo_weights = [0.15, 0.35, 0.15, 0.20, 0.10, 0.05]
        elif i < 120:  # Comercial (viagens)
            dept = 'Comercial'
            motivo_weights = [0.25, 0.20, 0.20, 0.15, 0.15, 0.05]
        else:
            dept = random.choice(departamentos)
            motivo_weights = [0.20, 0.25, 0.20, 0.15, 0.15, 0.05]
        
        motivo = np.random.choice(motivos, p=motivo_weights)
        
        # Justificação mais realista baseada no motivo
        if motivo in ['Doença', 'Médico']:
            justificada = np.random.choice(['Sim', 'Não'], p=[0.90, 0.10])
        elif motivo == 'Família':
            justificada = np.random.choice(['Sim', 'Não'], p=[0.75, 0.25])
        elif motivo == 'Pessoal':
            justificada = np.random.choice(['Sim', 'Não'], p=[0.60, 0.40])
        else:
            justificada = np.random.choice(['Sim', 'Não'], p=[0.30, 0.70])
        
        # Distribuição temporal mais realista
        base_date = datetime(2024, 1, 1)
        days_offset = random.randint(0, 365)
        
        data.append({
            'Nome': f'Funcionário {i+1:03d}',
            'Cargo': random.choice(cargos),
            'Departamento': dept,
            'Estado': random.choice(estados),
            'Data_Falta': base_date + timedelta(days=int(days_offset)),
            'Motivo': motivo,
            'Justificada': justificada,
            'Genero': random.choice(generos),
            'Data_Admissao': base_date - timedelta(days=random.randint(30, 2190)),
            'Salario_Estimado': random.randint(3000, 25000)  # Para cálculos de impacto
        })
    
    df = pd.DataFrame(data)
    
    # Processar dados adicionais
    df['Mes_Ano'] = df['Data_Falta'].dt.strftime('%Y-%m')
    df['Mes_Nome'] = df['Data_Falta'].dt.strftime('%b/%Y')
    df['Dia_Semana'] = df['Data_Falta'].dt.day_name()
    df['Tempo_Empresa_Anos'] = (datetime.now() - df['Data_Admissao']).dt.days // 365
    df['Trimestre'] = df['Data_Falta'].dt.quarter
    df['Semana_Ano'] = df['Data_Falta'].dt.isocalendar().week
    
    return df

@st.cache_data
def calculate_advanced_metrics(df):
    """Calcula métricas avançadas para análise"""
    total_faltas = len(df)
    
    if total_faltas == 0:
        return {
            'total_faltas': 0,
            'funcionarios_unicos': 0,
            'taxa_justificacao': 0,
            'departamentos_afetados': 0,
            'custo_estimado': 0,
            'media_salarial': 0,
            'faltas_por_funcionario': 0,
            'taxa_absenteismo': 0,
            'pico_mensal': 'N/A',
            'tendencia': 'Estável'
        }
    
    faltas_justificadas = len(df[df['Justificada'] == 'Sim'])
    funcionarios_unicos = df['Nome'].nunique()
    departamentos_afetados = df['Departamento'].nunique()
    taxa_justificacao = round((faltas_justificadas / total_faltas * 100), 1)
    
    # Métricas financeiras
    custo_medio_por_falta = 180  # R$ baseado em salário médio/produtividade
    custo_estimado = total_faltas * custo_medio_por_falta
    media_salarial = df['Salario_Estimado'].mean()
    
    # Métricas de RH
    faltas_por_funcionario = round(total_faltas / funcionarios_unicos, 2)
    taxa_absenteismo = round((total_faltas / (funcionarios_unicos * 22)) * 100, 2)  # 22 dias úteis/mês
    
    # Análise temporal
    monthly_counts = df['Mes_Nome'].value_counts()
    pico_mensal = monthly_counts.index[0] if len(monthly_counts) > 0 else 'N/A'
    
    # Tendência simples
    if len(monthly_counts) >= 2:
        recent_months = monthly_counts.head(2)
        if len(recent_months) >= 2:
            if recent_months.iloc[0] > recent_months.iloc[1]:
                tendencia = 'Crescente'
            elif recent_months.iloc[0] < recent_months.iloc[1]:
                tendencia = 'Decrescente'
            else:
                tendencia = 'Estável'
        else:
            tendencia = 'Estável'
    else:
        tendencia = 'Insuficiente'
    
    return {
        'total_faltas': total_faltas,
        'funcionarios_unicos': funcionarios_unicos,
        'taxa_justificacao': taxa_justificacao,
        'departamentos_afetados': departamentos_afetados,
        'custo_estimado': custo_estimado,
        'media_salarial': media_salarial,
        'faltas_por_funcionario': faltas_por_funcionario,
        'taxa_absenteismo': taxa_absenteismo,
        'pico_mensal': pico_mensal,
        'tendencia': tendencia
    }

def create_advanced_plotly_theme():
    """Tema avançado para gráficos Plotly"""
    return {
        'layout': {
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'font': {
                'color': 'white', 
                'family': 'Inter, sans-serif',
                'size': 12
            },
            'title': {
                'font': {'size': 18, 'color': 'white'},
                'x': 0.5,
                'xanchor': 'center'
            },
            'xaxis': {
                'gridcolor': 'rgba(255,255,255,0.1)',
                'linecolor': 'rgba(255,255,255,0.2)',
                'tickcolor': 'rgba(255,255,255,0.2)',
                'tickfont': {'color': 'rgba(255,255,255,0.8)', 'size': 11},
                'titlefont': {'color': 'white', 'size': 13}
            },
            'yaxis': {
                'gridcolor': 'rgba(255,255,255,0.1)',
                'linecolor': 'rgba(255,255,255,0.2)',
                'tickcolor': 'rgba(255,255,255,0.2)',
                'tickfont': {'color': 'rgba(255,255,255,0.8)', 'size': 11},
                'titlefont': {'color': 'white', 'size': 13}
            },
            'legend': {
                'font': {'color': 'white', 'size': 11},
                'bgcolor': 'rgba(255,255,255,0.1)',
                'bordercolor': 'rgba(255,255,255,0.2)',
                'borderwidth': 1
            },
            'colorway': ['#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#8b5a2b', '#6366f1', '#ec4899']
        }
    }

def display_loading_animation():
    """Exibe animação de loading elegante"""
    loading_placeholder = st.empty()
    with loading_placeholder.container():
        st.markdown("""
        <div class="loading-container">
            <div style="text-align: center;">
                <div class="loading-spinner"></div>
                <h3 style="color: white; margin-top: 1rem;">Carregando HR Analytics...</h3>
                <p style="color: rgba(255,255,255,0.7);">Processando dados inteligentes</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(1.5)  # Simula carregamento
    loading_placeholder.empty()

def main():
    # Animação de loading inicial
    if 'loaded' not in st.session_state:
        display_loading_animation()
        st.session_state.loaded = True
    
    # Header principal com design impressionante
    st.markdown("""
    <div class="main-header">
        <h1>📊 HR Analytics Dashboard</h1>
        <p>Análise Avançada de Absenteísmo Corporativo</p>
        <p class="subtitle">Dashboard Interativo com IA, Predições e Insights Estratégicos</p>
        <div style="margin-top: 1.5rem;">
            <span class="status-indicator status-online"></span>
            <span style="font-size: 0.9rem;">Sistema Online | Dados Atualizados</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregar dados
    with st.spinner("🔄 Processando dados avançados..."):
        df = generate_realistic_data()
    
    # Sucesso com estilo
    st.success(f"✅ **{len(df)} registros** processados com sucesso! 🚀 Sistema otimizado para análise empresarial.")
    
    # Sidebar avançada com filtros
    with st.sidebar:
        st.markdown("## 🔍 **Filtros Avançados**")
        st.markdown("*Personalize sua análise:*")
        
        # Filtros principais
        departamentos_selecionados = st.multiselect(
            "🏢 **Departamentos**",
            options=sorted(df['Departamento'].unique()),
            default=sorted(df['Departamento'].unique()),
            help="Selecione os departamentos para análise detalhada"
        )
        
        motivos_selecionados = st.multiselect(
            "📝 **Motivos das Faltas**",
            options=sorted(df['Motivo'].unique()),
            default=sorted(df['Motivo'].unique()),
            help="Filtre por motivos específicos de absenteísmo"
        )
        
        justificacao_filtro = st.selectbox(
            "✅ **Status de Justificação**",
            options=['Todas', 'Sim', 'Não'],
            help="Analisar faltas justificadas vs não justificadas"
        )
        
        genero_filtro = st.selectbox(
            "👥 **Análise por Gênero**",
            options=['Todos', 'M', 'F'],
            help="Segmentação demográfica dos dados"
        )
        
        # Filtros temporais avançados
        st.markdown("### 📅 **Período de Análise**")
        
        col1, col2 = st.columns(2)
        with col1:
            data_inicio = st.date_input(
                "Data Início",
                value=df['Data_Falta'].min().date(),
                help="Início do período de análise"
            )
        
        with col2:
            data_fim = st.date_input(
                "Data Fim",
                value=df['Data_Falta'].max().date(),
                help="Fim do período de análise"
            )
        
        # Filtros adicionais
        st.markdown("### ⚙️ **Filtros Especiais**")
        
        tempo_empresa_filtro = st.slider(
            "📊 **Tempo de Empresa (anos)**",
            min_value=0,
            max_value=int(df['Tempo_Empresa_Anos'].max()),
            value=(0, int(df['Tempo_Empresa_Anos'].max())),
            help="Filtrar por tempo de empresa dos funcionários"
        )
        
        salario_filtro = st.slider(
            "💰 **Faixa Salarial (R$)**",
            min_value=int(df['Salario_Estimado'].min()),
            max_value=int(df['Salario_Estimado'].max()),
            value=(int(df['Salario_Estimado'].min()), int(df['Salario_Estimado'].max())),
            step=1000,
            help="Análise por faixa salarial"
        )
    
    # Aplicar todos os filtros
    df_filtrado = df[
        (df['Departamento'].isin(departamentos_selecionados)) &
        (df['Motivo'].isin(motivos_selecionados)) &
        (df['Data_Falta'].dt.date >= data_inicio) &
        (df['Data_Falta'].dt.date <= data_fim) &
        (df['Tempo_Empresa_Anos'] >= tempo_empresa_filtro[0]) &
        (df['Tempo_Empresa_Anos'] <= tempo_empresa_filtro[1]) &
        (df['Salario_Estimado'] >= salario_filtro[0]) &
        (df['Salario_Estimado'] <= salario_filtro[1])
    ]
    
    if justificacao_filtro != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Justificada'] == justificacao_filtro]
        
    if genero_filtro != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Genero'] == genero_filtro]
    
    # Validar dados filtrados
    if len(df_filtrado) == 0:
        st.error("⚠️ **Nenhum dado encontrado** com os filtros aplicados. Ajuste os critérios de filtragem.")
        return
    
    # Calcular métricas avançadas
    metricas = calculate_advanced_metrics(df_filtrado)
    
    # Criar tema para gráficos
    plotly_theme = create_advanced_plotly_theme()
    
    # Sistema de abas profissional
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "👁️ **Visão Geral**", 
        "🏢 **Análise Departamental**", 
        "📈 **Tendências & Padrões**", 
        "🔮 **IA & Predições**",
        "📋 **Relatórios Executivos**"
    ])
    
    with tab1:
        st.markdown('<div class="section-title">📊 Dashboard Executivo - Métricas Principais</div>', unsafe_allow_html=True)
        
        # Cards de métricas principais com animações
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📅 Total de Faltas</div>
                <div class="metric-value">{metricas['total_faltas']}</div>
                <div class="metric-trend">
                    {round((metricas['total_faltas']/len(df)*100), 1)}% do total | 
                    {metricas['tendencia']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">👥 Funcionários Impactados</div>
                <div class="metric-value">{metricas['funcionarios_unicos']}</div>
                <div class="metric-trend">
                    {metricas['faltas_por_funcionario']} faltas/funcionário
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            taxa_cor = "success" if metricas['taxa_justificacao'] > 75 else "warning" if metricas['taxa_justificacao'] > 60 else "critical"
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">✅ Taxa de Justificação</div>
                <div class="metric-value">{metricas['taxa_justificacao']}%</div>
                <div class="metric-trend">
                    {'🟢 Excelente' if metricas['taxa_justificacao'] > 75 else '🟡 Boa' if metricas['taxa_justificacao'] > 60 else '🔴 Crítica'}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">💰 Impacto Financeiro</div>
                <div class="metric-value">R$ {metricas['custo_estimado']:,.0f}</div>
                <div class="metric-trend">
                    R$ {metricas['custo_estimado']/metricas['total_faltas']:,.0f} por falta
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Segunda linha de métricas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">🏢 Departamentos Afetados</div>
                <div class="metric-value">{metricas['departamentos_afetados']}</div>
                <div class="metric-trend">de 7 departamentos</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📊 Taxa de Absenteísmo</div>
                <div class="metric-value">{metricas['taxa_absenteismo']}%</div>
                <div class="metric-trend">
                    {'🟢 Baixa' if metricas['taxa_absenteismo'] < 3 else '🟡 Moderada' if metricas['taxa_absenteismo'] < 5 else '🔴 Alta'}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📈 Pico Mensal</div>
                <div class="metric-value" style="font-size: 1.8rem;">{metricas['pico_mensal']}</div>
                <div class="metric-trend">período crítico</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">💼 Salário Médio</div>
                <div class="metric-value">R$ {metricas['media_salarial']:,.0f}</div>
                <div class="metric-trend">funcionários afetados</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Gráficos principais com design avançado
        st.markdown('<div class="subsection-title">📊 Análise Visual Interativa</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🏢 **Distribuição por Departamento**")
            dept_counts = df_filtrado['Departamento'].value_counts()
            
            fig_dept = px.bar(
                x=dept_counts.values,
                y=dept_counts.index,
                orientation='h',
                title="",
                color=dept_counts.values,
                color_continuous_scale=['#8b5cf6', '#06b6d4', '#10b981'],
                text=dept_counts.values
            )
            
            fig_dept.update_layout(**plotly_theme['layout'])
            fig_dept.update_traces(
                texttemplate='%{text}',
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Faltas: %{x}<extra></extra>'
            )
            fig_dept.update_coloraxes(showscale=False)
            
            st.plotly_chart(fig_dept, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            st.markdown("#### 🎯 **Motivos das Faltas**")
            motivo_counts = df_filtrado['Motivo'].value_counts()
            
            fig_motivo = px.pie(
                values=motivo_counts.values,
                names=motivo_counts.index,
                title="",
                color_discrete_sequence=['#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#8b5a2b']
            )
            
            fig_motivo.update_layout(**plotly_theme['layout'])
            fig_motivo.update_traces(
                textinfo='percent+label',
                textfont_size=11,
                hovertemplate='<b>%{label}</b><br>Casos: %{value}<br>Percentual: %{percent}<extra></extra>',
                marker=dict(line=dict(color='rgba(255,255,255,0.3)', width=2))
            )
            
            st.plotly_chart(fig_motivo, use_container_width=True, config={'displayModeBar': False})
        
        # Análise temporal na visão geral
        st.markdown("#### 📅 **Evolução Temporal das Faltas**")
        
        monthly_data = df_filtrado.groupby('Mes_Nome').size().reset_index(name='Faltas')
        monthly_data['Data'] = pd.to_datetime(monthly_data['Mes_Nome'], format='%b/%Y')
        monthly_data = monthly_data.sort_values('Data')
        
        fig_timeline = px.line(
            monthly_data,
            x='Mes_Nome',
            y='Faltas',
            title="",
            markers=True,
            line_shape='spline'
        )
        
        fig_timeline.update_traces(
            line=dict(color='#8b5cf6', width=4),
            marker=dict(color='#06b6d4', size=10, line=dict(width=2, color='white')),
            hovertemplate='<b>%{x}</b><br>Faltas: %{y}<extra></extra>'
        )
        
        fig_timeline.update_layout(**plotly_theme['layout'])
        fig_timeline.update_layout(height=350)
        
        st.plotly_chart(fig_timeline, use_container_width=True, config={'displayModeBar': False})
        
        # Insights inteligentes
        st.markdown('<div class="subsection-title">🧠 Insights Inteligentes Automatizados</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            dept_top = dept_counts.index[0] if len(dept_counts) > 0 else "N/A"
            dept_valor = dept_counts.iloc[0] if len(dept_counts) > 0 else 0
            dept_perc = round((dept_valor / metricas['total_faltas'] * 100), 1)
            
            if dept_perc > 30:
                card_class = "critical-card"
                status_emoji = "🚨"
                urgencia = "CRÍTICO"
            elif dept_perc > 20:
                card_class = "warning-card"
                status_emoji = "⚠️"
                urgencia = "ATENÇÃO"
            else:
                card_class = "success-card"
                status_emoji = "✅"
                urgencia = "CONTROLADO"
                
            st.markdown(f"""
            <div class="insight-card {card_class}">
                <h4>{status_emoji} Departamento Crítico - {urgencia}</h4>
                <p><strong>{dept_top}</strong> concentra <strong>{dept_valor} faltas</strong> ({dept_perc}% do total)</p>
                <p>📊 <strong>Ação recomendada:</strong> {'Intervenção imediata necessária' if dept_perc > 30 else 'Monitoramento ativo' if dept_perc > 20 else 'Manter acompanhamento'}</p>
                <p>🎯 <strong>Impacto:</strong> R$ {dept_valor * 180:,.0f} em custos estimados</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            motivo_top = motivo_counts.index[0] if len(motivo_counts) > 0 else "N/A"
            motivo_valor = motivo_counts.iloc[0] if len(motivo_counts) > 0 else 0
            motivo_perc = round((motivo_valor / metricas['total_faltas'] * 100), 1)
            
            # Análise do motivo
            if motivo_top in ['Doença', 'Médico']:
                recomendacao = "Programa de saúde ocupacional"
                card_class = "warning-card"
            elif motivo_top == 'Família':
                recomendacao = "Política de flexibilidade familiar"
                card_class = "insight-card"
            elif motivo_top == 'Falta de transporte':
                recomendacao = "Auxílio transporte ou home office"
                card_class = "warning-card" 
            else:
                recomendacao = "Investigação detalhada necessária"
                card_class = "critical-card"
            
            st.markdown(f"""
            <div class="insight-card {card_class}">
                <h4>📝 Motivo Predominante</h4>
                <p><strong>{motivo_top}</strong> representa <strong>{motivo_valor} casos</strong> ({motivo_perc}% do total)</p>
                <p>💡 <strong>Solução sugerida:</strong> {recomendacao}</p>
                <p>📈 <strong>Potencial de redução:</strong> {'Alto' if motivo_perc > 25 else 'Médio' if motivo_perc > 15 else 'Baixo'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            taxa = metricas['taxa_justificacao']
            
            if taxa > 80:
                status = "EXCELENTE"
                card_class = "success-card"
                emoji = "🏆"
                acao = "Manter padrão de excelência"
            elif taxa > 70:
                status = "BOA"
                card_class = "success-card"
                emoji = "✅"
                acao = "Pequenos ajustes necessários"
            elif taxa > 60:
                status = "MODERADA"
                card_class = "warning-card"
                emoji = "⚠️"
                acao = "Melhorar comunicação interna"
            else:
                status = "CRÍTICA"
                card_class = "critical-card"
                emoji = "🚨"
                acao = "Revisão urgente dos processos"
            
            st.markdown(f"""
            <div class="insight-card {card_class}">
                <h4>{emoji} Gestão de Justificativas - {status}</h4>
                <p><strong>{taxa}%</strong> das faltas são adequadamente justificadas</p>
                <p>🎯 <strong>Próxima ação:</strong> {acao}</p>
                <p>📊 <strong>Meta corporativa:</strong> {'Atingida' if taxa > 75 else f'Faltam {75-taxa:.1f}% para meta'}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="section-title">🏢 Análise Departamental Avançada</div>', unsafe_allow_html=True)
        
        # Análise comparativa avançada
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 👥 **Segmentação por Gênero e Justificação**")
            
            genero_just = df_filtrado.groupby(['Genero', 'Justificada']).size().reset_index(name='count')
            genero_just['Genero_Label'] = genero_just['Genero'].map({'M': 'Masculino', 'F': 'Feminino'})
            
            fig_genero = px.bar(
                genero_just,
                x='Genero_Label',
                y='count',
                color='Justificada',
                title="",
                color_discrete_map={'Sim': '#10b981', 'Não': '#ef4444'},
                text='count',
                barmode='group'
            )
            
            fig_genero.update_layout(**plotly_theme['layout'])
            fig_genero.update_traces(
                texttemplate='%{text}',
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>%{fullData.name}: %{y}<extra></extra>'
            )
            
            st.plotly_chart(fig_genero, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            st.markdown("#### ⏰ **Análise por Tempo de Empresa**")
            
            # Criar bins para tempo de empresa
            df_tempo = df_filtrado.copy()
            df_tempo['Faixa_Tempo'] = pd.cut(
                df_tempo['Tempo_Empresa_Anos'],
                bins=[-1, 1, 3, 5, 10, 50],
                labels=['0-1 anos', '1-3 anos', '3-5 anos', '5-10 anos', '10+ anos']
            )
            
            tempo_counts = df_tempo['Faixa_Tempo'].value_counts().sort_index()
            
            fig_tempo = px.bar(
                x=tempo_counts.index.astype(str),
                y=tempo_counts.values,
                title="",
                color=tempo_counts.values,
                color_continuous_scale=['#8b5cf6', '#06b6d4', '#10b981'],
                text=tempo_counts.values
            )
            
            fig_tempo.update_layout(**plotly_theme['layout'])
            fig_tempo.update_traces(
                texttemplate='%{text}',
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Faltas: %{y}<extra></extra>'
            )
            fig_tempo.update_coloraxes(showscale=False)
            
            st.plotly_chart(fig_tempo, use_container_width=True, config={'displayModeBar': False})
        
        # Heatmap avançado departamento x motivo
        st.markdown("#### 🔥 **Mapa de Calor: Departamentos vs Motivos**")
        
        heatmap_data = pd.crosstab(df_filtrado['Departamento'], df_filtrado['Motivo'])
        
        fig_heatmap = px.imshow(
            heatmap_data.values,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            color_continuous_scale='Viridis',
            title="",
            aspect='auto',
            text_auto=True
        )
        
        fig_heatmap.update_layout(**plotly_theme['layout'])
        fig_heatmap.update_traces(
            textfont={"color": "white", "size": 12},
            hovertemplate='<b>%{y}</b> x <b>%{x}</b><br>Faltas: %{z}<extra></extra>'
        )
        fig_heatmap.update_layout(height=400)
        
        st.plotly_chart(fig_heatmap, use_container_width=True, config={'displayModeBar': False})
        
        # Tabela departamental analítica
        st.markdown("#### 💼 **Análise Departamental Detalhada**")
        
        dept_analysis = df_filtrado.groupby('Departamento').agg({
            'Nome': 'count',
            'Justificada': lambda x: (x == 'Sim').sum(),
            'Salario_Estimado': 'mean',
            'Tempo_Empresa_Anos': 'mean'
        }).reset_index()
        
        dept_analysis.columns = ['Departamento', 'Total_Faltas', 'Faltas_Justificadas', 'Salario_Medio', 'Tempo_Medio']
        dept_analysis['Taxa_Justificacao'] = round(
            (dept_analysis['Faltas_Justificadas'] / dept_analysis['Total_Faltas'] * 100), 1
        )
        dept_analysis['Custo_Estimado'] = dept_analysis['Total_Faltas'] * 180
        
        # Adicionar status
        def get_status_dept(row):
            if row['Taxa_Justificacao'] > 75 and row['Total_Faltas'] < 20:
                return '🟢 Controlado'
            elif row['Taxa_Justificacao'] > 60 and row['Total_Faltas'] < 35:
                return '🟡 Atenção'
            else:
                return '🔴 Crítico'
        
        dept_analysis['Status'] = dept_analysis.apply(get_status_dept, axis=1)
        
        # Ordenar por impacto
        dept_analysis = dept_analysis.sort_values('Custo_Estimado', ascending=False)
        
        st.dataframe(
            dept_analysis,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Departamento": st.column_config.TextColumn("🏢 Departamento", width="medium"),
                "Total_Faltas": st.column_config.NumberColumn("📊 Faltas", width="small"),
                "Taxa_Justificacao": st.column_config.NumberColumn("✅ Taxa (%)", format="%.1f", width="small"),
                "Salario_Medio": st.column_config.NumberColumn("💼 Salário Médio", format="R$ %.0f", width="medium"),
                "Custo_Estimado": st.column_config.NumberColumn("💰 Custo Total", format="R$ %.0f", width="medium"),
                "Status": st.column_config.TextColumn("🎯 Status", width="small")
            }
        )
        
    with tab3:
        st.markdown('<div class="section-title">📈 Análise de Tendências e Padrões</div>', unsafe_allow_html=True)
        
        # Análise de padrões semanais
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📅 **Padrão Semanal**")
            
            dias_semana = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            dia_counts = df_filtrado['Dia_Semana'].value_counts()
            dia_pt = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
            
            dia_data = []
            for i, dia_en in enumerate(dias_semana):
                count = dia_counts.get(dia_en, 0)
                dia_data.append({'Dia': dia_pt[i], 'Faltas': count})
            
            dia_df = pd.DataFrame(dia_data)
            
            fig_semana = px.bar(
                dia_df,
                x='Dia',
                y='Faltas',
                title="",
                color='Faltas',
                color_continuous_scale=['#ef4444', '#f59e0b', '#10b981'],
                text='Faltas'
            )
            
            fig_semana.update_layout(**plotly_theme['layout'])
            fig_semana.update_traces(
                texttemplate='%{text}',
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Faltas: %{y}<extra></extra>'
            )
            fig_semana.update_coloraxes(showscale=False)
            
            st.plotly_chart(fig_semana, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            st.markdown("#### 🗺️ **Distribuição Geográfica**")
            
            estado_counts = df_filtrado['Estado'].value_counts()
            
            fig_estado = px.bar(
                x=estado_counts.index,
                y=estado_counts.values,
                title="",
                color=estado_counts.values,
                color_continuous_scale=['#8b5cf6', '#06b6d4', '#10b981'],
                text=estado_counts.values
            )
            
            fig_estado.update_layout(**plotly_theme['layout'])
            fig_estado.update_traces(
                texttemplate='%{text}',
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Faltas: %{y}<extra></extra>'
            )
            fig_estado.update_coloraxes(showscale=False)
            
            st.plotly_chart(fig_estado, use_container_width=True, config={'displayModeBar': False})
        
        # Análise de correlação salário vs faltas
        st.markdown("#### 🔗 **Análise de Correlações**")
        
        correlation_data = df_filtrado.groupby('Nome').agg({
            'Salario_Estimado': 'first',
            'Data_Falta': 'count',
            'Tempo_Empresa_Anos': 'first'
        }).reset_index()
        correlation_data.columns = ['Funcionario', 'Salario', 'Num_Faltas', 'Tempo_Empresa']
        
        fig_scatter = px.scatter(
            correlation_data,
            x='Salario',
            y='Num_Faltas',
            size='Tempo_Empresa',
            title="Correlação: Salário vs Faltas (tamanho = tempo de empresa)",
            color='Tempo_Empresa',
            color_continuous_scale='Viridis'
        )
        
        fig_scatter.update_layout(**plotly_theme['layout'])
        fig_scatter.update_layout(height=400)
        
        st.plotly_chart(fig_scatter, use_container_width=True, config={'displayModeBar': False})
    
    with tab4:
        st.markdown('<div class="section-title">🔮 Inteligência Artificial & Análise Preditiva</div>', unsafe_allow_html=True)
        
        # Simulação de predições baseadas em tendências
        monthly_trend = df_filtrado.groupby('Mes_Nome').size().reset_index(name='Faltas')
        monthly_trend['Data'] = pd.to_datetime(monthly_trend['Mes_Nome'], format='%b/%Y')
        monthly_trend = monthly_trend.sort_values('Data')
        
        if len(monthly_trend) >= 3:
            # Predição simples baseada na média móvel
            recent_avg = monthly_trend['Faltas'].tail(3).mean()
            prediction = int(recent_avg * (1 + np.random.normal(0, 0.1)))
            confidence = 78  # Simulado
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">🎯 Predição - Próximo Mês</div>
                    <div class="metric-value">{prediction}</div>
                    <div class="metric-trend">Confiança: {confidence}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                trend_direction = "Crescente" if prediction > recent_avg else "Decrescente"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">📈 Tendência</div>
                    <div class="metric-value" style="font-size: 2rem;">{trend_direction}</div>
                    <div class="metric-trend">Baseado em IA</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                risk_level = "Alto" if prediction > recent_avg * 1.2 else "Médio" if prediction > recent_avg else "Baixo"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">⚠️ Nível de Risco</div>
                    <div class="metric-value" style="font-size: 2rem;">{risk_level}</div>
                    <div class="metric-trend">Análise preditiva</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Gráfico de predição
            st.markdown("#### 🤖 **Modelo Preditivo**")
            
            # Criar dados de predição
            last_date = monthly_trend['Data'].max()
            pred_dates = [last_date + pd.DateOffset(months=i) for i in range(1, 4)]
            pred_values = [prediction * (1 + np.random.normal(0, 0.05)) for _ in pred_dates]
            
            # Gráfico combinado
            fig_pred = go.Figure()
            
            # Dados históricos
            fig_pred.add_trace(go.Scatter(
                x=monthly_trend['Mes_Nome'],
                y=monthly_trend['Faltas'],
                mode='lines+markers',
                name='Dados Reais',
                line=dict(color='#8b5cf6', width=3),
                marker=dict(color='#06b6d4', size=10)
            ))
            
            # Predições
            pred_months = [d.strftime('%b/%Y') for d in pred_dates]
            fig_pred.add_trace(go.Scatter(
                x=pred_months,
                y=pred_values,
                mode='lines+markers',
                name='Predição IA',
                line=dict(color='#f59e0b', width=3, dash='dot'),
                marker=dict(color='#f59e0b', size=8, symbol='diamond')
            ))
            
            fig_pred.update_layout(**plotly_theme['layout'])
            fig_pred.update_layout(height=400)
            
            st.plotly_chart(fig_pred, use_container_width=True, config={'displayModeBar': False})
        
        else:
            st.info("📊 **Dados insuficientes** para análise preditiva. Necessários pelo menos 3 períodos históricos.")
        
        # Fatores de risco identificados pela IA
        st.markdown("#### ⚠️ **Fatores de Risco Identificados**")
        
        risk_factors = []
        
        # Análise de concentração departamental
        dept_counts = df_filtrado['Departamento'].value_counts()
        if len(dept_counts) > 0:
            dept_concentration = dept_counts.iloc[0] / metricas['total_faltas']
            if dept_concentration > 0.4:
                risk_factors.append({
                    'factor': 'Alta concentração departamental',
                    'impact': 'Crítico',
                    'score': 9,
                    'action': 'Intervenção imediata necessária'
                })
        
        # Análise de justificação
        if metricas['taxa_justificacao'] < 60:
            risk_factors.append({
                'factor': 'Taxa de justificação baixa',
                'impact': 'Alto',
                'score': 8,
                'action': 'Revisar processos de comunicação'
            })
        
        # Análise de tendência
        if len(monthly_trend) >= 2 and monthly_trend['Faltas'].iloc[-1] > monthly_trend['Faltas'].mean():
            risk_factors.append({
                'factor': 'Tendência crescente de faltas',
                'impact': 'Médio',
                'score': 6,
                'action': 'Monitoramento ativo'
            })
        
        # Exibir fatores de risco
        if risk_factors:
            for i, risk in enumerate(risk_factors):
                color_map = {
                    'Crítico': 'critical-card',
                    'Alto': 'warning-card',
                    'Médio': 'insight-card'
                }
                
                st.markdown(f"""
                <div class="insight-card {color_map.get(risk['impact'], 'insight-card')}">
                    <h4>🚨 Fator de Risco #{i+1} - Score: {risk['score']}/10</h4>
                    <p><strong>{risk['factor']}</strong></p>
                    <p><strong>Impacto:</strong> {risk['impact']}</p>
                    <p><strong>🎯 Ação Recomendada:</strong> {risk['action']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ **Nenhum fator de risco crítico identificado** pela análise de IA.")
    
    with tab5:
        st.markdown('<div class="section-title">📋 Centro de Relatórios Executivos</div>', unsafe_allow_html=True)
        
        # Seção de downloads
        st.markdown("#### 📥 **Downloads Disponíveis**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📊 **Excel Completo**", help="Dataset completo"):
                csv_data = df_filtrado.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv_data,
                    file_name=f"hr_analytics_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv"
                )
                st.success("✅ **Dados exportados!**")
        
        with col2:
            if st.button("📈 **Relatório Executivo**", help="Relatório para gestores"):
                relatorio_text = f"""
RELATÓRIO EXECUTIVO - HR ANALYTICS
==================================

📅 Período: {data_inicio.strftime('%d/%m/%Y')} a {data_fim.strftime('%d/%m/%Y')}
📊 Total de Faltas: {metricas['total_faltas']}
👥 Funcionários Impactados: {metricas['funcionarios_unicos']}
✅ Taxa de Justificação: {metricas['taxa_justificacao']}%
💰 Impacto Financeiro: R$ {metricas['custo_estimado']:,.2f}

🎯 PRINCIPAIS INSIGHTS:
- Departamento crítico: {dept_counts.index[0] if len(dept_counts) > 0 else 'N/A'}
- Motivo predominante: {df_filtrado['Motivo'].value_counts().index[0] if len(df_filtrado) > 0 else 'N/A'}
- Status geral: {'Controlado' if metricas['taxa_justificacao'] > 70 else 'Crítico'}

💡 RECOMENDAÇÕES:
1. Intervenção no departamento crítico
2. Implementar canal digital para justificativas
3. Programa de flexibilidade familiar
4. Monitoramento em tempo real

Relatório gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}
"""
                
                st.download_button(
                    label="⬇️ Download Relatório",
                    data=relatorio_text,
                    file_name=f"relatorio_hr_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain"
                )
                st.success("✅ **Relatório gerado!**")
        
        with col3:
            st.button("🔮 **Análise Preditiva**", help="Predições da IA", disabled=True)
            st.info("📊 Em desenvolvimento")
        
        with col4:
            st.button("📊 **Dashboard PDF**", help="Snapshot visual", disabled=True)
            st.info("🚧 Em breve!")
        
        # Resumo executivo final
        st.markdown("#### 📊 **Resumo Executivo Final**")
        
        st.markdown(f"""
        <div class="content-container">
            <h3 style="color: white; text-align: center; margin-bottom: 2rem;">
                📈 RELATÓRIO FINAL DE ABSENTEÍSMO
            </h3>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
                <div style="background: rgba(139, 92, 246, 0.1); padding: 1.5rem; border-radius: 12px;">
                    <h4 style="color: #8b5cf6;">📊 SITUAÇÃO ATUAL</h4>
                    <p><strong>Total de Faltas:</strong> {metricas['total_faltas']}</p>
                    <p><strong>Funcionários Afetados:</strong> {metricas['funcionarios_unicos']}</p>
                    <p><strong>Taxa de Justificação:</strong> {metricas['taxa_justificacao']}%</p>
                    <p><strong>Custo Estimado:</strong> R$ {metricas['custo_estimado']:,.0f}</p>
                </div>
                
                <div style="background: rgba(16, 185, 129, 0.1); padding: 1.5rem; border-radius: 12px;">
                    <h4 style="color: #10b981;">🎯 PONTOS FORTES</h4>
                    <p>✅ Sistema de monitoramento ativo</p>
                    <p>✅ Dados organizados e estruturados</p>
                    <p>✅ {'Taxa de justificação adequada' if metricas['taxa_justificacao'] > 70 else 'Processo de melhoria em andamento'}</p>
                    <p>✅ Visibilidade total dos dados</p>
                </div>
                
                <div style="background: rgba(245, 158, 11, 0.1); padding: 1.5rem; border-radius: 12px;">
                    <h4 style="color: #f59e0b;">⚠️ ÁREAS DE ATENÇÃO</h4>
                    <p>🔍 Concentração em departamentos específicos</p>
                    <p>🔍 Padrões sazonais de absenteísmo</p>
                    <p>🔍 Correlação com tempo de empresa</p>
                    <p>🔍 Impacto financeiro crescente</p>
                </div>
                
                <div style="background: rgba(239, 68, 68, 0.1); padding: 1.5rem; border-radius: 12px;">
                    <h4 style="color: #ef4444;">🚀 PRÓXIMOS PASSOS</h4>
                    <p>1. Implementar ações corretivas</p>
                    <p>2. Monitoramento contínuo</p>
                    <p>3. Programas de bem-estar</p>
                    <p>4. Análise preditiva avançada</p>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 2rem; padding: 1rem; background: rgba(255,255,255,0.05); border-radius: 8px;">
                <h4 style="color: white;">💡 RECOMENDAÇÃO ESTRATÉGICA</h4>
                <p style="color: rgba(255,255,255,0.9);">
                    Foco na implementação de um programa integrado de gestão de absenteísmo 
                    com ênfase em prevenção, comunicação efetiva e suporte aos funcionários.
                </p>
                <p style="color: #06b6d4; font-weight: 600;">
                    ROI Esperado: 25-40% de redução nos custos de absenteísmo em 6 meses
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer elegante
    st.markdown("""
    <div class="footer-container">
        <h3>🚀 HR Analytics Dashboard</h3>
        <p>Sistema desenvolvido para otimização da gestão de recursos humanos através de análise avançada de dados</p>
        <p style="margin-top: 1rem; font-size: 0.9rem; opacity: 0.7;">
            Powered by Streamlit • Python • Plotly | Dados simulados para demonstração
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
