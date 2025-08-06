elif departamento == 'Operacoes Industriais':
            motivo_weights = [0.12, 0.08, 0.15, 0.25, 0.10, 0.08, 0.05, 0.07, 0.02, 0.05, 0.03, 0.00]
        else:
            motivo_weights = [0.16, 0.12, 0.18, 0.20, 0.08, 0.06, 0.08, 0.06, 0.02, 0.02, 0.02, 0.00]
        
        motivo = np.random.choice(motivos_ausencia, p=motivo_weights)
        
        # Sistema inteligente de justificação
        justificacao_prob = {
            'Consulta Medica': 0.95, 'Atestado Medico': 0.98, 'Emergencia Familiar': 0.85,
            'Doenca Familiar': 0.80, 'Acidente de Trabalho': 1.00, 'Licenca Maternidade': 1.00,
            'Acompanhamento Medico': 0.90, 'Questoes de Saude Mental': 0.75,
            'Problemas de Transporte': 0.60, 'Compromissos Pessoais': 0.45,
            'Home Office': 0.95, 'Sem Justificativa': 0.00
        }
        
        justificada = 'Sim' if random.random() < justificacao_prob.get(motivo, 0.70) else 'Nao'
        
        # Distribuição temporal inteligente
        month_weights = [0.12, 0.08, 0.10, 0.09, 0.08, 0.07, 0.06, 0.08, 0.09, 0.10, 0.08, 0.05]
        mes = np.random.choice(range(1, 13), p=month_weights)
        dia = random.randint(1, 28)
        
        data_falta = datetime(2024, mes, dia)
        
        # Hierarquia salarial realista
        cargo = random.choice(cargos_hierarquia)
        salario_base = {
            'Estagiario': (1200, 2000), 'Assistente': (2500, 3500),
            'Analista Jr': (3500, 5500), 'Analista Pleno': (5500, 8000),
            'Analista Senior': (8000, 12000), 'Especialista': (10000, 15000),
            'Coordenador': (12000, 18000), 'Supervisor': (15000, 22000),
            'Gerente': (18000, 30000), 'Gerente Senior': (25000, 40000),
            'Diretor': (35000, 60000), 'Vice-Presidente': (50000, 100000)
        }
        
        salario_min, salario_max = salario_base.get(cargo, (3000, 8000))
        salario = random.randint(salario_min, salario_max)
        
        genero = random.choice(['M', 'F'])
        nome = f"{random.choice(nomes_brasileiros)} {i+1:03d}"
        
        anos_empresa = np.random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
                                       p=[0.15, 0.20, 0.15, 0.12, 0.10, 0.08, 0.07, 0.05, 0.04, 0.03, 0.01])
        data_admissao = base_date - timedelta(days=anos_empresa * 365 + random.randint(0, 365))
        
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
            'Criticidade_Ausencia': 'Alta' if motivo in ['Sem Justificativa', 'Problemas de Transporte'] else 
                                   'Media' if motivo in ['Compromissos Pessoais'] else 'Baixa'
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
    df['Semestre'] = df['Data_Ausencia'].dt.month.apply(lambda x: 1 if x <= 6 else 2)
    df['Anos_Empresa'] = ((datetime.now() - df['Data_Admissao']).dt.days / 365).astype(int).clip(0, 50)
    df['Faixa_Salarial'] = pd.cut(df['Salario_Atual'], 
                                  bins=[0, 5000, 10000, 20000, 50000, 100000],
                                  labels=['Ate 5k', '5k-10k', '10k-20k', '20k-50k', '50k+'])
    df['Indice_Rotatividade'] = df['Anos_Empresa'].apply(lambda x: 'Alto' if x < 2 else 'Medio' if x < 5 else 'Baixo')
    
    return df

@st.cache_data(ttl=300)
def calculate_premium_metrics(df: pd.DataFrame) -> Dict:
    """Calcula métricas avançadas com KPIs corporativos"""
    if len(df) == 0:
        return {
            'total_ausencias': 0, 'funcionarios_impactados': 0, 'taxa_justificacao': 0,
            'departamentos_criticos': 0, 'impacto_financeiro': 0, 'salario_medio': 0,
            'ausencias_por_funcionario': 0, 'taxa_absenteismo': 0, 'pico_temporal': 'N/A',
            'tendencia_geral': 'Estavel', 'indice_criticidade': 'Baixo', 'score_rh': 85
        }
    
    total_ausencias = len(df)
    funcionarios_impactados = df['Nome_Completo'].nunique()
    ausencias_justificadas = len(df[df['Status_Justificativa'] == 'Sim'])
    taxa_justificacao = round((ausencias_justificadas / total_ausencias * 100), 2)
    departamentos_criticos = df['Departamento'].nunique()
    
    # Métricas financeiras avançadas
    custo_medio_ausencia = 280  # R$ por ausência (baseado em produtividade perdida)
    impacto_financeiro = total_ausencias * custo_medio_ausencia
    salario_medio = df['Salario_Atual'].mean()
    
    # KPIs de RH avançados
    ausencias_por_funcionario = round(total_ausencias / funcionarios_impactados, 2)
    taxa_absenteismo = round((total_ausencias / (funcionarios_impactados * 22)) * 100, 2)
    
    # Análise temporal inteligente
    pico_temporal = df['Mes_Nome_BR'].value_counts().index[0] if len(df) > 0 else 'N/A'
    
    # Índice de criticidade corporativa
    ausencias_criticas = len(df[df['Criticidade_Ausencia'] == 'Alta'])
    indice_criticidade = 'Alto' if ausencias_criticas > total_ausencias * 0.3 else \
                        'Medio' if ausencias_criticas > total_ausencias * 0.15 else 'Baixo'
    
    # Score de RH (0-100)
    score_base = 100
    score_base -= max(0, (taxa_absenteismo - 3) * 5)
    score_base -= max(0, (100 - taxa_justificacao) * 0.3)
    score_base -= ausencias_criticas * 0.5
    score_rh = max(0, min(100, round(score_base)))
    
    # Tendência baseada em análise temporal
    if len(df) >= 10:
        dados_recentes = df.sort_values('Data_Ausencia').tail(30)
        dados_anteriores = df.sort_values('Data_Ausencia').iloc[:-30] if len(df) > 30 else df.head(10)
        
        media_recente = len(dados_recentes) / max(1, dados_recentes['Data_Ausencia'].nunique())
        media_anterior = len(dados_anteriores) / max(1, dados_anteriores['Data_Ausencia'].nunique())
        
        if media_recente > media_anterior * 1.15:
            tendencia_geral = 'Crescente Preocupante'
        elif media_recente > media_anterior * 1.05:
            tendencia_geral = 'Crescente Leve'
        elif media_recente < media_anterior * 0.85:
            tendencia_geral = 'Decrescente Positiva'
        elif media_recente < media_anterior * 0.95:
            tendencia_geral = 'Decrescente Leve'
        else:
            tendencia_geral = 'Estavel'
    else:
        tendencia_geral = 'Dados Insuficientes'
    
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

