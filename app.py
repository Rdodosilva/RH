import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import date, datetime
import warnings

warnings.filterwarnings('ignore')

# --- Funções Auxiliares (mantidas e aprimoradas)
def generate_data():
    """Gera um DataFrame fictício para demonstração."""
    np.random.seed(42)
    num_entries = 1500
    
    data = {
        'ID_Funcionario': range(1, num_entries + 1),
        'Nome': [f'Funcionario_{i}' for i in range(1, num_entries + 1)],
        'Departamento': np.random.choice(['Vendas', 'Marketing', 'RH', 'TI', 'Financeiro', 'Produção', 'Logística'], num_entries),
        'Motivo': np.random.choice(['Doença', 'Família', 'Consulta Médica', 'Falta de transporte', 'Outros'], num_entries),
        'Justificada': np.random.choice(['Sim', 'Não'], num_entries),
        'Genero': np.random.choice(['M', 'F'], num_entries),
        'Data_Falta': pd.to_datetime(pd.date_range(start='2023-01-01', end='2024-07-30', periods=num_entries)),
        'Tempo_Empresa_Anos': np.random.randint(0, 15, num_entries),
        'Salario_Estimado': np.random.randint(3000, 15000, num_entries),
        'Estado': np.random.choice(['SP', 'RJ', 'MG', 'BA', 'RS', 'PR', 'PE'], num_entries),
        'Dia_Semana': pd.to_datetime(pd.date_range(start='2023-01-01', end='2024-07-30', periods=num_entries)).day_name(),
    }
    df = pd.DataFrame(data)
    df['Mes_Nome'] = df['Data_Falta'].dt.strftime('%b/%Y')
    return df

@st.cache_data
def load_data():
    """Carrega os dados e retorna o DataFrame."""
    df = generate_data()
    df['Data_Falta'] = pd.to_datetime(df['Data_Falta'])
    return df

def calculate_advanced_metrics(df_filtrado):
    """Calcula todas as métricas para os cards principais."""
    if df_filtrado.empty:
        return {
            'total_faltas': 0, 'funcionarios_unicos': 0, 'taxa_justificacao': 0,
            'custo_estimado': 0, 'taxa_absenteismo': 0, 'pico_mensal': 'N/A',
            'media_salarial': 0, 'tendencia': 'N/A', 'departamentos_afetados': 0,
            'faltas_por_funcionario': 0, 'custo_por_falta': 0
        }

    total_faltas = len(df_filtrado)
    funcionarios_unicos = df_filtrado['ID_Funcionario'].nunique()
    faltas_justificadas = df_filtrado[df_filtrado['Justificada'] == 'Sim'].shape[0]
    taxa_justificacao = round((faltas_justificadas / total_faltas) * 100, 1) if total_faltas > 0 else 0
    
    custo_por_falta = 200  # Custo médio de um dia de trabalho
    custo_estimado = total_faltas * custo_por_falta
    
    total_dias_trabalho = (df_filtrado['Data_Falta'].max() - df_filtrado['Data_Falta'].min()).days + 1
    if total_dias_trabalho == 0: total_dias_trabalho = 1
    
    taxa_absenteismo = round((total_faltas / (funcionarios_unicos * total_dias_trabalho)) * 100, 2)
    
    pico_mensal = df_filtrado['Mes_Nome'].value_counts().idxmax() if not df_filtrado['Mes_Nome'].empty else 'N/A'
    
    monthly_counts = df_filtrado.groupby('Mes_Nome').size()
    tendencia = "Subindo" if len(monthly_counts) >= 2 and monthly_counts.iloc[-1] > monthly_counts.iloc[0] else "Descendo"
    
    departamentos_afetados = df_filtrado['Departamento'].nunique()
    faltas_por_funcionario = round(total_faltas / funcionarios_unicos, 1) if funcionarios_unicos > 0 else 0
    
    return {
        'total_faltas': total_faltas,
        'funcionarios_unicos': funcionarios_unicos,
        'taxa_justificacao': taxa_justificacao,
        'custo_estimado': custo_estimado,
        'taxa_absenteismo': taxa_absenteismo,
        'pico_mensal': pico_mensal,
        'media_salarial': round(df_filtrado['Salario_Estimado'].mean(), 0),
        'tendencia': tendencia,
        'departamentos_afetados': departamentos_afetados,
        'faltas_por_funcionario': faltas_por_funcionario,
        'custo_por_falta': custo_por_falta
    }

