import streamlit as st
import pandas as pd

# ==========================================
# 1. CONFIGURACIÓN VISUAL Y CSS
# ==========================================
st.set_page_config(
    page_title="Diagnóstico SSO Ecuador 2025",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Estilos CSS para Botones y Etiquetas de Riesgo
st.markdown("""
<style>
    /* Estilo para el botón de riesgo (Badge) */
    .risk-badge {
        padding: 10px 20px;
        color: white;
        border-radius: 5px;
        font-weight: bold;
        text-align: center;
        font-size: 1.2rem;
        display: inline-block;
        width: 100%;
    }
    .risk-bajo { background-color: #28a745; } /* Verde */
    .risk-medio { background-color: #ffc107; color: black !important; } /* Amarillo */
    .risk-alto { background-color: #dc3545; } /* Rojo */
    
    /* Estilo Botón WhatsApp */
    .whatsapp-btn {
        display: block;
        background-color: #25D366;
        color: white !important;
        padding: 15px;
        border-radius: 50px;
        text-decoration: none;
        font-weight: bold;
        text-align: center;
        font-size: 1.1rem;
        margin-top: 20px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.2);
    }
    .whatsapp-btn:hover { background-color: #128C7E; }
    
    /* Ocultar footer de Streamlit */
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. BASE DE DATOS CIIU (ANEXO 2 - Extracto Ampliado)
# ==========================================
# Esta lista simula la carga del Anexo 2 completo. 
# En producción, esto podría venir de un archivo .csv cargado con pd.read_csv()
lista_ciiu = [
    {"label": "A0111 - Cultivo de cereales y otros cultivos (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "A0111"},
    {"label": "C1010 - Procesamiento y conservación de carne (Riesgo Alto)", "riesgo": "Alto", "codigo": "C1010"},
    {"label": "C1071 - Elaboración de pan y productos de panadería (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "C1071"},
    {"label": "F4100 - Construcción de edificios (Riesgo Alto)", "riesgo": "Alto", "codigo": "F4100"},
    {"label": "G4520 - Mantenimiento y reparación de vehículos (Riesgo Medio)", "riesgo": "Medio", "codigo": "G4520"},
    {"label": "G4711 - Venta al por menor en tiendas/abarrotes (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "G4711"},
    {"label": "G4771 - Venta al por menor de prendas de vestir (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "G4771"},
    {"label": "G4773 - Venta de productos farmacéuticos/Farmacias (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "G4773"},
    {"label": "H4923 - Transporte de carga por carretera (Riesgo Medio)", "riesgo": "Medio", "codigo": "H4923"},
    {"label": "I5610 - Restaurantes y actividades de servicio de comidas (Riesgo Medio)", "riesgo": "Medio", "codigo": "I5610"},
    {"label": "J6201 - Actividades de programación informática (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "J6201"},
    {"label": "K6419 - Intermediación monetaria / Bancos (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "K6419"},
    {"label": "M6910 - Actividades Jurídicas / Abogados (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "M6910"},
    {"label": "N8010 - Actividades de seguridad privada (Riesgo Alto)", "riesgo": "Alto", "codigo": "N8010"},
    {"label": "N8121 - Limpieza general de edificios (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "N8121"},
    {"label": "Q8620 - Actividades médicas y odontológicas (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "Q8620"},
    {"label": "S9602 - Peluquería y otros tratamientos de belleza (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "S9602"}
]
# Convertimos a DataFrame para fácil manejo
df_ciiu = pd.DataFrame(lista_ciiu)

# ==========================================
# 3. INTERFAZ DE USUARIO (SIDEBAR)
# ==========================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6380/6380000.png", width=80)
    st.title("Datos de la Empresa")
    
    # Datos de Contacto (Requerimiento del usuario)
    nombre_empresa = st.text_input("Nombre Comercial / Razón Social")
    rep_legal = st.text_input("Nombre Representante Legal")
    telefono = st.text_input("Número de Teléfono / Celular")
    email = st.text_input("Correo Electrónico (Opcional)")
    
    st.markdown("---")
    
    # Datos Técnicos para Clasificación
    num_trabajadores = st.number_input("Número Total de Trabajadores", min_value=1, value=1, step=1)
    
    # Buscador CIIU
    actividad_seleccionada = st.selectbox(
        "Busca tu Actividad Económica (CIIU):",
        options=df_ciiu['label'].tolist(),
        index=None,
        placeholder="Escribe para buscar (ej: Construcción, Tienda...)"
    )
    
    btn_calcular = st.button("📊 GENERAR DIAGNÓSTICO", type="primary")

# ==========================================
# 4. LÓGICA DE CLASIFICACIÓN (MOTOR LEGAL)
# ==========================================

def obtener_requisitos(trabajadores, riesgo):
    # Inicializamos las listas
    admin = []
    tecnica = []
    talento = []
    operativos = []
    
    # --- LOGICA SEGÚN ACUERDO 196 y DECRETO 255 ---
    
    # 1. RESPONSABLE DE SEGURIDAD (Art. 18 Dec. 255 y Art. 13 AM 196)
    if trabajadores <= 9:
        if riesgo == "Alto":
             responsable = "Técnico de Seguridad (Visita Periódica)"
             admin.append("✅ Registro de Técnico de Seguridad (Art. 13 AM 196)")
        else:
             responsable = "Monitor de Seguridad (Trabajador)"
             admin.append("✅ Registro de Monitor de Seguridad (Art. 8 AM 196)")
    else: # 10 a 49 (Pequeña)
         if riesgo == "Alto":
              responsable = "Técnico de Seguridad (Visita Periódica)"
              admin.append("✅ Registro de Técnico de Seguridad (Art. 11 AM 196)")
         else:
              responsable = "Monitor de Seguridad" # Nota: Para 10-49 bajo/medio el Art 13 pide Monitor.
              admin.append("✅ Registro de Monitor de Seguridad (Art. 10 AM 196)")

    # 2. DOCUMENTO BASE (Art. 18 y 19 AM 196)
    if trabajadores <= 9:
        doc_base = "Plan de Prevención de Riesgos"
        # Con la reforma 186 ya no se registra, pero se debe cumplir
        admin.append("✅ Plan de Prevención de Riesgos (Cumplimiento Art. 6 Reformado)")
    else:
        doc_base = "Reglamento de Higiene y Seguridad"
        admin.append("⚠️ Reglamento de Higiene y Seguridad (Aprobado y Registrado SUT)")

    # 3. ORGANISMO PARITARIO (Art. 32 y 33 Dec. 255)
    if trabajadores >= 10:
        admin.append("⚠️ Registro de Delegado de Seguridad (Elegido por trabajadores)")
    
    # 4. PROGRAMAS DE PREVENCIÓN (Art. 19 AM 196)
    # Para 1-9 no se registran pero se gestionan. Para >10 es obligatorio registro.
    if trabajadores >= 10:
        talento.append("⚠️ Programa de Prevención de Riesgos Psicosociales (Registrado)")
        talento.append("⚠️ Programa de Prevención de Drogas (Registrado)")
    else:
        talento.append("✅ Gestión de Riesgos Psicosociales (Implementación Interna)")

    # --- REQUISITOS COMUNES (ANEXO 1 - APLICAN A TODOS) ---
    
    # Gestión Administrativa Adicional
    admin.append("✅ Política de Seguridad y Salud (Socializada)")
    admin.append("✅ Protocolo de Prevención de Acoso y Violencia (Art. 6 Reformado)")
    
    # Gestión Técnica (Anexo 1) [cite: 2616-2691]
    tecnica.append("✅ Matriz de Identificación de Peligros (GTC45 / INSHT)")
    tecnica.append("✅ Profesiogramas (Descripción de funciones y riesgos)")
    tecnica.append("✅ Mapa de Riesgos y Recursos (Gráfico)")
    if riesgo == "Alto" or riesgo == "Medio":
        tecnica.append("⚠️ Mediciones de Higiene Industrial (Ruido, Luz, etc.) [Si aplica]")
    
    # Gestión Talento Humano (Anexo 1) [cite: 2797-2843]
    talento.append("✅ Certificados de Aptitud Médica (Fichas Médicas)")
    talento.append("✅ Registro de Entrega de EPPs (Gratuito)")
    talento.append("✅ Plan Anual de Capacitación (Ejecutado)")
    
    # Procedimientos Operativos (Anexo 1) [cite: 2891-3077]
    operativos.append("✅ Plan de Emergencias y Contingencia")
    operativos.append("✅ Informe de Simulacros (Min. 1 al año)")
    operativos.append("✅ Botiquín de Primeros Auxilios y Extintores")
    operativos.append("✅ Inspecciones Internas de Seguridad (Checklist)")
    
    return responsable, doc_base, admin, tecnica, talento, operativos

# ==========================================
# 5. DESPLIEGUE DE RESULTADOS
# ==========================================
if btn_calcular and actividad_seleccionada:
    
    # Recuperar datos de la selección
    info_actividad = df_ciiu[df_ciiu['label'] == actividad_seleccionada].iloc[0]
    nivel_riesgo = info_actividad['riesgo']
    codigo_ciiu = info_actividad['codigo']
    
    # Ejecutar motor de lógica
    resp_legal, doc_legal, l_admin, l_tec, l_talento, l_oper = obtener_requisitos(num_trabajadores, nivel_riesgo)
    
    # --- SECCIÓN A: ENCABEZADO DE RESULTADOS ---
    st.title("Diagnóstico de Cumplimiento Normativo")
    st.markdown(f"**Empresa:** {nombre_empresa} | **RUC/CIIU:** {codigo_ciiu}")
    st.markdown("**Normativa Vigente:** Acuerdo Ministerial MDT-2024-196, Decreto Ejecutivo 255 y Reforma MDT-2025-186.")
    st.divider()
    
    # --- SECCIÓN B: SEMÁFORO DE RIESGO ---
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Nivel de Riesgo Laboral**")
        # Lógica de color para el botón
        clase_css = "risk-bajo"
        if nivel_riesgo == "Medio": clase_css = "risk-medio"
        if nivel_riesgo == "Alto": clase_css = "risk-alto"
        
        st.markdown(f'<div class="{clase_css}">{nivel_riesgo.upper()}</div>', unsafe_allow_html=True)
        
    with col2:
        st.metric("Tamaño Empresa", f"{'Micro' if num_trabajadores <=9 else 'Pequeña'}")
    
    with col3:
        st.metric("Responsable Técnico", "Monitor" if "Monitor" in resp_legal else "Técnico")

    st.write("")
    st.info(f"📌 **Responsabilidad Principal:** {resp_legal} y {doc_legal}")

    # --- SECCIÓN C: LISTA DE VERIFICACIÓN (ESTRUCTURA ANEXO 1) ---
    st.subheader("Lista de Obligaciones (Anexo 1)")
    
    with st.expander("1. GESTIÓN ADMINISTRATIVA", expanded=True):
        for item in l_admin:
            st.write(item)
            
    with st.expander("2. GESTIÓN TÉCNICA"):
        for item in l_tec:
            st.write(item)
            
    with st.expander("3. GESTIÓN DEL TALENTO HUMANO"):
        for item in l_talento:
            st.write(item)
            
    with st.expander("4. PROCEDIMIENTOS OPERATIVOS BÁSICOS"):
        for item in l_oper:
            st.write(item)

    # --- SECCIÓN D: CIERRE Y VENTA ---
    st.divider()
    st.success("💡 **Análisis Final:** El incumplimiento de estos puntos puede generar multas de 3 a 20 SBU (Art. 7 Mandato 8).")
    
    # Generar enlace de WhatsApp personalizado con los datos capturados
    mensaje = f"Hola, soy {rep_legal} de la empresa {nombre_empresa}. Hice el diagnóstico: Tengo {num_trabajadores} trabajadores, Riesgo {nivel_riesgo}. Necesito ayuda para cumplir con: {doc_legal}."
    telefono_destino = "593987996831" # <--- ¡PON TU NÚMERO AQUÍ!
    link_wa = f"https://wa.me/{telefono_destino}?text={mensaje.replace(' ', '%20')}"
    
    st.markdown(f"""
    <a href="{link_wa}" class="whatsapp-btn" target="_blank">
        📲 SOLICITAR IMPLEMENTACIÓN DE ESTOS REQUISITOS
    </a>
    """, unsafe_allow_html=True)

elif btn_calcular and not actividad_seleccionada:
    st.error("Por favor, selecciona una Actividad Económica del buscador para continuar.")
else:
    st.info("👋 Ingresa los datos de tu empresa en el menú lateral para iniciar el diagnóstico.")


