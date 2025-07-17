import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Dashboard de Análise de Faltas de RH")
st.markdown("--- ")

@st.cache_data
def load_data():
    # O arquivo CSV deve estar no mesmo diretório da aplicação Streamlit
    df = pd.read_csv("base_colaboradores_rh_tratada.csv")
    df["Data da Falta"] = pd.to_datetime(df["Data da Falta"])
    df["Data de Admissão"] = pd.to_datetime(df["Data de Admissão"])
    return df

df = load_data()

# Sidebar para filtros
st.sidebar.header("Filtros")

departamento_selecionado = st.sidebar.multiselect(
    "Selecione o Departamento:",
    options=df["Departamento"].unique(),
    default=df["Departamento"].unique()
)

motivo_selecionado = st.sidebar.multiselect(
    "Selecione o Motivo da Falta:",
    options=df["Motivo"].unique(),
    default=df["Motivo"].unique()
)

genero_selecionado = st.sidebar.multiselect(
    "Selecione o Gênero:",
    options=df["Gênero"].unique(),
    default=df["Gênero"].unique()
)

df_filtered = df[
    (df["Departamento"].isin(departamento_selecionado)) &
    (df["Motivo"].isin(motivo_selecionado)) &
    (df["Gênero"].isin(genero_selecionado))
]

# Cards de Métricas
st.subheader("Métricas Principais")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Total de Faltas", value=df_filtered.shape[0])

with col2:
    faltas_justificadas = df_filtered[df_filtered["Justificada"] == "Sim"].shape[0]
    st.metric(label="Faltas Justificadas", value=faltas_justificadas)

with col3:
    faltas_nao_justificadas = df_filtered[df_filtered["Justificada"] == "Não"].shape[0]
    st.metric(label="Faltas Não Justificadas", value=faltas_nao_justificadas)

with col4:
    st.metric(label="Departamentos Ativos", value=df_filtered["Departamento"].nunique())

st.markdown("--- ")

# Gráficos
st.subheader("Visualizações")

# Definindo uma paleta de cores vibrantes e futuristas
colors_futuristic = ["#00FFFF", "#FF00FF", "#FFFF00", "#00FF00", "#FF69B4", "#8A2BE2", "#00BFFF", "#FFD700"]

# Função para aplicar o layout futurista aos gráficos
def apply_futuristic_layout(fig, title_text):
    fig.update_layout(
        title_text=f"<span style=\"color:#00FFFF;\">{title_text}</span>",
        plot_bgcolor=\'rgba(0,0,0,0)\\' ,
        paper_bgcolor=\'rgba(0,0,0,0)\\' ,
        font=dict(color="#E0FFFF"),
        hoverlabel=dict(bgcolor="#1A1A1A", font_color="#E0FFFF"),
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color="#E0FFFF"), title_font_color="#00FFFF"),
        yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color="#E0FFFF"), title_font_color="#00FFFF"),
        legend=dict(font=dict(color="#E0FFFF"), bgcolor=\'rgba(0,0,0,0)\\' ),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    return fig

# 1. Faltas por Departamento
faltas_departamento = df_filtered["Departamento"].value_counts().reset_index()
faltas_departamento.columns = ["Departamento", "Número de Faltas"]
fig_dept = px.bar(faltas_departamento, x="Departamento", y="Número de Faltas", 
                  color="Departamento", 
                  color_discrete_sequence=colors_futuristic, template="plotly_dark")
fig_dept = apply_futuristic_layout(fig_dept, "Número de Faltas por Departamento")
fig_dept.update_xaxes(showgrid=False)
fig_dept.update_yaxes(showgrid=False)
st.plotly_chart(fig_dept, use_container_width=True)

# 2. Faltas por Motivo
faltas_motivo = df_filtered["Motivo"].value_counts().reset_index()
faltas_motivo.columns = ["Motivo", "Número de Faltas"]
fig_motivo = px.pie(faltas_motivo, names="Motivo", values="Número de Faltas", 
                    color_discrete_sequence=colors_futuristic, template="plotly_dark")