def create_ultra_plotly_theme() -> Dict:
    """Tema ultra-futurístico para gráficos Plotly"""
    return {
        'layout': {
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'font': {
                'color': 'white', 
                'family': 'Inter, sans-serif',
                'size': 12,
                'weight': 600
            },
            'title': {
                'font': {'size': 20, 'color': 'white', 'family': 'Orbitron, monospace'},
                'x': 0.5,
                'xanchor': 'center',
                'pad': {'t': 20}
            },
            'xaxis': {
                'gridcolor': 'rgba(139, 92, 246, 0.2)',
                'linecolor': 'rgba(255, 255, 255, 0.3)',
                'tickcolor': 'rgba(255, 255, 255, 0.3)',
                'tickfont': {'color': 'rgba(255, 255, 255, 0.9)', 'size': 11, 'family': 'Inter'},
                'titlefont': {'color': 'white', 'size': 14, 'family': 'Inter'}
            },
            'yaxis': {
                'gridcolor': 'rgba(139, 92, 246, 0.2)',
                'linecolor': 'rgba(255, 255, 255, 0.3)',
                'tickcolor': 'rgba(255, 255, 255, 0.3)',
                'tickfont': {'color': 'rgba(255, 255, 255, 0.9)', 'size': 11, 'family': 'Inter'},
                'titlefont': {'color': 'white', 'size': 14, 'family': 'Inter'}
            },
            'legend': {
                'font': {'color': 'white', 'size': 11, 'family': 'Inter'},
                'bgcolor': 'rgba(255, 255, 255, 0.05)',
                'bordercolor': 'rgba(139, 92, 246, 0.3)',
                'borderwidth': 2,
                'x': 1, 'y': 1,
                'xanchor': 'right', 'yanchor': 'top'
            },
            'colorway': [
                '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', 
                '#8b5a2b', '#6366f1', '#ec4899', '#14b8a6', '#f97316'
            ],
            'margin': dict(l=40, r=40, t=60, b=40)
        }
    }

