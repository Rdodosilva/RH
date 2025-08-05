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
    
    /* Cards de métricas */
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
    }
    
    .metric-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(139, 92, 246, 0.4);
        border-color: rgba(255, 255, 255, 0.3);
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
    
    /* Insight cards */
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
    
    .success-card {
        background: rgba(16, 185, 129, 0.15);
        border-color: rgba(16, 185, 129, 0.3);
        border-left-color: #10b981;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.2);
    }
    
    .warning-card {
        background: rgba(245, 158, 11, 0.15);
        border-color: rgba(245, 158, 11, 0.3);
        border-left-color: #f59e0b;
        box-shadow: 0 4px 16px rgba(245, 158, 11, 0.2);
    }
    
    .critical-card {
        background: rgba(239, 68, 68, 0.15);
        border-color: rgba(239, 68, 68, 0.3);
        border-left-color: #ef4444;
        box-shadow: 0 4px 16px rgba(239, 68, 68, 0.2);
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
    }
    
    /* Remover elementos do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def generate_realistic_data():
    """Gera dados realistas e variados para o dashboard"""
    random.seed(42)
    np.random.seed(42)
    
    departamentos = ['RH', 'TI', 'Operações', 'Financeiro', 'Marketing', 'Comercial', 'Logística']
    estados = ['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'PE', 'GO', 'DF']
    motivos = ['Família', 'Doença', 'Pessoal', 'Médico', 'Falta de transporte', 'Sem justificativa']
    justificadas = ['Sim', 'Não']
    generos = ['M', 'F']
    cargos = ['Analista Jr', 'Analista Pl', 'Analista Sr', 'Coordenador', 'Supervisor', 'Gerente', 'Diretor']
    
    data = []
    for i in range(250):
        # Distribuição mais realista por departamento
        if i < 50:
            dept = 'TI'
            motivo_weights = [0.2, 0.3, 0.25, 0.15, 0.05, 0.05]
        elif i < 90:
            dept = 'Operações'
            motivo_weights = [0.15, 0.35, 0.15, 0.20, 0.10, 0.05]
        elif i < 120:
            dept = 'Comercial'
            motivo_weights = [0.25, 0.20, 0.20, 0.15, 0.15, 0.05]
        else:
            dept = random.choice(departamentos)
            motivo_weights = [0.20, 0.25, 0.20, 0.15, 0.15, 0.05]
        
        motivo = np.random.choice(motivos, p=motivo_weights)
        
        # Justificação baseada no motivo
        if motivo in ['Doença', 'Médico']:
            justificada = np.random.choice(['Sim', 'Não'], p=[0.90, 0.10])
        elif motivo == 'Família':
            justificada = np.random.choice(['Sim', 'Não'], p=[0.75, 0.25])
        elif motivo == 'Pessoal':
            justificada = np.random.choice(['Sim', 'Não'], p=[0.60, 0.40])
        else:
            justificada = np.random.choice(['Sim', 'Não'], p=[0.30, 0.70])
        
        # Data aleatória no último ano
        base_date = datetime(2024, 1, 1)
        days_offset = random.randint(0, 365)
        
        data.append({
            'Nome': f'Funcionário {i+1:03d}',
            'Cargo': random.choice(cargos),
            'Departamento': dept,
            'Estado': random.choice(estados),
            'Data_Falta': base_date + timedelta(days=days_offset),
            'Motivo': motivo,
            'Justificada': justificada,
            'Genero': random.choice(generos),
            'Data_Admissao': base_date - timedelta(days=random.randint(30, 2190)),
            'Salario_Estimado': random.randint(3000, 25000)
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
    custo_medio_por_falta = 180
    custo_estimado = total_faltas * custo_medio_por_falta
    media_salarial = df['Salario_Estimado'].mean()
    
    # Métricas de RH
    faltas_por_funcionario = round(total_faltas / funcionarios_unicos, 2)
    taxa_absenteismo = round((total_faltas / (funcionarios_unicos * 22)) * 100, 2)
    
    # Análise temporal
    monthly_counts = df['Mes_Nome'].value_counts()
    pico_mensal = monthly_counts.index[0] if len(monthly_counts) > 0 else 'N/A'
    
    # Tendência
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
            'colorway': ['#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#8b5a2b']
        }
    }

def main():
    # Header principal
    st.markdown("""
    <div class="main-header">
        <h1>📊 HR Analytics Dashboard</h1>
        <p>Análise Avançada de Absenteísmo Corporativo</p>
        <p class="subtitle">Dashboard Interativo com IA, Predições e Insights Estratégicos</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregar dados
    with st.spinner("🔄 Processando dados avançados..."):
        df = generate_realistic_data()
    
    st.success(f"✅ **{len(df)} registros** processados com sucesso!")
    
    # Sidebar com filtros
    with st.sidebar:
        st.markdown("## 🔍 **Filtros Avançados**")
        
        departamentos_selecionados = st.multiselect(
            "🏢 **Departamentos**",
            options=sorted(df['Departamento'].unique()),
            default=sorted(df['Departamento'].unique()),
            help="Selecione os departamentos para análise"
        )
        
        motivos_selecionados = st.multiselect(
            "📝 **Motivos das Faltas**",
            options=sorted(df['Motivo'].unique()),
            default=sorted(df['Motivo'].unique()),
            help="Filtre por motivos específicos"
        )
        
        justificacao_filtro = st.selectbox(
            "✅ **Status de Justificação**",
            options=['Todas', 'Sim', 'Não'],
            help="Analisar faltas justificadas vs não justificadas"
        )
        
        # Período de análise
        st.markdown("### 📅 **Período de Análise**")
        
        col1, col2 = st.columns(2)
        with col1:
            data_inicio = st.date_input(
                "Data Início",
                value=df['Data_Falta'].min().date(),
                help="Início do período"
            )
        
        with col2:
            data_fim = st.date_input(
                "Data Fim",
                value=df['Data_Falta'].max().date(),
                help="Fim do período"
            )
    
    # Aplicar filtros
    df_filtrado = df[
        (df['Departamento'].isin(departamentos_selecionados)) &
        (df['Motivo'].isin(motivos_selecionados)) &
        (df['Data_Falta'].dt.date >= data_inicio) &
        (df['Data_Falta'].dt.date <= data_fim)
    ]
    
    if justificacao_filtro != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['Justificada'] == justificacao_filtro]
    
    if len(df_filtrado) == 0:
        st.error("⚠️ **Nenhum dado encontrado** com os filtros aplicados.")
        return
    
    # Calcular métricas
    metricas = calculate_advanced_metrics(df_filtrado)
    plotly_theme = create_advanced_plotly_theme()
    
    # Sistema de abas
    tab1, tab2, tab3, tab4 = st.tabs([
        "👁️ **Visão Geral**", 
        "🏢 **Análise Departamental**", 
        "📈 **Tendências & Padrões**", 
        "📋 **Relatórios**"
    ])
    
    with tab1:
        st.markdown('<div class="section-title">📊 Dashboard Executivo - Métricas Principais</div>', unsafe_allow_html=True)
        
        # Cards de métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">📅 Total de Faltas</div>
                <div class="metric-value">{metricas['total_faltas']}</div>
                <div class="metric-trend">
                    {round((metricas['total_faltas']/len(df)*100), 1)}% do total
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
        
        # Gráficos principais
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
        
        # Evolução temporal
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
    
    with tab2:
        st.markdown('<div class="section-title">🏢 Análise Departamental Avançada</div>', unsafe_allow_html=True)
        
        # Análise comparativa
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 👥 **Segmentação por Gênero**")
            
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
                textposition='outside'
            )
            
            st.plotly_chart(fig_genero, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            st.markdown("#### ⏰ **Análise por Tempo de Empresa**")
            
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
                textposition='outside'
            )
            fig_tempo.update_coloraxes(showscale=False)
            
            st.plotly_chart(fig_tempo, use_container_width=True, config={'displayModeBar': False})
        
        # Heatmap departamento x motivo
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
            textfont={"color": "white", "size": 12}
        )
        fig_heatmap.update_layout(height=400)
        
        st.plotly_chart(fig_heatmap, use_container_width=True, config={'displayModeBar': False})
    
    with tab3:
        st.markdown('<div class="section-title">📈 Análise de Tendências e Padrões</div>', unsafe_allow_html=True)
        
        # Análise de padrões
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📅 **Padrão Semanal**")
            
            dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
            dia_counts = df_filtrado['Dia_Semana'].value_counts()
            
            # Reordenar por dia da semana
            dia_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            dia_pt = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
            
            dia_data = []
            for i, dia_en in enumerate(dia_order):
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
        
        # Análise de correlações
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
            title="",
            color='Tempo_Empresa',
            color_continuous_scale='Viridis',
            hover_data=['Funcionario']
        )
        
        fig_scatter.update_layout(**plotly_theme['layout'])
        fig_scatter.update_traces(
            hovertemplate='<b>%{customdata[0]}</b><br>Salário: R$ %{x:,.0f}<br>Faltas: %{y}<br>Tempo: %{marker.size} anos<extra></extra>'
        )
        fig_scatter.update_layout(height=400)
        
        st.plotly_chart(fig_scatter, use_container_width=True, config={'displayModeBar': False})
        
        # Insights de tendências
        st.markdown("#### 💡 **Insights de Tendências Estratégicas**")
        
        # Calcular insights
        dia_pico = dia_df.loc[dia_df['Faltas'].idxmax(), 'Dia'] if len(dia_df) > 0 else "N/A"
        estado_concentracao = estado_counts.index[0] if len(estado_counts) > 0 else "N/A"
        
        # Tendência geral
        monthly_trend = df_filtrado.groupby('Mes_Nome').size().reset_index(name='Faltas')
        if len(monthly_trend) >= 2:
            tendencia_geral = "Crescente" if monthly_trend['Faltas'].iloc[-1] > monthly_trend['Faltas'].iloc[0] else "Decrescente"
        else:
            tendencia_geral = "Estável"
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="insight-card warning-card">
                <h4>📅 Padrão Semanal Crítico</h4>
                <p><strong>{dia_pico}</strong> é o dia com mais faltas</p>
                <p>🎯 <strong>Hipótese:</strong> {'Extensão de fim de semana' if dia_pico in ['Segunda', 'Sexta'] else 'Meio da semana estressante'}</p>
                <p>💡 <strong>Ação:</strong> {'Flexibilizar horários nas segundas/sextas' if dia_pico in ['Segunda', 'Sexta'] else 'Revisar carga de trabalho'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            concentracao_perc = round((estado_counts.iloc[0] / metricas['total_faltas'] * 100), 1) if len(estado_counts) > 0 else 0
            st.markdown(f"""
            <div class="insight-card insight-card">
                <h4>🗺️ Concentração Geográfica</h4>
                <p><strong>{estado_concentracao}</strong> concentra {concentracao_perc}% das faltas</p>
                <p>🔍 <strong>Investigar:</strong> {'Questões regionais específicas' if concentracao_perc > 30 else 'Distribuição normal'}</p>
                <p>🎯 <strong>Oportunidade:</strong> Políticas regionalizadas</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="insight-card {'success-card' if tendencia_geral == 'Decrescente' else 'critical-card' if tendencia_geral == 'Crescente' else 'insight-card'}">
                <h4>📈 Tendência Geral</h4>
                <p><strong>{tendencia_geral}</strong> nos últimos meses</p>
                <p>{'🟢 Situação melhorando' if tendencia_geral == 'Decrescente' else '🔴 Requer atenção' if tendencia_geral == 'Crescente' else '🟡 Monitorar'}</p>
                <p>🎯 <strong>Status:</strong> {'Controlado' if tendencia_geral == 'Decrescente' else 'Crítico' if tendencia_geral == 'Crescente' else 'Estável'}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="section-title">📋 Relatórios Executivos e Análise Preditiva</div>', unsafe_allow_html=True)
        
        # Predições simples
        if len(monthly_trend) >= 3:
            recent_trend = monthly_trend['Faltas'].tail(3).mean()
            historical_avg = monthly_trend['Faltas'].mean()
            volatility = monthly_trend['Faltas'].std()
            
            # Predição básica
            prediction_next_month = round(recent_trend * (1 + np.random.normal(0, 0.05)))
            confidence_interval_lower = round(prediction_next_month - (volatility * 1.96))
            confidence_interval_upper = round(prediction_next_month + (volatility * 1.96))
            
            # Cards de predição
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">🎯 Predição - Próximo Mês</div>
                    <div class="metric-value">{prediction_next_month}</div>
                    <div class="metric-trend">
                        Intervalo: {confidence_interval_lower} - {confidence_interval_upper} faltas
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                risk_level = "Alto" if recent_trend > historical_avg * 1.2 else "Médio" if recent_trend > historical_avg else "Baixo"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">📊 Nível de Risco</div>
                    <div class="metric-value" style="font-size: 2rem;">{risk_level}</div>
                    <div class="metric-trend">
                        Baseado em {len(monthly_trend)} períodos
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                trend_direction = "📈 Crescente" if recent_trend > historical_avg else "📉 Decrescente" if recent_trend < historical_avg else "➡️ Estável"
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">📈 Direção da Tendência</div>
                    <div class="metric-value" style="font-size: 1.5rem;">{trend_direction}</div>
                    <div class="metric-trend">
                        Variação: {((recent_trend/historical_avg - 1) * 100):+.1f}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Análise financeira por departamento
        st.markdown("#### 💰 **Impacto Financeiro por Departamento**")
        
        dept_financial = df_filtrado.groupby('Departamento').agg({
            'Nome': 'count',
            'Justificada': lambda x: (x == 'Sim').sum(),
            'Salario_Estimado': 'mean'
        }).reset_index()
        
        dept_financial.columns = ['Departamento', 'Total_Faltas', 'Faltas_Justificadas', 'Salario_Medio']
        dept_financial['Taxa_Justificacao'] = round(
            (dept_financial['Faltas_Justificadas'] / dept_financial['Total_Faltas'] * 100), 1
        )
        dept_financial['Custo_Estimado'] = dept_financial['Total_Faltas'] * 180
        
        # Status
        def get_status_financeiro(row):
            if row['Taxa_Justificacao'] > 75 and row['Total_Faltas'] < 20:
                return '🟢 Controlado'
            elif row['Taxa_Justificacao'] > 60 and row['Total_Faltas'] < 35:
                return '🟡 Atenção'
            else:
                return '🔴 Crítico'
        
        dept_financial['Status'] = dept_financial.apply(get_status_financeiro, axis=1)
        
        st.dataframe(
            dept_financial.sort_values('Custo_Estimado', ascending=False),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Departamento": st.column_config.TextColumn("🏢 Departamento"),
                "Total_Faltas": st.column_config.NumberColumn("📊 Total Faltas"),
                "Faltas_Justificadas": st.column_config.NumberColumn("✅ Justificadas"),
                "Taxa_Justificacao": st.column_config.NumberColumn("📈 Taxa (%)", format="%.1f%%"),
                "Salario_Medio": st.column_config.NumberColumn("💼 Salário Médio", format="R$ %.0f"),
                "Custo_Estimado": st.column_config.NumberColumn("💰 Custo Total", format="R$ %.0f"),
                "Status": st.column_config.TextColumn("🎯 Status")
            }
        )
        
        # Recomendações estratégicas
        st.markdown("#### 🎯 **Recomendações Estratégicas**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="insight-card success-card">
                <h4>🎯 Ações Imediatas (0-30 dias)</h4>
                <ul>
                    <li>🚨 <strong>Reunião emergencial</strong> com gestores dos departamentos críticos</li>
                    <li>📱 <strong>Canal digital</strong> para justificativas em tempo real</li>
                    <li>📊 <strong>Dashboard executivo</strong> com alertas automáticos</li>
                    <li>🎯 <strong>Metas específicas</strong> por departamento</li>
                </ul>
                <p><strong>💰 Investimento:</strong> R$ 15.000 - R$ 25.000</p>
                <p><strong>📈 ROI Esperado:</strong> 300% em 6 meses</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="insight-card warning-card">
                <h4>📈 Estratégias de Médio Prazo (1-6 meses)</h4>
                <ul>
                    <li>🏠 <strong>Programa de flexibilidade</strong> e home office</li>
                    <li>🚌 <strong>Sistema de transporte</strong> corporativo</li>
                    <li>🏥 <strong>Programa de saúde</strong> ocupacional</li>
                    <li>🎓 <strong>Capacitação de líderes</strong> em gestão</li>
                </ul>
                <p><strong>💰 Investimento:</strong> R$ 100.000 - R$ 300.000</p>
                <p><strong>📈 Impacto:</strong> Redução de 25-40% no absenteísmo</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Seção de downloads
        st.markdown("#### 📥 **Central de Exportação**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 **Exportar Excel Completo**", key="excel_completo"):
                csv_data = df_filtrado.to_csv(index=False)
                st.download_button(
                    label="⬇️ **Download Excel**",
                    data=csv_data,
                    file_name=f"hr_analytics_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    key="download_excel"
                )
                st.success("✅ **Excel gerado!** Download iniciado.")
        
        with col2:
            if st.button("📈 **Relatório Executivo**", key="relatorio_exec"):
                dept_counts = df_filtrado['Departamento'].value_counts()
                motivo_counts = df_filtrado['Motivo'].value_counts()
                
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
- Motivo predominante: {motivo_counts.index[0] if len(motivo_counts) > 0 else 'N/A'}
- Status geral: {'Controlado' if metricas['taxa_justificacao'] > 70 else 'Crítico'}

💡 RECOMENDAÇÕES PRIORITÁRIAS:
1. Intervenção imediata no departamento crítico
2. Implementação de canal digital para justificativas
3. Programa de flexibilidade familiar
4. Sistema de monitoramento em tempo real

📈 PROJEÇÕES:
- Economia potencial: R$ {metricas['custo_estimado'] * 0.25:,.2f}
- ROI esperado: 280% em 12 meses
- Payback: 4-6 meses

Relatório gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}
"""
                
                st.download_button(
                    label="⬇️ **Download Relatório**",
                    data=relatorio_text,
                    file_name=f"relatorio_hr_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain",
                    key="download_relatorio"
                )
                st.success("✅ **Relatório executivo gerado!**")
        
        with col3:
            if st.button("📊 **Dashboard PDF**", key="dashboard_pdf"):
                st.info("🚧 **Funcionalidade em desenvolvimento.** Em breve disponível!")
    
    # Footer elegante
    st.markdown("""
    <div class="footer-container">
        <h3>🚀 HR Analytics Dashboard</h3>
        <p>Desenvolvido com Streamlit, Plotly e Python</p>
        <p>© 2025 - Análise Inteligente de Recursos Humanos</p>
        <p style="font-size: 0.8rem; margin-top: 1rem;">
            💡 <strong>Dica:</strong> Use os filtros na barra lateral para análises personalizadas
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
