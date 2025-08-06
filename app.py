import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
import random
import time
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS com correções para erros de renderização
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e293b, #6d28d9, #1e293b);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        font-family: 'Inter', sans-serif;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-header {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.9), rgba(6, 182, 212, 0.9));
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 20px;
        padding: 2rem 1.5rem;
        text-align: center;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 8px 32px rgba(139, 92, 246, 0.37);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        color: white;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        color: white;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(139, 92, 246, 0.3);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
        color: white;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: rgba(255, 255, 255, 0.8);
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .metric-trend {
        font-size: 0.8rem;
        color: rgba(255, 255, 255, 0.7);
    }
    
    .insight-card {
        background: rgba(139, 92, 246, 0.15);
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        color: white;
        border-left: 4px solid #8b5cf6;
    }
    
    .success-card {
        background: rgba(16, 185, 129, 0.15);
        border-color: rgba(16, 185, 129, 0.3);
        border-left-color: #10b981;
    }
    
    .warning-card {
        background: rgba(245, 158, 11, 0.15);
        border-color: rgba(245, 158, 11, 0.3);
        border-left-color: #f59e0b;
    }
    
    .critical-card {
        background: rgba(239, 68, 68, 0.15);
        border-color: rgba(239, 68, 68, 0.3);
        border-left-color: #ef4444;
    }
    
    .section-title {
        color: white;
        font-size: 1.8rem;
        font-weight: 700;
        text-align: center;
        margin: 2rem 0 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #8b5cf6, #06b6d4) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(139, 92, 246, 0.4) !important;
    }
    
    /* Fix para elementos do Streamlit */
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
    }
    
    .stMultiSelect > div > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
    }
    
    /* Esconder elementos desnecessários */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def generate_safe_data():
    """Gera dados seguros sem erros de tipo"""
    try:
        random.seed(42)
        np.random.seed(42)
        
        departamentos = ['RH', 'TI', 'Operações', 'Financeiro', 'Marketing', 'Comercial', 'Logística']
        estados = ['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA']
        motivos = ['Família', 'Doença', 'Pessoal', 'Médico', 'Falta de transporte', 'Sem justificativa']
        generos = ['M', 'F']
        cargos = ['Analista Jr', 'Analista Pl', 'Analista Sr', 'Coordenador', 'Supervisor', 'Gerente']
        
        data = []
        base_date = datetime(2024, 1, 1)
        
        for i in range(200):
            # Distribuição controlada
            dept = np.random.choice(departamentos)
            motivo = np.random.choice(motivos)
            
            # Justificação baseada no motivo
            if motivo in ['Doença', 'Médico']:
                justificada = 'Sim' if random.random() > 0.2 else 'Não'
            elif motivo == 'Família':
                justificada = 'Sim' if random.random() > 0.3 else 'Não'
            else:
                justificada = 'Sim' if random.random() > 0.5 else 'Não'
            
            # Data aleatória no período
            days_offset = random.randint(0, 330)
            data_falta = base_date + timedelta(days=days_offset)
            
            data.append({
                'Nome': f'Funcionário {i+1:03d}',
                'Cargo': random.choice(cargos),
                'Departamento': dept,
                'Estado': random.choice(estados),
                'Data_Falta': data_falta,
                'Motivo': motivo,
                'Justificada': justificada,
                'Genero': random.choice(generos),
                'Data_Admissao': base_date - timedelta(days=random.randint(30, 1800)),
                'Salario_Estimado': random.randint(3000, 20000)
            })
        
        df = pd.DataFrame(data)
        
        # Processamento seguro
        df['Mes_Ano'] = df['Data_Falta'].dt.strftime('%Y-%m')
        df['Mes_Nome'] = df['Data_Falta'].dt.strftime('%b/%Y')
        df['Dia_Semana'] = df['Data_Falta'].dt.day_name()
        
        # Cálculo seguro do tempo de empresa
        hoje = datetime.now()
        df['Tempo_Empresa_Anos'] = ((hoje - df['Data_Admissao']).dt.days / 365).astype(int)
        df['Tempo_Empresa_Anos'] = df['Tempo_Empresa_Anos'].clip(lower=0, upper=20)
        
        return df
        
    except Exception as e:
        st.error(f"Erro ao gerar dados: {str(e)}")
        return pd.DataFrame()

