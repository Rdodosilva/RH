import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import date

# Configurações iniciais do dashboard
st.set_page_config(
    page_title="Dashboard de Absenteísmo RH",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Funções Auxiliares (mantidas como no código original)
# A função de geração de dados fictícios está aqui para que o código seja executável
def generate_data():
    np.random.seed(42)
    num_entries = 1000
    
    data = {
        'ID_Funcionario': range(1, num_entries + 1),
        'Nome': [f'Funcionario_{i}' for i in range(1, num_entries + 1)],
        'Departamento': np.random.choice(['Vendas', 'Marketing', 'RH', 'TI', 'Financeiro'], num_entries),
        'Motivo': np.random.choice(['Doença', 'Família', 'Consulta Médica', 'Falta de transporte'], num_entries),
        'Justificada': np.random.choice(['Sim', 'Não'], num_entries),
        'Genero': np.random.choice(['M', 'F'], num_entries),
        'Data_Falta': pd.to_datetime(pd.date_range(start='2024-01-01', periods=num_entries, freq='D')),
        'Tempo_Empresa_Anos': np.random.randint(0, 15, num_entries),
        'Salario_Estimado': np.random.randint(3000, 15000, num_entries),
        'Estado': np.random.choice(['SP', 'RJ', 'MG', 'BA', 'RS'], num_entries),
        'Dia_Semana': np.random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], num_entries),
    }

    df = pd.DataFrame(data)
    df['Mes_Nome'] = df['Data_Falta'].dt.strftime('%b/%Y')
    return df

@st.cache_data
def load_data():
    # Substitua esta função para carregar seu próprio arquivo de dados (CSV, Excel, etc.)
    # Exemplo: df = pd.read_csv('seu_arquivo.csv')
    df = generate_data()
    return df

def create_advanced_plotly_theme():
    # Tema de cores e layout para os gráficos
    return {
        'layout': {
            'font_family': "Roboto, sans-serif",
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'xaxis': {'showgrid': True, 'gridcolor': 'rgba(200,200,200,0.2)'},
            'yaxis': {'showgrid': True, 'gridcolor': 'rgba(200,200,200,0.2)'},
            'title_font_color': '#6b7280',
            'title_font_size': 16,
            'legend': {'bgcolor': 'rgba(255,255,255,0.1)', 'font_color': '#6b7280'}
        }
    }

def calculate_advanced_metrics(df_filtrado):
    if df_filtrado.empty:
        return {
            'total_faltas': 0, 'funcionarios_unicos': 0, 'taxa_justificacao': 0,
            'custo_estimado': 0, 'taxa_absenteismo': 0, 'pico_mensal': 'N/A',
            'media_salarial': 0, 'tendencia': 'N/A', 'departamentos_afetados': 0,
            'faltas_por_funcionario': 0
        }

    total_faltas = len(df_filtrado)
    funcionarios_unicos = df_filtrado['ID_Funcionario'].nunique()
    faltas_justificadas = df_filtrado[df_filtrado['Justificada'] == 'Sim'].shape[0]
    taxa_justificacao = round((faltas_justificadas / total_faltas) * 100, 1) if total_faltas > 0 else 0
    
    # Calcular custo estimado (valor fixo por falta)
    custo_estimado = total_faltas * 180
    
    # Taxa de absenteísmo (exemplo simplificado)
    total_dias_trabalho = (df_filtrado['Data_Falta'].max() - df_filtrado['Data_Falta'].min()).days
    if total_dias_trabalho == 0:
      total_dias_trabalho = 1
    total_funcionarios_empresa = len(load_data()['ID_Funcionario'].unique())
    taxa_absenteismo = round((total_faltas / (total_funcionarios_empresa * total_dias_trabalho)) * 100, 2)
    
    # Pico mensal
    pico_mensal = df_filtrado['Mes_Nome'].value_counts().idxmax()
    
    media_salarial = round(df_filtrado['Salario_Estimado'].mean(), 0)
    
    # Tendência (comparação simples entre o primeiro e último mês do período)
    monthly_counts = df_filtrado.groupby('Mes_Nome').size()
    if len(monthly_counts) >= 2:
      primeiro_mes_faltas = monthly_counts.iloc[0]
      ultimo_mes_faltas = monthly_counts.iloc[-1]
      tendencia = "Subindo" if ultimo_mes_faltas > primeiro_mes_faltas else "Descendo"
    else:
      tendencia = "Estável"
      
    departamentos_afetados = df_filtrado['Departamento'].nunique()
    faltas_por_funcionario = round(total_faltas / funcionarios_unicos, 1) if funcionarios_unicos > 0 else 0
    
    return {
        'total_faltas': total_faltas,
        'funcionarios_unicos': funcionarios_unicos,
        'taxa_justificacao': taxa_justificacao,
        'custo_estimado': custo_estimado,
        'taxa_absenteismo': taxa_absenteismo,
        'pico_mensal': pico_mensal,
        'media_salarial': media_salarial,
        'tendencia': tendencia,
        'departamentos_afetados': departamentos_afetados,
        'faltas_por_funcionario': faltas_por_funcionario
    }

