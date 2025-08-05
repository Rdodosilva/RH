import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta
import random

# Configuração da página
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# CSS minimal - SEM conflitos JavaScript
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1e293b, #3730a3, #1e293b);
    }
    
    .main-title {
        background: linear-gradient(90deg, #8b5cf6, #06b6d4);
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        color: white;
    }
    
    .metric-card {
        background: rgba(139, 92, 246, 0.2);
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        color: white;
        margin: 0.5rem 0;
    }
    
    .insight-box {
        background: rgba(6, 182, 212, 0.15);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 3px solid #06b6d4;
        color: white;
    }
    
    .success-box {
        border-left-color: #10b981;
        background: rgba(16, 185, 129, 0.15);
    }
    
    .warning-box {
        border-left-color: #f59e0b;
        background: rgba(245, 158, 11, 0.15);
    }
    
    /* Remover elementos do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Gera dados simulados"""
    random.seed(42)
    np.random.seed(42)
    
    departamentos = ['RH', 'TI', 'Operações', 'Financeiro', 'Marketing', 'Comercial', 'Logística']
    estados = ['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'PE']
    motivos = ['Família', 'Doença', 'Pessoal', 'Médico', 'Transporte', 'Sem justificativa']
    
    data = []
    for i in range(200):
        data.append({
            'Nome': f'Funcionário {i+1:03d}',
            'Departamento': random.choice(departamentos),
            'Estado': random.choice(estados),
            'Motivo': random.choice(motivos),
            'Justificada': random.choice(['Sim', 'Não']),
            'Genero': random.choice(['M', 'F']),
            'Data_Falta': datetime(2024, 1, 1) + timedelta(days=random.randint(0, 300)),
            'Mes': random.choice(['Jan/24', 'Fev/24', 'Mar/24', 'Abr/24', 'Mai/24', 'Jun/24'])
        })
    
    return pd.DataFrame(data)

def calculate_metrics(df):
    """Calcula métricas básicas"""
    total = len(df)
    justificadas = len(df[df['Justificada'] == 'Sim'])
    funcionarios = df['Nome'].nunique()
    departamentos = df['Departamento'].nunique()
    taxa = round((justificadas / total * 100), 1) if total > 0 else 0
    
    return {
        'total': total,
        'justificadas': justificadas,
        'funcionarios': funcionarios,
        'departamentos': departamentos,
        'taxa': taxa
    }

def main():
    # Header
    st.markdown("""
    <div class="main-title">
        <h1>📊 HR Analytics Dashboard</h1>
        <p>Análise de Absenteísmo Corporativo</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregar dados
    df = load_data()
    st.success(f"✅ {len(df)} registros carregados com sucesso!")
    
    # Sidebar
    st.sidebar.header("🔍 Filtros")
    
    deps_selecionados = st.sidebar.multiselect(
        "Departamentos",
        options=df['Departamento'].unique(),
        default=df['Departamento'].unique()
    )
    
    motivos_selecionados = st.sidebar.multiselect(
        "Motivos",
        options=df['Motivo'].unique(),
        default=df['Motivo'].unique()
    )
    
    # Aplicar filtros
    df_filtrado = df[
        (df['Departamento'].isin(deps_selecionados)) &
        (df['Motivo'].isin(motivos_selecionados))
    ]
    
    if len(df_filtrado) == 0:
        st.warning("Nenhum dado encontrado com os filtros aplicados.")
        return
    
    # Métricas
    metricas = calculate_metrics(df_filtrado)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "🏢 Departamentos", "📈 Tendências", "📋 Relatórios"])
    
    with tab1:
        st.header("📊 Métricas Principais")
        
        # Cards de métricas
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{metricas['total']}</h3>
                <p>Total de Faltas</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{metricas['funcionarios']}</h3>
                <p>Funcionários</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{metricas['taxa']}%</h3>
                <p>Taxa Justificação</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{metricas['departamentos']}</h3>
                <p>Departamentos</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Faltas por Departamento")
            dept_counts = df_filtrado['Departamento'].value_counts()
            
            fig = px.bar(
                x=dept_counts.values,
                y=dept_counts.index,
                orientation='h',
                color_discrete_sequence=['#8b5cf6']
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🎯 Motivos das Faltas")
            motivo_counts = df_filtrado['Motivo'].value_counts()
            
            fig2 = px.pie(
                values=motivo_counts.values,
                names=motivo_counts.index,
                color_discrete_sequence=['#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ef4444', '#8b5a2b']
            )
            fig2.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white',
                showlegend=True
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        # Insights
        st.subheader("💡 Principais Insights")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            dept_top = dept_counts.index[0] if len(dept_counts) > 0 else "N/A"
            st.markdown(f"""
            <div class="insight-box">
                <h4>🏢 Departamento Crítico</h4>
                <p><strong>{dept_top}</strong></p>
                <p>Maior número de faltas</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            motivo_top = motivo_counts.index[0] if len(motivo_counts) > 0 else "N/A"
            st.markdown(f"""
            <div class="insight-box success-box">
                <h4>📝 Motivo Principal</h4>
                <p><strong>{motivo_top}</strong></p>
                <p>Causa mais comum</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            status = "Boa" if metricas['taxa'] > 70 else "Crítica"
            st.markdown(f"""
            <div class="insight-box warning-box">
                <h4>✅ Taxa Justificação</h4>
                <p><strong>{status}</strong></p>
                <p>{metricas['taxa']}% das faltas</p>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:
        st.header("🏢 Análise Departamental")
        
        # Gráfico por gênero
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👥 Análise por Gênero")
            genero_counts = df_filtrado['Genero'].value_counts()
            
            fig3 = px.bar(
                x=['Masculino' if x == 'M' else 'Feminino' for x in genero_counts.index],
                y=genero_counts.values,
                color_discrete_sequence=['#06b6d4']
            )
            fig3.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            st.subheader("📊 Justificação por Departamento")
            
            # Criar dados para o gráfico
            dept_just = df_filtrado.groupby(['Departamento', 'Justificada']).size().reset_index(name='count')
            
            fig4 = px.bar(
                dept_just,
                x='Departamento',
                y='count',
                color='Justificada',
                color_discrete_map={'Sim': '#10b981', 'Não': '#ef4444'}
            )
            fig4.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font_color='white'
            )
            st.plotly_chart(fig4, use_container_width=True)
        
        # Tabela resumo
        st.subheader("📋 Resumo por Departamento")
        
        summary = df_filtrado.groupby('Departamento').agg({
            'Nome': 'count',
            'Justificada': lambda x: (x == 'Sim').sum()
        }).reset_index()
        
        summary.columns = ['Departamento', 'Total_Faltas', 'Justificadas']
        summary['Taxa_Justificacao'] = round((summary['Justificadas'] / summary['Total_Faltas'] * 100), 1)
        
        st.dataframe(summary, use_container_width=True)
    
    with tab3:
        st.header("📈 Análise de Tendências")
        
        # Tendência mensal
        monthly = df_filtrado['Mes'].value_counts().sort_index()
        
        st.subheader("📊 Faltas por Mês")
        
        fig5 = px.line(
            x=monthly.index,
            y=monthly.values,
            markers=True
        )
        fig5.update_traces(line_color='#8b5cf6', marker_color='#06b6d4')
        fig5.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig5, use_container_width=True)
        
        # Estados
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🗺️ Por Estados")
            estado_counts = df_filtrado['Estado'].value_counts()
