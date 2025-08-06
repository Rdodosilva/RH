# -*- coding: utf-8 -*-
"""
HR Analytics Intelligence Suite
Dashboard Premium para Análise de Recursos Humanos
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import random
import time
from typing import Dict
import warnings

warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="HR Analytics Intelligence Suite",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Ultra Premium
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e293b, #6d28d9, #1e293b);
        background-size: 400% 400%;
        animation: gradientShift 20s ease infinite;
        font-family: 'Inter', sans-serif;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 0%; }
        25% { background-position: 100% 0%; }
        50% { background-position: 100% 100%; }
        75% { background-position: 0% 100%; }
        100% { background-position: 0% 0%; }
    }
    
    .mega-header {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(6, 182, 212, 0.2));
        backdrop-filter: blur(20px);
        border: 2px solid rgba(255, 255, 255, 0.18);
        border-radius: 25px;
        padding: 4rem 3rem;
        text-align: center;
        margin: 2rem 0;
        color: white;
        box-shadow: 0 25px 50px -12px rgba(139, 92, 246, 0.5);
        position: relative;
        overflow: hidden;
    }
    
    .mega-header h1 {
        font-family: 'Orbitron', monospace;
        font-size: 4rem;
        font-weight: 900;
        margin: 0;
        background: linear-gradient(135deg, #ffffff, #8b5cf6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 50px rgba(255, 255, 255, 0.3);
        letter-spacing: 2px;
    }
    
    .mega-header .subtitle {
        font-size: 1.5rem;
        font-weight: 300;
        margin: 1rem 0;
        opacity: 0.9;
        letter-spacing: 1px;
    }
    
    .tech-badge {
        display: inline-block;
        background: rgba(139, 92, 246, 0.2);
        border: 1px solid rgba(139, 92, 246, 0.5);
        border-radius: 20px;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }
    
    .tech-badge:hover {
        background: rgba(139, 92, 246, 0.4);
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 5px 15px rgba(139, 92, 246, 0.4);
    }
    
    .premium-metric-card {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        backdrop-filter: blur(15px);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    .premium-metric-card:hover {
        transform: translateY(-15px) scale(1.02);
        box-shadow: 0 30px 60px rgba(139, 92, 246, 0.3);
        border-color: rgba(139, 92, 246, 0.5);
    }
    
    .premium-metric-value {
        font-family: 'Orbitron', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        margin: 1rem 0;
        background: linear-gradient(135deg, #ffffff, #8b5cf6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.2);
    }
    
    .premium-metric-label {
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 1rem;
    }
    
    .premium-metric-trend {
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.7);
        margin-top: 1rem;
        font-weight: 500;
    }
    
    .trend-positive { color: #10b981; }
    .trend-negative { color: #ef4444; }
    .trend-neutral { color: #f59e0b; }
    
    .ultra-insight-card {
        background: linear-gradient(145deg, rgba(139, 92, 246, 0.15), rgba(139, 92, 246, 0.05));
        backdrop-filter: blur(20px);
        border: 2px solid rgba(139, 92, 246, 0.3);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        color: white;
        border-left: 6px solid #8b5cf6;
        box-shadow: 0 15px 35px rgba(139, 92, 246, 0.2);
        transition: all 0.4s ease;
    }
    
    .ultra-insight-card:hover {
        transform: translateX(10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(139, 92, 246, 0.3);
    }
    
    .ultra-insight-card h4 {
        font-family: 'Orbitron', monospace;
        color: #ffffff;
        margin-bottom: 1rem;
        font-size: 1.2rem;
        font-weight: 700;
    }
    
    .success-insight {
        background: linear-gradient(145deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.05));
        border-color: rgba(16, 185, 129, 0.3);
        border-left-color: #10b981;
        box-shadow: 0 15px 35px rgba(16, 185, 129, 0.2);
    }
    
    .warning-insight {
        background: linear-gradient(145deg, rgba(245, 158, 11, 0.15), rgba(245, 158, 11, 0.05));
        border-color: rgba(245, 158, 11, 0.3);
        border-left-color: #f59e0b;
        box-shadow: 0 15px 35px rgba(245, 158, 11, 0.2);
    }
    
    .critical-insight {
        background: linear-gradient(145deg, rgba(239, 68, 68, 0.15), rgba(239, 68, 68, 0.05));
        border-color: rgba(239, 68, 68, 0.3);
        border-left-color: #ef4444;
        box-shadow: 0 15px 35px rgba(239, 68, 68, 0.2);
    }
    
    .ultra-section-title {
        color: white;
        font-family: 'Orbitron', monospace;
        font-size: 2.5rem;
        font-weight: 900;
        text-align: center;
        margin: 4rem 0 2rem 0;
        background: linear-gradient(135deg, #ffffff, #8b5cf6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 50px rgba(255, 255, 255, 0.3);
        letter-spacing: 3px;
        text-transform: uppercase;
        position: relative;
    }
    
    .ultra-section-title::after {
        content: '';
        position: absolute;
        bottom: -15px;
        left: 50%;
        transform: translateX(-50%);
        width: 200px;
        height: 4px;
        background: linear-gradient(90deg, transparent, #8b5cf6, #06b6d4, #10b981, transparent);
        border-radius: 2px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6, #06b6d4) !important;
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 10px 25px rgba(139, 92, 246, 0.3) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 0 20px 40px rgba(139, 92, 246, 0.4) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
        background: linear-gradient(135deg, #7c3aed, #0891b2) !important;
    }
    
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:hover,
    .stMultiSelect > div > div:hover {
        border-color: rgba(139, 92, 246, 0.5) !important;
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.2) !important;
    }
    
    .stDataFrame {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 15px !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2) !important;
    }
    
    .premium-loading {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        height: 300px;
        color: white;
    }
    
    .premium-spinner {
        width: 80px;
        height: 80px;
        border: 4px solid rgba(139, 92, 246, 0.3);
        border-top: 4px solid #8b5cf6;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-bottom: 2rem;
        box-shadow: 0 0 30px rgba(139, 92, 246, 0.5);
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-text {
        font-family: 'Orbitron', monospace;
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #8b5cf6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .status-indicator {
        display: inline-block;
        width: 15px;
        height: 15px;
        border-radius: 50%;
        margin-right: 10px;
        background: #10b981;
        animation: pulse 2s infinite;
        box-shadow: 0 0 10px #10b981;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.1); opacity: 0.7; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 30px !important;
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 15px !important;
        padding: 10px !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 10px !important;
        color: rgba(255, 255, 255, 0.8) !important;
        font-weight: 700 !important;
        padding: 15px 30px !important;
        transition: all 0.4s ease !important;
        border: 2px solid transparent !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-family: 'Orbitron', monospace !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8b5cf6, #06b6d4) !important;
        color: white !important;
        box-shadow: 0 10px 25px rgba(139, 92, 246, 0.4) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        transform: translateY(-2px) !important;
    }
    
    @media (max-width: 768px) {
        .mega-header h1 { font-size: 2.5rem; }
        .premium-metric-value { font-size: 2rem; }
        .ultra-section-title { font-size: 1.8rem; }
        .premium-metric-card { padding: 1.5rem 1rem; }
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    header {visibility: hidden;}
    
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #8b5cf6, #06b6d4);
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(139, 92, 246, 0.5);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300, show_spinner=False)
def generate_premium_dataset() -> pd.DataFrame:
    """Gera dataset ultra-realista para demonstração premium"""
    random.seed(42)
    np.random.seed(42)
    
    # Dados corporativos realistas
    departamentos = [
        'Tecnologia da Informacao', 'Recursos Humanos', 'Operacoes Industriais',
        'Financeiro e Controladoria', 'Marketing Digital', 'Vendas Corporativas', 
        'Logistica Integrada', 'Qualidade e Processos', 'Juridico Empresarial'
    ]
    
    estados_brasileiros = [
        'SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'PE', 'GO', 'DF'
    ]
    
    motivos_ausencia = [
        'Consulta Medica', 'Doenca Familiar', 'Compromissos Pessoais',
        'Atestado Medico', 'Emergencia Familiar', 'Problemas de Transporte',
        'Questoes de Saude Mental', 'Acompanhamento Medico', 'Licenca Maternidade',
        'Acidente de Trabalho', 'Sem Justificativa', 'Home Office'
    ]
    
    cargos_hierarquia = [
        'Estagiario', 'Assistente', 'Analista Jr', 'Analista Pleno', 
        'Analista Senior', 'Especialista', 'Coordenador', 'Supervisor',
        'Gerente', 'Gerente Senior', 'Diretor', 'Vice-Presidente'
    ]
    
    nomes_brasileiros = [
        'Ana Silva', 'Joao Santos', 'Maria Oliveira', 'Pedro Costa', 'Carla Souza',
        'Bruno Almeida', 'Fernanda Lima', 'Rafael Pereira', 'Juliana Rodrigues',
        'Thiago Ferreira', 'Camila Martins', 'Lucas Barbosa', 'Patricia Gomes'
    ]
    
    dados_corporativos = []
    base_date = datetime(2024, 1, 1)
    
    # Gerar 400 registros ultra-realistas
    for i in range(400):
        # Distribuição inteligente por departamento
        departamento = random.choice(departamentos)
        motivo = random.choice(motivos_ausencia)
        
        # Sistema inteligente de justificação
        if motivo in ['Consulta Medica', 'Atestado Medico']:
            justificada = 'Sim' if random.random() > 0.1 else 'Nao'
        elif motivo == 'Emergencia Familiar':
            justificada = 'Sim' if random.random() > 0.2 else 'Nao'
        elif motivo == 'Sem Justificativa':
            justificada = 'Nao'
        else:
            justificada = 'Sim' if random.random() > 0.4 else 'Nao'
        
        # Distribuição temporal realista
        mes = random.randint(1, 12)
        dia = random.randint(1, 28)
        data_falta = datetime(2024, mes, dia)
        
        # Hierarquia salarial realista
        cargo = random.choice(cargos_hierarquia)
        salario_ranges = {
            'Estagiario': (1500, 2500), 'Assistente': (2800, 4000),
            'Analista Jr': (4000, 6500), 'Analista Pleno': (6500, 9500),
            'Analista Senior': (9000, 14000), 'Especialista': (12000, 18000),
            'Coordenador': (15000, 22000), 'Supervisor': (18000, 26000),
            'Gerente': (22000, 35000), 'Gerente Senior': (30000, 50000),
            'Diretor': (40000, 70000), 'Vice-Presidente': (60000, 120000)
        }
        
        salario_min, salario_max = salario_ranges.get(cargo, (4000, 10000))
        salario = random.randint(salario_min, salario_max)
        
        genero = random.choice(['M', 'F'])
        nome = f"{random.choice(nomes_brasileiros)} {i+1:03d}"
        
        # Anos de empresa realista
        anos_empresa = random.choices(
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15], 
            weights=[15, 20, 15, 12, 10, 8, 7, 5, 4, 2, 1, 1]
        )[0]
        
        data_admissao = base_date - timedelta(days=anos_empresa * 365 + random.randint(0, 365))
        
        # Criticidade baseada no motivo
        if motivo in ['Sem Justificativa', 'Problemas de Transporte']:
            criticidade = 'Alta'
        elif motivo in ['Compromissos Pessoais']:
            criticidade = 'Media'
        else:
            criticidade = 'Baixa'
        
        dados_corporativos.append({
            'ID_Funcionario': f"EMP{i+1:04d}",
            'Nome_Completo': nome,
            'Cargo_Atual': cargo,
            'Departamento': departamento,
            'Estado_UF': random.choice(estados_brasileiros),
            'Data_Ausencia': data_falta,
            'Motivo_Ausencia': motivo,
            'Status_Justificativa': justificada,
            'Genero': genero,
            'Data_Admissao': data_admissao,
            'Salario_Atual': salario,
            'Nivel_Hierarquico': cargos_hierarquia.index(cargo),
            'Criticidade_Ausencia': criticidade
        })
    
    df = pd.DataFrame(dados_corporativos)
    
    # Processamento avançado de dados
    df['Mes_Referencia'] = df['Data_Ausencia'].dt.strftime('%Y-%m')
    df['Mes_Nome_BR'] = df['Data_Ausencia'].dt.strftime('%b/%Y')
    df['Dia_Semana_BR'] = df['Data_Ausencia'].dt.day_name().map({
        'Monday': 'Segunda-feira', 'Tuesday': 'Terca-feira', 'Wednesday': 'Quarta-feira',
        'Thursday': 'Quinta-feira', 'Friday': 'Sexta-feira', 'Saturday': 'Sabado', 'Sunday': 'Domingo'
    })
    df['Trimestre'] = df['Data_Ausencia'].dt.quarter
    df['Anos_Empresa'] = ((datetime.now() - df['Data_Admissao']).dt.days / 365).astype(int).clip(0, 50)
    df['Faixa_Salarial'] = pd.cut(df['Salario_Atual'], 
                                  bins=[0, 5000, 10000, 20000, 50000, 150000],
                                  labels=['Ate 5k', '5k-10k', '10k-20k', '20k-50k', '50k+'])
    
    return df

@st.cache_data(ttl=300)
def calculate_premium_metrics(df: pd.DataFrame) -> Dict:
    """Calcula métricas avançadas com KPIs corporativos"""
    if len(df) == 0:
        return {
            'total_ausencias': 0, 'funcionarios_impactados': 0, 'taxa_justificacao': 0,
            'departamentos_criticos': 0, 'impacto_financeiro': 0, 'salario_medio': 0,
            'ausencias_por_funcionario': 0, 'taxa_absenteismo': 0, 'pico_temporal': 'N/A',
            'tendencia_geral': 'Estavel', 'indice_criticidade': 'Baixo', 'score_rh': 85,
            'ausencias_criticas': 0
        }
    
    total_ausencias = len(df)
    funcionarios_impactados = df['Nome_Completo'].nunique()
    ausencias_justificadas = len(df[df['Status_Justificativa'] == 'Sim'])
    taxa_justificacao = round((ausencias_justificadas / total_ausencias * 100), 2)
    departamentos_criticos = df['Departamento'].nunique()
    
    # Métricas financeiras avançadas
    custo_medio_ausencia = 280
    impacto_financeiro = total_ausencias * custo_medio_ausencia
    salario_medio = df['Salario_Atual'].mean()
    
    # KPIs de RH avançados
    ausencias_por_funcionario = round(total_ausencias / funcionarios_impactados, 2)
    taxa_absenteismo = round((total_ausencias / (funcionarios_impactados * 22)) * 100, 2)
    
    # Análise temporal
    pico_temporal = df['Mes_Nome_BR'].value_counts().index[0] if len(df) > 0 else 'N/A'
    
    # Índice de criticidade
    ausencias_criticas = len(df[df['Criticidade_Ausencia'] == 'Alta'])
    indice_criticidade = 'Alto' if ausencias_criticas > total_ausencias * 0.3 else \
                        'Medio' if ausencias_criticas > total_ausencias * 0.15 else 'Baixo'
    
    # Score de RH (0-100)
    score_base = 100
    score_base -= max(0, (taxa_absenteismo - 3) * 5)
    score_base -= max(0, (100 - taxa_justificacao) * 0.3)
    score_base -= ausencias_criticas * 0.5
    score_rh = max(0, min(100, round(score_base)))
    
    # Tendência
    tendencia_geral = 'Estavel'
    if total_ausencias > 150:
        tendencia_geral = 'Crescente Preocupante'
    elif total_ausencias > 100:
        tendencia_geral = 'Crescente Leve'
    elif total_ausencias < 50:
        tendencia_geral = 'Decrescente Positiva'
    
    return {
        'total_ausencias': total_ausencias,
        'funcionarios_impactados': funcionarios_impactados,
        'taxa_justificacao': taxa_justificacao,
        'departamentos_criticos': departamentos_criticos,
        'impacto_financeiro': impacto_financeiro,
        'salario_medio': salario_medio,
        'ausencias_por_funcionario': ausencias_por_funcionario,
        'taxa_absenteismo': taxa_absenteismo,
        'pico_temporal': pico_temporal,
        'tendencia_geral': tendencia_geral,
        'indice_criticidade': indice_criticidade,
        'score_rh': score_rh,
        'ausencias_criticas': ausencias_criticas
    }

def create_plotly_theme() -> Dict:
    """Tema para gráficos Plotly"""
    return {
        'layout': {
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'font': {'color': 'white', 'family': 'Inter, sans-serif', 'size': 12},
            'title': {'font': {'size': 18, 'color': 'white'}, 'x': 0.5},
            'xaxis': {
                'gridcolor': 'rgba(139, 92, 246, 0.2)',
                'linecolor': 'rgba(255, 255, 255, 0.3)',
                'tickcolor': 'rgba(255, 255, 255, 0.3)',
                'tickfont': {'color': 'white', 'size': 11}
            },
            'yaxis': {
                'gridcolor': 'rgba(139, 92, 246, 0.2)',
                'linecolor': 'rgba(255, 255, 255, 0.3)',
                'tickcolor': 'rgba(255, 255, 255, 0.3)',
                'tickfont': {'color': 'white', 'size': 11}
            },
            'legend': {'font': {'color': 'white', 'size': 11}},
            'colorway': ['#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444'],
            'margin': dict(l=40, r=40, t=60, b=40)
        }
    }

def display_loading():
    """Loading premium"""
    loading_placeholder = st.empty()
    with loading_placeholder.container():
        st.markdown("""
        <div class="premium-loading