def calculate_safe_metrics(df):
    """Calcula métricas de forma segura"""
    try:
        if len(df) == 0:
            return {
                'total_faltas': 0,
                'funcionarios_unicos': 0,
                'taxa_justificacao': 0,
                'departamentos_afetados': 0,
                'custo_estimado': 0,
                'media_salarial': 0,
                'faltas_por_funcionario': 0,
                'taxa_absenteismo': 2.5,
                'pico_mensal': 'N/A',
                'tendencia': 'Estável'
            }
        
        total_faltas = len(df)
        funcionarios_unicos = df['Nome'].nunique()
        departamentos_afetados = df['Departamento'].nunique()
        
        # Taxa de justificação segura
        faltas_justificadas = len(df[df['Justificada'] == 'Sim'])
        taxa_justificacao = round((faltas_justificadas / total_faltas * 100), 1) if total_faltas > 0 else 0
        
        # Métricas financeiras
        custo_estimado = total_faltas * 180
        media_salarial = df['Salario_Estimado'].mean()
        
        # Métricas de RH
        faltas_por_funcionario = round(total_faltas / funcionarios_unicos, 2) if funcionarios_unicos > 0 else 0
        taxa_absenteismo = round((total_faltas / (funcionarios_unicos * 22)) * 100, 2) if funcionarios_unicos > 0 else 0
        
        # Análise temporal segura
        if 'Mes_Nome' in df.columns:
            monthly_counts = df['Mes_Nome'].value_counts()
            pico_mensal = monthly_counts.index[0] if len(monthly_counts) > 0 else 'N/A'
        else:
            pico_mensal = 'N/A'
        
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
            'tendencia': 'Estável'
        }
        
    except Exception as e:
        st.error(f"Erro ao calcular métricas: {str(e)}")
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

def create_plotly_theme():
    """Tema simples para gráficos"""
    return {
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'font': {'color': 'white', 'family': 'Inter', 'size': 11},
        'xaxis': {
            'gridcolor': 'rgba(255,255,255,0.1)',
            'linecolor': 'rgba(255,255,255,0.2)',
            'tickcolor': 'rgba(255,255,255,0.2)',
            'tickfont': {'color': 'white', 'size': 10}
        },
        'yaxis': {
            'gridcolor': 'rgba(255,255,255,0.1)',
            'linecolor': 'rgba(255,255,255,0.2)',
            'tickcolor': 'rgba(255,255,255,0.2)',
            'tickfont': {'color': 'white', 'size': 10}
        },
        'legend': {'font': {'color': 'white', 'size': 10}}
    }

def safe_multiselect(label, options, default_all=True, key=None):
    """Multiselect seguro que não gera erros"""
    try:
        if len(options) == 0:
            return []
        
        default = list(options) if default_all else []
        
        return st.multiselect(
            label,
            options=sorted(list(options)),
            default=sorted(default),
            key=key
        )
    except Exception:
        return list(options) if options else []

