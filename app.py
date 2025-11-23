import streamlit as st
import pandas as pd

# ==========================================
# 1. CONFIGURACIÓN VISUAL Y CSS AVANZADO
# ==========================================
st.set_page_config(
    page_title="Diagnóstico SSO Ecuador",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Inyectamos CSS para forzar el diseño centrado y tarjetas uniformes
st.markdown("""
<style>
    /* 1. ENCABEZADO CENTRADO */
    .main-header {
        text-align: center;
        padding-bottom: 20px;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #004d40;
        margin-bottom: 5px;
    }
    .sub-title {
        font-size: 1.1rem;
        color: #555;
        font-style: italic;
    }

    /* 2. TARJETAS DE RESULTADOS (RESULT CARDS) */
    /* Esto asegura que las 3 cajas se vean iguales */
    .result-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        height: 100%; /* Altura uniforme */
        margin-bottom: 10px;
    }
    .card-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
        font-weight: 600;
    }
    .card-value {
        font-size: 1.3rem;
        font-weight: 800;
        color: #333;
    }

    /* 3. COLORES DE RIESGO */
    .risk-value {
        font-size: 1.4rem;
        font-weight: 900;
        padding: 5px 10px;
        border-radius: 5px;
        color: white;
        display: inline-block;
    }
    .bg-bajo { background-color: #28a745; }   /* Verde */
    .bg-medio { background-color: #ffc107; color: #000 !important; } /* Amarillo */
    .bg-alto { background-color: #dc3545; }   /* Rojo */

    /* 4. BOTÓN WHATSAPP */
    .whatsapp-btn {
        display: block;
        background-color: #25D366;
        color: white !important;
        padding: 15px;
        border-radius: 50px;
        text-decoration: none;
        font-weight: 800;
        text-align: center;
        font-size: 1.1rem;
        margin-top: 20px;
        box-shadow: 0 4px 10px rgba(37, 211, 102, 0.3);
        transition: transform 0.2s;
    }
    .whatsapp-btn:hover {
        background-color: #128C7E;
        transform: scale(1.02);
    }
    
    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. BASE DE DATOS Y LÓGICA
# ==========================================
lista_ciiu = [
    {"label": "Q8610.01 - Hospitales Básicos y Generales (Riesgo Medio)", "riesgo": "Medio", "codigo": "Q8610"},
    {"label": "Q8610.03 - Hospitales Especializados (Riesgo Medio)", "riesgo": "Medio", "codigo": "Q8610"},
    {"label": "Q8620.01 - Consultorios Médicos (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "Q8620"},
    {"label": "Q8620.02 - Consultorios Odontológicos (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "Q8620"},
    {"label": "G4711.01 - Tiendas de Barrio / Abarrotes (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "G4711"},
    {"label": "G4771.11 - Boutiques / Venta de Ropa (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "G4771"},
    {"label": "G4773.21 - Farmacias (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "G4773"},
    {"label": "G4520.01 - Talleres Mecánicos (Riesgo Medio)", "riesgo": "Medio", "codigo": "G4520"},
    {"label": "G4530.00 - Repuestos Automotrices (Riesgo Medio)", "riesgo": "Medio", "codigo": "G4530"},
    {"label": "I5610.01 - Restaurantes / Comida (Riesgo Medio)", "riesgo": "Medio", "codigo": "I5610"},
    {"label": "S9602.00 - Peluquerías / Belleza (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "S9602"},
    {"label": "N8121.00 - Limpieza de Interiores (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "N8121"},
    {"label": "F4100.10 - Construcción de Edificios (Riesgo Alto)", "riesgo": "Alto", "codigo": "F4100"},
    {"label": "C1071.01 - Panaderías (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "C1071"},
    {"label": "H4923.01 - Transporte de Carga (Riesgo Medio)", "riesgo": "Medio", "codigo": "H4923"},
    {"label": "M6910.01 - Servicios Jurídicos / Oficinas (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "M6910"},
    {"label": "J6201.01 - Servicios de Software (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "J6201"},
    {"label": "N8010.01 - Seguridad Privada (Riesgo Alto)", "riesgo": "Alto", "codigo": "N8010"}
]
df_ciiu = pd.DataFrame(lista_ciiu)

def obtener_requisitos(trabajadores, riesgo):
    admin, tecnica, talento, operativos = [], [], [], []
    
    if trabajadores <= 9:
        if riesgo == "Alto":
             responsable = "Técnico de Seguridad (Visita)"
             admin.append("✅ Registro de Técnico (Art. 13 AM 196)")
        else:
             responsable = "Monitor de Seguridad"
             admin.append("✅ Registro de Monitor (Art. 8 AM 196)")
        doc_base = "Plan de Prevención (Interno)"
        admin.append("✅ Plan de Prevención de Riesgos")
    else:
         if riesgo == "Alto":
              responsable = "Técnico de Seguridad"
              admin.append("✅ Registro de Técnico (Art. 11 AM 196)")
         else:
              responsable = "Monitor de Seguridad"
              admin.append("✅ Registro de Monitor (Art. 10 AM 196)")
         doc_base = "Reglamento de Higiene (SUT)"
         admin.append("⚠️ Reglamento de Higiene y Seguridad")

    if trabajadores >= 10:
        admin.append("⚠️ Registro de Delegado de Seguridad")
        talento.append("⚠️ Programa de Riesgos Psicosociales")
        talento.append("⚠️ Programa de Prevención de Drogas")
    else:
        talento.append("✅ Gestión Psicosocial y Drogas (Interno)")

    admin.append("✅ Política de SSO")
    admin.append("✅ Protocolo Violencia y Acoso")
    tecnica.append("✅ Matriz de Riesgos (GTC45)")
    tecnica.append("✅ Profesiogramas")
    talento.append("✅ Fichas Médicas")
    talento.append("✅ Registro Entrega EPPs")
    talento.append("✅ Plan de Capacitación")
    operativos.append("✅ Plan de Emergencias")
    operativos.append("✅ Botiquín y Extintores")
    
    return responsable, doc_base, admin, tecnica, talento, operativos

# ==========================================
# 3. INTERFAZ PRINCIPAL
# ==========================================

# --- ENCABEZADO HTML PERSONALIZADO ---
st.markdown("""
    <div class="main-header">
        <div style="font-size: 3rem;">🛡️</div>
        <div class="main-title">Diagnóstico SSO Ecuador</div>
        <div class="sub-title">Verifica tus obligaciones según la Normativa 2025</div>
    </div>
""", unsafe_allow_html=True)

# --- FORMULARIO DE DATOS ---
with st.container():
    # Uso columnas para que en PC se vea lado a lado, en móvil se apila solo
    c1, c2 = st.columns(2)
    with c1:
        nombre_empresa = st.text_input("Nombre de tu Empresa", placeholder="Ej: Farmacia Cruz Azul")
        rep_legal = st.text_input("Representante Legal", placeholder="Tu nombre")
    with c2:
        telefono = st.text_input("Tu Celular (WhatsApp)", placeholder="099...")
        email = st.text_input("Tu Correo (Opcional)")
    
    st.write("")
    st.markdown("**Datos para el análisis legal:**")
    
    # Inputs grandes
    num_trabajadores = st.number_input("Número de Trabajadores (IESS)", min_value=1, value=1)
    actividad_seleccionada = st.selectbox("Actividad Económica (Escribe para buscar):", options=df_ciiu['label'].tolist(), index=None, placeholder="Ej: Tienda, Construcción, Médico...")

    st.write("")
    # Botón centrado
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        btn_calcular = st.button("🚀 VER MIS OBLIGACIONES")

# ==========================================
# 4. RESULTADOS (DISEÑO DE TARJETAS)
# ==========================================
if btn_calcular and actividad_seleccionada:
    info_actividad = df_ciiu[df_ciiu['label'] == actividad_seleccionada].iloc[0]
    nivel_riesgo = info_actividad['riesgo']
    resp_legal, doc_legal, l_admin, l_tec, l_talento, l_oper = obtener_requisitos(num_trabajadores, nivel_riesgo)
    
    st.divider()
    st.subheader(f"Resultados para: {nombre_empresa}")

    # --- TARJETAS UNIFORMES (HTML) ---
    # Definimos el color de fondo del riesgo
    bg_class = "bg-bajo"
    if nivel_riesgo == "Medio": bg_class = "bg-medio"
    if nivel_riesgo == "Alto": bg_class = "bg-alto"
    
    tipo_empresa = "Microempresa" if num_trabajadores <= 9 else "Pequeña/Mediana"

    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="result-card">
            <div class="card-label">Nivel de Riesgo</div>
            <div class="risk-value {bg_class}">{nivel_riesgo.upper()}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="result-card">
            <div class="card-label">Clasificación</div>
            <div class="card-value">{tipo_empresa}</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        # Ajustamos texto largo del responsable para que no rompa el diseño
        resp_short = "Monitor" if "Monitor" in resp_legal else "Técnico"
        st.markdown(f"""
        <div class="result-card">
            <div class="card-label">Responsable</div>
            <div class="card-value">{resp_short}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.caption(f"ℹ️ *Detalle del Responsable:* {resp_legal}")

    # --- LISTA DE REQUISITOS ---
    st.write("")
    st.markdown("### 📋 Tu Lista de Cumplimiento (Anexo 1)")
    
    with st.expander("1. GESTIÓN ADMINISTRATIVA", expanded=True):
        for item in l_admin: st.write(item)
    with st.expander("2. GESTIÓN TÉCNICA"):
        for item in l_tec: st.write(item)
    with st.expander("3. GESTIÓN DEL TALENTO HUMANO"):
        for item in l_talento: st.write(item)
    with st.expander("4. PROCEDIMIENTOS OPERATIVOS"):
        for item in l_oper: st.write(item)

    # --- CALL TO ACTION ---
    st.divider()
    
    msg = f"Hola, soy {rep_legal}. Mi empresa {nombre_empresa} tiene {num_trabajadores} trabajadores y es Riesgo {nivel_riesgo}. Necesito el {doc_legal} y cumplir con la normativa."
    telefono_destino = "593999999999" # <--- PON TU NÚMERO AQUÍ
    link_wa = f"https://wa.me/{telefono_destino}?text={msg.replace(' ', '%20')}"
    
    st.markdown(f"""
    <div style="text-align: center;">
        <p style="font-size: 1.1rem;">⚠️ El incumplimiento genera multas de hasta $9.200 USD.</p>
        <a href="{link_wa}" class="whatsapp-btn" target="_blank">
            📲 SOLICITAR GESTIÓN COMPLETA AHORA
        </a>
    </div>
    """, unsafe_allow_html=True)

elif btn_calcular:
    st.error("⚠️ Por favor selecciona una actividad económica.")