def display_loading():
    """Loading premium"""
    loading_placeholder = st.empty()
    with loading_placeholder.container():
        st.markdown("""
        <div class="premium-loading">
            <div class="premium-spinner"></div>
            <div class="loading-text">Iniciando HR Analytics Intelligence Suite...</div>
            <p style="color: rgba(255,255,255,0.6); margin-top: 1rem;">
                Processando 400+ registros corporativos
            </p>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(2)
    loading_placeholder.empty()

def create_chart(df: pd.DataFrame, chart_type: str):
    """Criador de gráficos"""
    theme = create_plotly_theme()
    
    if chart_type == "departmental":
        dept_data = df['Departamento'].value_counts().head(8)
        fig = px.bar(
            x=dept_data.values,
            y=dept_data.index,
            orientation='h',
            title="Análise Departamental",
            color=dept_data.values,
            color_continuous_scale=['#ef4444', '#f59e0b', '#8b5cf6', '#06b6d4', '#10b981']
        )
        fig.update_traces(
            texttemplate='%{x}',
            textposition='outside',
            textfont=dict(size=12, color='white')
        )
        fig.update_layout(**theme['layout'])
        fig.update_layout(height=400, showlegend=False)
        fig.update_coloraxes(showscale=False)
        return fig
    
    elif chart_type == "motivos":
        motivo_data = df['Motivo_Ausencia'].value_counts().head(6)
        fig = px.pie(
            values=motivo_data.values,
            names=motivo_data.index,
            title="Distribuição de Motivos",
            color_discrete_sequence=['#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#ec4899']
        )
        fig.update_traces(
            textinfo='percent+label',
            textfont_size=11,
            textfont_color='white'
        )
        fig.update_layout(**theme['layout'])
        fig.update_layout(height=400)
        return fig
    
    elif chart_type == "timeline":
        timeline_data = df.groupby('Mes_Nome_BR').size().reset_index(name='Ausencias')
        timeline_data['Data_Sort'] = pd.to_datetime(timeline_data['Mes_Nome_BR'], format='%b/%Y')
        timeline_data = timeline_data.sort_values('Data_Sort')
        
        fig = px.line(
            timeline_data,
            x='Mes_Nome_BR',
            y='Ausencias',
            title="Evolução Temporal",
            markers=True
        )
        fig.update_traces(
            line=dict(color='#8b5cf6', width=3),
            marker=dict(color='#06b6d4', size=8)
        )
        fig.update_layout(**theme['layout'])
        fig.update_layout(height=350)
        return fig

def main():
    """Função principal"""
    
    # Loading inicial
    if 'loaded' not in st.session_state:
        display_loading()
        st.session_state.loaded = True
    
    # Header
    st.markdown("""
    <div class="mega-header">
        <h1>HR ANALYTICS INTELLIGENCE SUITE</h1>
        <p class="subtitle">Plataforma Avançada de Análise Corporativa com IA</p>
        <div style="margin-top: 2rem;">
            <span class="tech-badge">Machine Learning</span>
            <span class="tech-badge">Real-time Analytics</span>
            <span class="tech-badge">Business Intelligence</span>
            <span class="tech-badge">Corporate Dashboard</span>
        </div>
        <div style="margin-top: 1.5rem;">
            <span class="status-indicator"></span>
            <span style="font-size: 0.9rem;">SISTEMA OPERACIONAL | DADOS SINCRONIZADOS</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregamento de dados
    with st.spinner(""):
        df = generate_premium_dataset()
    
    if len(df) == 0:
        st.error("❌ Falha no carregamento dos dados.")
        return
    
    st.success(f"✅ **{len(df)} registros corporativos** processados com sucesso!")
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h2 style="color: white; font-family: 'Orbitron', monospace;">
                CENTRO DE CONTROLE
            </h2>
            <p style="color: rgba(255,255,255,0.7);">Configure sua análise</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### **Filtros Departamentais**")
        departamentos_selecionados = st.multiselect(
            "Departamentos:",
            options=sorted(df['Departamento'].unique()),
            default=sorted(df['Departamento'].unique())
        )
        
        st.markdown("### **Análise de Motivos**")
        motivos_selecionados = st.multiselect(
            "Motivos:",
            options=sorted(df['Motivo_Ausencia'].unique()),
            default=sorted(df['Motivo_Ausencia'].unique())
        )
        
        st.markdown("### **Status de Conformidade**")
        justificacao_filtro = st.selectbox(
            "Justificativas:",
            options=['Todas', 'Sim', 'Nao']
        )
        
        st.markdown("### **Período de Análise**")
        try:
            col1, col2 = st.columns(2)
            with col1:
                data_inicio = st.date_input(
                    "Início:",
                    value=df['Data_Ausencia'].min().date()
                )
            with col2:
                data_fim = st.date_input(
                    "Fim:",
                    value=df['Data_Ausencia'].max().date()
                )
        except:
            data_inicio = datetime.now().date()
            data_fim = datetime.now().date()
    
    # Aplicar filtros
    try:
        df_filtrado = df.copy()
        
        if departamentos_selecionados:
            df_filtrado = df_filtrado[df_filtrado['Departamento'].isin(departamentos_selecionados)]
        
        if motivos_selecionados:
            df_filtrado = df_filtrado[df_filtrado['Motivo_Ausencia'].isin(motivos_selecionados)]
        
        if justificacao_filtro != 'Todas':
            df_filtrado = df_filtrado[df_filtrado['Status_Justificativa'] == justificacao_filtro]
        
        try:
            df_filtrado = df_filtrado[
                (df_filtrado['Data_Ausencia'].dt.date >= data_inicio) &
                (df_filtrado['Data_Ausencia'].dt.date <= data_fim)
            ]
        except:
            pass
            
    except Exception:
        df_filtrado = df.copy()
    
    if len(df_filtrado) == 0:
        st.warning("⚠️ Nenhum registro encontrado. Exibindo dados completos.")
        df_filtrado = df.copy()
    
    # Calcular métricas
    metricas = calculate_premium_metrics(df_filtrado)
    
    # Sistema de abas
    tab1, tab2, tab3 = st.tabs([
        "🎯 COMMAND CENTER",
        "📊 ANALYTICS 360°", 
        "📋 EXECUTIVE SUITE"
    ])
    
    with tab1:
        st.markdown('<div class="ultra-section-title">CENTRO DE COMANDO EXECUTIVO</div>', unsafe_allow_html=True)
        
        # Cards de métricas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            trend_class = "trend-negative" if metricas['total_ausencias'] > 150 else "trend-positive" if metricas['total_ausencias'] < 100 else "trend-neutral"
            st.markdown(f"""
            <div class="premium-metric-card">
                <div class="premium-metric-label">TOTAL DE AUSÊNCIAS</div>
                <div class="premium-metric-value">{metricas['total_ausencias']}</div>
                <div class="premium-metric-trend {trend_class}">
                    {round((metricas['total_ausencias']/len(df)*100), 1)}% do dataset
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="premium-metric-card">
                <div class="premium-metric-label">COLABORADORES IMPACTADOS</div>
                <div class="premium-metric-value">{metricas['funcionarios_impactados']}</div>
                <div class="premium-metric-trend">
                    {metricas['ausencias_por_funcionario']} ausências/pessoa
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            taxa_cor = "trend-positive" if metricas['taxa_justificacao'] > 80 else "trend-negative" if metricas['taxa_justificacao'] < 60 else "trend-neutral"
            st.markdown(f"""
            <div class="premium-metric-card">
                <div class="premium-metric-label">TAXA DE CONFORMIDADE</div>
                <div class="premium-metric-value">{metricas['taxa_justificacao']}%</div>
                <div class="premium-metric-trend {taxa_cor}">
                    {'🟢 Excelente' if metricas['taxa_justificacao'] > 80 else '🔴 Crítica' if metricas['taxa_justificacao'] < 60 else '🟡 Moderada'}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="premium-metric-card">
                <div class="premium-metric-label">IMPACTO FINANCEIRO</div>
                <div class="premium-metric-value">R$ {metricas['impacto_financeiro']:,.0f}</div>
                <div class="premium-metric-trend">
                    R$ {metricas['impacto_financeiro']/max(1, metricas['total_ausencias']):,.0f} por ausência
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Segunda linha de métricas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="premium-metric-card">
                <div class="premium-metric-label">DEPARTAMENTOS CRÍTICOS</div>
                <div class="premium-metric-value">{metricas['departamentos_criticos']}</div>
                <div class="premium-metric-trend">de 9 departamentos</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            taxa_cor = "trend-positive" if metricas['taxa_absenteismo'] < 3 else "trend-negative" if metricas['taxa_absenteismo'] > 6 else "trend-neutral"
            st.markdown(f"""
            <div class="premium-metric-card">
                <div class="premium-metric-label">TAXA DE ABSENTEÍSMO</div>
                <div class="premium-metric-value">{metricas['taxa_absenteismo']}%</div>
                <div class="premium-metric-trend {taxa_cor}">
                    {'🟢 Baixa' if metricas['taxa_absenteismo'] < 3 else '🔴 Alta' if metricas['taxa_absenteismo'] > 6 else '🟡 Moderada'}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="premium-metric-card">
                <div class="premium-metric-label">PICO TEMPORAL</div>
                <div class="premium-metric-value" style="font-size: 2rem;">{metricas['pico_temporal']}</div>
                <div class="premium-metric-trend">período crítico</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            score_cor = "trend-positive" if metricas['score_rh'] > 80 else "trend-negative" if metricas['score_rh'] < 60 else "trend-neutral"
            st.markdown(f"""
            <div class="premium-metric-card">
                <div class="premium-metric-label">SCORE CORPORATIVO</div>
                <div class="premium-metric-value">{metricas['score_rh']}</div>
                <div class="premium-metric-trend {score_cor}">
                    {'🏆 Excelente' if metricas['score_rh'] > 80 else '⚠️ Crítico' if metricas['score_rh'] < 60 else '📊 Bom'}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Gráficos principais
        st.markdown('<div class="ultra-section-title">ANÁLISE VISUAL INTELIGENTE</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                fig_dept = create_chart(df_filtrado, "departmental")
                st.plotly_chart(fig_dept, use_container_width=True, config={'displayModeBar': False})
            except Exception as e:
                st.error(f"Erro no gráfico: {str(e)}")
        
        with col2:
            try:
                fig_motivos = create_chart(df_filtrado, "motivos")
                st.plotly_chart(fig_motivos, use_container_width=True, config={'displayModeBar': False})
            except Exception as e:
                st.error(f"Erro no gráfico: {str(e)}")
        
        # Timeline
        try:
            fig_timeline = create_chart(df_filtrado, "timeline")
            st.plotly_chart(fig_timeline, use_container_width=True, config={'displayModeBar': False})
        except Exception as e:
            st.error(f"Erro na timeline: {str(e)}")
        
        # Insights inteligentes
        st.markdown('<div class="ultra-section-title">INSIGHTS DE IA</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            try:
                if len(df_filtrado) > 0:
                    dept_counts = df_filtrado['Departamento'].value_counts()
                    dept_top = dept_counts.index[0]
                    dept_valor = dept_counts.iloc[0]
                    dept_perc = round((dept_valor / metricas['total_ausencias'] * 100), 1)
                    
                    card_class = "critical-insight" if dept_perc > 35 else "warning-insight" if dept_perc > 25 else "success-insight"
                    status = "CRÍTICO" if dept_perc > 35 else "ATENÇÃO" if dept_perc > 25 else "CONTROLADO"
                    
                    st.markdown(f"""
                    <div class="ultra-insight-card {card_class}">
                        <h4>DEPARTAMENTO CRÍTICO - {status}</h4>
                        <p><strong>{dept_top}</strong> concentra <strong>{dept_valor} ausências</strong> ({dept_perc}% do total)</p>
                        <p><strong>Impacto:</strong> R$ {dept_valor * 280:,.0f}</p>
                        <p><strong>Ação IA:</strong> {'Intervenção imediata' if dept_perc > 35 else 'Monitoramento ativo' if dept_perc > 25 else 'Manter padrão'}</p>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception:
                st.info("Dados insuficientes")
        
        with col2:
            try:
                if len(df_filtrado) > 0:
                    motivo_counts = df_filtrado['Motivo_Ausencia'].value_counts()
                    motivo_top = motivo_counts.index[0]
                    motivo_valor = motivo_counts.iloc[0]
                    motivo_perc = round((motivo_valor / metricas['total_ausencias'] * 100), 1)
                    
                    recomendacoes = {
                        'Consulta Medica': 'Programa de saúde preventiva',
                        'Atestado Medico': 'Análise ambiente ocupacional',
                        'Emergencia Familiar': 'Flexibilização horários',
                        'Sem Justificativa': 'Revisão disciplinar'
                    }
                    
                    recomendacao = recomendacoes.get(motivo_top, 'Investigação detalhada')
                    card_class = "critical-insight" if motivo_top == 'Sem Justificativa' else "warning-insight"
                    
                    st.markdown(f"""
                    <div class="ultra-insight-card {card_class}">
                        <h4>MOTIVO PREDOMINANTE</h4>
                        <p><strong>{motivo_top}</strong> - {motivo_valor} casos ({motivo_perc}%)</p>
                        <p><strong>Solução IA:</strong> {recomendacao}</p>
                        <p><strong>ROI Estimado:</strong> {'Alto' if motivo_perc > 25 else 'Médio' if motivo_perc > 15 else 'Baixo'}</p>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception:
                st.info("Dados insuficientes")
        
        with col3:
            taxa = metricas['taxa_justificacao']
            score = metricas['score_rh']
            
            if score > 85:
                status = "EXCEPCIONAL"
                card_class = "success-insight"
                acao = "Manter excelência"
            elif score > 70:
                status = "BOM"
                card_class = "ultra-insight-card"
                acao = "Otimizações pontuais"
            elif score > 60:
                status = "MODERADO"
                card_class = "warning-insight"
                acao = "Melhorias estruturais"
            else:
                status = "CRÍTICO"
                card_class = "critical-insight"
                acao = "Intervenção imediata"
            
            st.markdown(f"""
            <div class="ultra-insight-card {card_class}">
                <h4>SCORE CORPORATIVO - {status}</h4>
                <p><strong>Score:</strong> {score}/100</p>
                <p><strong>Conformidade:</strong> {taxa}%</p>
                <p><strong>Estratégia:</strong> {acao}</p>
                <p><strong>Benchmark:</strong> {'Acima' if score > 75 else 'Médio' if score > 60 else 'Abaixo'} do mercado</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="ultra-section-title">ANALYTICS 360° AVANÇADO</div>', unsafe_allow_html=True)
        
        # Análise por gênero e padrões semanais
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### **Análise por Gênero**")
            try:
                if len(df_filtrado) > 0:
                    genero_counts = df_filtrado['Genero'].value_counts()
                    fig_genero = px.bar(
                        x=['Masculino' if x == 'M' else 'Feminino' for x in genero_counts.index],
                        y=genero_counts.values,
                        title="Distribuição por Gênero",
                        color=genero_counts.values,
                        color_continuous_scale=['#06b6d4', '#8b5cf6']
                    )
                    theme = create_plotly_theme()
                    fig_genero.update_layout(**theme['layout'])
                    fig_genero.update_layout(height=350, showlegend=False)
                    fig_genero.update_coloraxes(showscale=False)
                    st.plotly_chart(fig_genero, use_container_width=True, config={'displayModeBar': False})
            except Exception as e:
                st.error(f"Erro: {str(e)}")
        
        with col2:
            st.markdown("#### **Padrão Semanal**")
            try:
                if len(df_filtrado) > 0:
                    dias_map = {
                        'Monday': 'Segunda', 'Tuesday': 'Terça', 'Wednesday': 'Quarta',
                        'Thursday': 'Quinta', 'Friday': 'Sexta', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
                    }
                    dia_counts = df_filtrado['Data_Ausencia'].dt.day_name().value_counts()
                    dia_data = []
                    for dia_en, count in dia_counts.items():
                        dia_data.append({'Dia': dias_map.get(dia_en, dia_en), 'Ausencias': count})
                    
                    if dia_data:
                        dia_df = pd.DataFrame(dia_data)
                        fig_semana = px.bar(
                            dia_df,
                            x='Dia',
                            y='Ausencias',
                            title="Ausências por Dia da Semana",
                            color='Ausencias',
                            color_continuous_scale=['#10b981', '#f59e0b', '#ef4444']
                        )
                        theme = create_plotly_theme()
                        fig_semana.update_layout(**theme['layout'])
                        fig_semana.update_layout(height=350, showlegend=False)
                        fig_semana.update_coloraxes(showscale=False)
                        st.plotly_chart(fig_semana, use_container_width=True, config={'displayModeBar': False})
            except Exception as e:
                st.error(f"Erro: {str(e)}")
        
        # Tabela analítica
        st.markdown("#### **Análise Departamental Detalhada**")
        try:
            if len(df_filtrado) > 0:
                dept_analysis = df_filtrado.groupby('Departamento').agg({
                    'Nome_Completo': 'count',
                    'Status_Justificativa': lambda x: (x == 'Sim').sum(),
                    'Salario_Atual': 'mean',
                    'Criticidade_Ausencia': lambda x: (x == 'Alta').sum()
                }).reset_index()
                
                dept_analysis.columns = ['Departamento', 'Total_Ausencias', 'Justificadas', 'Salario_Medio', 'Criticas']
                dept_analysis['Taxa_Justificacao'] = round(
                    (dept_analysis['Justificadas'] / dept_analysis['Total_Ausencias'] * 100), 1
                )
                dept_analysis['Impacto_Financeiro'] = dept_analysis['Total_Ausencias'] * 280
                
                # Status
                def get_status(row):
                    if row['Taxa_Justificacao'] > 75 and row['Criticas'] < 3:
                        return '🟢 Controlado'
                    elif row['Taxa_Justificacao'] > 60:
                        return '🟡 Atenção'
                    else:
                        return '🔴 Crítico'
                
                dept_analysis['Status'] = dept_analysis.apply(get_status, axis=1)
                dept_analysis = dept_analysis.sort_values('Impacto_Financeiro', ascending=False)
                
                st.dataframe(
                    dept_analysis,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Departamento": st.column_config.TextColumn("🏢 Departamento", width="large"),
                        "Total_Ausencias": st.column_config.NumberColumn("📊 Ausências", width="small"),
                        "Taxa_Justificacao": st.column_config.NumberColumn("✅ Taxa (%)", format="%.1f", width="small"),
                        "Salario_Medio": st.column_config.NumberColumn("💼 Salário", format="R$ %.0f", width="medium"),
                        "Impacto_Financeiro": st.column_config.NumberColumn("💰 Impacto", format="R$ %.0f", width="medium"),
                        "Status": st.column_config.TextColumn("🎯 Status", width="small")
                    }
                )
        except Exception as e:
            st.error(f"Erro na tabela: {str(e)}")
    
    with tab3:
        st.markdown('<div class="ultra-section-title">EXECUTIVE SUITE & RELATÓRIOS</div>', unsafe_allow_html=True)
        
        # Downloads
        st.markdown("#### **Centro de Downloads Executivos**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📊 Excel Premium"):
                try:
                    csv_data = df_filtrado.to_csv(index=False)
                    st.download_button(
                        label="⬇️ Download Excel",
                        data=csv_data,
                        file_name=f"hr_analytics_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv"
                    )
                    st.success("✅ Excel gerado!")
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
        
        with col2:
            if st.button("📈 Relatório Executivo"):
                try:
                    relatorio = f"""
HR ANALYTICS INTELLIGENCE SUITE - RELATÓRIO EXECUTIVO
===================================================

PERÍODO: {data_inicio.strftime('%d/%m/%Y')} - {data_fim.strftime('%d/%m/%Y')}
GERADO EM: {datetime.now().strftime('%d/%m/%Y às %H:%M')}

MÉTRICAS PRINCIPAIS
------------------
• Total de Ausências: {metricas['total_ausencias']:,}
• Colaboradores Impactados: {metricas['funcionarios_impactados']:,}
• Taxa de Conformidade: {metricas['taxa_justificacao']}%
• Score Corporativo: {metricas['score_rh']}/100
• Impacto Financeiro: R$ {metricas['impacto_financeiro']:,.2f}
• Taxa de Absenteísmo: {metricas['taxa_absenteismo']}%

STATUS CORPORATIVO
-----------------
• Tendência: {metricas['tendencia_geral']}
• Criticidade: {metricas['indice_criticidade']}
• Pico Temporal: {metricas['pico_temporal']}

RECOMENDAÇÕES ESTRATÉGICAS
-------------------------
1. Implementação de canal digital para justificativas
2. Programa de wellness corporativo
3. Flexibilização de políticas de trabalho
4. Sistema de monitoramento preditivo
5. Benchmarking competitivo

PROJEÇÃO FINANCEIRA
------------------
• ROI Estimado: 280% em 12 meses
• Economia Potencial: R$ {metricas['impacto_financeiro'] * 0.30:,.0f}
• Payback: 4-6 meses

Relatório gerado pelo HR Analytics Intelligence Suite
                    """
                    
                    st.download_button(
                        label="⬇️ Download Relatório",
                        data=relatorio,
                        file_name=f"relatorio_hr_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain"
                    )
                    st.success("✅ Relatório gerado!")
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
        
        with col3:
            if st.button("🔮 Análise Preditiva"):
                st.info("🚧 Módulo em desenvolvimento")
        
        with col4:
            if st.button("📊 Dashboard PDF"):
                st.info("🎯 Funcionalidade Premium")
        
        # Resumo executivo
        st.markdown("#### **Resumo Executivo Final**")
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(145deg, rgba(139, 92, 246, 0.1), rgba(6, 182, 212, 0.1));
            backdrop-filter: blur(20px);
            border: 2px solid rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 3rem 2rem;
            margin: 2rem 0;
            color: white;
        ">
            <h2 style="text-align: center; margin-bottom: 2rem;">
                📈 DASHBOARD EXECUTIVO FINAL
            </h2>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
                
                <div style="background: rgba(139, 92, 246, 0.15); border-radius: 15px; padding: 2rem; border-left: 6px solid #8b5cf6;">
                    <h3 style="color: #8b5cf6;">📊 SITUAÇÃO ATUAL</h3>
                    <p><strong>Ausências:</strong> {metricas['total_ausencias']:,} registros</p>
                    <p><strong>Colaboradores:</strong> {metricas['funcionarios_impactados']:,} pessoas</p>
                    <p><strong>Conformidade:</strong> {metricas['taxa_justificacao']}%</p>
                    <p><strong>Impacto:</strong> R$ {metricas['impacto_financeiro']:,.0f}</p>
                    <p><strong>Score:</strong> {metricas['score_rh']}/100</p>
                </div>
                
                <div style="background: rgba(16, 185, 129, 0.15); border-radius: 15px; padding: 2rem; border-left: 6px solid #10b981;">
                    <h3 style="color: #10b981;">🎯 PONTOS FORTES</h3>
                    <p>✅ Sistema de monitoramento ativo</p>
                    <p>✅ Dados estruturados</p>
                    <p>✅ {'Score acima da média' if metricas['score_rh'] > 75 else 'Base sólida'}</p>
                    <p>✅ Dashboard com IA</p>
                    <p>✅ Visibilidade total</p>
                </div>
                
                <div style="background: rgba(245, 158, 11, 0.15); border-radius: 15px; padding: 2rem; border-left: 6px solid #f59e0b;">
                    <h3 style="color: #f59e0b;">⚠️ OPORTUNIDADES</h3>
                    <p>🔍 {'Otimizar conformidade' if metricas['taxa_justificacao'] < 85 else 'Manter excelência'}</p>
                    <p>🔍 Reduzir ausências críticas</p>
                    <p>🔍 Analytics preditivos</p>
                    <p>🔍 Benchmarking contínuo</p>
                    <p>🔍 ROI de 280% estimado</p>
                </div>
                
                <div style="background: rgba(239, 68, 68, 0.15); border-radius: 15px; padding: 2rem; border-left: 6px solid #ef4444;">
                    <h3 style="color: #ef4444;">🚀 PRÓXIMOS PASSOS</h3>
                    <p>1. Aprovação de budget</p>
                    <p>2. Task force multidisciplinar</p>
                    <p>3. Quick wins em 30 dias</p>
                    <p>4. IA preditiva</p>
                    <p>5. Review trimestral</p>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 3rem; padding: 2rem; background: rgba(255, 255, 255, 0.05); border-radius: 15px;">
                <h3 style="margin-bottom: 1rem;">💡 RECOMENDAÇÃO ESTRATÉGICA</h3>
                <p style="font-size: 1.1rem; line-height: 1.6;">
                    Implementar <strong>programa integrado de gestão de absenteísmo</strong> com foco em 
                    <span style="color: #8b5cf6;">prevenção inteligente</span>, 
                    <span style="color: #06b6d4;">comunicação digital</span> e 
                    <span style="color: #10b981;">suporte proativo</span>.
                </p>
                <div style="margin-top: 2rem; display: flex; justify-content: space-around; flex-wrap: wrap;">
                    <div style="text-align: center; margin: 1rem;">
                        <div style="font-size: 2rem; color: #10b981;">25-40%</div>
                        <div style="opacity: 0.8;">Redução de Custos</div>
                    </div>
                    <div style="text-align: center; margin: 1rem;">
                        <div style="font-size: 2rem; color: #06b6d4;">6 meses</div>
                        <div style="opacity: 0.8;">Payback Period</div>
                    </div>
                    <div style="text-align: center; margin: 1rem;">
                        <div style="font-size: 2rem; color: #8b5cf6;">280%</div>
                        <div style="opacity: 0.8;">ROI Projetado</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer premium
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(6, 182, 212, 0.1));
        backdrop-filter: blur(20px);
        border: 2px solid rgba(255, 255, 255, 0.1);
        border-radius: 25px;
        padding: 4rem 3rem;
        margin-top: 5rem;
        text-align: center;
        color: white;
        position: relative;
        overflow: hidden;
    ">
        <h2 style="
            font-family: 'Orbitron', monospace;
            font-size: 2.5rem;
            font-weight: 900;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #ffffff, #8b5cf6, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        ">
            HR ANALYTICS INTELLIGENCE SUITE
        </h2>
        <p style="font-size: 1.2rem; margin-bottom: 2rem; opacity: 0.9;">
            Plataforma Premium de Business Intelligence para RH
        </p>
        <div style="margin: 2rem 0;">
            <span style="background: rgba(139, 92, 246, 0.2); padding: 0.5rem 1rem; border-radius: 15px; margin: 0.25rem; display: inline-block;">
                Machine Learning
            </span>
            <span style="background: rgba(6, 182, 212, 0.2); padding: 0.5rem 1rem; border-radius: 15px; margin: 0.25rem; display: inline-block;">
                Predictive Analytics
            </span>
            <span style="background: rgba(16, 185, 129, 0.2); padding: 0.5rem 1rem; border-radius: 15px; margin: 0.25rem; display: inline-block;">
                Real-time Insights
            </span>
            <span style="background: rgba(245, 158, 11, 0.2); padding: 0.5rem 1rem; border-radius: 15px; margin: 0.25rem; display: inline-block;">
                Executive Dashboard
            </span>
        </div>
        <p style="margin-top: 2rem; font-size: 0.95rem; opacity: 0.7;">
            Powered by Streamlit • Python • Plotly • Machine Learning<br>
            Dashboard desenvolvido para portfólio profissional
        </p>
        <div style="margin-top: 2rem;">
            <p style="font-size: 0.9rem; opacity: 0.6;">
                © 2024 HR Analytics Intelligence Suite • Versão 2.0 Premium<br>
                Desenvolvido para showcasing de habilidades em Data Science
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()# -*- coding: utf-8 -*-
"""
HR Analytics Intelligence Suite
Dashboard Premium para Análise de Recursos Humanos
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import random
import time
from typing import Dict
import warnings

warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="HR Analytics Intelligence Suite",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Ultra Premium
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e293b, #6d28d9, #1e293b);
        background-size: 400% 400%;
        animation: gradientShift 20s ease infinite;
        font-family: 'Inter', sans-serif;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 0%; }
        25% { background-position: 100% 0%; }
        50% { background-position: 100% 100%; }
        75% { background-position: 0% 100%; }
        100% { background-position: 0% 0%; }
    }
    
    .mega-header {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.2), rgba(6, 182, 212, 0.2));
        backdrop-filter: blur(20px);
        border: 2px solid rgba(255, 255, 255, 0.18);
        border-radius: 25px;
        padding: 4rem 3rem;
        text-align: center;
        margin: 2rem 0;
        color: white;
        box-shadow: 0 25px 50px -12px rgba(139, 92, 246, 0.5);
        position: relative;
        overflow: hidden;
    }
    
    .mega-header h1 {
        font-family: 'Orbitron', monospace;
        font-size: 4rem;
        font-weight: 900;
        margin: 0;
        background: linear-gradient(135deg, #ffffff, #8b5cf6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 50px rgba(255, 255, 255, 0.3);
        letter-spacing: 2px;
    }
    
    .mega-header .subtitle {
        font-size: 1.5rem;
        font-weight: 300;
        margin: 1rem 0;
        opacity: 0.9;
        letter-spacing: 1px;
    }
    
    .tech-badge {
        display: inline-block;
        background: rgba(139, 92, 246, 0.2);
        border: 1px solid rgba(139, 92, 246, 0.5);
        border-radius: 20px;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
    }
    
    .tech-badge:hover {
        background: rgba(139, 92, 246, 0.4);
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 5px 15px rgba(139, 92, 246, 0.4);
    }
    
    .premium-metric-card {
        background: linear-gradient(145deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        backdrop-filter: blur(15px);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
        transition: all 0.4s ease;
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    .premium-metric-card:hover {
        transform: translateY(-15px) scale(1.02);
        box-shadow: 0 30px 60px rgba(139, 92, 246, 0.3);
        border-color: rgba(139, 92, 246, 0.5);
    }
    
    .premium-metric-value {
        font-family: 'Orbitron', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        margin: 1rem 0;
        background: linear-gradient(135deg, #ffffff, #8b5cf6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.2);
    }
    
    .premium-metric-label {
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 1rem;
    }
    
    .premium-metric-trend {
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.7);
        margin-top: 1rem;
        font-weight: 500;
    }
    
    .trend-positive { color: #10b981; }
    .trend-negative { color: #ef4444; }
    .trend-neutral { color: #f59e0b; }
    
    .ultra-insight-card {
        background: linear-gradient(145deg, rgba(139, 92, 246, 0.15), rgba(139, 92, 246, 0.05));
        backdrop-filter: blur(20px);
        border: 2px solid rgba(139, 92, 246, 0.3);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        color: white;
        border-left: 6px solid #8b5cf6;
        box-shadow: 0 15px 35px rgba(139, 92, 246, 0.2);
        transition: all 0.4s ease;
    }
    
    .ultra-insight-card:hover {
        transform: translateX(10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(139, 92, 246, 0.3);
    }
    
    .ultra-insight-card h4 {
        font-family: 'Orbitron', monospace;
        color: #ffffff;
        margin-bottom: 1rem;
        font-size: 1.2rem;
        font-weight: 700;
    }
    
    .success-insight {
        background: linear-gradient(145deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.05));
        border-color: rgba(16, 185, 129, 0.3);
        border-left-color: #10b981;
        box-shadow: 0 15px 35px rgba(16, 185, 129, 0.2);
    }
    
    .warning-insight {
        background: linear-gradient(145deg, rgba(245, 158, 11, 0.15), rgba(245, 158, 11, 0.05));
        border-color: rgba(245, 158, 11, 0.3);
        border-left-color: #f59e0b;
        box-shadow: 0 15px 35px rgba(245, 158, 11, 0.2);
    }
    
    .critical-insight {
        background: linear-gradient(145deg, rgba(239, 68, 68, 0.15), rgba(239, 68, 68, 0.05));
        border-color: rgba(239, 68, 68, 0.3);
        border-left-color: #ef4444;
        box-shadow: 0 15px 35px rgba(239, 68, 68, 0.2);
    }
    
    .ultra-section-title {
        color: white;
        font-family: 'Orbitron', monospace;
        font-size: 2.5rem;
        font-weight: 900;
        text-align: center;
        margin: 4rem 0 2rem 0;
        background: linear-gradient(135deg, #ffffff, #8b5cf6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 50px rgba(255, 255, 255, 0.3);
        letter-spacing: 3px;
        text-transform: uppercase;
        position: relative;
    }
    
    .ultra-section-title::after {
        content: '';
        position: absolute;
        bottom: -15px;
        left: 50%;
        transform: translateX(-50%);
        width: 200px;
        height: 4px;
        background: linear-gradient(90deg, transparent, #8b5cf6, #06b6d4, #10b981, transparent);
        border-radius: 2px;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6, #06b6d4) !important;
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 10px 25px rgba(139, 92, 246, 0.3) !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 0 20px 40px rgba(139, 92, 246, 0.4) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
        background: linear-gradient(135deg, #7c3aed, #0891b2) !important;
    }
    
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        color: white !important;
        transition: all 0.3s ease !important;
    }
    
    .stSelectbox > div > div:hover,
    .stMultiSelect > div > div:hover {
        border-color: rgba(139, 92, 246, 0.5) !important;
        box-shadow: 0 0 15px rgba(139, 92, 246, 0.2) !important;
    }
    
    .stDataFrame {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 15px !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2) !important;
    }
    
    .premium-loading {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        height: 300px;
        color: white;
    }
    
    .premium-spinner {
        width: 80px;
        height: 80px;
        border: 4px solid rgba(139, 92, 246, 0.3);
        border-top: 4px solid #8b5cf6;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-bottom: 2rem;
        box-shadow: 0 0 30px rgba(139, 92, 246, 0.5);
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-text {
        font-family: 'Orbitron', monospace;
        font-size: 1.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #8b5cf6, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .status-indicator {
        display: inline-block;
        width: 15px;
        height: 15px;
        border-radius: 50%;
        margin-right: 10px;
        background: #10b981;
        animation: pulse 2s infinite;
        box-shadow: 0 0 10px #10b981;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.1); opacity: 0.7; }
        100% { transform: scale(1); opacity: 1; }
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 30px !important;
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 15px !important;
        padding: 10px !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 10px !important;
        color: rgba(255, 255, 255, 0.8) !important;
        font-weight: 700 !important;
        padding: 15px 30px !important;
        transition: all 0.4s ease !important;
        border: 2px solid transparent !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-family: 'Orbitron', monospace !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8b5cf6, #06b6d4) !important;
        color: white !important;
        box-shadow: 0 10px 25px rgba(139, 92, 246, 0.4) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        transform: translateY(-2px) !important;
    }
    
    @media (max-width: 768px) {
        .mega-header h1 { font-size: 2.5rem; }
        .premium-metric-value { font-size: 2rem; }
        .ultra-section-title { font-size: 1.8rem; }
        .premium-metric-card { padding: 1.5rem 1rem; }
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    header {visibility: hidden;}
    
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #8b5cf6, #06b6d4);
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(139, 92, 246, 0.5);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300, show_spinner=False)
def generate_premium_dataset() -> pd.DataFrame:
    """Gera dataset ultra-realista para demonstração premium"""
    random.seed(42)
    np.random.seed(42)
    
    # Dados corporativos realistas
    departamentos = [
        'Tecnologia da Informacao', 'Recursos Humanos', 'Operacoes Industriais',
        'Financeiro e Controladoria', 'Marketing Digital', 'Vendas Corporativas', 
        'Logistica Integrada', 'Qualidade e Processos', 'Juridico Empresarial'
    ]
    
    estados_brasileiros = [
        'SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'PE', 'GO', 'DF'
    ]
    
    motivos_ausencia = [
        'Consulta Medica', 'Doenca Familiar', 'Compromissos Pessoais',
        'Atestado Medico', 'Emergencia Familiar', 'Problemas de Transporte',
        'Questoes de Saude Mental', 'Acompanhamento Medico', 'Licenca Maternidade',
        'Acidente de Trabalho', 'Sem Justificativa', 'Home Office'
    ]
    
    cargos_hierarquia = [
        'Estagiario', 'Assistente', 'Analista Jr', 'Analista Pleno', 
        'Analista Senior', 'Especialista', 'Coordenador', 'Supervisor',
        'Gerente', 'Gerente Senior', 'Diretor', 'Vice-Presidente'
    ]
    
    nomes_brasileiros = [
        'Ana Silva', 'Joao Santos', 'Maria Oliveira', 'Pedro Costa', 'Carla Souza',
        'Bruno Almeida', 'Fernanda Lima', 'Rafael Pereira', 'Juliana Rodrigues',
        'Thiago Ferreira', 'Camila Martins', 'Lucas Barbosa', 'Patricia Gomes'
    ]
    
    dados_corporativos = []
    base_date = datetime(2024, 1, 1)
    
    # Gerar 400 registros ultra-realistas
    for i in range(400):
        # Distribuição inteligente por departamento
        departamento = random.choice(departamentos)
        motivo = random.choice(motivos_ausencia)
        
        # Sistema inteligente de justificação
        if motivo in ['Consulta Medica', 'Atestado Medico']:
            justificada = 'Sim' if random.random() > 0.1 else 'Nao'
        elif motivo == 'Emergencia Familiar':
            justificada = 'Sim' if random.random() > 0.2 else 'Nao'
        elif motivo == 'Sem Justificativa':
            justificada = 'Nao'
        else:
            justificada = 'Sim' if random.random() > 0.4 else 'Nao'
        
        # Distribuição temporal realista
        mes = random.randint(1, 12)
        dia = random.randint(1, 28)
        data_falta = datetime(2024, mes, dia)
        
        # Hierarquia salarial realista
        cargo = random.choice(cargos_hierarquia)
        salario_ranges = {
            'Estagiario': (1500, 2500), 'Assistente': (2800, 4000),
            'Analista Jr': (4000, 6500), 'Analista Pleno': (6500, 9500),
            'Analista Senior': (9000, 14000), 'Especialista': (12000, 18000),
            'Coordenador': (15000, 22000), 'Supervisor': (18000, 26000),
            'Gerente': (22000, 35000), 'Gerente Senior': (30000, 50000),
            'Diretor': (40000, 70000), 'Vice-Presidente': (60000, 120000)
        }
        
        salario_min, salario_max = salario_ranges.get(cargo, (4000, 10000))
        salario = random.randint(salario_min, salario_max)
        
        genero = random.choice(['M', 'F'])
        nome = f"{random.choice(nomes_brasileiros)} {i+1:03d}"
        
        # Anos de empresa realista
        anos_empresa = random.choices(
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15], 
            weights=[15, 20, 15, 12, 10, 8, 7, 5, 4, 2, 1, 1]
        )[0]
        
        data_admissao = base_date - timedelta(days=anos_empresa * 365 + random.randint(0, 365))
        
        # Criticidade baseada no motivo
        if motivo in ['Sem Justificativa', 'Problemas de Transporte']:
            criticidade = 'Alta'
        elif motivo in ['Compromissos Pessoais']:
            criticidade = 'Media'
        else:
            criticidade = 'Baixa'
        
        dados_corporativos.append({
            'ID_Funcionario': f"EMP{i+1:04d}",
            'Nome_Completo': nome,
            'Cargo_Atual': cargo,
            'Departamento': departamento,
            'Estado_UF': random.choice(estados_brasileiros),
            'Data_Ausencia': data_falta,
            'Motivo_Ausencia': motivo,
            'Status_Justificativa': justificada,
            'Genero': genero,
            'Data_Admissao': data_admissao,
            'Salario_Atual': salario,
            'Nivel_Hierarquico': cargos_hierarquia.index(cargo),
            'Criticidade_Ausencia': criticidade
        })
    
    df = pd.DataFrame(dados_corporativos)
    
    # Processamento avançado de dados
    df['Mes_Referencia'] = df['Data_Ausencia'].dt.strftime('%Y-%m')
    df['Mes_Nome_BR'] = df['Data_Ausencia'].dt.strftime('%b/%Y')
    df['Dia_Semana_BR'] = df['Data_Ausencia'].dt.day_name().map({
        'Monday': 'Segunda-feira', 'Tuesday': 'Terca-feira', 'Wednesday': 'Quarta-feira',
        'Thursday': 'Quinta-feira', 'Friday': 'Sexta-feira', 'Saturday': 'Sabado', 'Sunday': 'Domingo'
    })
    df['Trimestre'] = df['Data_Ausencia'].dt.quarter
    df['Anos_Empresa'] = ((datetime.now() - df['Data_Admissao']).dt.days / 365).astype(int).clip(0, 50)
    df['Faixa_Salarial'] = pd.cut(df['Salario_Atual'], 
                                  bins=[0, 5000, 10000, 20000, 50000, 150000],
                                  labels=['Ate 5k', '5k-10k', '10k-20k', '20k-50k', '50k+'])
    
    return df

@st.cache_data(ttl=300)
def calculate_premium_metrics(df: pd.DataFrame) -> Dict:
    """Calcula métricas avançadas com KPIs corporativos"""
    if len(df) == 0:
        return {
            'total_ausencias': 0, 'funcionarios_impactados': 0, 'taxa_justificacao': 0,
            'departamentos_criticos': 0, 'impacto_financeiro': 0, 'salario_medio': 0,
            'ausencias_por_funcionario': 0, 'taxa_absenteismo': 0, 'pico_temporal': 'N/A',
            'tendencia_geral': 'Estavel', 'indice_criticidade': 'Baixo', 'score_rh': 85,
            'ausencias_criticas': 0
        }
    
    total_ausencias = len(df)
    funcionarios_impactados = df['Nome_Completo'].nunique()
    ausencias_justificadas = len(df[df['Status_Justificativa'] == 'Sim'])
    taxa_justificacao = round((ausencias_justificadas / total_ausencias * 100), 2)
    departamentos_criticos = df['Departamento'].nunique()
    
    # Métricas financeiras avançadas
    custo_medio_ausencia = 280
    impacto_financeiro = total_ausencias * custo_medio_ausencia
    salario_medio = df['Salario_Atual'].mean()
    
    # KPIs de RH avançados
    ausencias_por_funcionario = round(total_ausencias / funcionarios_impactados, 2)
    taxa_absenteismo = round((total_ausencias / (funcionarios_impactados * 22)) * 100, 2)
    
    # Análise temporal
    pico_temporal = df['Mes_Nome_BR'].value_counts().index[0] if len(df) > 0 else 'N/A'
    
    # Índice de criticidade
    ausencias_criticas = len(df[df['Criticidade_Ausencia'] == 'Alta'])
    indice_criticidade = 'Alto' if ausencias_criticas > total_ausencias * 0.3 else \
                        'Medio' if ausencias_criticas > total_ausencias * 0.15 else 'Baixo'
    
    # Score de RH (0-100)
    score_base = 100
    score_base -= max(0, (taxa_absenteismo - 3) * 5)
    score_base -= max(0, (100 - taxa_justificacao) * 0.3)
    score_base -= ausencias_criticas * 0.5
    score_rh = max(0, min(100, round(score_base)))
    
    # Tendência
    tendencia_geral = 'Estavel'
    if total_ausencias > 150:
        tendencia_geral = 'Crescente Preocupante'
    elif total_ausencias > 100:
        tendencia_geral = 'Crescente Leve'
    elif total_ausencias < 50:
        tendencia_geral = 'Decrescente Positiva'
    
    return {
        'total_ausencias': total_ausencias,
        'funcionarios_impactados': funcionarios_impactados,
        'taxa_justificacao': taxa_justificacao,
        'departamentos_criticos': departamentos_criticos,
        'impacto_financeiro': impacto_financeiro,
        'salario_medio': salario_medio,
        'ausencias_por_funcionario': ausencias_por_funcionario,
        'taxa_absenteismo': taxa_absenteismo,
        'pico_temporal': pico_temporal,
        'tendencia_geral': tendencia_geral,
        'indice_criticidade': indice_criticidade,
        'score_rh': score_rh,
        'ausencias_criticas': ausencias_criticas
    }

def create_plotly_theme() -> Dict:
    """Tema para gráficos Plotly"""
    return {
        'layout': {
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'font': {'color': 'white', 'family': 'Inter, sans-serif', 'size': 12},
            'title': {'font': {'size': 18, 'color': 'white'}, 'x': 0.5},
            'xaxis': {
                'gridcolor': 'rgba(139, 92, 246, 0.2)',
                'linecolor': 'rgba(255, 255, 255, 0.3)',
                'tickcolor': 'rgba(255, 255, 255, 0.3)',
                'tickfont': {'color': 'white', 'size': 11}
            },
            'yaxis': {
                'gridcolor': 'rgba(139, 92, 246, 0.2)',
                'linecolor': 'rgba(255, 255, 255, 0.3)',
                'tickcolor': 'rgba(255, 255, 255, 0.3)',
                'tickfont': {'color': 'white', 'size': 11}
            },
            'legend': {'font': {'color': 'white', 'size': 11}},
            'colorway': ['#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444'],
            'margin': dict(l=40, r=40, t=60, b=40)
        }
    }

def display_loading():
    """Loading premium"""
    loading_placeholder = st.empty()
    with loading_placeholder.container():
        st.markdown("""
        <div class="premium-loading