def main():
    """Função principal com tratamento de erros"""
    try:
        # Header principal
        st.markdown("""
        <div class="main-header">
            <h1>📊 HR Analytics Dashboard</h1>
            <p>Análise de Absenteísmo Corporativo</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Carregar dados com tratamento de erro
        with st.spinner("Carregando dados..."):
            df = generate_safe_data()
        
        if len(df) == 0:
            st.error("❌ Erro ao carregar dados. Tente recarregar a página.")
            return
        
        st.success(f"✅ {len(df)} registros carregados com sucesso!")
        
        # Sidebar com filtros seguros
        with st.sidebar:
            st.markdown("## 🔍 Filtros Avançados")
            
            # Filtros com verificação de dados
            departamentos_selecionados = safe_multiselect(
                "🏢 Departamentos",
                df['Departamento'].unique() if 'Departamento' in df.columns else [],
                key="dept_filter"
            )
            
            motivos_selecionados = safe_multiselect(
                "📝 Motivos das Faltas", 
                df['Motivo'].unique() if 'Motivo' in df.columns else [],
                key="motivo_filter"
            )
            
            justificacao_filtro = st.selectbox(
                "✅ Status de Justificação",
                options=['Todas', 'Sim', 'Não'],
                key="just_filter"
            )
            
            # Filtros de data seguros
            try:
                data_min = df['Data_Falta'].min().date()
                data_max = df['Data_Falta'].max().date()
                
                col1, col2 = st.columns(2)
                with col1:
                    data_inicio = st.date_input("Data Início", value=data_min)
                with col2:
                    data_fim = st.date_input("Data Fim", value=data_max)
            except Exception:
                data_inicio = datetime.now().date()
                data_fim = datetime.now().date()
        
        # Aplicar filtros com segurança
        try:
            df_filtrado = df.copy()
            
            if departamentos_selecionados:
                df_filtrado = df_filtrado[df_filtrado['Departamento'].isin(departamentos_selecionados)]
            
            if motivos_selecionados:
                df_filtrado = df_filtrado[df_filtrado['Motivo'].isin(motivos_selecionados)]
            
            if justificacao_filtro != 'Todas':
                df_filtrado = df_filtrado[df_filtrado['Justificada'] == justificacao_filtro]
            
            # Filtro de data seguro
            try:
                df_filtrado = df_filtrado[
                    (df_filtrado['Data_Falta'].dt.date >= data_inicio) &
                    (df_filtrado['Data_Falta'].dt.date <= data_fim)
                ]
            except Exception:
                pass  # Manter dados originais se filtro de data falhar
            
        except Exception as e:
            st.warning(f"Aviso nos filtros: {str(e)}")
            df_filtrado = df.copy()
        
        # Verificar se há dados após filtros
        if len(df_filtrado) == 0:
            st.warning("⚠️ Nenhum dado encontrado com os filtros aplicados.")
            df_filtrado = df.copy()  # Usar dados originais
        
        # Calcular métricas
        metricas = calculate_safe_metrics(df_filtrado)
        
        # Criar abas
        tab1, tab2, tab3 = st.tabs(["👁️ Visão Geral", "📊 Análise Detalhada", "📋 Relatórios"])
        
        with tab1:
            st.markdown('<div class="section-title">Dashboard Principal</div>', unsafe_allow_html=True)
            
            # Cards de métricas
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">📅 Total de Faltas</div>
                    <div class="metric-value">{metricas['total_faltas']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">👥 Funcionários</div>
                    <div class="metric-value">{metricas['funcionarios_unicos']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">✅ Taxa Justificação</div>
                    <div class="metric-value">{metricas['taxa_justificacao']}%</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">💰 Custo Total</div>
                    <div class="metric-value">R$ {metricas['custo_estimado']:,.0f}</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Gráficos principais
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🏢 Faltas por Departamento")
                try:
                    if 'Departamento' in df_filtrado.columns and len(df_filtrado) > 0:
                        dept_counts = df_filtrado['Departamento'].value_counts()
                        
                        fig_dept = px.bar(
                            x=dept_counts.index,
                            y=dept_counts.values,
                            title="",
                            color_discrete_sequence=['#8b5cf6']
                        )
                        
                        fig_dept.update_layout(**create_plotly_theme())
                        st.plotly_chart(fig_dept, use_container_width=True)
                    else:
                        st.info("Dados insuficientes para o gráfico")
                except Exception as e:
                    st.error(f"Erro no gráfico: {str(e)}")
            
            with col2:
                st.markdown("#### 🎯 Motivos das Faltas")
                try:
                    if 'Motivo' in df_filtrado.columns and len(df_filtrado) > 0:
                        motivo_counts = df_filtrado['Motivo'].value_counts()
                        
                        fig_motivo = px.pie(
                            values=motivo_counts.values,
                            names=motivo_counts.index,
                            title="",
                            color_discrete_sequence=['#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444']
                        )
                        
                        fig_motivo.update_layout(**create_plotly_theme())
                        st.plotly_chart(fig_motivo, use_container_width=True)
                    else:
                        st.info("Dados insuficientes para o gráfico")
                except Exception as e:
                    st.error(f"Erro no gráfico: {str(e)}")
        
        with tab2:
            st.markdown('<div class="section-title">Análise Detalhada</div>', unsafe_allow_html=True)
            
            # Análise por gênero
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 👥 Análise por Gênero")
                try:
                    if 'Genero' in df_filtrado.columns and len(df_filtrado) > 0:
                        genero_counts = df_filtrado['Genero'].value_counts()
                        
                        fig_genero = px.bar(
                            x=['Masculino' if x == 'M' else 'Feminino' for x in genero_counts.index],
                            y=genero_counts.values,
                            title="",
                            color_discrete_sequence=['#06b6d4', '#8b5cf6']
                        )
                        
                        fig_genero.update_layout(**create_plotly_theme())
                        st.plotly_chart(fig_genero, use_container_width=True)
                    else:
                        st.info("Dados insuficientes")
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
            
            with col2:
                st.markdown("#### 📊 Status de Justificação")
                try:
                    if 'Justificada' in df_filtrado.columns and len(df_filtrado) > 0:
                        just_counts = df_filtrado['Justificada'].value_counts()
                        
                        fig_just = px.pie(
                            values=just_counts.values,
                            names=just_counts.index,
                            title="",
                            color_discrete_map={'Sim': '#10b981', 'Não': '#ef4444'}
                        )
                        
                        fig_just.update_layout(**create_plotly_theme())
                        st.plotly_chart(fig_just, use_container_width=True)
                    else:
                        st.info("Dados insuficientes")
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
            
            # Tabela de dados
            st.markdown("#### 📋 Dados Detalhados")
            try:
                if len(df_filtrado) > 0:
                    # Mostrar apenas colunas essenciais
                    colunas_mostrar = ['Nome', 'Departamento', 'Data_Falta', 'Motivo', 'Justificada']
                    colunas_existentes = [col for col in colunas_mostrar if col in df_filtrado.columns]
                    
                    if colunas_existentes:
                        st.dataframe(
                            df_filtrado[colunas_existentes].head(20),
                            use_container_width=True
                        )
                    else:
                        st.info("Colunas não disponíveis")
                else:
                    st.info("Nenhum dado disponível")
            except Exception as e:
                st.error(f"Erro na tabela: {str(e)}")
        
        with tab3:
            st.markdown('<div class="section-title">Relatórios e Insights</div>', unsafe_allow_html=True)
            
            # Insights principais
            col1, col2, col3 = st.columns(3)
            
            with col1:
                try:
                    if len(df_filtrado) > 0 and 'Departamento' in df_filtrado.columns:
                        dept_top = df_filtrado['Departamento'].value_counts().index[0]
                        dept_count = df_filtrado['Departamento'].value_counts().iloc[0]
                        
                        st.markdown(f"""
                        <div class="insight-card warning-card">
                            <h4>🏢 Departamento Crítico</h4>
                            <p><strong>{dept_top}</strong> tem {dept_count} faltas</p>
                            <p>Representa {round(dept_count/len(df_filtrado)*100, 1)}% do total</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info("Dados insuficientes para análise")
                except Exception:
                    st.info("Erro na análise departamental")
            
            with col2:
                try:
                    if len(df_filtrado) > 0 and 'Motivo' in df_filtrado.columns:
                        motivo_top = df_filtrado['Motivo'].value_counts().index[0]
                        motivo_count = df_filtrado['Motivo'].value_counts().iloc[0]
                        
                        st.markdown(f"""
                        <div class="insight-card success-card">
                            <h4>📝 Motivo Principal</h4>
                            <p><strong>{motivo_top}</strong> é o motivo mais comum</p>
                            <p>{motivo_count} ocorrências registradas</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info("Dados insuficientes para análise")
                except Exception:
                    st.info("Erro na análise de motivos")
            
            with col3:
                taxa = metricas['taxa_justificacao']
                status = "Boa" if taxa > 70 else "Crítica" if taxa < 50 else "Moderada"
                card_type = "success-card" if taxa > 70 else "critical-card" if taxa < 50 else "warning-card"
                
                st.markdown(f"""
                <div class="insight-card {card_type}">
                    <h4>✅ Gestão de Justificativas</h4>
                    <p><strong>{taxa}%</strong> das faltas são justificadas</p>
                    <p>Status: <strong>{status}</strong></p>
                </div>
                """, unsafe_allow_html=True)
            
            # Botões de download
            st.markdown("#### 📥 Downloads")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📊 Baixar dados (CSV)", key="download_csv"):
                    try:
                        csv = df_filtrado.to_csv(index=False)
                        st.download_button(
                            label="⬇️ Download CSV",
                            data=csv,
                            file_name=f"hr_dados_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                            mime="text/csv"
                        )
                        st.success("✅ Arquivo preparado para download!")
                    except Exception as e:
                        st.error(f"Erro no download: {str(e)}")
            
            with col2:
                if st.button("📋 Gerar Relatório", key="generate_report"):
                    try:
                        relatorio = f"""
RELATÓRIO HR ANALYTICS
=====================

Período: {data_inicio} a {data_fim}
Total de Faltas: {metricas['total_faltas']}
Funcionários Afetados: {metricas['funcionarios_unicos']}
Taxa de Justificação: {metricas['taxa_justificacao']}%
Custo Estimado: R$ {metricas['custo_estimado']:,.2f}

RECOMENDAÇÕES:
- Foco no departamento com mais faltas
- Melhorar comunicação sobre justificativas
- Implementar ações preventivas

Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}
                        """
                        
                        st.download_button(
                            label="⬇️ Download Relatório",
                            data=relatorio,
                            file_name=f"relatorio_hr_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                            mime="text/plain"
                        )
                        st.success("✅ Relatório gerado com sucesso!")
                    except Exception as e:
                        st.error(f"Erro no relatório: {str(e)}")
    
    except Exception as e:
        st.error(f"❌ Erro geral na aplicação: {str(e)}")
        st.info("🔄 Tente recarregar a página ou verificar os dados.")

if __name__ == "__main__":
    main()