fig_motivo = apply_futuristic_layout(fig_motivo, "Distribuição de Faltas por Motivo")
fig_motivo.update_traces(textposition=\'inside\", textinfo=\'percent+label\", marker=dict(line=dict(color=\'#0A0A0A\", width=1)))
st.plotly_chart(fig_motivo, use_container_width=True)

# 3. Faltas por Gênero
faltas_genero = df_filtered["Gênero"].value_counts().reset_index()
faltas_genero.columns = ["Gênero", "Número de Faltas"]
fig_genero = px.bar(faltas_genero, x="Gênero", y="Número de Faltas", 
                    color="Gênero", 
                    color_discrete_sequence=colors_futuristic, template="plotly_dark")
fig_genero = apply_futuristic_layout(fig_genero, "Número de Faltas por Gênero")
fig_genero.update_xaxes(showgrid=False)
fig_genero.update_yaxes(showgrid=False)
st.plotly_chart(fig_genero, use_container_width=True)

# 4. Faltas Justificadas vs. Não Justificadas
faltas_justificadas_df = df_filtered["Justificada"].value_counts().reset_index()
faltas_justificadas_df.columns = ["Justificada", "Número de Faltas"]
fig_just = px.bar(faltas_justificadas_df, x="Justificada", y="Número de Faltas", 
                  color="Justificada", 
                  color_discrete_sequence=colors_futuristic, template="plotly_dark")
fig_just = apply_futuristic_layout(fig_just, "Faltas Justificadas vs. Não Justificadas")
fig_just.update_xaxes(showgrid=False)
fig_just.update_yaxes(showgrid=False)
st.plotly_chart(fig_just, use_container_width=True)

# 5. Faltas por Cargo (Top 5)
faltas_cargo = df_filtered["Cargo"].value_counts().nlargest(5).reset_index()
faltas_cargo.columns = ["Cargo", "Número de Faltas"]
fig_cargo = px.bar(faltas_cargo, x="Cargo", y="Número de Faltas", 
                   color="Cargo", 
                   color_discrete_sequence=colors_futuristic, template="plotly_dark")
fig_cargo = apply_futuristic_layout(fig_cargo, "Top 5 Cargos com Mais Faltas")
fig_cargo.update_xaxes(showgrid=False)
fig_cargo.update_yaxes(showgrid=False)
st.plotly_chart(fig_cargo, use_container_width=True)

# Análise de Tendências de Faltas ao Longo do Tempo
st.subheader("Tendência de Faltas ao Longo do Tempo")
df_monthly = df_filtered.set_index("Data da Falta").resample("M").size().reset_index(name="Número de Faltas")
fig_trend = px.line(df_monthly, x="Data da Falta", y="Número de Faltas", 
                    color_discrete_sequence=colors_futuristic, template="plotly_dark")
fig_trend = apply_futuristic_layout(fig_trend, "Faltas Mensais ao Longo do Tempo")
fig_trend.update_xaxes(showgrid=False)
fig_trend.update_yaxes(showgrid=False)
st.plotly_chart(fig_trend, use_container_width=True)

# Comparativo de Faltas entre Diferentes Estados
st.subheader("Comparativo de Faltas por Estado")
faltas_estado = df_filtered["Estado"].value_counts().reset_index()
faltas_estado.columns = ["Estado", "Número de Faltas"]
fig_estado = px.bar(faltas_estado, x="Estado", y="Número de Faltas", 
                    color="Estado", 
                    color_discrete_sequence=colors_futuristic, template="plotly_dark")
fig_estado = apply_futuristic_layout(fig_estado, "Número de Faltas por Estado")
fig_estado.update_xaxes(showgrid=False)
fig_estado.update_yaxes(showgrid=False)
st.plotly_chart(fig_estado, use_container_width=True)

# Correlação entre faltas e cargos/departamentos específicos (Matriz)
st.subheader("Faltas por Departamento e Cargo")
faltas_dept_cargo = df_filtered.groupby(["Departamento", "Cargo"]).size().reset_index(name="Número de Faltas")
fig_heatmap = px.density_heatmap(faltas_dept_cargo, x="Cargo", y="Departamento", z="Número de Faltas", 
                                 color_continuous_scale="Viridis", template="plotly_dark")
fig_heatmap = apply_futuristic_layout(fig_heatmap, "Faltas por Departamento e Cargo")
fig_heatmap.update_xaxes(showgrid=False)
fig_heatmap.update_yaxes(showgrid=False)
st.plotly_chart(fig_heatmap, use_container_width=True)

# Impacto das faltas na produtividade (simulação)
st.subheader("Impacto das Faltas na Produtividade (Simulação)")
st.write("Como não temos dados diretos de produtividade, esta seção apresenta uma simulação baseada na proporção de faltas não justificadas.")

produtividade_impacto = pd.DataFrame({
    "Tipo de Falta": ["Justificada", "Não Justificada"],
    "Impacto na Produtividade": ["Baixo", "Alto"]
})

fig_prod = px.bar(produtividade_impacto, x="Tipo de Falta", y="Impacto na Produtividade", 
                  color="Tipo de Falta",
                  color_discrete_map={"Justificada": "#00FF00", "Não Justificada": "#FF00FF"}, template="plotly_dark")
fig_prod = apply_futuristic_layout(fig_prod, "Impacto Simulado das Faltas na Produtividade")
fig_prod.update_xaxes(showgrid=False)
fig_prod.update_yaxes(showgrid=False)
st.plotly_chart(fig_prod, use_container_width=True)

st.write("**Observação:** Para uma análise real do impacto na produtividade, seria necessário integrar dados de desempenho ou produção dos colaboradores.")