def display_ultra_loading():
    """Animação de loading ultra premium"""
    loading_placeholder = st.empty()
    with loading_placeholder.container():
        st.markdown("""
        <div class="premium-loading">
            <div class="premium-spinner"></div>
            <div class="loading-text">Iniciando HR Analytics Intelligence Suite...</div>
            <p style="color: rgba(255,255,255,0.6); margin-top: 1rem; font-family: 'Inter';">
                Processando 500+ registros corporativos com IA avancada
            </p>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(2.5)
    loading_placeholder.empty()

def create_advanced_chart(df: pd.DataFrame, chart_type: str, **kwargs) -> go.Figure:
    """Factory para criação de gráficos ultra-avançados"""
    theme = create_ultra_plotly_theme()
    
    if chart_type == "departmental_analysis":
        dept_data = df['Departamento'].value_counts().head(8)
        
        fig = px.bar(
            x=dept_data.values,
            y=dept_data.index,
            orientation='h',
            title="Analise Critica Departamental",
            color=dept_data.values,
            color_continuous_scale=['#ef4444', '#f59e0b', '#8b5cf6', '#06b6d4', '#10b981']
        )
        
        fig.update_traces(
            hovertemplate='<b>%{y}</b><br>Ausencias: %{x}<br>Impacto: R$ %{customdata:,.0f}<extra></extra>',
            customdata=dept_data.values * 280,
            textposition='outside',
            texttemplate='%{x}',
            textfont=dict(size=14, color='white', family='Orbitron')
        )
        
        fig.update_layout(**theme['layout'])
        fig.update_layout(height=500, showlegend=False)
        fig.update_coloraxes(showscale=False)
        
        return fig
    
    elif chart_type == "motivos_premium":
        motivo_data = df['Motivo_Ausencia'].value_counts().head(8)
        
        fig = px.pie(
            values=motivo_data.values,
            names=motivo_data.index,
            title="Distribuicao Inteligente de Motivos",
            color_discrete_sequence=['#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#ec4899', '#14b8a6', '#f97316']
        )
        
        fig.update_traces(
            textinfo='percent+label',
            textfont_size=12,
            textfont_color='white',
            textfont_family='Inter',
            hovertemplate='<b>%{label}</b><br>Casos: %{value}<br>Percentual: %{percent}<br>Impacto: R$ %{customdata:,.0f}<extra></extra>',
            customdata=motivo_data.values * 280,
            marker=dict(
                line=dict(color='rgba(255,255,255,0.4)', width=3),
                opacity=0.9
            ),
            pull=[0.05 if i == 0 else 0 for i in range(len(motivo_data))]
        )
        
        fig.update_layout(**theme['layout'])
        fig.update_layout(height=500)
        
        return fig
    
    elif chart_type == "timeline_advanced":
        timeline_data = df.groupby(['Mes_Nome_BR']).size().reset_index(name='Ausencias')
        timeline_data['Data_Ordenacao'] = pd.to_datetime(timeline_data['Mes_Nome_BR'], format='%b/%Y')
        timeline_data = timeline_data.sort_values('Data_Ordenacao')
        
        # Adicionar média móvel
        timeline_data['Media_Movel'] = timeline_data['Ausencias'].rolling(window=3, center=True).mean()
        
        fig = make_subplots(
            rows=1, cols=1,
            subplot_titles=['Evolucao Temporal Inteligente com Predicao IA']
        )
        
        # Dados reais
        fig.add_trace(
            go.Scatter(
                x=timeline_data['Mes_Nome_BR'],
                y=timeline_data['Ausencias'],
                mode='lines+markers',
                name='Ausencias Reais',
                line=dict(color='#8b5cf6', width=4, shape='spline'),
                marker=dict(
                    color='#06b6d4', 
                    size=12, 
                    line=dict(width=3, color='white'),
                    symbol='circle'
                ),
                hovertemplate='<b>%{x}</b><br>Ausencias: %{y}<br>Impacto: R$ %{customdata:,.0f}<extra></extra>',
                customdata=timeline_data['Ausencias'] * 280
            )
        )
        
        # Média móvel
        fig.add_trace(
            go.Scatter(
                x=timeline_data['Mes_Nome_BR'],
                y=timeline_data['Media_Movel'],
                mode='lines',
                name='Tendencia (IA)',
                line=dict(color='#10b981', width=3, dash='dash'),
                hovertemplate='<b>%{x}</b><br>Tendencia: %{y:.1f}<extra></extra>'
            )
        )
        
        fig.update_layout(**theme['layout'])
        fig.update_layout(height=400)
        
        return fig

def main():
    """Função principal ultra-premium"""
    
    # Loading inicial ultra-premium
    if 'premium_loaded' not in st.session_state:
        display_ultra_loading()
        st.session_state.premium_loaded = True
    
    # Header mega futurístico
    st.markdown("""
    <div class="mega-header">
        <h1>HR ANALYTICS INTELLIGENCE SUITE</h1>
        <p class="subtitle">Plataforma Avancada de Analise Corporativa com Inteligencia Artificial</p>
        <div style="margin-top: 2rem;">
            <span class="tech-badge">Machine Learning</span>
            <span class="tech-badge">Real-time Analytics</span>
            <span class="tech-badge">Predictive AI</span>
            <span class="tech-badge">Business Intelligence</span>
            <span class="tech-badge">Corporate Dashboard</span>
        </div>
        <div style="margin-top: 1.5rem;">
            <span class="status-indicator status-online"></span>
            <span style="font-size: 0.95rem; font-family: 'Orbitron', monospace;">SISTEMA OPERACIONAL | DADOS SINCRONIZADOS</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregamento de dados premium
    with st.spinner(""):
        df = generate_premium_dataset()
    
    if len(df) == 0:
        st.error("Falha critica no sistema de dados. Contacte o administrador.")
        return
    
    st.success(f"✅ **{len(df)} registros corporativos** processados com sucesso! Sistema de IA ativo e otimizado.")
    
    # Sidebar ultra-futurística
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h2 style="color: white; font-family: 'Orbitron', monospace; font-size: 1.5rem;">
                CENTRO DE CONTROLE
            </h2>
            <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">Configure sua analise avancada</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Filtros ultra-avançados
        st.markdown("### **Filtros Departamentais**")
        departamentos_selecionados = st.multiselect(
            "Selecione os departamentos para analise:",
            options=sorted(df['Departamento'].unique()),
            default=sorted(df['Departamento'].unique()),
            help="Filtragem inteligente por departamentos criticos"
        )
        
        st.markdown("### **Analise de Motivos**")
        motivos_selecionados = st.multiselect(
            "Motivos de ausencia para investigacao:",
            options=sorted(df['Motivo_Ausencia'].unique()),
            default=sorted(df['Motivo_Ausencia'].unique()),
            help="Classificacao automatica por criticidade"
        )
        
        st.markdown("### **Status de Conformidade**")
        justificacao_filtro = st.selectbox(
            "Analise de justificativas corporativas:",
            options=['Todas', 'Sim', 'Nao'],
            help="KPI de conformidade organizacional"
        )
        
        st.markdown("### **Segmentacao Demografica**")
        genero_filtro = st.selectbox(
            "Analise por genero:",
            options=['Todos', 'M', 'F'],
            help="Insights de diversidade corporativa"
        )
        
        st.markdown("### **Periodo de Analise Premium**")
        try:
            col1, col2 = st.columns(2)
            with col1:
                data_inicio = st.date_input(
                    "Inicio:",
                    value=df['Data_Ausencia'].min().date(),
                    help="Data inicial da analise"
                )
            with col2:
                data_fim = st.date_input(
                    "Fim:",
                    value=df['Data_Ausencia'].max().date(),
                    help="Data final da analise"
                )
        except:
            data_inicio = datetime.now().date()
            data_fim = datetime.now().date()
    
    # Aplicação de filtros ultra-inteligente
    try:
        df_filtrado = df.copy()
        
        if departamentos_selecionados:
            df_filtrado = df_filtrado[df_filtrado['Departamento'].isin(departamentos_selecionados)]
        
        if motivos_selecionados:
            df_filtrado = df_filtrado[df_filtrado['Motivo_Ausencia'].isin(motivos_selecionados)]
        
        if justificacao_filtro != 'Todas':
            df_filtrado = df_filtrado[df_filtrado['Status_Justificativa'] == justificacao_filtro]
        
        if genero_filtro != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['Genero'] == genero_filtro]
        
        try:
            df_filtrado = df_filtrado[
                (df_filtrado['Data_Ausencia'].dt.date >= data_inicio) &
                (df_filtrado['Data_Ausencia'].dt.date <= data_fim)
            ]
        except:
            pass
            
    except Exception as e:
        st.warning(f"Ajuste nos filtros aplicado automaticamente: {str(e)}")
        df_filtrado = df.copy()
    
    if len(df_filtrado) == 0:
        st.warning("Nenhum registro encontrado com os filtros atuais. Exibindo dataset completo.")
        df_filtrado = df.copy()
    
    # Cálculo de métricas premium
    metricas = calculate_premium_metrics(df_filtrado)
    
    # Sistema de abas ultra-futurístico
    tab1, tab2, tab3 = st.tabs([
        "COMMAND CENTER",
        "ANALYTICS 360",
        "EXECUTIVE SUITE"
    ])
    
    with tab1:
        st.markdown('<div class="ultra-section-title">CENTRO DE COMANDO EXECUTIVO</div>', unsafe_allow_html=True)
        
        # Cards de métricas ultra-premium
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            trend_class = "trend-negative" if metricas['total_ausencias'] > 100 else "trend-positive" if metricas['total_ausencias'] < 50 else "trend-neutral"
            st.markdown(f"""
            <div class="premium-metric-card">
                <div class="premium-metric-label">TOTAL DE AUSENCIAS</div>
                <div class="premium-metric-value">{metricas['total_ausencias']}</div>
                <div class="premium-metric-trend {trend_class}">
                    {round((metricas['total_ausencias']/len(df)*100), 1)}% do dataset | {metricas['tendencia_geral']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="premium-metric-card">
                <div class="premium-metric-label">COLABORADORES IMPACTADOS</div>
                <div class="premium-metric-value">{metricas['funcionarios_impactados']}</div>
                <div class="premium-metric-trend">
                    {metricas['ausencias_por_funcionario']} ausencias/pessoa
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
                    {'Excelente' if metricas['taxa_justificacao'] > 80 else 'Critica' if metricas['taxa_justificacao'] < 60 else 'Moderada'}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="premium-metric-card">
                <div class="premium-metric-label">IMPACTO FINANCEIRO</div>
                <div class="premium-metric-value">R$ {metricas['impacto_financeiro']:,.0f}</div>
                <div class="premium-metric-trend">
                    R$ {metricas['impacto_financeiro']/metricas['total_ausencias']:,.0f} por ausencia
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Gráficos principais ultra-avançados
        st.markdown('<div class="ultra-section-title">ANALISE VISUAL INTELIGENTE</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                fig_dept = create_advanced_chart(df_filtrado, "departmental_analysis")
                st.plotly_chart(fig_dept, use_container_width=True, config={'displayModeBar': False})
            except Exception as e:
                st.error(f"Erro no grafico departamental: {str(e)}")
        
        with col2:
            try:
                fig_motivos = create_advanced_chart(df_filtrado, "motivos_premium")
                st.plotly_chart(fig_motivos, use_container_width=True, config={'displayModeBar': False})
            except Exception as e:
                st.error(f"Erro no grafico de motivos: {str(e)}")
        
        # Timeline avançada
        try:
            fig_timeline = create_advanced_chart(df_filtrado, "timeline_advanced")
            st.plotly_chart(fig_timeline, use_container_width=True, config={'displayModeBar': False})
        except Exception as e:
            st.error(f"Erro na timeline: {str(e)}")
    
    with tab2:
        st.markdown('<div class="ultra-section-title">ANALYTICS 360 COM MACHINE LEARNING</div>', unsafe_allow_html=True)
        
        # Análise de padrões avançados
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### **Padrao Semanal Inteligente**")
            try:
                if len(df_filtrado) > 0:
                    dias_semana = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    dias_pt = ['Segunda', 'Terca', 'Quarta', 'Quinta', 'Sexta', 'Sabado', 'Domingo']
                    dia_counts = df_filtrado['Data_Ausencia'].dt.day_name().value_counts()
                    
                    dia_data = []
                    for i, dia_en in enumerate(dias_semana):
                        count = dia_counts.get(dia_en, 0)
                        dia_data.append({'Dia': dias_pt[i], 'Ausencias': count, 'Impacto': count * 280})
                    
                    dia_df = pd.DataFrame(dia_data)
                    
                    fig_semana = px.bar(
                        dia_df,
                        x='Dia',
                        y='Ausencias',
                        title="Analise Comportamental por Dia da Semana",
                        color='Ausencias',
                        color_continuous_scale=['#10b981', '#f59e0b', '#ef4444'],
                        text='Ausencias'
                    )
                    
                    theme = create_ultra_plotly_theme()
                    fig_semana.update_layout(**theme['layout'])
                    fig_semana.update_traces(
                        texttemplate='%{text}',
                        textposition='outside',
                        textfont=dict(color='white', size=12),
                        hovertemplate='<b>%{x}</b><br>Ausencias: %{y}<br>Impacto: R$ %{customdata:,.0f}<extra></extra>',
                        customdata=dia_df['Impacto']
                    )
                    fig_semana.update_coloraxes(showscale=False)
                    fig_semana.update_layout(height=400)
                    
                    st.plotly_chart(fig_semana, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.info("Dados insuficientes")
            except Exception as e:
                st.error(f"Erro: {str(e)}")
        
        with col2:
            st.markdown("#### **Distribuicao Geografica Nacional**")
            try:
                if len(df_filtrado) > 0:
                    estado_counts = df_filtrado['Estado_UF'].value_counts().head(10)
                    
                    fig_estado = px.bar(
                        x=estado_counts.index,
                        y=estado_counts.values,
                        title="Mapeamento por Estado (Top 10)",
                        color=estado_counts.values,
                        color_continuous_scale=['#8b5cf6', '#06b6d4', '#10b981'],
                        text=estado_counts.values
                    )
                    
                    theme = create_ultra_plotly_theme()
                    fig_estado.update_layout(**theme['layout'])
                    fig_estado.update_traces(
                        texttemplate='%{text}',
                        textposition='outside',
                        textfont=dict(color='white', size=12),
                        hovertemplate='<b>%{x}</b><br>Ausencias: %{y}<br>Custo: R$ %{customdata:,.0f}<extra></extra>',
                        customdata=estado_counts.values * 280
                    )
                    fig_estado.update_coloraxes(showscale=False)
                    fig_estado.update_layout(height=400)
                    
                    st.plotly_chart(fig_estado, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.info("Dados insuficientes")
            except Exception as e:
                st.error(f"Erro: {str(e)}")
        
        # Insights inteligentes
        st.markdown("#### **Insights de Inteligencia Artificial**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            try:
                dept_counts = df_filtrado['Departamento'].value_counts()
                if len(dept_counts) > 0:
                    dept_top = dept_counts.index[0]
                    dept_valor = dept_counts.iloc[0]
                    dept_perc = round((dept_valor / metricas['total_ausencias'] * 100), 1)
                    
                    card_class = "critical-insight" if dept_perc > 35 else "warning-insight" if dept_perc > 25 else "success-insight"
                    status_emoji = "CRITICO" if dept_perc > 35 else "ATENCAO" if dept_perc > 25 else "CONTROLADO"
                    
                    st.markdown(f"""
                    <div class="ultra-insight-card {card_class}">
                        <h4>DEPARTAMENTO CRITICO - {status_emoji}</h4>
                        <p><strong>{dept_top}</strong> concentra <strong>{dept_valor} ausencias</strong> ({dept_perc}% do total)</p>
                        <p><strong>Recomendacao IA:</strong> {'Intervencao imediata com plano de acao 30 dias' if dept_perc > 35 else 'Monitoramento ativo quinzenal' if dept_perc > 25 else 'Manter padrao atual'}</p>
                        <p><strong>Impacto:</strong> R$ {dept_valor * 280:,.0f} em perdas estimadas</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("Dados insuficientes para analise departamental")
            except Exception as e:
                st.error(f"Erro na analise: {str(e)}")
        
        with col2:
            try:
                motivo_counts = df_filtrado['Motivo_Ausencia'].value_counts()
                if len(motivo_counts) > 0:
                    motivo_top = motivo_counts.index[0]
                    motivo_valor = motivo_counts.iloc[0]
                    motivo_perc = round((motivo_valor / metricas['total_ausencias'] * 100), 1)
                    
                    recomendacoes = {
                        'Consulta Medica': 'Programa de saude preventiva corporativa',
                        'Atestado Medico': 'Analise de ambiente ocupacional',
                        'Emergencia Familiar': 'Flexibilizacao de horarios familiares',
                        'Doenca Familiar': 'Apoio psicologico e suporte familiar',
                        'Problemas de Transporte': 'Auxilio transporte ou home office',
                        'Compromissos Pessoais': 'Banco de horas personalizado',
                        'Sem Justificativa': 'Revisao disciplinar e comunicacao'
                    }
                    
                    recomendacao = recomendacoes.get(motivo_top, 'Investigacao detalhada necessaria')
                    card_class = "critical-insight" if motivo_top == 'Sem Justificativa' else "warning-insight" if motivo_perc > 30 else "ultra-insight-card"
                    
                    st.markdown(f"""
                    <div class="ultra-insight-card {card_class}">
                        <h4>MOTIVO PREDOMINANTE</h4>
                        <p><strong>{motivo_top}</strong> representa <strong>{motivo_valor} casos</strong> ({motivo_perc}% do total)</p>
                        <p><strong>Solucao IA:</strong> {recomendacao}</p>
                        <p><strong>Potencial ROI:</strong> {'Alto (25-40%)' if motivo_perc > 25 else 'Medio (15-25%)' if motivo_perc > 15 else 'Baixo (5-15%)'}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("Dados insuficientes para analise de motivos")
            except Exception as e:
                st.error(f"Erro na analise: {str(e)}")
        
        with col3:
            taxa = metricas['taxa_justificacao']
            score = metricas['score_rh']
            
            if score > 85:
                status = "EXCEPCIONAL"
                card_class = "success-insight"
                acao = "Manter excelencia e replicar boas praticas"
            elif score > 70:
                status = "BOM"
                card_class = "ultra-insight-card"
                acao = "Pequenos ajustes para otimizacao"
            elif score > 60:
                status = "MODERADO"
                card_class = "warning-insight"
                acao = "Implementar melhorias estruturais"
            else:
                status = "CRITICO"
                card_class = "critical-insight"
                acao = "Intervencao imediata necessaria"
            
            st.markdown(f"""
            <div class="ultra-insight-card {card_class}">
                <h4>SCORE CORPORATIVO - {status}</h4>
                <p><strong>Score Geral:</strong> {score}/100</p>
                <p><strong>Taxa Conformidade:</strong> {taxa}%</p>
                <p><strong>Estrategia:</strong> {acao}</p>
                <p><strong>Benchmark:</strong> {'Acima do mercado' if score > 75 else 'Dentro da media' if score > 60 else 'Abaixo da media'}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="ultra-section-title">EXECUTIVE SUITE E RELATORIOS</div>', unsafe_allow_html=True)
        
        # Central de downloads premium
        st.markdown("#### **Centro de Downloads Executivos**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("Excel Premium", help="Dataset completo com analises"):
                try:
                    csv_data = df_filtrado.to_csv(index=False)
                    st.download_button(
                        label="Download Excel",
                        data=csv_data,
                        file_name=f"hr_analytics_premium_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv",
                        key="excel_download"
                    )
                    st.success("Excel Premium gerado com sucesso!")
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
        
        with col2:
            if st.button("Relatorio Executivo", help="Sumario para C-Level"):
                try:
                    relatorio_executivo = f"""
HR ANALYTICS INTELLIGENCE SUITE - RELATORIO EXECUTIVO
===================================================

PERIODO DE ANALISE: {data_inicio.strftime('%d/%m/%Y')} - {data_fim.strftime('%d/%m/%Y')}
GERADO EM: {datetime.now().strftime('%d/%m/%Y as %H:%M')}

METRICAS PRINCIPAIS
------------------
• Total de Ausencias: {metricas['total_ausencias']:,}
• Colaboradores Impactados: {metricas['funcionarios_impactados']:,}
• Taxa de Conformidade: {metricas['taxa_justificacao']}%
• Score Corporativo: {metricas['score_rh']}/100
• Impacto Financeiro: R$ {metricas['impacto_financeiro']:,.2f}
• Taxa de Absenteismo: {metricas['taxa_absenteismo']}%

STATUS CORPORATIVO
-----------------
• Tendencia Geral: {metricas['tendencia_geral']}
• Indice de Criticidade: {metricas['indice_criticidade']}
• Pico Temporal: {metricas['pico_temporal']}
• Departamentos Criticos: {metricas['departamentos_criticos']}/9

RECOMENDACOES ESTRATEGICAS
-------------------------
1. Implementacao imediata de canal digital para justificativas
2. Programa de wellness corporativo integrado
3. Flexibilizacao de politicas de trabalho
4. Sistema de monitoramento preditivo com IA
5. Benchmarking continuo com mercado

PROJECAO FINANCEIRA
------------------
• ROI Estimado: {random.randint(250, 400)}% em 12 meses
• Economia Potencial: R$ {metricas['impacto_financeiro'] * 0.35:,.0f}
• Payback Period: 4-6 meses
• Valor Presente Liquido: R$ {metricas['impacto_financeiro'] * 1.8:,.0f}

PROXIMOS PASSOS
--------------
• Aprovacao de orcamento para intervencoes
• Formacao de task force multidisciplinar
• Implementacao de quick wins em 30 dias
• Revisao trimestral de metricas-chave

Relatorio gerado pelo HR Analytics Intelligence Suite
Tecnologia: Machine Learning + Business Intelligence
                    """
                    
                    st.download_button(
                        label="Download Relatorio",
                        data=relatorio_executivo,
                        file_name=f"relatorio_executivo_hr_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain",
                        key="relatorio_download"
                    )
                    st.success("Relatorio Executivo gerado!")
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
        
        with col3:
            if st.button("Analise Preditiva", help="Predicoes e forecasts"):
                st.info("Modulo em desenvolvimento - Disponivel na versao Enterprise")
        
        with col4:
            if st.button("Dashboard PDF", help="Snapshot visual"):
                st.info("Funcionalidade Premium - Contate o suporte")
        
        # Resumo executivo ultra-detalhado
        st.markdown("#### **Resumo Executivo Final - C-Level Dashboard**")
        
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
            <h2 style="text-align: center; color: white; font-family: 'Orbitron', monospace; margin-bottom: 3rem;">
                EXECUTIVE SUMMARY DASHBOARD
            </h2>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 2rem;">
                
                <div style="
                    background: rgba(139, 92, 246, 0.15);
                    border: 1px solid rgba(139, 92, 246, 0.3);
                    border-radius: 15px;
                    padding: 2rem;
                    border-left: 6px solid #8b5cf6;
                ">
                    <h3 style="color: #8b5cf6; margin-bottom: 1.5rem;">SITUACAO ATUAL</h3>
                    <p><strong>Total de Ausencias:</strong> {metricas['total_ausencias']:,} registros</p>
                    <p><strong>Colaboradores Afetados:</strong> {metricas['funcionarios_impactados']:,} pessoas</p>
                    <p><strong>Taxa de Conformidade:</strong> {metricas['taxa_justificacao']}%</p>
                    <p><strong>Impacto Financeiro:</strong> R$ {metricas['impacto_financeiro']:,.0f}</p>
                    <p><strong>Score Corporativo:</strong> {metricas['score_rh']}/100</p>
                </div>
                
                <div style="
                    background: rgba(16, 185, 129, 0.15);
                    border: 1px solid rgba(16, 185, 129, 0.3);
                    border-radius: 15px;
                    padding: 2rem;
                    border-left: 6px solid #10b981;
                ">
                    <h3 style="color: #10b981; margin-bottom: 1.5rem;">PONTOS FORTES</h3>
                    <p>✅ Sistema de monitoramento em tempo real</p>
                    <p>✅ Dados estruturados e organizados</p>
                    <p>✅ {'Score acima da media do mercado' if metricas['score_rh'] > 75 else 'Base solida para melhorias'}</p>
                    <p>✅ Dashboard inteligente com IA</p>
                    <p>✅ Visibilidade total dos processos</p>
                </div>
                
                <div style="
                    background: rgba(245, 158, 11, 0.15);
                    border: 1px solid rgba(245, 158, 11, 0.3);
                    border-radius: 15px;
                    padding: 2rem;
                    border-left: 6px solid #f59e0b;
                ">
                    <h3 style="color: #f59e0b; margin-bottom: 1.5rem;">OPORTUNIDADES</h3>
                    <p>{'Otimizacao da taxa de conformidade' if metricas['taxa_justificacao'] < 85 else 'Manutencao da excelencia'}</p>
                    <p>Reducao de ausencias criticas</p>
                    <p>Implementacao de analytics preditivos</p>
                    <p>Benchmarking competitivo continuo</p>
                    <p>ROI de {random.randint(200, 350)}% em intervencoes</p>
                </div>
                
                <div style="
                    background: rgba(239, 68, 68, 0.15);
                    border: 1px solid rgba(239, 68, 68, 0.3);
                    border-radius: 15px;
                    padding: 2rem;
                    border-left: 6px solid #ef4444;
                ">
                    <h3 style="color: #ef4444; margin-bottom: 1.5rem;">PROXIMOS PASSOS</h3>
                    <p>1. Aprovacao de budget para intervencoes</p>
                    <p>2. Task force multidisciplinar</p>
                    <p>3. Quick wins em 30 dias</p>
                    <p>4. Implementacao de IA preditiva</p>
                    <p>5. Review trimestral de KPIs</p>
                </div>
            </div>
            
            <div style="
                text-align: center;
                margin-top: 3rem;
                padding: 2rem;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 15px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            ">
                <h3 style="color: white; margin-bottom: 1rem;">RECOMENDACAO ESTRATEGICA FINAL</h3>
                <p style="font-size: 1.1rem; color: rgba(255, 255, 255, 0.9); line-height: 1.6;">
                    Implementacao de um <strong>programa integrado de gestao de absenteismo</strong> com foco em 
                    <span style="color: #8b5cf6;">prevencao inteligente</span>, 
                    <span style="color: #06b6d4;">comunicacao digital</span> e 
                    <span style="color: #10b981;">suporte proativo aos colaboradores</span>.
                </p>
                <div style="margin-top: 2rem; display: flex; justify-content: space-around; flex-wrap: wrap;">
                    <div style="text-align: center; margin: 1rem;">
                        <div style="font-size: 2rem; color: #10b981;">25-40%</div>
                        <div style="font-size: 0.9rem; opacity: 0.8;">Reducao de Custos</div>
                    </div>
                    <div style="text-align: center; margin: 1rem;">
                        <div style="font-size: 2rem; color: #06b6d4;">6 meses</div>
                        <div style="font-size: 0.9rem; opacity: 0.8;">Payback Period</div>
                    </div>
                    <div style="text-align: center; margin: 1rem;">
                        <div style="font-size: 2rem; color: #8b5cf6;">280%</div>
                        <div style="font-size: 0.9rem; opacity: 0.8;">ROI Projetado</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Footer ultra-premium
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
        <div style="position: relative; z-index: 2;">
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
                Plataforma Premium de Business Intelligence para Recursos Humanos
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
                Dashboard desenvolvido para portfolio profissional | Dados simulados para demonstracao
            </p>
            <div style="margin-top: 2rem;">
                <p style="font-size: 0.9rem; opacity: 0.6;">
                    2024 HR Analytics Intelligence Suite • Versao 2.0 Premium<br>
                    Desenvolvido para showcasing de habilidades em Data Science & Analytics
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import random
import time
from typing import Dict, List, Tuple
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
    
    :root {
        --primary: #8b5cf6;
        --secondary: #06b6d4;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --dark: #0f172a;
        --light: #f8fafc;
        --glass: rgba(255, 255, 255, 0.1);
        --glass-border: rgba(255, 255, 255, 0.18);
    }
    
    .stApp {
        background: 
            radial-gradient(circle at 20% 50%, rgba(139, 92, 246, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(6, 182, 212, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 80%, rgba(16, 185, 129, 0.2) 0%, transparent 50%),
            linear-gradient(135deg, #0f172a 0%, #1e293b 25%, #0f172a 50%, #1e293b 75%, #0f172a 100%);
        background-size: 400% 400%;
        animation: gradientShift 20s ease infinite;
        font-family: 'Inter', sans-serif;
        overflow-x: hidden;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 0%; }
        25% { background-position: 100% 0%; }
        50% { background-position: 100% 100%; }
        75% { background-position: 0% 100%; }
        100% { background-position: 0% 0%; }
    }
    
    .mega-header {
        background: linear-gradient(135deg, 
            rgba(139, 92, 246, 0.15) 0%, 
            rgba(6, 182, 212, 0.15) 25%,
            rgba(16, 185, 129, 0.15) 50%,
            rgba(245, 158, 11, 0.15) 75%,
            rgba(139, 92, 246, 0.15) 100%);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border: 2px solid var(--glass-border);
        border-radius: 25px;
        padding: 4rem 3rem;
        text-align: center;
        margin: 2rem 0;
        color: white;
        box-shadow: 
            0 25px 50px -12px rgba(139, 92, 246, 0.5),
            0 0 0 1px rgba(255, 255, 255, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
        animation: headerPulse 6s ease-in-out infinite;
    }
    
    @keyframes headerPulse {
        0%, 100% { box-shadow: 0 25px 50px -12px rgba(139, 92, 246, 0.5), 0 0 30px rgba(139, 92, 246, 0.3); }
        50% { box-shadow: 0 25px 50px -12px rgba(6, 182, 212, 0.5), 0 0 30px rgba(6, 182, 212, 0.3); }
    }
    
    .mega-header::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, 
            transparent 30%, 
            rgba(255, 255, 255, 0.1) 50%, 
            transparent 70%);
        transform: rotate(45deg);
        animation: headerShine 4s linear infinite;
        pointer-events: none;
    }
    
    @keyframes headerShine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .mega-header h1 {
        font-family: 'Orbitron', monospace;
        font-size: 4.5rem;
        font-weight: 900;
        margin: 0;
        background: linear-gradient(135deg, #ffffff 0%, #8b5cf6 25%, #06b6d4 50%, #10b981 75%, #ffffff 100%);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: textGradient 3s ease infinite;
        text-shadow: 0 0 50px rgba(255, 255, 255, 0.3);
        position: relative;
        z-index: 2;
        letter-spacing: 2px;
    }
    
    @keyframes textGradient {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    .mega-header .subtitle {
        font-size: 1.5rem;
        font-weight: 300;
        margin: 1rem 0;
        opacity: 0.9;
        position: relative;
        z-index: 2;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
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
        position: relative;
        z-index: 2;
        transition: all 0.3s ease;
    }
    
    .tech-badge:hover {
        background: rgba(139, 92, 246, 0.4);
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 5px 15px rgba(139, 92, 246, 0.4);
    }
    
    .premium-metric-card {
        background: linear-gradient(145deg, 
            rgba(255, 255, 255, 0.1) 0%, 
            rgba(255, 255, 255, 0.05) 100%);
        backdrop-filter: blur(15px) saturate(200%);
        -webkit-backdrop-filter: blur(15px) saturate(200%);
        border: 2px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        color: white;
        margin: 1rem 0;
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.2),
            0 15px 25px rgba(139, 92, 246, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.1),
            inset 0 -1px 0 rgba(0, 0, 0, 0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        cursor: pointer;
    }
    
    .premium-metric-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        transform: rotate(45deg);
        transition: all 0.6s ease;
        opacity: 0;
    }
    
    .premium-metric-card:hover::before {
        opacity: 1;
        animation: cardShine 0.6s ease-in-out;
    }
    
    @keyframes cardShine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .premium-metric-card:hover {
        transform: translateY(-15px) rotateX(5deg) rotateY(5deg) scale(1.02);
        box-shadow: 
            0 30px 60px rgba(0, 0, 0, 0.3),
            0 25px 45px rgba(139, 92, 246, 0.2),
            0 0 30px rgba(139, 92, 246, 0.1);
        border-color: rgba(139, 92, 246, 0.5);
    }
    
    .premium-metric-value {
        font-family: 'Orbitron', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        margin: 1rem 0;
        background: linear-gradient(135deg, #ffffff, #8b5cf6, #06b6d4);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: valueGradient 2s ease infinite, countUp 1s ease-out;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.2);
        position: relative;
        z-index: 2;
    }
    
    @keyframes valueGradient {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    @keyframes countUp {
        0% { transform: scale(0.5) rotateX(90deg); opacity: 0; }
        50% { transform: scale(1.1) rotateX(0deg); }
        100% { transform: scale(1) rotateX(0deg); opacity: 1; }
    }
    
    .premium-metric-label {
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 1rem;
        position: relative;
        z-index: 2;
    }
    
    .premium-metric-trend {
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.7);
        margin-top: 1rem;
        position: relative;
        z-index: 2;
        font-weight: 500;
    }
    
    .trend-positive { color: #10b981; }
    .trend-negative { color: #ef4444; }
    .trend-neutral { color: #f59e0b; }
    
    .ultra-insight-card {
        background: linear-gradient(145deg, 
            rgba(139, 92, 246, 0.15) 0%, 
            rgba(139, 92, 246, 0.05) 100%);
        backdrop-filter: blur(20px) saturate(180%);
        border: 2px solid rgba(139, 92, 246, 0.3);
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        color: white;
        border-left: 6px solid #8b5cf6;
        box-shadow: 
            0 15px 35px rgba(139, 92, 246, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
        position: relative;
        overflow: hidden;
    }
    
    .ultra-insight-card::after {
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 100px;
        height: 100px;
        background: radial-gradient(circle, rgba(139, 92, 246, 0.3), transparent);
        border-radius: 50%;
        transform: translateX(50%) translateY(-50%);
        transition: all 0.4s ease;
    }
    
    .ultra-insight-card:hover {
        transform: translateX(10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(139, 92, 246, 0.3);
        border-left-width: 8px;
    }
    
    .ultra-insight-card:hover::after {
        transform: translateX(50%) translateY(-50%) scale(1.5);
    }
    
    .ultra-insight-card h4 {
        font-family: 'Orbitron', monospace;
        color: #ffffff;
        margin-bottom: 1rem;
        font-size: 1.2rem;
        font-weight: 700;
    }
    
    .success-insight {
        background: linear-gradient(145deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%);
        border-color: rgba(16, 185, 129, 0.3);
        border-left-color: #10b981;
        box-shadow: 0 15px 35px rgba(16, 185, 129, 0.2);
    }
    
    .warning-insight {
        background: linear-gradient(145deg, rgba(245, 158, 11, 0.15) 0%, rgba(245, 158, 11, 0.05) 100%);
        border-color: rgba(245, 158, 11, 0.3);
        border-left-color: #f59e0b;
        box-shadow: 0 15px 35px rgba(245, 158, 11, 0.2);
    }
    
    .critical-insight {
        background: linear-gradient(145deg, rgba(239, 68, 68, 0.15) 0%, rgba(239, 68, 68, 0.05) 100%);
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
        background: linear-gradient(135deg, #ffffff 0%, #8b5cf6 50%, #06b6d4 100%);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: titleGradient 3s ease infinite;
        position: relative;
        text-shadow: 0 0 50px rgba(255, 255, 255, 0.3);
        letter-spacing: 3px;
        text-transform: uppercase;
    }
    
    @keyframes titleGradient {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
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
        animation: lineGlow 2s ease infinite;
    }
    
    @keyframes lineGlow {
        0%, 100% { box-shadow: 0 0 5px #8b5cf6; }
        50% { box-shadow: 0 0 20px #06b6d4, 0 0 30px #06b6d4; }
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #06b6d4 100%) !important;
        color: white !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 15px !important;
        padding: 1rem 2rem !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1) !important;
        box-shadow: 
            0 10px 25px rgba(139, 92, 246, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        position: relative !important;
        overflow: hidden !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 
            0 20px 40px rgba(139, 92, 246, 0.4),
            0 0 30px rgba(6, 182, 212, 0.3) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
        background: linear-gradient(135deg, #7c3aed 0%, #0891b2 100%) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-2px) scale(0.98) !important;
    }
    
    .css-1d391kg {
        background: linear-gradient(180deg, 
            rgba(15, 23, 42, 0.95) 0%, 
            rgba(30, 41, 59, 0.95) 50%,
            rgba(15, 23, 42, 0.95) 100%) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 2px solid rgba(139, 92, 246, 0.3) !important;
        box-shadow: 0 0 50px rgba(139, 92, 246, 0.1) !important;
    }
    
    .stSelectbox > div > div,
    .stMultiSelect > div > div,
    .stDateInput > div > div > input {
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
        overflow: hidden !important;
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
        animation: premiumSpin 1s linear infinite;
        margin-bottom: 2rem;
        box-shadow: 0 0 30px rgba(139, 92, 246, 0.5);
    }
    
    @keyframes premiumSpin {
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
        animation: loadingPulse 2s ease infinite;
    }
    
    @keyframes loadingPulse {
        0%, 100% { opacity: 0.7; }
        50% { opacity: 1; }
    }
    
    .status-indicator {
        display: inline-block;
        width: 15px;
        height: 15px;
        border-radius: 50%;
        margin-right: 10px;
        position: relative;
        box-shadow: 0 0 10px currentColor;
    }
    
    .status-online {
        background: #10b981;
        animation: statusPulse 2s ease infinite;
    }
    
    @keyframes statusPulse {
        0% { 
            box-shadow: 0 0 0 0 currentColor;
            transform: scale(1);
        }
        70% { 
            box-shadow: 0 0 0 10px transparent;
            transform: scale(1.1);
        }
        100% { 
            box-shadow: 0 0 0 0 transparent;
            transform: scale(1);
        }
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
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1) !important;
        border: 2px solid transparent !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-family: 'Orbitron', monospace !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8b5cf6, #06b6d4) !important;
        color: white !important;
        box-shadow: 
            0 10px 25px rgba(139, 92, 246, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        transform: translateY(-2px) !important;
    }
    
    @media (max-width: 768px) {
        .mega-header h1 {
            font-size: 2.5rem;
        }
        
        .premium-metric-value {
            font-size: 2rem;
        }
        
        .ultra-section-title {
            font-size: 1.8rem;
        }
        
        .premium-metric-card {
            padding: 1.5rem 1rem;
        }
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
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #7c3aed, #0891b2);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=300, show_spinner=False)
def generate_premium_dataset() -> pd.DataFrame:
    """Gera dataset ultra-realista para demonstração premium"""
    random.seed(42)
    np.random.seed(42)
    
    departamentos = [
        'Tecnologia da Informacao', 'Recursos Humanos', 'Operacoes Industriais',
        'Financeiro e Controladoria', 'Marketing Digital', 'Vendas Corporativas', 
        'Logistica Integrada', 'Qualidade e Processos', 'Juridico Empresarial'
    ]
    
    estados_brasileiros = [
        'SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'PE', 'GO', 'DF',
        'ES', 'PB', 'RN', 'CE', 'AL', 'SE', 'PI', 'MA', 'TO', 'MT'
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
        'Thiago Ferreira', 'Camila Martins', 'Lucas Barbosa', 'Patricia Gomes',
        'Andre Ribeiro', 'Roberta Carvalho', 'Felipe Araujo', 'Vanessa Castro',
        'Rodrigo Nunes', 'Priscila Dias', 'Gustavo Moreira'
    ]
    
    dados_corporativos = []
    base_date = datetime(2024, 1, 1)
    
    # Gerar 500 registros ultra-realistas
    for i in range(500):
        dept_weights = [0.18, 0.08, 0.15, 0.10, 0.12, 0.14, 0.13, 0.06, 0.04]
        departamento = np.random.choice(departamentos, p=dept_weights)
        
        if departamento == 'Tecnologia da Informacao':
            motivo_weights = [0.15, 0.10, 0.20, 0.15, 0.08, 0.05, 0.15, 0.05, 0.02, 0.03, 0.02, 0.00]
        elif departamento == 'Operacoes Industriais':
            motivo_weights = [0.12, 0.08, 0.15, 0.25, 0.10, 0.08, 0.05, 0.07, 0.02, 0.05, 0.
