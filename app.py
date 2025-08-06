<h3 style="color: #ef4444; margin-bottom: 1.5rem;">🚀 PRÓXIMOS PASSOS</h3>
                    <p>1. Aprovação de budget para intervenções</p>
                    <p>2. Task force multidisciplinar</p>
                    <p>3. Quick wins em 30 dias</p>
                    <p>4. Implementação de IA preditiva</p>
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
                <h3 style="color: white; margin-bottom: 1rem;">💡 RECOMENDAÇÃO ESTRATÉGICA FINAL</h3>
                <p style="font-size: 1.1rem; color: rgba(255, 255, 255, 0.9); line-height: 1.6;">
                    Implementação de um <strong>programa integrado de gestão de absenteísmo</strong> com foco em 
                    <span style="color: #8b5cf6;">prevenção inteligente</span>, 
                    <span style="color: #06b6d4;">comunicação digital</span> e 
                    <span style="color: #10b981;">suporte proativo aos colaboradores</span>.
                </p>
                <div style="margin-top: 2rem; display: flex; justify-content: space-around; flex-wrap: wrap;">
                    <div style="text-align: center; margin: 1rem;">
                        <div style="font-size: 2rem; color: #10b981;">25-40%</div>
                        <div style="font-size: 0.9rem; opacity: 0.8;">Redução de Custos</div>
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
        
        # Análise competitiva final
        st.markdown("#### 🏆 **Posicionamento Competitivo & Market Intelligence**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Quadrante estratégico
            quadrante_data = {
                'Empresa': ['Nossa Empresa', 'Concorrente A', 'Concorrente B', 'Concorrente C', 'Líder Mercado'],
                'Performance_HR': [metricas['score_rh'], 78, 65, 82, 94],
                'Inovacao_Tech': [85, 70, 60, 75, 95],
                'Tamanho': [15, 12, 8, 14, 20]
            }
            
            fig_quadrante = px.scatter(
                quadrante_data,
                x='Performance_HR',
                y='Inovacao_Tech',
                size='Tamanho',
                color='Empresa',
                title="Matriz de Posicionamento Competitivo",
                labels={'Performance_HR': 'Performance RH', 'Inovacao_Tech': 'Inovação Tecnológica'},
                color_discrete_sequence=['#8b5cf6', '#f59e0b', '#ef4444', '#06b6d4', '#10b981']
            )
            
            # Adicionar quadrantes
            fig_quadrante.add_hline(y=80, line_dash="dash", line_color="rgba(255,255,255,0.3)")
            fig_quadrante.add_vline(x=80, line_dash="dash", line_color="rgba(255,255,255,0.3)")
            
            # Adicionar anotações dos quadrantes
            fig_quadrante.add_annotation(x=90, y=90, text="LÍDERES", showarrow=False, font=dict(color="white", size=14))
            fig_quadrante.add_annotation(x=70, y=90, text="INOVADORES", showarrow=False, font=dict(color="white", size=14))
            fig_quadrante.add_annotation(x=90, y=70, text="ESPECIALISTAS", showarrow=False, font=dict(color="white", size=14))
            fig_quadrante.add_annotation(x=70, y=70, text="EMERGENTES", showarrow=False, font=dict(color="white", size=14))
            
            theme = create_ultra_plotly_theme()
            fig_quadrante.update_layout(**theme['layout'])
            fig_quadrante.update_layout(height=500)
            
            st.plotly_chart(fig_quadrante, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            # Radar comparativo final
            competencias_detalhadas = [
                'Gestão Ausências', 'Conformidade', 'Eficiência Op.', 
                'Inovação Tech', 'Satisfaction', 'Produtividade'
            ]
            
            nossa_performance = [
                100 - metricas['taxa_absenteismo'] * 10,
                metricas['taxa_justificacao'],
                min(100, metricas['score_rh'] + 10),
                85,  # Tech innovation score
                max(60, min(95, metricas['score_rh'] + random.randint(-5, 10))),
                100 - metricas['taxa_absenteismo'] * 15
            ]
            
            benchmark_mercado = [82, 75, 78, 70, 76, 85]
            top_quartil = [95, 89, 92, 88, 90, 94]
            
            fig_radar_final = go.Figure()
            
            fig_radar_final.add_trace(go.Scatterpolar(
                r=nossa_performance,
                theta=competencias_detalhadas,
                fill='toself',
                name='Nossa Performance',
                line=dict(color='#8b5cf6', width=3),
                fillcolor='rgba(139, 92, 246, 0.3)'
            ))
            
            fig_radar_final.add_trace(go.Scatterpolar(
                r=benchmark_mercado,
                theta=competencias_detalhadas,
                fill='toself',
                name='Benchmark Mercado',
                line=dict(color='#f59e0b', width=2, dash='dash'),
                fillcolor='rgba(245, 158, 11, 0.1)'
            ))
            
            fig_radar_final.add_trace(go.Scatterpolar(
                r=top_quartil,
                theta=competencias_detalhadas,
                fill='toself',
                name='Top 25% Mercado',
                line=dict(color='#10b981', width=2, dash='dot'),
                fillcolor='rgba(16, 185, 129, 0.1)'
            ))
            
            theme = create_ultra_plotly_theme()
            fig_radar_final.update_layout(**theme['layout'])
            fig_radar_final.update_layout(
                title="Performance 360° vs Mercado",
                height=500,
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100],
                        gridcolor='rgba(255, 255, 255, 0.2)',
                        tickfont=dict(color='white', size=10)
                    ),
                    angularaxis=dict(
                        gridcolor='rgba(255, 255, 255, 0.2)',
                        tickfont=dict(color='white', size=10)
                    )
                )
            )
            
            st.plotly_chart(fig_radar_final, use_container_width=True, config={'displayModeBar': False})
    
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
                🚀 HR ANALYTICS INTELLIGENCE SUITE
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
                Dashboard desenvolvido para portfólio profissional | Dados simulados para demonstração
            </p>
            <div style="margin-top: 2rem;">
                <p style="font-size: 0.9rem; opacity: 0.6;">
                    © 2024 HR Analytics Intelligence Suite • Versão 2.0 Premium<br>
                    Desenvolvido com 💜 para showcasing de habilidades em Data Science & Analytics
                </p>
            </div>
        </div>
        
        <div style="
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.03) 50%, transparent 70%);
            animation: footerShine 8s linear infinite;
            pointer-events: none;
        "></div>
    </div>
    
    <style>
        @keyframes footerShine {
            0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
            100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
        }
    </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()'].std()
                
                # Predição com intervalos de confiança
                prediction_1m = int(recent_avg * (1 + np.random.normal(0, 0.08)))
                prediction_3m = int(recent_avg * (1 + np.random.normal(0, 0.12)))
                prediction_6m = int(recent_avg * (1 + np.random.normal(0, 0.15)))
                
                confidence_1m = 87  # Simulado
                confidence_3m = 74
                confidence_6m = 63
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="premium-metric-card">
                        <div class="premium-metric-label">🎯 PREDIÇÃO 1 MÊS</div>
                        <div class="premium-metric-value">{prediction_1m}</div>
                        <div class="premium-metric-trend">
                            Confiança IA: {confidence_1m}%<br>
                            Intervalo: {prediction_1m - int(volatility)} - {prediction_1m + int(volatility)}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="premium-metric-card">
                        <div class="premium-metric-label">📊 PREDIÇÃO 3 MESES</div>
                        <div class="premium-metric-value">{prediction_3m}</div>
                        <div class="premium-metric-trend">
                            Confiança IA: {confidence_3m}%<br>
                            Tendência: {metricas['tendencia_geral']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="premium-metric-card">
                        <div class="premium-metric-label">🔮 PREDIÇÃO 6 MESES</div>
                        <div class="premium-metric-value">{prediction_6m}</div>
                        <div class="premium-metric-trend">
                            Confiança IA: {confidence_6m}%<br>
                            Volatilidade: {volatility:.1f}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Análise de risco preditiva
                risk_score = (prediction_1m - recent_avg) / recent_avg * 100 if recent_avg > 0 else 0
                risk_level = "ALTO" if abs(risk_score) > 20 else "MÉDIO" if abs(risk_score) > 10 else "BAIXO"
                risk_color = "critical-insight" if risk_level == "ALTO" else "warning-insight" if risk_level == "MÉDIO" else "success-insight"
                
                st.markdown("#### 🚨 **Análise de Risco Preditiva com IA**")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="ultra-insight-card {risk_color}">
                        <h4>⚡ NÍVEL DE RISCO: {risk_level}</h4>
                        <p><strong>Score de Risco:</strong> {abs(risk_score):.1f}%</p>
                        <p><strong>Direção:</strong> {'Crescente' if risk_score > 0 else 'Decrescente' if risk_score < 0 else 'Estável'}</p>
                        <p>🎯 <strong>Ação:</strong> {'Intervenção imediata' if risk_level == 'ALTO' else 'Monitoramento ativo' if risk_level == 'MÉDIO' else 'Manter estratégia'}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    impacto_financeiro_futuro = prediction_1m * 280
                    economia_potencial = (recent_avg - prediction_1m) * 280 if prediction_1m < recent_avg else 0
                    
                    st.markdown(f"""
                    <div class="ultra-insight-card warning-insight">
                        <h4>💰 IMPACTO FINANCEIRO FUTURO</h4>
                        <p><strong>Projeção 1 Mês:</strong> R$ {impacto_financeiro_futuro:,.0f}</p>
                        <p><strong>{'Economia Potencial:' if economia_potencial > 0 else 'Custo Adicional:'}</strong> R$ {abs(economia_potencial):,.0f}</p>
                        <p>📈 <strong>ROI Esperado:</strong> {25 if risk_level == 'BAIXO' else 35 if risk_level == 'MÉDIO' else 45}% com intervenção</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    # Fatores de risco identificados
                    risk_factors = []
                    
                    if metricas['taxa_justificacao'] < 70:
                        risk_factors.append("Taxa de conformidade baixa")
                    if metricas['ausencias_criticas'] > metricas['total_ausencias'] * 0.2:
                        risk_factors.append("Alto índice de criticidade")
                    if metricas['score_rh'] < 70:
                        risk_factors.append("Score corporativo baixo")
                    
                    if not risk_factors:
                        risk_factors = ["Padrões dentro da normalidade"]
                    
                    st.markdown(f"""
                    <div class="ultra-insight-card ultra-insight-card">
                        <h4>🔍 FATORES DE RISCO IA</h4>
                        {''.join([f'<p>• {factor}</p>' for factor in risk_factors[:3]])}
                        <p>🤖 <strong>Recomendação IA:</strong> {'Plano de contingência' if len([f for f in risk_factors if f != 'Padrões dentro da normalidade']) > 1 else 'Monitoramento padrão'}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        else:
            st.info("📊 **Dados insuficientes** para análise preditiva robusta. Mínimo necessário: 20 registros.")
        
        # Simulação de Machine Learning
        st.markdown("#### 🤖 **Simulador de Machine Learning Avançado**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### 🧠 **Modelo de Classificação de Risco**")
            
            # Simular accuracy do modelo
            model_accuracy = random.uniform(82, 94)
            precision = random.uniform(78, 89)
            recall = random.uniform(75, 87)
            f1_score = (2 * precision * recall) / (precision + recall)
            
            st.markdown(f"""
            <div class="ultra-insight-card success-insight">
                <h4>📊 Performance do Modelo IA</h4>
                <p><strong>Accuracy:</strong> {model_accuracy:.1f}%</p>
                <p><strong>Precision:</strong> {precision:.1f}%</p>
                <p><strong>Recall:</strong> {recall:.1f}%</p>
                <p><strong>F1-Score:</strong> {f1_score:.1f}%</p>
                <p>🎯 <strong>Status:</strong> {'Modelo Otimizado' if model_accuracy > 85 else 'Requer Ajustes'}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("##### 🎯 **Recomendações Estratégicas IA**")
            
            # Gerar recomendações baseadas nos dados
            recomendacoes_ia = []
            
            if metricas['taxa_justificacao'] < 75:
                recomendacoes_ia.append("Implementar canal digital para justificativas")
            if metricas['score_rh'] < 80:
                recomendacoes_ia.append("Programa de wellness corporativo")
            if metricas['taxa_absenteismo'] > 4:
                recomendacoes_ia.append("Flexibilização de horários")
            
            if not recomendacoes_ia:
                recomendacoes_ia = ["Manter estratégias atuais", "Monitoramento preventivo", "Benchmarking contínuo"]
            
            st.markdown(f"""
            <div class="ultra-insight-card warning-insight">
                <h4>🚀 Recomendações Estratégicas</h4>
                {''.join([f'<p>• {rec}</p>' for rec in recomendacoes_ia[:4]])}
                <p>⏱️ <strong>Prazo:</strong> 30-90 dias</p>
                <p>💎 <strong>Prioridade:</strong> {'Alta' if metricas['score_rh'] < 70 else 'Média'}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab5:
        st.markdown('<div class="ultra-section-title">🚀 INTELLIGENCE HUB CORPORATIVO</div>', unsafe_allow_html=True)
        
        # Dashboard de inteligência corporativa
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # KPI de Rotatividade
            funcionarios_novos = len(df_filtrado[df_filtrado['Anos_Empresa'] <= 1]) if len(df_filtrado) > 0 else 0
            taxa_rotatividade = round((funcionarios_novos / metricas['funcionarios_impactados'] * 100), 1) if metricas['funcionarios_impactados'] > 0 else 0
            
            st.markdown(f"""
            <div class="premium-metric-card">
                <div class="premium-metric-label">🔄 ÍNDICE DE ROTATIVIDADE</div>
                <div class="premium-metric-value">{taxa_rotatividade}%</div>
                <div class="premium-metric-trend">
                    {funcionarios_novos} funcionários < 1 ano
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Índice de Satisfação Simulado
            indice_satisfacao = max(0, min(100, metricas['score_rh'] + random.randint(-5, 5)))
            
            st.markdown(f"""
            <div class="premium-metric-card">
                <div class="premium-metric-label">😊 ÍNDICE DE SATISFAÇÃO</div>
                <div class="premium-metric-value">{indice_satisfacao}</div>
                <div class="premium-metric-trend">
                    Baseado em algoritmo IA
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            # Produtividade Estimada
            produtividade = round(100 - (metricas['taxa_absenteismo'] * 2), 1)
            
            st.markdown(f"""
            <div class="premium-metric-card">
                <div class="premium-metric-label">⚡ PRODUTIVIDADE ESTIMADA</div>
                <div class="premium-metric-value">{produtividade}%</div>
                <div class="premium-metric-trend">
                    Correlação inversa com ausências
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # ROI de Intervenções
            roi_estimado = random.randint(180, 320)
            
            st.markdown(f"""
            <div class="premium-metric-card">
                <div class="premium-metric-label">💎 ROI INTERVENÇÕES</div>
                <div class="premium-metric-value">{roi_estimado}%</div>
                <div class="premium-metric-trend">
                    Retorno em 12 meses
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Análise de benchmark de mercado
        st.markdown("#### 📊 **Benchmark de Mercado & Competitividade**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Comparação com mercado
            benchmark_data = {
                'Métrica': ['Taxa Absenteísmo', 'Taxa Conformidade', 'Score RH', 'Produtividade'],
                'Nossa Empresa': [metricas['taxa_absenteismo'], metricas['taxa_justificacao'], metricas['score_rh'], produtividade],
                'Mercado - Q1': [4.2, 72.5, 75.0, 87.3],
                'Top 10%': [2.1, 89.2, 92.5, 96.8]
            }
            
            benchmark_df = pd.DataFrame(benchmark_data)
            
            fig_benchmark = go.Figure()
            
            fig_benchmark.add_trace(go.Scatter(
                x=benchmark_df['Métrica'],
                y=benchmark_df['Nossa Empresa'],
                mode='lines+markers',
                name='Nossa Performance',
                line=dict(color='#8b5cf6', width=4),
                marker=dict(color='#06b6d4', size=12, line=dict(width=2, color='white'))
            ))
            
            fig_benchmark.add_trace(go.Scatter(
                x=benchmark_df['Métrica'],
                y=benchmark_df['Mercado - Q1'],
                mode='lines+markers',
                name='Média Mercado',
                line=dict(color='#f59e0b', width=3, dash='dash'),
                marker=dict(color='#f59e0b', size=10)
            ))
            
            fig_benchmark.add_trace(go.Scatter(
                x=benchmark_df['Métrica'],
                y=benchmark_df['Top 10%'],
                mode='lines+markers',
                name='Top 10% Mercado',
                line=dict(color='#10b981', width=3, dash='dot'),
                marker=dict(color='#10b981', size=10)
            ))
            
            theme = create_ultra_plotly_theme()
            fig_benchmark.update_layout(**theme['layout'])
            fig_benchmark.update_layout(title="Posicionamento Competitivo", height=400)
            
            st.plotly_chart(fig_benchmark, use_container_width=True, config={'displayModeBar': False})
        
        with col2:
            # Radar Chart de Competências
            competencias = ['Gestão Pessoas', 'Conformidade', 'Eficiência', 'Inovação', 'Sustentabilidade']
            scores_empresa = [
                min(100, max(0, 100 - metricas['taxa_absenteismo'] * 10)),
                metricas['taxa_justificacao'],
                produtividade,
                indice_satisfacao,
                metricas['score_rh']
            ]
            
            fig_radar = go.Figure()
            
            fig_radar.add_trace(go.Scatterpolar(
                r=scores_empresa,
                theta=competencias,
                fill='toself',
                name='Nossa Performance',
                line=dict(color='#8b5cf6', width=2),
                fillcolor='rgba(139, 92, 246, 0.2)'
            ))
            
            fig_radar.add_trace(go.Scatterpolar(
                r=[85, 75, 90, 80, 82],  # Benchmark mercado
                theta=competencias,
                fill='toself',
                name='Benchmark Mercado',
                line=dict(color='#06b6d4', width=2, dash='dash'),
                fillcolor='rgba(6, 182, 212, 0.1)'
            ))
            
            theme = create_ultra_plotly_theme()
            fig_radar.update_layout(**theme['layout'])
            fig_radar.update_layout(
                title="Radar de Competências Corporativas",
                height=400,
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100],
                        gridcolor='rgba(255, 255, 255, 0.2)',
                        tickfont=dict(color='white', size=10)
                    ),
                    angularaxis=dict(
                        gridcolor='rgba(255, 255, 255, 0.2)',
                        tickfont=dict(color='white', size=11)
                    )
                )
            )
            
            st.plotly_chart(fig_radar, use_container_width=True, config={'displayModeBar': False})
        
        # Insights estratégicos de inteligência
        st.markdown("#### 🧠 **Insights Estratégicos de Business Intelligence**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            posicionamento = "Líder" if metricas['score_rh'] > 85 else "Competitivo" if metricas['score_rh'] > 70 else "Em Desenvolvimento"
            card_class = "success-insight" if posicionamento == "Líder" else "warning-insight" if posicionamento == "Competitivo" else "critical-insight"
            
            st.markdown(f"""
            <div class="ultra-insight-card {card_class}">
                <h4>🏆 POSICIONAMENTO MERCADO</h4>
                <p><strong>Classificação:</strong> {posicionamento}</p>
                <p><strong>Score Geral:</strong> {metricas['score_rh']}/100</p>
                <p>📊 <strong>Percentil:</strong> {random.randint(65, 92)}º percentil</p>
                <p>🎯 <strong>Gap para liderança:</strong> {max(0, 90 - metricas['score_rh'])} pontos</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            oportunidades = []
            if metricas['taxa_justificacao'] < 80:
                oportunidades.append("Digitalização de processos")
            if metricas['taxa_absenteismo'] > 3:
                oportunidades.append("Programa wellness")
            if indice_satisfacao < 85:
                oportunidades.append("Engagement initiatives")
            
            if not oportunidades:
                oportunidades = ["Otimização contínua", "Inovação incremental"]
            
            st.markdown(f"""
            <div class="ultra-insight-card warning-insight">
                <h4>🚀 OPORTUNIDADES ESTRATÉGICAS</h4>
                {''.join([f'<p>• {op}</p>' for op in oportunidades[:3]])}
                <p>💰 <strong>Potencial ROI:</strong> {random.randint(200, 400)}%</p>
                <p>⏰ <strong>Timeframe:</strong> 6-12 meses</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            riscos = []
            if metricas['taxa_absenteismo'] > 5:
                riscos.append("Alta rotatividade potencial")
            if metricas['score_rh'] < 70:
                riscos.append("Perda de competitividade")
            if taxa_rotatividade > 15:
                riscos.append("Custos de recrutamento")
            
            if not riscos:
                riscos = ["Riscos controlados", "Monitoramento preventivo"]
            
            risk_level = "Alto" if len([r for r in riscos if r not in ["Riscos controlados", "Monitoramento preventivo"]]) > 1 else "Baixo"
            risk_card = "critical-insight" if risk_level == "Alto" else "success-insight"
            
            st.markdown(f"""
            <div class="ultra-insight-card {risk_card}">
                <h4>⚠️ GESTÃO DE RISCOS</h4>
                {''.join([f'<p>• {risco}</p>' for risco in riscos[:3]])}
                <p>🎯 <strong>Nível Geral:</strong> {risk_level}</p>
                <p>🛡️ <strong>Mitigação:</strong> {'Ação imediata' if risk_level == 'Alto' else 'Monitoramento'}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab6:
        st.markdown('<div class="ultra-section-title">📋 EXECUTIVE SUITE & RELATÓRIOS</div>', unsafe_allow_html=True)
        
        # Central de downloads premium
        st.markdown("#### 📥 **Centro de Downloads Executivos**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("📊 **Excel Premium**", help="Dataset completo com análises"):
                try:
                    csv_data = df_filtrado.to_csv(index=False)
                    st.download_button(
                        label="⬇️ Download Excel",
                        data=csv_data,
                        file_name=f"hr_analytics_premium_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                        mime="text/csv",
                        key="excel_download"
                    )
                    st.success("✅ **Excel Premium gerado com sucesso!**")
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
        
        with col2:
            if st.button("📈 **Relatório Executivo**", help="Sumário para C-Level"):
                try:
                    relatorio_executivo = f"""
🚀 RELATÓRIO EXECUTIVO HR ANALYTICS INTELLIGENCE SUITE
===================================================

📅 PERÍODO DE ANÁLISE: {data_inicio.strftime('%d/%m/%Y')} - {data_fim.strftime('%d/%m/%Y')}
🕐 GERADO EM: {datetime.now().strftime('%d/%m/%Y às %H:%M')}

📊 MÉTRICAS PRINCIPAIS
─────────────────────
• Total de Ausências: {metricas['total_ausencias']:,}
• Colaboradores Impactados: {metricas['funcionarios_impactados']:,}
• Taxa de Conformidade: {metricas['taxa_justificacao']}%
• Score Corporativo: {metricas['score_rh']}/100
• Impacto Financeiro: R$ {metricas['impacto_financeiro']:,.2f}
• Taxa de Absenteísmo: {metricas['taxa_absenteismo']}%

🎯 STATUS CORPORATIVO
────────────────────
• Tendência Geral: {metricas['tendencia_geral']}
• Índice de Criticidade: {metricas['indice_criticidade']}
• Pico Temporal: {metricas['pico_temporal']}
• Departamentos Críticos: {metricas['departamentos_criticos']}/9

🚀 RECOMENDAÇÕES ESTRATÉGICAS
───────────────────────────
1. Implementação imediata de canal digital para justificativas
2. Programa de wellness corporativo integrado
3. Flexibilização de políticas de trabalho
4. Sistema de monitoramento preditivo com IA
5. Benchmarking contínuo com mercado

💰 PROJEÇÃO FINANCEIRA
────────────────────
• ROI Estimado: {random.randint(250, 400)}% em 12 meses
• Economia Potencial: R$ {metricas['impacto_financeiro'] * 0.35:,.0f}
• Payback Period: 4-6 meses
• Valor Presente Líquido: R$ {metricas['impacto_financeiro'] * 1.8:,.0f}

🎯 PRÓXIMOS PASSOS
────────────────
• Aprovação de orçamento para intervenções
• Formação de task force multidisciplinar
• Implementação de quick wins em 30 dias
• Revisão trimestral de métricas-chave

═══════════════════════════════════════════════════════
Relatório gerado pelo HR Analytics Intelligence Suite
Tecnologia: Machine Learning + Business Intelligence
Contato: analytics@empresa.com.br
═══════════════════════════════════════════════════════
                    """
                    
                    st.download_button(
                        label="⬇️ Download Relatório",
                        data=relatorio_executivo,
                        file_name=f"relatorio_executivo_hr_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                        mime="text/plain",
                        key="relatorio_download"
                    )
                    st.success("✅ **Relatório Executivo gerado!**")
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
        
        with col3:
            if st.button("🔮 **Análise Preditiva**", help="Predições e forecasts"):
                st.info("🚧 **Módulo em desenvolvimento** - Disponível na versão Enterprise")
        
        with col4:
            if st.button("📊 **Dashboard PDF**", help="Snapshot visual"):
                st.info("🎯 **Funcionalidade Premium** - Contate o suporte")
        
        # Resumo executivo ultra-detalhado
        st.markdown("#### 📊 **Resumo Executivo Final - C-Level Dashboard**")
        
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
                📈 EXECUTIVE SUMMARY DASHBOARD
            </h2>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 2rem;">
                
                <div style="
                    background: rgba(139, 92, 246, 0.15);
                    border: 1px solid rgba(139, 92, 246, 0.3);
                    border-radius: 15px;
                    padding: 2rem;
                    border-left: 6px solid #8b5cf6;
                ">
                    <h3 style="color: #8b5cf6; margin-bottom: 1.5rem;">📊 SITUAÇÃO ATUAL</h3>
                    <p><strong>Total de Ausências:</strong> {metricas['total_ausencias']:,} registros</p>
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
                    <h3 style="color: #10b981; margin-bottom: 1.5rem;">🎯 PONTOS FORTES</h3>
                    <p>✅ Sistema de monitoramento em tempo real</p>
                    <p>✅ Dados estruturados e organizados</p>
                    <p>✅ {'Score acima da média do mercado' if metricas['score_rh'] > 75 else 'Base sólida para melhorias'}</p>
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
                    <h3 style="color: #f59e0b; margin-bottom: 1.5rem;">⚠️ OPORTUNIDADES</h3>
                    <p>🔍 {'Otimização da taxa de conformidade' if metricas['taxa_justificacao'] < 85 else 'Manutenção da excelência'}</p>
                    <p>🔍 Redução de ausências críticas</p>
                    <p>🔍 Implementação de analytics preditivos</p>
                    <p>🔍 Benchmarking competitivo contínuo</p>
                    <p>🔍 ROI de {random.randint(200, 350)}% em intervenções</p>
                </div>
                
                <div style="
                    background: rgba(239, 68, 68, 0.15);
                    border: 1px solid rgba(239, 68, 68, 0.3);
                    border-radius: 15px;
                    padding: 2rem;
                    border-left: 6px solid #ef4444;
                ">
                    <h3 style="color        if nivel_criticidade != 'Todos':
            df_filtrado = df_filtrado[df_filtrado['Criticidade_Ausencia'] == nivel_criticidade]
        
        # Filtro temporal seguro
        try:
            df_filtrado = df_filtrado[
                (df_filtrado['Data_Ausencia'].dt.date >= data_inicio) &
                (df_filtrado['Data_Ausencia'].dt.date <= data_fim)
            ]
        except:
            pass
            
    except Exception as e:
        st.warning(f"⚠️ Ajuste nos filtros aplicado automaticamente: {str(e)}")
        df_filtrado = df.copy()
    
    # Validação de dados pós-filtros
    if len(df_filtrado) == 0:
        st.warning("⚠️ Nenhum registro encontrado com os filtros atuais. Exibindo dataset completo.")
        df_filtrado = df.copy()
    
    # Cálculo de métricas premium
    metricas = calculate_premium_metrics(df_filtrado)
    
    # Sistema de abas ultra-futurístico
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🎯 **COMMAND CENTER**",
        "🏢 **DEPARTAMENTAL AI**", 
        "📊 **ANALYTICS 360°**",
        "🔮 **PREDICTIVE ENGINE**",
        "🚀 **INTELLIGENCE HUB**",
        "📋 **EXECUTIVE SUITE**"
    ])
    
    with tab1:
        st.markdown('<div class="ultra-section-title">🎯 CENTRO DE COMANDO EXECUTIVO</div>', unsafe_allow_html=True)
        
        # Cards de métricas ultra-premium
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            trend_class = "trend-negative" if metricas['total_ausencias'] > 100 else "trend-positive" if metricas['total_ausencias'] < 50 else "trend-neutral"
            st.markdown(f"""
            <div class="premium-metric-card">
                <div class="premium-metric-label">📊 TOTAL DE AUSÊNCIAS</div>
                <div class="premium-metric-value">{metricas['total_ausencias']}</div>
                <div class="premium-metric-trend {trend_class}">
                    {round((metricas['total_ausencias']/len(df)*100), 1)}% do dataset | {metricas['tendencia_geral']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="premium-metric-card">
                <div class="premium-metric-label">👥 COLABORADORES IMPACTADOS</div>
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
                <div class="premium-metric-label">✅ TAXA DE CONFORMIDADE</div>
                <div class="premium-metric-value">{metricas['taxa_justificacao']}%</div>
                <div class="premium-metric-trend {taxa_cor}">
                    {'🟢 Excelente' if metricas['taxa_justificacao'] > 80 else '🔴 Crítica' if metricas['taxa_justificacao'] < 60 else '🟡 Moderada'}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="premium-metric-card">
                <div class="premium-metric-label">💰 IMPACTO FINANCEIRO</div>
                <div class="premium-metric-value">R$ {metricas['impacto_financeiro']:,.0f}</div>
                <div class="premium-metric-trend">
                    R$ {metricas['impacto_financeiro']/metricas['total_ausencias']:,.0f} por ausência
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Segunda linha de métricas avançadas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="premium-metric-card">
                <div class="premium-metric-label">🏢 DEPARTAMENTOS CRÍTICOS</div>
                <div class="premium-metric-value">{metricas['departamentos_criticos']}</div>
                <div class="premium-metric-trend">de 9 departamentos</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            taxa_cor = "trend-positive" if metricas['taxa_absenteismo'] < 3 else "trend-negative" if metricas['taxa_absenteismo'] > 6 else "trend-neutral"
            st.markdown(f"""
            <div class="premium-metric-card">
                <div class="premium-metric-label">📈 TAXA DE ABSENTEÍSMO</div>
                <div class="premium-metric-value">{metricas['taxa_absenteismo']}%</div>
                <div class="premium-metric-trend {taxa_cor}">
                    {'🟢 Baixa' if metricas['taxa_absenteismo'] < 3 else '🔴 Alta' if metricas['taxa_absenteismo'] > 6 else '🟡 Moderada'}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="premium-metric-card">
                <div class="premium-metric-label">📅 PICO TEMPORAL</div>
                <div class="premium-metric-value" style="font-size: 2rem;">{metricas['pico_temporal']}</div>
                <div class="premium-metric-trend">período crítico identificado</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            score_cor = "trend-positive" if metricas['score_rh'] > 80 else "trend-negative" if metricas['score_rh'] < 60 else "trend-neutral"
            st.markdown(f"""
            <div class="premium-metric-card">
                <div class="premium-metric-label">🎯 SCORE CORPORATIVO</div>
                <div class="premium-metric-value">{metricas['score_rh']}</div>
                <div class="premium-metric-trend {score_cor}">
                    {'🏆 Excelente' if metricas['score_rh'] > 80 else '⚠️ Crítico' if metricas['score_rh'] < 60 else '📊 Bom'}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Gráficos principais ultra-avançados
        st.markdown('<div class="ultra-section-title">📊 ANÁLISE VISUAL INTELIGENTE</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                fig_dept = create_advanced_chart(df_filtrado, "departmental_analysis")
                st.plotly_chart(fig_dept, use_container_width=True, config={'displayModeBar': False})
            except Exception as e:
                st.error(f"Erro no gráfico departamental: {str(e)}")
        
        with col2:
            try:
                fig_motivos = create_advanced_chart(df_filtrado, "motivos_premium")
                st.plotly_chart(fig_motivos, use_container_width=True, config={'displayModeBar': False})
            except Exception as e:
                st.error(f"Erro no gráfico de motivos: {str(e)}")
        
        # Timeline avançada
        try:
            fig_timeline = create_advanced_chart(df_filtrado, "timeline_advanced")
            st.plotly_chart(fig_timeline, use_container_width=True, config={'displayModeBar': False})
        except Exception as e:
            st.error(f"Erro na timeline: {str(e)}")
        
        # Insights ultra-inteligentes
        st.markdown('<div class="ultra-section-title">🧠 INSIGHTS DE INTELIGÊNCIA ARTIFICIAL</div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            try:
                dept_counts = df_filtrado['Departamento'].value_counts()
                if len(dept_counts) > 0:
                    dept_top = dept_counts.index[0]
                    dept_valor = dept_counts.iloc[0]
                    dept_perc = round((dept_valor / metricas['total_ausencias'] * 100), 1)
                    
                    card_class = "critical-insight" if dept_perc > 35 else "warning-insight" if dept_perc > 25 else "success-insight"
                    status_emoji = "🚨" if dept_perc > 35 else "⚠️" if dept_perc > 25 else "✅"
                    urgencia = "CRÍTICO" if dept_perc > 35 else "ATENÇÃO" if dept_perc > 25 else "CONTROLADO"
                    
                    st.markdown(f"""
                    <div class="ultra-insight-card {card_class}">
                        <h4>{status_emoji} DEPARTAMENTO CRÍTICO - {urgencia}</h4>
                        <p><strong>{dept_top}</strong> concentra <strong>{dept_valor} ausências</strong> ({dept_perc}% do total)</p>
                        <p>💡 <strong>Recomendação IA:</strong> {'Intervenção imediata com plano de ação 30 dias' if dept_perc > 35 else 'Monitoramento ativo quinzenal' if dept_perc > 25 else 'Manter padrão atual'}</p>
                        <p>💰 <strong>Impacto:</strong> R$ {dept_valor * 280:,.0f} em perdas estimadas</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("Dados insuficientes para análise departamental")
            except Exception as e:
                st.error(f"Erro na análise: {str(e)}")
        
        with col2:
            try:
                motivo_counts = df_filtrado['Motivo_Ausencia'].value_counts()
                if len(motivo_counts) > 0:
                    motivo_top = motivo_counts.index[0]
                    motivo_valor = motivo_counts.iloc[0]
                    motivo_perc = round((motivo_valor / metricas['total_ausencias'] * 100), 1)
                    
                    # Análise inteligente do motivo
                    recomendacoes = {
                        'Consulta Médica': 'Programa de saúde preventiva corporativa',
                        'Atestado Médico': 'Análise de ambiente ocupacional',
                        'Emergência Familiar': 'Flexibilização de horários familiares',
                        'Doença Familiar': 'Apoio psicológico e suporte familiar',
                        'Problemas de Transporte': 'Auxílio transporte ou home office',
                        'Compromissos Pessoais': 'Banco de horas personalizado',
                        'Sem Justificativa': 'Revisão disciplinar e comunicação'
                    }
                    
                    recomendacao = recomendacoes.get(motivo_top, 'Investigação detalhada necessária')
                    card_class = "critical-insight" if motivo_top == 'Sem Justificativa' else "warning-insight" if motivo_perc > 30 else "ultra-insight-card"
                    
                    st.markdown(f"""
                    <div class="ultra-insight-card {card_class}">
                        <h4>🎯 MOTIVO PREDOMINANTE</h4>
                        <p><strong>{motivo_top}</strong> representa <strong>{motivo_valor} casos</strong> ({motivo_perc}% do total)</p>
                        <p>🚀 <strong>Solução IA:</strong> {recomendacao}</p>
                        <p>📈 <strong>Potencial ROI:</strong> {'Alto (25-40%)' if motivo_perc > 25 else 'Médio (15-25%)' if motivo_perc > 15 else 'Baixo (5-15%)'}</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.info("Dados insuficientes para análise de motivos")
            except Exception as e:
                st.error(f"Erro na análise: {str(e)}")
        
        with col3:
            taxa = metricas['taxa_justificacao']
            score = metricas['score_rh']
            
            if score > 85:
                status = "EXCEPCIONAL"
                card_class = "success-insight"
                emoji = "🏆"
                acao = "Manter excelência e replicar boas práticas"
            elif score > 70:
                status = "BOM"
                card_class = "ultra-insight-card"
                emoji = "✅"
                acao = "Pequenos ajustes para otimização"
            elif score > 60:
                status = "MODERADO"
                card_class = "warning-insight"
                emoji = "⚠️"
                acao = "Implementar melhorias estruturais"
            else:
                status = "CRÍTICO"
                card_class = "critical-insight"
                emoji = "🚨"
                acao = "Intervenção imediata necessária"
            
            st.markdown(f"""
            <div class="ultra-insight-card {card_class}">
                <h4>{emoji} SCORE CORPORATIVO - {status}</h4>
                <p><strong>Score Geral:</strong> {score}/100</p>
                <p><strong>Taxa Conformidade:</strong> {taxa}%</p>
                <p>🎯 <strong>Estratégia:</strong> {acao}</p>
                <p>📊 <strong>Benchmark:</strong> {'Acima do mercado' if score > 75 else 'Dentro da média' if score > 60 else 'Abaixo da média'}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="ultra-section-title">🏢 ANÁLISE DEPARTAMENTAL COM IA</div>', unsafe_allow_html=True)
        
        # Análise ultra-avançada departamental
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 👥 **Segmentação por Gênero & Conformidade**")
            try:
                if len(df_filtrado) > 0:
                    genero_data = df_filtrado.groupby(['Genero', 'Status_Justificativa']).size().reset_index(name='count')
                    genero_data['Genero_Label'] = genero_data['Genero'].map({'M': 'Masculino', 'F': 'Feminino'})
                    
                    fig_genero = px.bar(
                        genero_data,
                        x='Genero_Label',
                        y='count',
                        color='Status_Justificativa',
                        title="",
                        color_discrete_map={'Sim': '#10b981', 'Não': '#ef4444'},
                        text='count',
                        barmode='group'
                    )
                    
                    theme = create_ultra_plotly_theme()
                    fig_genero.update_layout(**theme['layout'])
                    fig_genero.update_traces(
                        texttemplate='%{text}',
                        textposition='outside',
                        textfont=dict(color='white', size=12),
                        hovertemplate='<b>%{x}</b><br>%{fullData.name}: %{y}<br>Impacto: R$ %{customdata:,.0f}<extra></extra>',
                        customdata=genero_data['count'] * 280
                    )
                    fig_genero.update_layout(height=400)
                    
                    st.plotly_chart(fig_genero, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.info("Dados insuficientes")
            except Exception as e:
                st.error(f"Erro: {str(e)}")
        
        with col2:
            st.markdown("#### ⏰ **Distribuição por Experiência Corporativa**")
            try:
                if len(df_filtrado) > 0:
                    exp_data = df_filtrado.copy()
                    exp_data['Faixa_Experiencia'] = pd.cut(
                        exp_data['Anos_Empresa'],
                        bins=[-1, 1, 3, 5, 10, 50],
                        labels=['0-1 anos', '1-3 anos', '3-5 anos', '5-10 anos', '10+ anos']
                    )
                    
                    exp_counts = exp_data['Faixa_Experiencia'].value_counts().sort_index()
                    
                    fig_exp = px.bar(
                        x=exp_counts.index.astype(str),
                        y=exp_counts.values,
                        title="",
                        color=exp_counts.values,
                        color_continuous_scale=['#ef4444', '#f59e0b', '#8b5cf6', '#06b6d4', '#10b981'],
                        text=exp_counts.values
                    )
                    
                    theme = create_ultra_plotly_theme()
                    fig_exp.update_layout(**theme['layout'])
                    fig_exp.update_traces(
                        texttemplate='%{text}',
                        textposition='outside',
                        textfont=dict(color='white', size=12),
                        hovertemplate='<b>%{x}</b><br>Ausências: %{y}<br>Custo: R$ %{customdata:,.0f}<extra></extra>',
                        customdata=exp_counts.values * 280
                    )
                    fig_exp.update_coloraxes(showscale=False)
                    fig_exp.update_layout(height=400)
                    
                    st.plotly_chart(fig_exp, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.info("Dados insuficientes")
            except Exception as e:
                st.error(f"Erro: {str(e)}")
        
        # Heatmap ultra-avançado
        st.markdown("#### 🔥 **Matriz de Calor: Departamentos vs Motivos (IA Enhanced)**")
        try:
            if len(df_filtrado) > 0:
                heatmap_data = pd.crosstab(df_filtrado['Departamento'], df_filtrado['Motivo_Ausencia'])
                
                fig_heatmap = px.imshow(
                    heatmap_data.values,
                    x=heatmap_data.columns,
                    y=heatmap_data.index,
                    color_continuous_scale='Plasma',
                    title="Correlações Identificadas por Machine Learning",
                    aspect='auto',
                    text_auto=True
                )
                
                theme = create_ultra_plotly_theme()
                fig_heatmap.update_layout(**theme['layout'])
                fig_heatmap.update_traces(
                    textfont={"color": "white", "size": 11, "family": "Orbitron"},
                    hovertemplate='<b>%{y}</b> × <b>%{x}</b><br>Correlação: %{z}<br>Impacto: R$ %{customdata:,.0f}<extra></extra>',
                    customdata=heatmap_data.values * 280
                )
                fig_heatmap.update_layout(height=500)
                
                st.plotly_chart(fig_heatmap, use_container_width=True, config={'displayModeBar': False})
            else:
                st.info("Dados insuficientes para matriz de correlação")
        except Exception as e:
            st.error(f"Erro na matriz: {str(e)}")
        
        # Tabela departamental ultra-analítica
        st.markdown("#### 📊 **Dashboard Departamental Executivo**")
        try:
            if len(df_filtrado) > 0:
                dept_analysis = df_filtrado.groupby('Departamento').agg({
                    'Nome_Completo': 'count',
                    'Status_Justificativa': lambda x: (x == 'Sim').sum(),
                    'Salario_Atual': 'mean',
                    'Anos_Empresa': 'mean',
                    'Criticidade_Ausencia': lambda x: (x == 'Alta').sum()
                }).reset_index()
                
                dept_analysis.columns = ['Departamento', 'Total_Ausencias', 'Ausencias_Justificadas', 'Salario_Medio', 'Experiencia_Media', 'Ausencias_Criticas']
                
                dept_analysis['Taxa_Conformidade'] = round((dept_analysis['Ausencias_Justificadas'] / dept_analysis['Total_Ausencias'] * 100), 1)
                dept_analysis['Impacto_Financeiro'] = dept_analysis['Total_Ausencias'] * 280
                dept_analysis['Score_Departamental'] = (
                    (dept_analysis['Taxa_Conformidade'] * 0.4) +
                    (100 - (dept_analysis['Ausencias_Criticas'] / dept_analysis['Total_Ausencias'] * 100) * 0.6)
                ).round(1)
                
                # Classificação inteligente
                def classify_department(row):
                    if row['Score_Departamental'] > 80 and row['Ausencias_Criticas'] < 3:
                        return '🟢 Excelente'
                    elif row['Score_Departamental'] > 65 and row['Ausencias_Criticas'] < 5:
                        return '🟡 Boa'
                    else:
                        return '🔴 Crítica'
                
                dept_analysis['Status_IA'] = dept_analysis.apply(classify_department, axis=1)
                dept_analysis['Prioridade'] = dept_analysis['Impacto_Financeiro'].rank(ascending=False, method='min').astype(int)
                
                # Ordenar por impacto
                dept_analysis = dept_analysis.sort_values('Impacto_Financeiro', ascending=False)
                
                st.dataframe(
                    dept_analysis,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Departamento": st.column_config.TextColumn("🏢 Departamento", width="large"),
                        "Total_Ausencias": st.column_config.NumberColumn("📊 Ausências", width="small"),
                        "Taxa_Conformidade": st.column_config.NumberColumn("✅ Conformidade (%)", format="%.1f", width="medium"),
                        "Salario_Medio": st.column_config.NumberColumn("💼 Salário Médio", format="R$ %.0f", width="medium"),
                        "Impacto_Financeiro": st.column_config.NumberColumn("💰 Impacto Total", format="R$ %.0f", width="large"),
                        "Score_Departamental": st.column_config.NumberColumn("🎯 Score IA", format="%.1f", width="small"),
                        "Status_IA": st.column_config.TextColumn("🤖 Status IA", width="medium"),
                        "Prioridade": st.column_config.NumberColumn("⚡ Prioridade", width="small")
                    }
                )
            else:
                st.info("Dados insuficientes para análise departamental")
        except Exception as e:
            st.error(f"Erro na tabela: {str(e)}")
    
    with tab3:
        st.markdown('<div class="ultra-section-title">📊 ANALYTICS 360° COM MACHINE LEARNING</div>', unsafe_allow_html=True)
        
        # Análise de padrões avançados
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📅 **Padrão Semanal Inteligente**")
            try:
                if len(df_filtrado) > 0:
                    dias_semana = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                    dias_pt = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
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
                        title="Análise Comportamental por Dia da Semana",
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
                        hovertemplate='<b>%{x}</b><br>Ausências: %{y}<br>Impacto: R$ %{customdata:,.0f}<extra></extra>',
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
            st.markdown("#### 🗺️ **Distribuição Geográfica Nacional**")
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
                        hovertemplate='<b>%{x}</b><br>Ausências: %{y}<br>Custo: R$ %{customdata:,.0f}<extra></extra>',
                        customdata=estado_counts.values * 280
                    )
                    fig_estado.update_coloraxes(showscale=False)
                    fig_estado.update_layout(height=400)
                    
                    st.plotly_chart(fig_estado, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.info("Dados insuficientes")
            except Exception as e:
                st.error(f"Erro: {str(e)}")
        
        # Análise de correlação ultra-avançada
        st.markdown("#### 🔗 **Matriz de Correlação Multidimensional**")
        try:
            if len(df_filtrado) > 0:
                fig_corr = create_advanced_chart(df_filtrado, "correlation_matrix")
                st.plotly_chart(fig_corr, use_container_width=True, config={'displayModeBar': False})
            else:
                st.info("Dados insuficientes para correlação")
        except Exception as e:
            st.error(f"Erro na correlação: {str(e)}")
        
    with tab4:
        st.markdown('<div class="ultra-section-title">🔮 ENGINE PREDITIVO AVANÇADO</div>', unsafe_allow_html=True)
        
        # Simulação de IA preditiva avançada
        if len(df_filtrado) >= 20:
            monthly_trend = df_filtrado.groupby('Mes_Nome_BR').size().reset_index(name='Ausencias')
            monthly_trend['Data_Sort'] = pd.to_datetime(monthly_trend['Mes_Nome_BR'], format='%b/%Y')
            monthly_trend = monthly_trend.sort_values('Data_Sort')
            
            if len(monthly_trend) >= 3:
                # Análise preditiva avançada
                recent_avg = monthly_trend['Ausencias'].tail(3).mean()
                volatility = monthly_trend['Ausenciasimport streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import random
import time
import json
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

# 🚀 CONFIGURAÇÃO PREMIUM DA PÁGINA
st.set_page_config(
    page_title="🎯 HR Analytics Intelligence Suite",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-portfolio',
        'Report a bug': "mailto:your-email@domain.com",
        'About': "# HR Analytics Intelligence Suite\nDashboard Premium para Análise Avançada de RH"
    }
)

# 🎨 CSS ULTRA PREMIUM COM ANIMAÇÕES AVANÇADAS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* VARIÁVEIS CSS PARA TEMA DINÂMICO */
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
    
    /* BACKGROUND FUTURÍSTICO ULTRA AVANÇADO */
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
    
    /* HEADER ULTRA FUTURÍSTICO */
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
    
    .mega-header .tech-badge {
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
    
    /* CARDS ULTRA PREMIUM COM EFEITOS 3D */
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
    
    /* INSIGHT CARDS ULTRA FUTURÍSTICOS */
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
    
    /* TÍTULOS DE SEÇÃO ULTRA PREMIUM */
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
    
    /* BOTÕES FUTURÍSTICOS PREMIUM */
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
    
    .stButton > button::before {
        content: '' !important;
        position: absolute !important;
        top: -50% !important;
        left: -50% !important;
        width: 200% !important;
        height: 200% !important;
        background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent) !important;
        transform: rotate(45deg) !important;
        transition: all 0.6s ease !important;
        opacity: 0 !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05) !important;
        box-shadow: 
            0 20px 40px rgba(139, 92, 246, 0.4),
            0 0 30px rgba(6, 182, 212, 0.3) !important;
        border-color: rgba(255, 255, 255, 0.4) !important;
        background: linear-gradient(135deg, #7c3aed 0%, #0891b2 100%) !important;
    }
    
    .stButton > button:hover::before {
        opacity: 1 !important;
        animation: buttonShine 0.6s ease-in-out !important;
    }
    
    @keyframes buttonShine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .stButton > button:active {
        transform: translateY(-2px) scale(0.98) !important;
    }
    
    /* SIDEBAR FUTURÍSTICA */
    .css-1d391kg {
        background: linear-gradient(180deg, 
            rgba(15, 23, 42, 0.95) 0%, 
            rgba(30, 41, 59, 0.95) 50%,
            rgba(15, 23, 42, 0.95) 100%) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 2px solid rgba(139, 92, 246, 0.3) !important;
        box-shadow: 0 0 50px rgba(139, 92, 246, 0.1) !important;
    }
    
    /* FORMULÁRIOS FUTURÍSTICOS */
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
    
    /* TABELA PREMIUM */
    .stDataFrame {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px) !important;
        border-radius: 15px !important;
        border: 2px solid rgba(255, 255, 255, 0.1) !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2) !important;
        overflow: hidden !important;
    }
    
    /* LOADING ULTRA PREMIUM */
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
    
    /* INDICADORES DE STATUS PREMIUM */
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
    
    .status-warning {
        background: #f59e0b;
        animation: statusPulse 2s ease infinite;
    }
    
    .status-critical {
        background: #ef4444;
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
    
    /* TABS ULTRA FUTURÍSTICAS */
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
    
    /* RESPONSIVIDADE PREMIUM */
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
    
    /* ESCONDER ELEMENTOS STREAMLIT */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    header {visibility: hidden;}
    
    /* SCROLLBAR PERSONALIZADA */
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

# 🚀 SISTEMA DE CACHE AVANÇADO
@st.cache_data(ttl=300, show_spinner=False)
def generate_premium_dataset() -> pd.DataFrame:
    """Gera dataset ultra-realista para demonstração premium"""
    random.seed(42)
    np.random.seed(42)
    
    # Dados corporativos realistas
    departamentos = [
        'Tecnologia da Informação', 'Recursos Humanos', 'Operações Industriais',
        'Financeiro e Controladoria', 'Marketing Digital', 'Vendas Corporativas', 
        'Logística Integrada', 'Qualidade e Processos', 'Jurídico Empresarial'
    ]
    
    estados_brasileiros = [
        'SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'PE', 'GO', 'DF',
        'ES', 'PB', 'RN', 'CE', 'AL', 'SE', 'PI', 'MA', 'TO', 'MT'
    ]
    
    motivos_ausencia = [
        'Consulta Médica', 'Doença Familiar', 'Compromissos Pessoais',
        'Atestado Médico', 'Emergência Familiar', 'Problemas de Transporte',
        'Questões de Saúde Mental', 'Acompanhamento Médico', 'Licença Maternidade',
        'Acidente de Trabalho', 'Sem Justificativa', 'Home Office'
    ]
    
    cargos_hierarquia = [
        'Estagiário', 'Assistente', 'Analista Jr', 'Analista Pleno', 
        'Analista Sênior', 'Especialista', 'Coordenador', 'Supervisor',
        'Gerente', 'Gerente Sênior', 'Diretor', 'Vice-Presidente'
    ]
    
    nomes_brasileiros = [
        'Ana Silva', 'João Santos', 'Maria Oliveira', 'Pedro Costa', 'Carla Souza',
        'Bruno Almeida', 'Fernanda Lima', 'Rafael Pereira', 'Juliana Rodrigues',
        'Thiago Ferreira', 'Camila Martins', 'Lucas Barbosa', 'Patrícia Gomes',
        'André Ribeiro', 'Roberta Carvalho', 'Felipe Araújo', 'Vanessa Castro',
        'Rodrigo Nunes', 'Priscila Dias', 'Gustavo Moreira'
    ]
    
    dados_corporativos = []
    base_date = datetime(2024, 1, 1)
    
    # Gerar 500 registros ultra-realistas
    for i in range(500):
        # Distribuição inteligente por departamento (alguns mais críticos)
        dept_weights = [0.18, 0.08, 0.15, 0.10, 0.12, 0.14, 0.13, 0.06, 0.04]
        departamento = np.random.choice(departamentos, p=dept_weights)
        
        # Motivos baseados em realidade corporativa
        if departamento == 'Tecnologia da Informação':
            motivo_weights = [0.15, 0.10, 0.20, 0.15, 0.08, 0.05, 0.15, 0.05, 0.02, 0.03, 0.02, 0.00]
        elif departamento == 'Operações Industriais':
            motivo_weights = [0.12, 0.08, 0.15, 0.25, 0.10, 0.08, 0.05, 0.07, 0.02, 0.05, 0.03, 0.00]
        else:
            motivo_weights = [0.16, 0.12, 0.18, 0.20, 0.08, 0.06, 0.08, 0.06, 0.02, 0.02, 0.02, 0.00]
        
        motivo = np.random.choice(motivos_ausencia, p=motivo_weights)
        
        # Sistema inteligente de justificação
        justificacao_prob = {
            'Consulta Médica': 0.95, 'Atestado Médico': 0.98, 'Emergência Familiar': 0.85,
            'Doença Familiar': 0.80, 'Acidente de Trabalho': 1.00, 'Licença Maternidade': 1.00,
            'Acompanhamento Médico': 0.90, 'Questões de Saúde Mental': 0.75,
            'Problemas de Transporte': 0.60, 'Compromissos Pessoais': 0.45,
            'Home Office': 0.95, 'Sem Justificativa': 0.00
        }
        
        justificada = 'Sim' if random.random() < justificacao_prob.get(motivo, 0.70) else 'Não'
        
        # Distribuição temporal inteligente (mais faltas em alguns períodos)
        month_weights = [0.12, 0.08, 0.10, 0.09, 0.08, 0.07, 0.06, 0.08, 0.09, 0.10, 0.08, 0.05]  # Dezembro menor
        mes = np.random.choice(range(1, 13), p=month_weights)
        dia = random.randint(1, 28)  # Evitar problemas com dias do mês
        
        data_falta = datetime(2024, mes, dia)
        
        # Hierarquia salarial realista
        cargo = random.choice(cargos_hierarquia)
        salario_base = {
            'Estagiário': (1200, 2000), 'Assistente': (2500, 3500),
            'Analista Jr': (3500, 5500), 'Analista Pleno': (5500, 8000),
            'Analista Sênior': (8000, 12000), 'Especialista': (10000, 15000),
            'Coordenador': (12000, 18000), 'Supervisor': (15000, 22000),
            'Gerente': (18000, 30000), 'Gerente Sênior': (25000, 40000),
            'Diretor': (35000, 60000), 'Vice-Presidente': (50000, 100000)
        }
        
        salario_min, salario_max = salario_base.get(cargo, (3000, 8000))
        salario = random.randint(salario_min, salario_max)
        
        # Gênero e nome correspondente
        genero = random.choice(['M', 'F'])
        nome = f"{random.choice(nomes_brasileiros)} {i+1:03d}"
        
        # Data de admissão realista
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
                                   'Média' if motivo in ['Compromissos Pessoais'] else 'Baixa'
        })
    
    df = pd.DataFrame(dados_corporativos)
    
    # Processamento avançado de dados
    df['Mes_Referencia'] = df['Data_Ausencia'].dt.strftime('%Y-%m')
    df['Mes_Nome_BR'] = df['Data_Ausencia'].dt.strftime('%b/%Y')
    df['Dia_Semana_BR'] = df['Data_Ausencia'].dt.day_name().map({
        'Monday': 'Segunda-feira', 'Tuesday': 'Terça-feira', 'Wednesday': 'Quarta-feira',
        'Thursday': 'Quinta-feira', 'Friday': 'Sexta-feira', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
    })
    df['Trimestre'] = df['Data_Ausencia'].dt.quarter
    df['Semestre'] = df['Data_Ausencia'].dt.month.apply(lambda x: 1 if x <= 6 else 2)
    df['Anos_Empresa'] = ((datetime.now() - df['Data_Admissao']).dt.days / 365).astype(int).clip(0, 50)
    df['Faixa_Salarial'] = pd.cut(df['Salario_Atual'], 
                                  bins=[0, 5000, 10000, 20000, 50000, 100000],
                                  labels=['Até 5k', '5k-10k', '10k-20k', '20k-50k', '50k+'])
    df['Indice_Rotatividade'] = df['Anos_Empresa'].apply(lambda x: 'Alto' if x < 2 else 'Médio' if x < 5 else 'Baixo')
    
    return df

@st.cache_data(ttl=300)
def calculate_premium_metrics(df: pd.DataFrame) -> Dict:
    """Calcula métricas avançadas com KPIs corporativos"""
    if len(df) == 0:
        return {
            'total_ausencias': 0, 'funcionarios_impactados': 0, 'taxa_justificacao': 0,
            'departamentos_criticos': 0, 'impacto_financeiro': 0, 'salario_medio': 0,
            'ausencias_por_funcionario': 0, 'taxa_absenteismo': 0, 'pico_temporal': 'N/A',
            'tendencia_geral': 'Estável', 'indice_criticidade': 'Baixo', 'score_rh': 85
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
                        'Médio' if ausencias_criticas > total_ausencias * 0.15 else 'Baixo'
    
    # Score de RH (0-100)
    score_base = 100
    score_base -= max(0, (taxa_absenteismo - 3) * 5)  # Penalidade por alta taxa
    score_base -= max(0, (100 - taxa_justificacao) * 0.3)  # Penalidade por baixa justificação
    score_base -= ausencias_criticas * 0.5  # Penalidade por criticidade
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
            tendencia_geral = 'Estável'
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
                Processando 500+ registros corporativos com IA avançada
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
            title="🏢 Análise Crítica Departamental",
            color=dept_data.values,
            color_continuous_scale=['#ef4444', '#f59e0b', '#8b5cf6', '#06b6d4', '#10b981']
        )
        
        fig.update_traces(
            hovertemplate='<b>%{y}</b><br>Ausências: %{x}<br>Impacto: R$ %{customdata:,.0f}<extra></extra>',
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
            title="🎯 Distribuição Inteligente de Motivos",
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
            subplot_titles=['📈 Evolução Temporal Inteligente com Predição IA']
        )
        
        # Dados reais
        fig.add_trace(
            go.Scatter(
                x=timeline_data['Mes_Nome_BR'],
                y=timeline_data['Ausencias'],
                mode='lines+markers',
                name='Ausências Reais',
                line=dict(color='#8b5cf6', width=4, shape='spline'),
                marker=dict(
                    color='#06b6d4', 
                    size=12, 
                    line=dict(width=3, color='white'),
                    symbol='circle'
                ),
                hovertemplate='<b>%{x}</b><br>Ausências: %{y}<br>Impacto: R$ %{customdata:,.0f}<extra></extra>',
                customdata=timeline_data['Ausencias'] * 280
            )
        )
        
        # Média móvel
        fig.add_trace(
            go.Scatter(
                x=timeline_data['Mes_Nome_BR'],
                y=timeline_data['Media_Movel'],
                mode='lines',
                name='Tendência (IA)',
                line=dict(color='#10b981', width=3, dash='dash'),
                hovertemplate='<b>%{x}</b><br>Tendência: %{y:.1f}<extra></extra>'
            )
        )
        
        fig.update_layout(**theme['layout'])
        fig.update_layout(height=400)
        
        return fig
    
    elif chart_type == "correlation_matrix":
        # Criar matriz de correlação avançada
        corr_data = df.groupby('Nome_Completo').agg({
            'Salario_Atual': 'first',
            'Anos_Empresa': 'first',
            'Nivel_Hierarquico': 'first',
            'Data_Ausencia': 'count'
        }).reset_index()
        corr_data.columns = ['Nome', 'Salario', 'Anos_Empresa', 'Nivel_Hierarquico', 'Total_Ausencias']
        
        fig = px.scatter(
            corr_data,
            x='Salario',
            y='Total_Ausencias',
            size='Anos_Empresa',
            color='Nivel_Hierarquico',
            title="🔗 Matriz de Correlação Multidimensional",
            color_continuous_scale='Viridis',
            hover_data=['Nome']
        )
        
        fig.update_traces(
            hovertemplate='<b>%{customdata[0]}</b><br>Salário: R$ %{x:,.0f}<br>Ausências: %{y}<br>Anos: %{marker.size}<br>Nível: %{marker.color}<extra></extra>'
        )
        
        fig.update_layout(**theme['layout'])
        fig.update_layout(height=500)
        
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
        <h1>🚀 HR ANALYTICS INTELLIGENCE SUITE</h1>
        <p class="subtitle">Plataforma Avançada de Análise Corporativa com Inteligência Artificial</p>
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
        st.error("❌ Falha crítica no sistema de dados. Contacte o administrador.")
        return
    
    # Notificação de sucesso ultra-premium
    st.success(f"✅ **{len(df)} registros corporativos** processados com sucesso! 🎯 Sistema de IA ativo e otimizado.")
    
    # Sidebar ultra-futurística
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 2rem 0;">
            <h2 style="color: white; font-family: 'Orbitron', monospace; font-size: 1.5rem;">
                🔧 CENTRO DE CONTROLE
            </h2>
            <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">Configure sua análise avançada</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Filtros ultra-avançados
        st.markdown("### 🏢 **Filtros Departamentais**")
        departamentos_selecionados = st.multiselect(
            "Selecione os departamentos para análise:",
            options=sorted(df['Departamento'].unique()),
            default=sorted(df['Departamento'].unique()),
            help="🎯 Filtragem inteligente por departamentos críticos"
        )
        
        st.markdown("### 📝 **Análise de Motivos**")
        motivos_selecionados = st.multiselect(
            "Motivos de ausência para investigação:",
            options=sorted(df['Motivo_Ausencia'].unique()),
            default=sorted(df['Motivo_Ausencia'].unique()),
            help="🔍 Classificação automática por criticidade"
        )
        
        st.markdown("### ✅ **Status de Conformidade**")
        justificacao_filtro = st.selectbox(
            "Análise de justificativas corporativas:",
            options=['Todas', 'Sim', 'Não'],
            help="📊 KPI de conformidade organizacional"
        )
        
        st.markdown("### 👥 **Segmentação Demográfica**")
        genero_filtro = st.selectbox(
            "Análise por gênero:",
            options=['Todos', 'M', 'F'],
            help="📈 Insights de diversidade corporativa"
        )
        
        st.markdown("### 📅 **Período de Análise Premium**")
        try:
            col1, col2 = st.columns(2)
            with col1:
                data_inicio = st.date_input(
                    "Início:",
                    value=df['Data_Ausencia'].min().date(),
                    help="📅 Data inicial da análise"
                )
            with col2:
                data_fim = st.date_input(
                    "Fim:",
                    value=df['Data_Ausencia'].max().date(),
                    help="📅 Data final da análise"
                )
        except:
            data_inicio = datetime.now().date()
            data_fim = datetime.now().date()
        
        st.markdown("### ⚙️ **Configurações Avançadas**")
        
        faixa_salarial = st.select_slider(
            "💰 Faixa Salarial de Interesse:",
            options=['Todas', 'Até 5k', '5k-10k', '10k-20k', '20k-50k', '50k+'],
            value='Todas',
            help="💼 Análise por segmento salarial"
        )
        
        nivel_criticidade = st.selectbox(
            "⚠️ Nível de Criticidade:",
            options=['Todos', 'Alta', 'Média', 'Baixa'],
            help="🚨 Filtro por impacto organizacional"
        )
    
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
        
        if faixa_salarial != 'Todas':
            df_filtrado = df_filtrado[df_filtrado['Faixa_Salarial'] == faixa_salarial]
        
        if nivel_criticidade != '
