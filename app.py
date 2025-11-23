import streamlit as st
import pandas as pd
from datetime import datetime

# ==========================================
# 1. CONFIGURACIÓN VISUAL (ESTILO PRO)
# ==========================================
st.set_page_config(
    page_title="Diagnóstico SSO Ecuador",
    page_icon="🛡️",
    layout="centered", # "centered" se ve mejor en móviles que "wide"
    initial_sidebar_state="collapsed" # Ocultamos menú para enfocar en la App
)

# Inyectar CSS para mejorar la estética (Botones y Tarjetas)
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #004d40;
        color: white;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #00695c;
        border-color: #00695c;
        color: white;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
    }
    .whatsapp-btn {
        display: inline-block;
        background-color: #25D366;
        color: white;
        padding: 10px 20px;
        border-radius: 50px;
        text-decoration: none;
        font-weight: bold;
        text-align: center;
        width: 100%;
        margin-top: 20px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
    }
    .whatsapp-btn:hover {
        background-color: #128C7E;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LÓGICA (SIMPLIFICADA PARA EL EJEMPLO)
# ==========================================
# Simulación de Base de Datos Anexo 2
actividades_db = {
    "Tienda de Barrio / Víveres": {"riesgo": "Bajo", "ciiu": "G4711"},
    "Restaurante / Comida Rápida": {"riesgo": "Medio", "ciiu": "I5610"},
    "Peluquería / Estética": {"riesgo": "Bajo", "ciiu": "S9602"},
    "Construcción / Obra Civil": {"riesgo": "Alto", "ciiu": "F4100"},
    "Taller Mecánico / Automotriz": {"riesgo": "Medio", "ciiu": "G4520"},
    "Transporte de Carga": {"riesgo": "Medio", "ciiu": "H4923"},
    "Oficina / Servicios Profesionales": {"riesgo": "Bajo", "ciiu": "M6910"},
    "Consultorio Médico / Dental": {"riesgo": "Bajo", "ciiu": "Q8620"}
}

# ==========================================
# 3. INTERFAZ DE USUARIO (FRONTEND)
# ==========================================

# --- ENCABEZADO ---
st.image("https://cdn-icons-png.flaticon.com/512/9563/9563683.png", width=60) # Puedes poner tu logo aquí
st.title("Diagnóstico Legal SSO")
st.markdown("Verifica en **30 segundos** si tu empresa cumple con la nueva normativa del Ministerio del Trabajo (2025).")
st.divider()

# --- PASO 1: DATOS (TARJETA LIMPIA) ---
with st.container():
    st.subheader("1. Datos de tu Negocio")
    col_a, col_b = st.columns(2)
    with col_a:
        empresa = st.text_input("Nombre de la Empresa", placeholder="Ej: Comercial Don Pepe")
    with col_b:
        trabajadores = st.number_input("Nº Trabajadores", min_value=1, value=3, step=1)
    
    actividad = st.selectbox("Actividad Económica Principal", list(actividades_db.keys()))
    
    # Botón Principal
    calcular = st.button("🔍 ANALIZAR MI CUMPLIMIENTO")

# --- PASO 2: RESULTADOS (APARECEN AL DAR CLIC) ---
if calcular:
    st.divider()
    
    # Lógica de Clasificación
    datos_actividad = actividades_db[actividad]
    riesgo = datos_actividad["riesgo"]
    
    # Determinar tipo de empresa
    if trabajadores <= 9:
        tipo_empresa = "Microempresa"
        obligacion_base = "Plan de Prevención (Interno)"
        responsable = "Monitor de Seguridad"
        color_riesgo = "off" if riesgo == "Bajo" else "inverse"
    else:
        tipo_empresa = "Pequeña/Mediana"
        obligacion_base = "Reglamento de Higiene (SUT)"
        responsable = "Delegado de Seguridad"
    
    # Tarjetas de Resumen (Metrics) - Se ven genial en celular
    st.subheader("2. Tu Perfil de Riesgo")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Nivel de Riesgo", riesgo, delta="MDT-2025", delta_color=color_riesgo)
    col2.metric("Clasificación", tipo_empresa)
    col3.metric("Responsable", responsable)
    
    # --- PASO 3: LISTA DE VERIFICACIÓN (ACORDEÓN) ---
    st.markdown("### 3. ¿Qué documentos te faltan?")
    st.info(f"Según el Anexo 1, para una empresa de **Riesgo {riesgo}**, necesitas:")
    
    # Usamos "expander" para que no ocupe mucho espacio en el celular
    with st.expander("📂 A. Documentación Legal (Obligatorio)", expanded=True):
        if trabajadores < 10:
            st.markdown("✅ **Plan de Prevención de Riesgos:** (No requiere registro SUT, pero sí físico).")
            st.markdown("✅ **Acta de Designación de Monitor:** Firmada por el Representante Legal.")
        else:
            st.error("❌ **Reglamento de Higiene:** Aprobado y Registrado en SUT.")
            st.error("❌ **Delegado de Seguridad:** Acta de elección registrada.")
            
    with st.expander("🚑 B. Programas y Salud (Obligatorio)"):
        st.markdown("✅ **Botiquín de Primeros Auxilios:** Acorde al riesgo.")
        st.markdown("✅ **Protocolo de Prevención de Violencia/Acoso:** Firmado y socializado.")
        if trabajadores >= 10:
             st.warning("⚠️ **Programa de Prevención de Drogas:** Implementado.")
             st.warning("⚠️ **Programa de Riesgo Psicosocial:** Evaluado.")

    with st.expander("👷 C. Seguridad Operativa (Lo que revisan)"):
        st.markdown("✅ **Matriz de Riesgos:** Identificación de peligros.")
        st.markdown("✅ **Registro de EPPs:** Actas de entrega firmadas.")
        st.markdown("✅ **Señalización:** Extintores y rutas de evacuación.")

    # --- PASO 4: LLAMADO A LA ACCIÓN (VENTA) ---
    st.divider()
    st.success("💡 **Diagnóstico Final:** Si no tienes alguno de estos documentos, estás expuesto a multas de hasta $200 USD por trabajador.")
    
    # Mensaje personalizado para WhatsApp
    mensaje_ws = f"Hola, hice el diagnóstico en la App. Soy {empresa}, tengo {trabajadores} trabajadores ({actividad}) y me faltan documentos de seguridad. ¿Me ayudas?"
    link_ws = f"https://wa.me/593987996831?text={mensaje_ws.replace(' ', '%20')}" # CAMBIA TU NÚMERO AQUÍ
    
    st.markdown(f"""
    <a href="{link_ws}" class="whatsapp-btn" target="_blank">
        🚀 SOLICITAR DOCUMENTOS FALTANTES POR WHATSAPP
    </a>
    """, unsafe_allow_html=True)