# --- Estilos CSS personalizados para o dashboard
def load_css():
    st.markdown("""
    <style>
    .metric-card {
        background-color: #2b2b2b;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .metric-label {
        font-size: 1.1rem;
        color: #a0a0a0;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #8b5cf6;
    }
    .metric-trend {
        font-size: 0.9rem;
        color: #a0a0a0;
        margin-top: 5px;
    }
    .section-title {
        font-size: 2rem;
        font-weight: bold;
        color: #f5f5f5;
        border-bottom: 2px solid #8b5cf6;
        padding-bottom: 10px;
        margin-top: 30px;
    }
    .subsection-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #8b5cf6;
        margin-top: 20px;
        margin-bottom: 15px;
    }
    .insight-card {
        background-color: #1e1e1e;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 5px solid;
    }
    .insight-card h4 {
        color: #fff;
        margin: 0 0 10px 0;
        font-size: 1.2rem;
    }
    .insight-card p {
        font-size: 0.9rem;
        color: #a0a0a0;
        margin: 5px 0;
    }
    .critical-card { border-color: #ef4444; }
    .warning-card { border-color: #f59e0b; }
    .success-card { border-color: #10b981; }
    </style>
    """, unsafe_allow_html=True)


# --- Aplicação principal do Streamlit
def main():
    # Carregar CSS
    load_css()
    
    st.markdown('<div class="section-title">📊 Análise de Absenteísmo de Funcionários</div>', unsafe_allow_html=True)
    st.markdown("<p>Bem-vindo ao dashboard de absenteísmo. Use os filtros para explorar os dados.</p>", unsafe_allow_html=True)
    
    # Carregar dados
    df = load_data()
    
    # Convertendo a coluna 'Data_Falta' para datetime
    df['Data_Falta'] = pd.to_datetime(df['Data_Falta'])
    
    # --- Barra Lateral de Filtros
    st.sidebar.markdown('## 🛠️ **Filtros Personalizados**')
    
    # Novo filtro para Departamentos
    departamentos_selecionados = st.sidebar.multiselect(
        "🏢 **Filtrar por Departamento**",
        options=sorted(df['Departamento'].unique()),
        default=sorted(df['Departamento'].unique()),
        help="Selecione um ou mais departamentos para analisar"
    )

    motivos_selecionados = st.sidebar.multiselect(
        "📝 **Motivos das Faltas**",
        options=sorted(df['Motivo'].unique()),
        default=sorted(df['Motivo'].unique()),
        help="Filtre por motivos específicos de absenteísmo"
    )
    
    justificacao_filtro = st.sidebar.selectbox(
        "✅ **Status de Justificação**",
        options=['Todas', 'Sim', 'Não'],
        help="Analisar faltas justificadas vs não justificadas"
    )
    
    genero_filtro = st.sidebar.selectbox(
        "👥 **Análise por Gênero**",
        options=['Todos', 'M', 'F'],
        help="Segmentação demográfica dos dados"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📅 **Período de Análise**")
    data_inicio = st.sidebar.date_input(
        "Data Início",
        value=df['Data_Falta'].min().date(),
        help="Início do período de análise"
    )
    
    data_fim = st.sidebar.date_input(
        "Data Fim",
        value=df['Data_Falta'].max().date(),
        help="Fim do período de análise"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ **Filtros Especiais**")
    
    tempo_empresa_filtro = st.sidebar.slider(
        "📊 **Tempo de Empresa (anos)**",
        min_value=0,
        max_value=int(df['Tempo_Empresa_Anos'].max()),
        value=(0, int(df['Tempo_Empresa_Anos'].max())),
        help="Filtrar por tempo de empresa dos funcionários"
    )
    
    salario_filtro = st.sidebar.slider(
        "💰 **Faixa Salarial (R$)**",
        min_value=int(df['Salario_Estimado'].min()),
        max_value=int(df['Salario_Estimado'].max()),
        value=(int(df['Salario_Estimado'].min()), int(df['Salario_Estimado'].max())),
        step=1000,
        help="Análise por faixa salarial"
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
                    R$ {180:,.0f} por falta (estimado)
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
                <div class="metric-trend">de {df['Departamento'].nunique()} departamentos</div>
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
            if motivo_top in ['Doença', 'Consulta Médica']:
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
        
        # Análise financeira por departamento
        st.markdown("#### 💰 **Impacto Financeiro por Departamento**")
        
        dept_financial = df_filtrado.groupby('Departamento').agg(
            Total_Faltas=('Nome', 'count'),
            Faltas_Justificadas=('Justificada', lambda x: (x == 'Sim').sum()),
            Salario_Medio=('Salario_Estimado', 'mean')
        ).reset_index()
        
        dept_financial['Taxa_Justificacao'] = round(
            (dept_financial['Faltas_Justificadas'] / dept_financial['Total_Faltas'] * 100), 1
        )
        dept_financial['Custo_Estimado'] = dept_financial['Total_Faltas'] * 180
        dept_financial['Custo_por_Funcionario'] = round(dept_financial['Custo_Estimado'] / dept_financial['Total_Faltas'], 0)
        
        # Adicionar classificações
        def get_status_financeiro(row):
            if row['Taxa_Justificacao'] > 75 and row['Total_Faltas'] < 20:
                return '🟢 Controlado'
            elif row['Taxa_Justificacao'] > 60 and row['Total_Faltas'] < 35:
                return '🟡 Atenção'
            else:
                return '🔴 Crítico'
        
        dept_financial['Status'] = dept_financial.apply(get_status_financeiro, axis=1)
        
        def get_prioridade(row):
            score = (100 - row['Taxa_Justificacao']) + (row['Total_Faltas'] * 2)
            if score > 80:
                return 'Alta'
            elif score > 50:
                return 'Média'
            else:
                return 'Baixa'
        
        dept_financial['Prioridade'] = dept_financial.apply(get_prioridade, axis=1)
        
        # Exibir tabela com configuração avançada
        st.dataframe(
            dept_financial.sort_values('Custo_Estimado', ascending=False),
            use_container_width=True,
            hide_index=True,
            column_config={
                "Departamento": st.column_config.TextColumn("🏢 Departamento", width="medium"),
                "Total_Faltas": st.column_config.NumberColumn("📊 Total Faltas", width="small"),
                "Faltas_Justificadas": st.column_config.NumberColumn("✅ Justificadas", width="small"),
                "Taxa_Justificacao": st.column_config.NumberColumn("📈 Taxa (%)", format="%.1f%%", width="small"),
                "Salario_Medio": st.column_config.NumberColumn("💼 Salário Médio", format="R$ %.0f", width="medium"),
                "Custo_Estimado": st.column_config.NumberColumn("💰 Custo Total", format="R$ %.0f", width="medium"),
                "Status": st.column_config.TextColumn("🎯 Status", width="small"),
                "Prioridade": st.column_config.TextColumn("⚡ Prioridade", width="small")
            }
        )
        
        # Insights departamentais
        st.markdown("#### 💡 **Insights Departamentais Estratégicos**")
        
        # Departamento mais custoso
        dept_mais_custoso = dept_financial.loc[dept_financial['Custo_Estimado'].idxmax()] if not dept_financial.empty else pd.Series(
            {'Departamento': 'N/A', 'Custo_Estimado': 0, 'Total_Faltas': 0, 'Taxa_Justificacao': 0, 'Status': 'N/A', 'Prioridade': 'N/A'}
        )
        dept_melhor_taxa = dept_financial.loc[dept_financial['Taxa_Justificacao'].idxmax()] if not dept_financial.empty else pd.Series(
            {'Departamento': 'N/A', 'Custo_Estimado': 0, 'Total_Faltas': 0, 'Taxa_Justificacao': 0, 'Status': 'N/A', 'Prioridade': 'N/A'}
        )
        dept_pior_taxa = dept_financial.loc[dept_financial['Taxa_Justificacao'].idxmin()] if not dept_financial.empty else pd.Series(
            {'Departamento': 'N/A', 'Custo_Estimado': 0, 'Total_Faltas': 0, 'Taxa_Justificacao': 0, 'Status': 'N/A', 'Prioridade': 'N/A'}
        )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="insight-card critical-card">
                <h4>💸 Maior Impacto Financeiro</h4>
                <p><strong>{dept_mais_custoso['Departamento']}</strong></p>
                <p>💰 <strong>R$ {dept_mais_custoso['Custo_Estimado']:,.0f}</strong> em custos</p>
                <p>📊 {dept_mais_custoso['Total_Faltas']} faltas registradas</p>
                <p>🎯 <strong>ROI esperado:</strong> R$ {dept_mais_custoso['Custo_Estimado'] * 0.3:,.0f} com intervenção</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="insight-card success-card">
                <h4>🏆 Melhor Gestão</h4>
                <p><strong>{dept_melhor_taxa['Departamento']}</strong></p>
                <p>✅ <strong>{dept_melhor_taxa['Taxa_Justificacao']:.1f}%</strong> de justificação</p>
                <p>📚 <strong>Benchmark:</strong> Modelo para outros setores</p>
                <p>🎯 <strong>Ação:</strong> Replicar boas práticas</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="insight-card warning-card">
                <h4>⚠️ Necessita Intervenção</h4>
                <p><strong>{dept_pior_taxa['Departamento']}</strong></p>
                <p>📉 <strong>{dept_pior_taxa['Taxa_Justificacao']:.1f}%</strong> de justificação</p>
                <p>🚨 <strong>Status:</strong> {dept_pior_taxa['Status']}</p>
                <p>🎯 <strong>Prioridade:</strong> {dept_pior_taxa['Prioridade']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="section-title">📈 Análise de Tendências e Padrões Avançados</div>', unsafe_allow_html=True)
        
        # Análise temporal detalhada
        st.markdown("#### 📊 **Evolução Temporal Detalhada**")
        
        # Preparar dados temporais
        df_temporal = df_filtrado.copy()
        df_temporal['Semana'] = df_temporal['Data_Falta'].dt.isocalendar().week.astype(str)
        df_temporal['Mes'] = df_temporal['Data_Falta'].dt.month
        df_temporal['Dia_Semana_Num'] = df_temporal['Data_Falta'].dt.dayofweek
        
        # Gráfico de tendência mensal com predição
        monthly_trend = df_temporal.groupby('Mes_Nome').size().reset_index(name='Faltas')
        monthly_trend['Data'] = pd.to_datetime(monthly_trend['Mes_Nome'], format='%b/%Y')
        monthly_trend = monthly_trend.sort_values('Data')
        
        # Calcular média móvel
        if len(monthly_trend) >= 3:
            monthly_trend['Media_Movel'] = monthly_trend['Faltas'].rolling(window=3, center=True).mean()
            
            # Predição simples (próximos 2 meses)
            ultima_media = monthly_trend['Media_Movel'].dropna().iloc[-1]
            
            # Adicionar predições
            last_date = monthly_trend['Data'].max()
            pred_dates = [last_date + pd.DateOffset(months=i) for i in range(1, 3)]
            pred_values = [ultima_media * (1 + np.random.normal(0, 0.1)) for _ in pred_dates]
            
            pred_df = pd.DataFrame({
                'Data': pred_dates,
                'Mes_Nome': [d.strftime('%b/%Y') for d in pred_dates],
                'Faltas': [None] * len(pred_dates),
                'Media_Movel': [None] * len(pred_dates),
                'Predicao': pred_values
            })
            
            monthly_trend['Predicao'] = [None] * len(monthly_trend)
            trend_combined = pd.concat([monthly_trend, pred_df], ignore_index=True)
            
            # Criar gráfico de tendência com predição
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
            fig_trend_pred.add_trace(go.Scatter(
                x=pred_df['Mes_Nome'],
                y=pred_df['Predicao'],
                mode='lines+markers',
                name='Predição',
                line=dict(color='#f59e0b', width=3, dash='dot'),
                marker=dict(color='#f59e0b', size=8),
                hovertemplate='<b>%{x}</b><br>Predição: %{y:.1f}<extra></extra>'
            ))
            
            fig_trend_pred.update_layout(**plotly_theme['layout'])
            fig_trend_pred.update_layout(height=400, showlegend=True)
            
            st.plotly_chart(fig_trend_pred, use_container_width=True, config={'displayModeBar': False})
        else:
            st.info("Não há dados suficientes para plotar a tendência mensal. Selecione um período maior.")
        
        # Análises de padrões
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📅 **Padrão Semanal**")
            
            dias_semana_ordem = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            dias_semana_pt = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
            dia_counts = df_temporal['Dia_Semana'].value_counts().reindex(dias_semana_ordem, fill_value=0)
            
            fig_semana = px.bar(
                x=dias_semana_pt,
                y=dia_counts.values,
                title="",
                color=dia_counts.values,
                color_continuous_scale=['#ef4444', '#f59e0b', '#10b981'],
                text=dia_counts.values
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
        st.markdown("#### 🔗 **Análise de Correlações Avançadas**")
        
        # Correlação salário vs faltas
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
        dia_pico = dia_counts.idxmax() if not dia_counts.empty else "N/A"
        estado_concentracao = estado_counts.index[0] if not estado_counts.empty else "N/A"
        
        # Tendência geral
        if len(monthly_trend) >= 2:
            tendencia_geral = "Crescente" if monthly_trend['Faltas'].iloc[-1] > monthly_trend['Faltas'].iloc[0] else "Decrescente"
        else:
            tendencia_geral = "Estável"
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="insight-card warning-card">
                <h4>📅 Padrão Semanal Crítico</h4>
                <p><strong>{dias_semana_pt[dias_semana_ordem.index(dia_pico)] if dia_pico != 'N/A' else 'N/A'}</strong> é o dia com mais faltas</p>
                <p>🎯 <strong>Hipótese:</strong> {'Extensão de fim de semana' if dia_pico in ['Monday', 'Friday'] else 'Meio da semana estressante' if dia_pico in ['Wednesday'] else 'Sem padrão claro'}</p>
                <p>💡 <strong>Ação:</strong> {'Flexibilizar o horário' if dia_pico in ['Monday', 'Friday'] else 'Realizar pesquisa de clima'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="insight-card success-card">
                <h4>🗺️ Concentração Geográfica</h4>
                <p>A maior parte das faltas se concentra em <strong>{estado_concentracao}</strong></p>
                <p>📈 <strong>Total de faltas:</strong> {estado_counts.iloc[0] if not estado_counts.empty else 0}</p>
                <p>💡 <strong>Ação:</strong> Analisar fatores locais (transporte, saúde pública)</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="insight-card critical-card">
                <h4>📈 Tendência Geral</h4>
                <p>A tendência de faltas no período é <strong>{tendencia_geral}</strong></p>
                <p>🚨 <strong>Alerta:</strong> {'Alta probabilidade de aumento futuro' if tendencia_geral == 'Crescente' else 'Situação sob controle'}</p>
                <p>🎯 <strong>Foco:</strong> {'Revisão de políticas de RH e bem-estar' if tendencia_geral == 'Crescente' else 'Manutenção de práticas atuais'}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab4:
        st.markdown('<div class="section-title">🔮 IA & Predições (Em Desenvolvimento)</div>', unsafe_allow_html=True)
        st.info("Esta seção será dedicada a modelos de IA para prever absenteísmo e identificar funcionários em risco. Em breve!")
    
    with tab5:
        st.markdown('<div class="section-title">📋 Relatórios Executivos</div>', unsafe_allow_html=True)
        st.warning("Funcionalidade de download de relatórios em PDF e Excel está sendo implementada.")
        
        # Mostrar o DataFrame filtrado
        st.markdown("#### **Tabela de Dados Filtrados**")
        st.dataframe(df_filtrado, use_container_width=True)

if __name__ == '__main__':
    main()