def create_advanced_plotly_theme():
    """Define um tema de cores e layout para os gráficos do Plotly."""
    return {
        'layout': {
            'font_family': "Inter, sans-serif",
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'xaxis': {'showgrid': False, 'gridcolor': 'rgba(200,200,200,0.1)'},
            'yaxis': {'showgrid': True, 'gridcolor': 'rgba(200,200,200,0.1)'},
            'title_font_color': '#f8f9fa',
            'title_font_size': 18,
            'legend': {'bgcolor': 'rgba(255,255,255,0.1)', 'font_color': '#f8f9fa'},
            'hoverlabel': {'bgcolor': 'rgba(45, 52, 64, 0.8)', 'font_color': '#f8f9fa'}
        }
    }

# --- Estilos CSS personalizados para Glassmorphism e animações
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        color: #f8f9fa;
        background: radial-gradient(circle at 10% 20%, rgb(40, 48, 59) 0%, rgb(18, 25, 34) 100.2%);
        background-size: 400% 400%;
        animation: gradientAnimation 15s ease infinite;
    }
    
    @keyframes gradientAnimation {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* Estilos para a sidebar com glassmorphism */
    [data-testid="stSidebar"] {
        background: rgba(45, 52, 64, 0.2);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 1rem;
        margin: 1rem;
    }
    
    [data-testid="stSidebar"] h2, h3, h4 {
        color: #d1d8e0;
        font-weight: 600;
        text-shadow: 0 0 5px rgba(255, 255, 255, 0.1);
    }
    
    /* Estilos para cards com glassmorphism */
    .metric-card {
        background: rgba(45, 52, 64, 0.2);
        backdrop-filter: blur(8px);
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        text-align: center;
        transition: all 0.3s ease-in-out;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .metric-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
    }
    .metric-label {
        font-size: 1rem;
        color: #a0a0a0;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 2.8rem;
        font-weight: bold;
        color: #c993ff; /* Cor primária */
        text-shadow: 0 0 10px rgba(201, 147, 255, 0.4);
    }
    .metric-trend {
        font-size: 0.9rem;
        color: #a0a0a0;
        margin-top: 5px;
    }
    
    /* Estilos para títulos */
    .section-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #f8f9fa;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
        border-bottom: 3px solid #c993ff;
        padding-bottom: 15px;
        margin-top: 40px;
    }
    .subsection-title {
        font-size: 1.8rem;
        font-weight: 600;
        color: #c993ff;
        margin-top: 25px;
        margin-bottom: 15px;
    }
    
    /* Estilos para insights com glassmorphism */
    .insight-card {
        background: rgba(45, 52, 64, 0.2);
        backdrop-filter: blur(8px);
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        border-left: 5px solid;
        transition: transform 0.3s ease;
    }
    .insight-card:hover {
        transform: scale(1.05);
    }
    .insight-card h4 {
        color: #f8f9fa;
        margin: 0 0 10px 0;
        font-size: 1.2rem;
    }
    .insight-card p {
        font-size: 0.9rem;
        color: #a0a0a0;
        margin: 5px 0;
    }
    
    /* Cores das bordas dos insights */
    .critical-card { border-color: #ef4444; }
    .warning-card { border-color: #f59e0b; }
    .success-card { border-color: #10b981; }
    .info-card { border-color: #0ea5e9; }
    
    /* Estilos para o st.tabs */
    [data-testid="stTabs"] button {
        background: rgba(45, 52, 64, 0.2);
        color: #f8f9fa;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        margin: 0 5px;
        transition: all 0.3s ease;
    }
    [data-testid="stTabs"] button:hover {
        background: rgba(60, 68, 80, 0.4);
        box-shadow: 0 0 10px rgba(201, 147, 255, 0.3);
    }
    [data-testid="stTabs"] button[aria-selected="true"] {
        background: #c993ff;
        color: #000;
        border: 1px solid #c993ff;
    }
    
    /* Melhoria de sliders e inputs */
    .stSlider > div > div > div > div {
        background: #c993ff;
    }
    .stSlider > div > div > div {
        background: #4a5568;
    }
    .stDateInput > label, .stMultiSelect > label {
        color: #f8f9fa;
        font-weight: 600;
    }

    /* Estilos para o footer */
    .footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        text-align: center;
        padding: 10px;
        background: rgba(45, 52, 64, 0.2);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        color: #a0a0a0;
        font-size: 0.8rem;
        border-top: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)


# --- Aplicação principal do Streamlit
def main():
    load_css()
    
    st.set_page_config(
        page_title="Dashboard de Absenteísmo RH",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.markdown('<div class="section-title">📊 Análise de Absenteísmo de Funcionários</div>', unsafe_allow_html=True)
    st.markdown("Bem-vindo ao dashboard de absenteísmo. Use os filtros para explorar os dados e insights inteligentes.", unsafe_allow_html=True)
    
    # Carregar dados
    df = load_data()
    
    # --- Barra Lateral de Filtros (agora com design glassmorphism)
    with st.sidebar:
        st.markdown('## 🛠️ **Filtros Personalizados**')
        
        departamentos_selecionados = st.multiselect(
            "🏢 **Departamento**",
            options=sorted(df['Departamento'].unique()),
            default=sorted(df['Departamento'].unique())
        )
    
        motivos_selecionados = st.multiselect(
            "📝 **Motivos das Faltas**",
            options=sorted(df['Motivo'].unique()),
            default=sorted(df['Motivo'].unique())
        )
        
        justificacao_filtro = st.selectbox("✅ **Status de Justificação**", options=['Todos', 'Sim', 'Não'])
        genero_filtro = st.selectbox("👥 **Análise por Gênero**", options=['Todos', 'M', 'F'])

        st.markdown("---")
        
        col1_filtro, col2_filtro = st.columns(2)
        with col1_filtro:
            data_inicio = st.date_input("Data Início", value=df['Data_Falta'].min().date())
        with col2_filtro:
            data_fim = st.date_input("Data Fim", value=df['Data_Falta'].max().date())
        
        st.markdown("---")
        
        tempo_empresa_filtro = st.slider(
            "📊 **Tempo de Empresa (anos)**",
            min_value=0, max_value=int(df['Tempo_Empresa_Anos'].max()),
            value=(0, int(df['Tempo_Empresa_Anos'].max()))
        )
        
        salario_filtro = st.slider(
            "💰 **Faixa Salarial (R$)**",
            min_value=int(df['Salario_Estimado'].min()), max_value=int(df['Salario_Estimado'].max()),
            value=(int(df['Salario_Estimado'].min()), int(df['Salario_Estimado'].max())),
            step=1000
        )
    
    # --- Aplicar todos os filtros
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
    
    if justificacao_filtro != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Justificada'] == justificacao_filtro]
        
    if genero_filtro != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Genero'] == genero_filtro]
    
    if len(df_filtrado) == 0:
        st.error("⚠️ **Nenhum dado encontrado** com os filtros aplicados. Ajuste os critérios de filtragem.")
        return
    
    # Cálculos para o dashboard
    metricas = calculate_advanced_metrics(df_filtrado)
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
        st.markdown('<div class="subsection-title">Dashboard Executivo - Métricas Principais</div>', unsafe_allow_html=True)
        
        # Cards de métricas com hover effects
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
                    R$ {metricas['custo_por_falta']:,.0f} por falta (estimado)
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="subsection-title">Análise Visual Interativa</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🏢 **Distribuição por Departamento**")
            dept_counts = df_filtrado['Departamento'].value_counts()
            fig_dept = px.bar(x=dept_counts.values, y=dept_counts.index, orientation='h', color_discrete_sequence=['#c993ff'])
            fig_dept.update_layout(**plotly_theme['layout'])
            fig_dept.update_traces(hovertemplate='<b>%{y}</b><br>Faltas: %{x}<extra></extra>')
            st.plotly_chart(fig_dept, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            st.markdown("#### 🎯 **Motivos das Faltas**")
            motivo_counts = df_filtrado['Motivo'].value_counts()
            fig_motivo = px.pie(values=motivo_counts.values, names=motivo_counts.index, hole=0.4, 
                                color_discrete_sequence=px.colors.sequential.Agsunset)
            fig_motivo.update_layout(**plotly_theme['layout'])
            st.plotly_chart(fig_motivo, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown('<div class="subsection-title">🧠 Insights Inteligentes Automatizados</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            dept_top = dept_counts.index[0] if len(dept_counts) > 0 else "N/A"
            dept_perc = round((dept_counts.iloc[0] / metricas['total_faltas'] * 100), 1) if len(dept_counts) > 0 else 0
            card_class = "critical-card" if dept_perc > 30 else "warning-card" if dept_perc > 20 else "success-card"
            st.markdown(f"""
            <div class="insight-card {card_class}">
                <h4>🚨 Departamento Crítico</h4>
                <p><strong>{dept_top}</strong> concentra <strong>{dept_perc}%</strong> das faltas.</p>
                <p>💡 Recomendação: Iniciar plano de ação com o gestor e RH.</p>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            motivo_top = motivo_counts.index[0] if len(motivo_counts) > 0 else "N/A"
            card_class = "warning-card" if motivo_top in ['Doença', 'Falta de transporte'] else "info-card"
            st.markdown(f"""
            <div class="insight-card {card_class}">
                <h4>📝 Motivo Predominante</h4>
                <p>O principal motivo é <strong>{motivo_top}</strong>, que exige atenção imediata.</p>
                <p>💡 Recomendação: Analisar políticas de benefícios ou ambiente de trabalho.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            justificacao = metricas['taxa_justificacao']
            card_class = "success-card" if justificacao > 70 else "warning-card" if justificacao > 50 else "critical-card"
            st.markdown(f"""
            <div class="insight-card {card_class}">
                <h4>✅ Gestão de Justificativas</h4>
                <p>Taxa de justificação de <strong>{justificacao}%</strong>.</p>
                <p>💡 Recomendação: {'Reforçar a comunicação sobre os processos' if justificacao < 70 else 'Manter o padrão de excelência'}.</p>
            </div>
            """, unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="subsection-title">Análise Departamental Avançada</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 👥 Segmentação por Gênero e Justificação")
            genero_just = df_filtrado.groupby(['Genero', 'Justificada']).size().unstack(fill_value=0)
            fig_genero = px.bar(genero_just, barmode='group', color_discrete_map={'Sim': '#10b981', 'Não': '#ef4444'})
            fig_genero.update_layout(**plotly_theme['layout'])
            st.plotly_chart(fig_genero, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            st.markdown("#### 🔥 Heatmap: Departamentos vs Motivos")
            heatmap_data = pd.crosstab(df_filtrado['Departamento'], df_filtrado['Motivo'])
            fig_heatmap = px.imshow(heatmap_data, color_continuous_scale='Agsunset', aspect='auto')
            fig_heatmap.update_layout(**plotly_theme['layout'])
            st.plotly_chart(fig_heatmap, use_container_width=True, config={'displayModeBar': False})
        
        st.markdown("#### 💰 Custo Financeiro por Departamento")
        dept_financial = df_filtrado.groupby('Departamento').size().reset_index(name='Total_Faltas')
        dept_financial['Custo_Estimado'] = dept_financial['Total_Faltas'] * metricas['custo_por_falta']
        fig_custo_dept = px.bar(dept_financial, x='Departamento', y='Custo_Estimado', color='Custo_Estimado',
                                color_continuous_scale='Inferno')
        fig_custo_dept.update_layout(**plotly_theme['layout'])
        st.plotly_chart(fig_custo_dept, use_container_width=True, config={'displayModeBar': False})

    with tab3:
        st.markdown('<div class="subsection-title">Tendências & Padrões</div>', unsafe_allow_html=True)
        
        st.markdown("#### 📅 Evolução Temporal com Predição")
        monthly_trend = df_filtrado.groupby('Mes_Nome').size().reset_index(name='Faltas')
        monthly_trend['Data'] = pd.to_datetime(monthly_trend['Mes_Nome'], format='%b/%Y')
        monthly_trend = monthly_trend.sort_values('Data')
        
        # Predição simples (simulada) e média móvel
        monthly_trend['Media_Movel'] = monthly_trend['Faltas'].rolling(window=3, min_periods=1).mean().fillna(0)
        
        pred_df = pd.DataFrame()
        if len(monthly_trend) >= 3:
            last_value = monthly_trend['Faltas'].iloc[-1]
            pred_value = last_value * (1 + np.random.uniform(-0.1, 0.1))
            
            # Adicionar dados de predição em um DataFrame separado
            pred_df = pd.DataFrame({
                'Mes_Nome': ['Próximo Mês'],
                'Faltas': [pred_value],
            })
            
        fig_trend_pred = go.Figure()
        
        # Dados históricos
        fig_trend_pred.add_trace(go.Scatter(
            x=monthly_trend['Mes_Nome'],
            y=monthly_trend['Faltas'],
            mode='lines+markers',
            name='Dados Reais',
            line=dict(color='#8b5cf6', width=3),
            marker=dict(color='#06b6d4', size=10, line=dict(width=2, color='white')),
            hovertemplate='<b>%{x}</b><br>Faltas: %{y}<extra></extra>'
        ))
        
        # Média móvel
        fig_trend_pred.add_trace(go.Scatter(
            x=monthly_trend['Mes_Nome'],
            y=monthly_trend['Media_Movel'],
            mode='lines',
            name='Tendência',
            line=dict(color='#10b981', width=2, dash='dash'),
            hovertemplate='<b>%{x}</b><br>Tendência: %{y:.1f}<extra></extra>'
        ))
        
        # Predições
        if not pred_df.empty:
            fig_trend_pred.add_trace(go.Scatter(
                x=pred_df['Mes_Nome'],
                y=pred_df['Faltas'],
                mode='lines+markers',
                name='Predição',
                line=dict(color='#f59e0b', width=3, dash='dot'),
                marker=dict(color='#f59e0b', size=8),
                hovertemplate='<b>%{x}</b><br>Predição: %{y:.1f}<extra></extra>'
            ))
        
        fig_trend_pred.update_layout(**plotly_theme['layout'])
        fig_trend_pred.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig_trend_pred, use_container_width=True, config={'displayModeBar': False})
        
        # Análises de padrões
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 📅 **Padrão Semanal**")
            dias_ordem = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            dias_pt = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
            
            dia_counts = df_filtrado['Dia_Semana'].value_counts().reindex(dias_ordem, fill_value=0)
            
            fig_semana = px.bar(x=dias_pt, y=dia_counts.values, color=dia_counts.values,
                                color_continuous_scale=['#ef4444', '#f59e0b', '#10b981'])
            
            fig_semana.update_layout(**plotly_theme['layout'])
            fig_semana.update_traces(
                texttemplate='%{y}',
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
        st.markdown("#### 🔗 **Análise de Correlações Avançadas**")
        correlation_data = df_filtrado.groupby('ID_Funcionario').agg(
            Salario_Estimado=('Salario_Estimado', 'first'),
            Num_Faltas=('ID_Funcionario', 'count'),
            Tempo_Empresa_Anos=('Tempo_Empresa_Anos', 'first')
        ).reset_index()
        correlation_data.columns = ['ID_Funcionario', 'Salario', 'Num_Faltas', 'Tempo_Empresa']
        
        fig_scatter = px.scatter(
            correlation_data,
            x='Salario',
            y='Num_Faltas',
            size='Tempo_Empresa',
            title="",
            color='Tempo_Empresa',
            color_continuous_scale='Viridis',
            hover_data=['ID_Funcionario']
        )
        
        fig_scatter.update_layout(**plotly_theme['layout'])
        fig_scatter.update_traces(
            hovertemplate='<b>ID: %{customdata[0]}</b><br>Salário: R$ %{x:,.0f}<br>Faltas: %{y}<br>Tempo: %{marker.size} anos<extra></extra>'
        )
        fig_scatter.update_layout(height=400)
        st.plotly_chart(fig_scatter, use_container_width=True, config={'displayModeBar': False})
    
    with tab4:
        st.markdown('<div class="section-title">🔮 Inteligência Artificial & Análise Preditiva</div>', unsafe_allow_html=True)
        
        # Predições avançadas
        if len(monthly_trend) >= 3:
            recent_trend = monthly_trend['Faltas'].tail(3).mean()
            historical_avg = monthly_trend['Faltas'].mean()
            volatility = monthly_trend['Faltas'].std()
            
            # Predição com intervalos de confiança
            prediction_next_month = round(recent_trend * (1 + np.random.normal(0, 0.05)))
            confidence_interval_lower = round(max(0, prediction_next_month - (volatility * 1.96)))
            confidence_interval_upper = round(prediction_next_month + (volatility * 1.96))
            confidence_level = 82
            
            if recent_trend > historical_avg * 1.1:
                trend_direction = "📈 Crescente Acelerada"
                trend_risk = "Alto"
            elif recent_trend > historical_avg:
                trend_direction = "📈 Crescente Moderada"
                trend_risk = "Médio"
            elif recent_trend < historical_avg * 0.9:
                trend_direction = "📉 Decrescente"
                trend_risk = "Baixo"
            else:
                trend_direction = "➡️ Estável"
                trend_risk = "Controlado"
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">🎯 Predição IA - Próximo Mês</div>
                    <div class="metric-value">{prediction_next_month}</div>
                    <div class="metric-trend">
                        Intervalo: {confidence_interval_lower} - {confidence_interval_upper} faltas<br>
                        Confiança: {confidence_level}%
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">📊 Nível de Risco</div>
                    <div class="metric-value" style="font-size: 2rem;">{trend_risk}</div>
                    <div class="metric-trend">
                        Baseado em {len(monthly_trend)} períodos<br>
                        Volatilidade: {volatility:.1f}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">📈 Direção da Tendência</div>
                    <div class="metric-value" style="font-size: 1.5rem;">{trend_direction}</div>
                    <div class="metric-trend">
                        Variação: {((recent_trend/historical_avg - 1) * 100):+.1f}%<br>
                        vs média histórica
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("#### 🤖 **Modelo Preditivo com Intervalos de Confiança**")
            
            # Preparar dados para visualização
            chart_data = monthly_trend.copy()
            chart_data['Tipo'] = 'Histórico'
            
            next_months = pd.date_range(start=monthly_trend['Data'].max() + pd.DateOffset(months=1), periods=3, freq='M')
            predictions = [prediction_next_month * (1 + np.random.normal(0, 0.08)) for _ in range(3)]
            
            pred_data = pd.DataFrame({
                'Data': next_months,
                'Mes_Nome': [d.strftime('%b/%Y') for d in next_months],
                'Faltas': predictions,
                'Limite_Superior': [p + volatility * 1.96 for p in predictions],
                'Limite_Inferior': [max(0, p - volatility * 1.96) for p in predictions]
            })
            
            fig_ai = go.Figure()
            
            fig_ai.add_trace(go.Scatter(
                x=chart_data['Mes_Nome'],
                y=chart_data['Faltas'],
                mode='lines+markers',
                name='Dados Históricos',
                line=dict(color='#8b5cf6', width=4),
                marker=dict(color='#06b6d4', size=12, line=dict(width=2, color='white')),
                hovertemplate='<b>%{x}</b><br>Faltas: %{y}<extra></extra>'
            ))
            
            fig_ai.add_trace(go.Scatter(
                x=pred_data['Mes_Nome'],
                y=pred_data['Faltas'],
                mode='lines+markers',
                name='Predição IA',
                line=dict(color='#f59e0b', width=4, dash='dot'),
                marker=dict(color='#f59e0b', size=12, symbol='diamond'),
                hovertemplate='<b>%{x}</b><br>Predição: %{y:.1f}<extra></extra>'
            ))
            
            fig_ai.add_trace(go.Scatter(
                x=pred_data['Mes_Nome'],
                y=pred_data['Limite_Superior'],
                mode='lines',
                name='Limite Superior',
                line=dict(color='rgba(245, 158, 11, 0.3)', width=0),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            fig_ai.add_trace(go.Scatter(
                x=pred_data['Mes_Nome'],
                y=pred_data['Limite_Inferior'],
                mode='lines',
                name='Intervalo de Confiança',
                line=dict(color='rgba(245, 158, 11, 0.3)', width=0),
                fill='tonexty',
                fillcolor='rgba(245, 158, 11, 0.2)',
                hovertemplate='<b>%{x}</b><br>Intervalo: %{y:.1f} - %{customdata}',
                customdata=[f'{u:.1f}' for u in pred_data['Limite_Superior'].values],
                showlegend=True
            ))
            
            fig_ai.update_layout(**plotly_theme['layout'])
            fig_ai.update_layout(height=450, showlegend=True)
            st.plotly_chart(fig_ai, use_container_width=True, config={'displayModeBar': False})
        
        else:
            st.info("📊 **Dados insuficientes** para análise preditiva robusta. Necessários pelo menos 3 períodos históricos.")
            
        st.markdown("#### ⚠️ **Fatores de Risco Identificados pela IA**")
        risk_factors = []
        
        dept_concentration = (dept_counts.iloc[0] / metricas['total_faltas']) if len(dept_counts) > 0 else 0
        if dept_concentration > 0.4:
            risk_factors.append({
                'fator': 'Alta concentração em departamento específico',
                'impacto': 'Crítico', 'probabilidade': '92%', 'score': 9, 'acao': 'Intervenção imediata no departamento crítico'
            })
        elif dept_concentration > 0.25:
            risk_factors.append({
                'fator': 'Concentração moderada em departamento',
                'impacto': 'Alto', 'probabilidade': '78%', 'score': 7, 'acao': 'Monitoramento ativo e plano de melhoria'
            })
        
        if metricas['taxa_justificacao'] < 60:
            risk_factors.append({
                'fator': 'Taxa de justificação abaixo do padrão',
                'impacto': 'Alto', 'probabilidade': '85%', 'score': 8, 'acao': 'Revisar processos de comunicação interna'
            })
        elif metricas['taxa_justificacao'] < 75:
            risk_factors.append({
                'fator': 'Taxa de justificação moderada',
                'impacto': 'Médio', 'probabilidade': '68%', 'score': 6, 'acao': 'Melhorar canais de justificativa'
            })
        
        dia_pico = df_filtrado['Dia_Semana'].mode()[0]
        if dia_pico in ['Monday', 'Friday']:
            risk_factors.append({
                'fator': 'Padrão de faltas em início/fim de semana',
                'impacto': 'Médio', 'probabilidade': '72%', 'score': 6, 'acao': 'Implementar flexibilidade de horários'
            })
        
        risk_factors.sort(key=lambda x: x['score'], reverse=True)
        
        for i, risk in enumerate(risk_factors[:4]):
            color_map = {'Crítico': 'critical-card', 'Alto': 'warning-card', 'Médio': 'info-card', 'Baixo': 'success-card'}
            st.markdown(f"""
            <div class="insight-card {color_map.get(risk['impacto'], 'insight-card')}">
                <h4>🚨 Fator de Risco #{i+1} - Score: {risk['score']}/10</h4>
                <p><strong>{risk['fator']}</strong></p>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin: 1rem 0;">
                    <div><strong>Impacto:</strong> {risk['impacto']}</div>
                    <div><strong>Probabilidade:</strong> {risk['probabilidade']}</div>
                </div>
                <p><strong>🎯 Ação Recomendada:</strong> {risk['acao']}</p>
            </div>
            """, unsafe_allow_html=True)
        
    with tab5:
        st.markdown('<div class="section-title">📋 Centro de Relatórios Executivos e Exportação</div>', unsafe_allow_html=True)
        
        st.markdown("#### 📥 **Central de Downloads e Exportação**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            csv_data = df_filtrado.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="⬇️ **Exportar Excel Completo**",
                data=csv_data,
                file_name=f"hr_analytics_completo_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                mime="text/csv",
                help="Download do dataset filtrado em formato CSV (compatível com Excel)"
            )
        
        with col2:
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

Relatório gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}
"""
            st.download_button(
                label="⬇️ **Download Relatório Executivo**",
                data=relatorio_text,
                file_name=f"relatorio_executivo_hr_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                help="Download de um resumo executivo em texto"
            )
        
        with col3:
            if 'pred_data' in locals():
                pred_export = pred_data.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="⬇️ **Download Predições IA**",
                    data=pred_export,
                    file_name=f"predicoes_ia_hr_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    mime="text/csv",
                    help="Dados e predições da IA"
                )
            else:
                st.info("📊 Predições não disponíveis para download com dados atuais.")
        
        with col4:
            st.button("📊 **Dashboard PDF**", help="Snapshot visual do dashboard")
            st.warning("🚧 **Funcionalidade em desenvolvimento.** Em breve disponível!")
            
        st.markdown("---")
        st.markdown("#### 📊 **Tabela de Dados Filtrados**")
        st.dataframe(df_filtrado, use_container_width=True, hide_index=True)

    st.markdown('<div class="footer">Dashboard de Absenteísmo - Desenvolvido para portfólio | © 2024</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
