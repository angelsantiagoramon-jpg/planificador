import streamlit as st
import matplotlib.pyplot as plt
import math

# Configuración de la página responsiva
st.set_page_config(page_title="Planificador PD", layout="centered")

st.title("📊 Planificador Cuantitativo de Indicadores Académicos (PD)")
st.write("Modifica los valores para calcular las brechas y estrategias en tiempo real.")

# --- SECCIÓN 1: DATOS DEL PERSONAL DOCENTE ---
st.header("1. Datos del Personal Docente (Denominador)")
col1, col2, col3 = st.columns(3)
with col1:
    ntc = st.number_input("Profesores TC (NTC):", min_value=0.0, value=10.0, step=1.0)
with col2:
    nmt = st.number_input("Profesores MT (NMT):", min_value=0.0, value=0.0, step=1.0)
with col3:
    ntp = st.number_input("Profesores TP (NTP):", min_value=0.0, value=0.0, step=1.0)

# --- SECCIÓN 2: PUBLICACIONES ACTUALES ---
st.header("2. Publicaciones Actuales (Numerador)")
col4, col5 = st.columns(2)
with col4:
    nlt = st.number_input("Libros de Texto (NLT):", min_value=0.0, value=0.0, step=1.0)
    nf = st.number_input("Folletos Docentes (NF):", min_value=0.0, value=0.0, step=1.0)
with col5:
    ncl = st.number_input("Capítulos de Libros (NCL):", min_value=0.0, value=0.0, step=1.0)
    ng = st.number_input("Guías Publicadas (NG):", min_value=0.0, value=0.0, step=1.0)

# --- SECCIÓN 3: META ---
st.header("3. Configuración de la Meta")
meta = st.number_input("Meta del Indicador (1.0 = 100%):", min_value=0.0, value=1.0, step=0.1)

st.markdown("---")

# --- LÓGICA DE CÁLCULO ---
denominador = ntc + (0.5 * nmt) + (0.25 * ntp)

if denominador == 0:
    st.error("⚠️ El número de profesores no puede ser 0 (Denominador cero).")
else:
    # Cálculo base
    pd_actual = ((4 * nlt) + (1.5 * nf) + (1 * ncl) + (1 * ng)) / denominador
    
    # Mostrar KPI principal destacado
    st.metric(label="PD Actual Calculado", value=f"{pd_actual:.4f}")
    
    # Análisis de déficit
    num_requerido = meta * denominador
    num_actual_fijo = (1.5 * nf) + (1 * ncl)
    puntos_faltantes = num_requerido - num_actual_fijo
    gap_total = num_requerido - ((4 * nlt) + (1.5 * nf) + (1 * ncl) + (1 * ng))
    
    if gap_total <= 0:
        st.success("🎉 ¡Indicador Cumplido al 100% o más! No se requieren publicaciones adicionales.")
    else:
        nlt_extra_nec = gap_total / 4
        ng_extra_nec = gap_total / 1
        
        st.info(
            f"**Para alcanzar el 100% de la meta necesitas:**\n\n"
            f"• **Opción A:** +{nlt_extra_nec:.2f} Libros de Texto (Mínimo {math.ceil(nlt_extra_nec)} enteros)\n\n"
            f"• **Opción B:** +{ng_extra_nec:.2f} Guías Publicadas (Mínimo {math.ceil(ng_extra_nec)} enteros)\n\n"
            f"• O cualquier combinación lineal entre ambas opciones."
        )
        
    # --- GRÁFICO DE FRONTERA ---
    fig, ax = plt.subplots(figsize=(6, 4))
    val_max_x = max(nlt * 1.5, 5)
    val_max_y = max(ng * 1.5, 5)
    
    if puntos_faltantes > 0:
        nlt_max = puntos_faltantes / 4
        ng_max = puntos_faltantes / 1
        
        ax.plot([0, nlt_max], [ng_max, 0], color='#2196F3', linestyle='-', linewidth=2.5, label='Línea de Cumplimiento 100%')
        ax.fill_between([0, nlt_max], [ng_max, 0], max(ng_max, val_max_y)*2, color='#4CAF50', alpha=0.15, label='Zona de Cumplimiento')
        
        val_max_x = max(nlt_max * 1.3, nlt * 1.3)
        val_max_y = max(ng_max * 1.3, ng * 1.3)
    else:
        ax.text(0.5, 0.5, "Meta superada mediante NF/NCL", ha='center', color='green')
        
    cumple = (4 * nlt + ng) >= puntos_faltantes
    color_punto = '#4CAF50' if cumple else '#F44336'
    etiqueta_punto = f'Estado Actual ({nlt:.0f} L, {ng:.0f} G) - {"CUMPLE" if cumple else "NO CUMPLE"}'
    
    ax.scatter(nlt, ng, color=color_punto, s=150, zorder=5, edgecolor='black', label=etiqueta_punto)
    
    ax.set_xlim(0, val_max_x)
    ax.set_ylim(0, val_max_y)
    ax.set_xlabel('Libros de Texto (NLT) [Peso: 4.0]')
    ax.set_ylabel('Guías (NG) [Peso: 1.0]')
    ax.set_title('Estrategia NLT vs NG')
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='upper right', fontsize='small')
    
    # Renderizar el gráfico en la interfaz web de manera limpia
    st.pyplot(fig)