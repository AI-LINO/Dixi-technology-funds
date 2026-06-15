import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# ==========================================
# 1. CONFIGURACIÓN DE LA PÁGINA Y ESTILO (UI)
# ==========================================
st.set_page_config(
    page_title="AI.Lino Pro | Control Estadístico",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inyección de CSS para diseño de alta densidad y estilo industrial
st.markdown("""
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    h1, h2, h3 {font-family: 'Courier New', Courier, monospace; font-weight: 700;}
    div[data-testid="stMetricValue"] {font-size: 2.2rem; font-weight: bold; color: #00FFCC;}
    div[data-testid="stMetricLabel"] {font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;}
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 2. GENERACIÓN DE DATOS DE PRUEBA (SIMULACIÓN AUTOMÁTICA)
# ==========================================
@st.cache_data
def generar_datos_financieros():
    np.random.seed(42)
    fechas = [datetime(2026, 5, 1) + timedelta(days=i/3, hours=np.random.randint(8, 16)) for i in range(90)]
    tickers = ['MU', 'PEÑOLES', 'GFNORTE', 'GMEXICO', 'FSLR']
    
    data = []
    for f in fechas:
        tipo = 'VENTA' if np.random.rand() > 0.4 else 'COMPRA'
        monto = np.random.uniform(5000, 15000)
        # Rendimientos simulados con ligera ventaja matemática (Win Rate ~60%)
        rendimiento = np.random.normal(0.015, 0.04) if tipo == 'VENTA' else 0.0
        
        data.append({
            'fecha_hora': f,
            'dia_semana': f.strftime('%A'),
            'hora': f.hour,
            'ticker': np.random.choice(tickers),
            'tipo': tipo,
            'monto_total': round(monto, 2),
            'rendimiento_op': round(rendimiento * 100, 2) if tipo == 'VENTA' else 0.0
        })
    return pd.DataFrame(data)

df_transacciones = generar_datos_financieros()
df_ventas = df_transacciones[df_transacciones['tipo'] == 'VENTA']

# ==========================================
# 3. HEADER EJECUTIVO
# ==========================================
st.title("AI.LINO PRO ─── FINANCIAL QUANT ENGINE")
st.caption(f"ENTORNO DE VALIDACIÓN ESTADÍSTICA | CORTE OPERATIVO: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
st.hr()

# ==========================================
# 4. CAPA DE MÉTRICAS PRINCIPALES (KPI DE ALTO IMPACTO)
# ==========================================
col1, col2, col3, col4 = st.columns(4)

total_ops = len(df_transacciones)
win_rate = (len(df_ventas[df_ventas['rendimiento_op'] > 0]) / len(df_ventas)) * 100
rendimiento_acumulado = df_ventas['rendimiento_op'].sum()

with col1:
    st.metric(label="Volume / Operaciones Totales", value=f"{total_ops} Exec")
with col2:
    st.metric(label="Win Rate (Eficiencia)", value=f"{win_rate:.1f}%", delta="Target OEE > 60%")
with col3:
    st.metric(label="Net Yield / Rendimiento Acum", value=f"+{rendimiento_acumulado:.2f}%")
with col4:
    # Simulación de la tasa exponencial requerida si hubiera rezago
    st.metric(label="TRR (Tasa Req. Recuperación)", value="0.00%", delta="Estable / En Meta", delta_color="inverse")

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 5. CAPA DE ANÁLISIS HORARIO Y DE FRECUENCIA (HEATMAP & DISTRIBUCIÓN)
# ==========================================
st.subheader("I. ANÁLISIS DE DISCIPLINA Y EFICIENCIA TEMPORAL")

col_graph1, col_graph2 = st.columns([3, 2])

with col_graph1:
    # Crear matriz para el Heatmap: Días de la semana vs Horas
    dias_ordenados = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    heatmap_data = df_ventas.groupby(['dia_semana', 'hora'])['rendimiento_op'].mean().unstack().reindex(dias_ordenados).fillna(0)
    
    fig_heatmap = px.imshow(
        heatmap_data,
        labels=dict(x="Hora del Día", y="Día de la Semana", color="Rendimiento Promedio (%)"),
        x=heatmap_data.columns,
        y=heatmap_data.index,
        color_continuous_scale='Viridis',
        title="Matriz de Rendimiento por Bloque Horario (Filtro Operativo)"
    )
    fig_heatmap.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=40, b=20))
    st.plotly_chart(fig_heatmap, use_container_width=True)

with col_graph2:
    # Gráfico de dispersión para control de volatilidad de rendimientos
    fig_scatter = go.Figure()
    fig_scatter.add_trace(go.Scatter(
        x=df_ventas['fecha_hora'], y=df_ventas['rendimiento_op'],
        mode='markers',
        marker=dict(size=10, color=df_ventas['rendimiento_op'], colorscale='RdYlGn', showscale=False),
        name='Operación'
    ))
    # Líneas de Límites de Control Estadístico (SPC)
    ucl = df_ventas['rendimiento_op'].mean() + (2 * df_ventas['rendimiento_op'].std())
    lcl = df_ventas['rendimiento_op'].mean() - (2 * df_ventas['rendimiento_op'].std())
    
    fig_scatter.add_hline(y=ucl, line_dash="dash", line_color="red", annotation_text="Límite Control Sup (UCL)")
    fig_scatter.add_hline(y=lcl, line_dash="dash", line_color="red", annotation_text="Límite Control Inf (LCL)")
    
    fig_scatter.update_layout(
        title="Estabilidad de Rendimientos (Límites Estadísticos)",
        template="plotly_dark",
        margin=dict(l=20, r=20, t=40, b=20)
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ==========================================
# 6. CAPA DE SEGUIMIENTO EXPOENCIAL DE METAS
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("II. TERMÓMETRO DE CRECIMIENTO EXPONENCIAL Y AHORRO")

# Generar curvas de crecimiento (Real vs Meta Teórica)
df_ventas = df_ventas.sort_values('fecha_hora').reset_index()
df_ventas['balance_real'] = 50000 + (df_ventas['rendimiento_op'].cumsum() * 500) # Capital inicial base sim
df_ventas['balance_meta_teorica'] = [50000 * (1 + 0.0035)**i for i in range(len(df_ventas))] # Crecimiento meta constante

fig_meta = go.Figure()
fig_meta.add_trace(go.Scatter(
    x=df_ventas['fecha_hora'], y=df_ventas['balance_meta_teorica'],
    mode='lines', line=dict(color='gray', width=2, dash='dash'), name='Curva Proyectada (Meta Ene 2028)'
))
fig_meta.add_trace(go.Scatter(
    x=df_ventas['fecha_hora'], y=df_ventas['balance_real'],
    mode='lines', fill='tozeroy', line=dict(color='#00FFCC', width=3), name='Evolución de Capital Real (AI.Lino)'
))

fig_meta.update_layout(
    title="Análisis de Desviación Acumulada vs Trayectoria Teórica",
    template="plotly_dark",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=20, r=20, t=40, b=20)
)
st.plotly_chart(fig_meta, use_container_width=True)

# Mensaje analítico automatizado de diagnóstico de brecha
ultimo_real = df_ventas['balance_real'].iloc[-1]
ultimo_meta = df_ventas['balance_meta_teorica'].iloc[-1]
diferencia = ultimo_real - ultimo_meta

st.markdown("### 🔍 DIAGNÓSTICO DEL MOTOR CUÁNTICO")
if diferencia >= 0:
    st.success(f"**SUPERÁVIT OPERATIVO:** El portafolio actual se encuentra un **{((diferencia/ultimo_meta)*100):.2f}%** por encima de la trayectoria requerida. La eficiencia actual valida la estabilidad del modelo de ejecución manual.")
else:
    st.warning(f"**DESVIACIÓN DETECTADA:** Brecha de **${abs(diferencia):,.2f} MXN** respecto a la curva teórica. Para romper el techo de la meta actual sin alterar el nivel de riesgo, el sistema sugiere un incremento de aportación de capital semanal o una optimización del filtro de paros/señales.")
