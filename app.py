import streamlit as st
import pandas as pd

# ==========================================
# 1. CONFIGURACIÓN VISUAL Y ESTADO
# ==========================================
st.set_page_config(
    page_title="Auditoría SSO Ecuador 2025",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Inicializar variables de estado para guardar los checks del usuario
if 'checklist_state' not in st.session_state:
    st.session_state['checklist_state'] = {}
if 'score' not in st.session_state:
    st.session_state['score'] = 0

# Estilos CSS
st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #004d40;
        color: white;
        border-radius: 8px;
        height: 3.5em;
        font-weight: bold;
        font-size: 1.2rem;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .risk-badge {
        padding: 15px;
        color: white;
        border-radius: 8px;
        font-weight: bold;
        text-align: center;
        font-size: 1.5rem;
        display: block;
        margin-bottom: 10px;
    }
    .risk-bajo { background-color: #28a745; }
    .risk-medio { background-color: #ffc107; color: #333 !important; }
    .risk-alto { background-color: #dc3545; }
    
    .compliance-card {
        background-color: #e8f5e9;
        border: 2px solid #4caf50;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        margin-top: 20px;
    }
    .whatsapp-btn {
        display: block;
        background-color: #25D366;
        color: white !important;
        padding: 15px;
        border-radius: 50px;
        text-decoration: none;
        font-weight: 800;
        text-align: center;
        font-size: 1.2rem;
        margin-top: 10px;
        box-shadow: 0 4px 15px rgba(37, 211, 102, 0.4);
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. BASE DE DATOS Y LÓGICA
# ==========================================
lista_ciiu = [
    {"label": "Q8610.01 - Hospitales Básicos y Generales (Riesgo Medio)", "riesgo": "Medio", "codigo": "Q8610"},
    {"label": "Q8620.01 - Consultorios Médicos (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "Q8620"},
    {"label": "Q8620.02 - Consultorios Odontológicos (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "Q8620"},
    {"label": "G4711.01 - Tiendas de Barrio / Abarrotes (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "G4711"},
    {"label": "G4771.11 - Boutiques / Venta de Ropa (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "G4771"},
    {"label": "G4773.21 - Farmacias (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "G4773"},
    {"label": "G4520.01 - Talleres Mecánicos (Riesgo Medio)", "riesgo": "Medio", "codigo": "G4520"},
    {"label": "I5610.01 - Restaurantes / Comida (Riesgo Medio)", "riesgo": "Medio", "codigo": "I5610"},
    {"label": "N8121.00 - Limpieza de Interiores (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "N8121"},
    {"label": "F4100.10 - Construcción de Edificios (Riesgo Alto)", "riesgo": "Alto", "codigo": "F4100"},
    {"label": "C1071.01 - Panaderías (Riesgo Bajo)", "riesgo": "Bajo", "codigo": "C1071"},
    {"label": "H4923.01 - Transporte de Carga (Riesgo Medio)", "riesgo": "Medio", "codigo": "H4923"},
    {"label": "N8010.01 - Seguridad Privada (Riesgo Alto)", "riesgo": "Alto", "codigo": "N8010"}
]
df_ciiu = pd.DataFrame(lista_ciiu)

def generar_lista_requisitos(trabajadores, riesgo):
    """Genera una lista de diccionarios con los requisitos específicos"""
    reqs = []
    
    # --- BLOQUE 1: GESTIÓN ADMINISTRATIVA ---
    reqs.append({"cat": "Gestión Administrativa", "item": "Política de Seguridad y Salud (Firmada y Socializada)"})
    
    # Lógica de Responsable y sus derivados (Informes)
    if trabajadores <= 9:
        if riesgo == "Alto":
            reqs.append({"cat": "Gestión Administrativa", "item": "Registro de Técnico de Seguridad (Visita Periódica)"})
            reqs.append({"cat": "Gestión Administrativa", "item": "Informes Mensuales de Gestión del Técnico"})
        else:
            reqs.append({"cat": "Gestión Administrativa", "item": "Registro de Monitor de Seguridad (SUT)"})
            reqs.append({"cat": "Gestión Administrativa", "item": "Diploma de Capacitación del Monitor (MDT/SECAP)"})
            reqs.append({"cat": "Gestión Administrativa", "item": "Informes de Gestión del Monitor (Evidencias)"})
        
        # Documento Base (Reforma 186)
        reqs.append({"cat": "Gestión Administrativa", "item": "Plan de Prevención de Riesgos Laborales (Interno)"})
        
    else: # 10 o más
        if riesgo == "Alto":
            reqs.append({"cat": "Gestión Administrativa", "item": "Registro de Técnico de Seguridad (SUT)"})
            reqs.append({"cat": "Gestión Administrativa", "item": "Informes Mensuales del Técnico"})
        else:
            # Nota: Para 10-49 bajo/medio se usa Monitor o Técnico según art 13, simplificado aquí a Monitor por defecto
            reqs.append({"cat": "Gestión Administrativa", "item": "Registro de Monitor de Seguridad (SUT)"})
            reqs.append({"cat": "Gestión Administrativa", "item": "Informes de Gestión"})
        
        reqs.append({"cat": "Gestión Administrativa", "item": "Reglamento de Higiene y Seguridad (Aprobado)"})

    # Organismo Paritario
    if trabajadores >= 10:
        reqs.append({"cat": "Gestión Administrativa", "item": "Registro de Delegado de Seguridad"})
        reqs.append({"cat": "Gestión Administrativa", "item": "Informes Mensuales del Delegado"})
    
    # Protocolo Acoso (Obligatorio Todos)
    reqs.append({"cat": "Gestión Administrativa", "item": "Protocolo de Prevención de Acoso y Violencia (Art. 6 Reformado)"})
    reqs.append({"cat": "Gestión Administrativa", "item": "Actas de Socialización del Protocolo"})

    # --- BLOQUE 2: GESTIÓN TÉCNICA ---
    reqs.append({"cat": "Gestión Técnica", "item": "Matriz de Identificación de Peligros (GTC45 / INSHT)"})
    reqs.append({"cat": "Gestión Técnica", "item": "Profesiogramas (Fichas de Riesgo por Puesto)"})
    if riesgo in ["Alto", "Medio"]:
        reqs.append({"cat": "Gestión Técnica", "item": "Mediciones de Ruido / Iluminación (Informes Técnicos)"})

    # --- BLOQUE 3: TALENTO HUMANO ---
    reqs.append({"cat": "Gestión Talento Humano", "item": "Certificados de Aptitud Médica (Fichas Médicas)"})
    reqs.append({"cat": "Gestión Talento Humano", "item": "Registro de Entrega de EPPs (Firmados)"})
    reqs.append({"cat": "Gestión Talento Humano", "item": "Plan Anual de Capacitación"})
    reqs.append({"cat": "Gestión Talento Humano", "item": "Registros de Asistencia a Capacitaciones"})

    if trabajadores >= 10:
        reqs.append({"cat": "Gestión Talento Humano", "item": "Programa de Riesgo Psicosocial (Implementado)"})
        reqs.append({"cat": "Gestión Talento Humano", "item": "Programa de Drogas (Implementado)"})

    # --- BLOQUE 4: OPERATIVO ---
    reqs.append({"cat": "Procedimientos Operativos", "item": "Plan de Emergencias y Contingencia"})
    reqs.append({"cat": "Procedimientos Operativos", "item": "Informe de Simulacro (Con fotos y tiempos)"})
    reqs.append({"cat": "Procedimientos Operativos", "item": "Botiquín de Primeros Auxilios y Extintores"})
    reqs.append({"cat": "Procedimientos Operativos", "item": "Inspecciones de Seguridad (Checklist Periódico)"})

    return reqs

# ==========================================
# 3. INTERFAZ DE USUARIO
# ==========================================

# Header Centrado
st.markdown("""
    <div class="main-header" style="text-align:center">
        <div style="font-size: 3rem;">🕵️‍♂️</div>
        <h1 style="color: #004d40;">Auto-Auditoría SSO</h1>
        <p style="font-style: italic; color: #555;">Verifica tu nivel de cumplimiento real según la normativa 2025</p>
    </div>
""", unsafe_allow_html=True)

# --- PASO 1: CONFIGURACIÓN INICIAL ---
if 'diagnostico_activo' not in st.session_state:
    st.session_state['diagnostico_activo'] = False

with st.container():
    st.markdown("### 1. Configura tu Empresa")
    col_a, col_b = st.columns(2)
    with col_a:
        nombre_empresa = st.text_input("Nombre Comercial / Razón Social")
    with col_b:
        num_trabajadores = st.number_input("Número de Trabajadores (IESS)", min_value=1, value=1)
    
    actividad_seleccionada = st.selectbox(
        "Actividad Económica (Buscador Anexo 2):",
        options=df_ciiu['label'].tolist(),
        index=None,
        placeholder="Escribe para buscar (ej: Tienda, Construcción, Transporte...)"
    )
    
    if st.button("INICIAR AUDITORÍA"):
        if actividad_seleccionada and nombre_empresa:
            st.session_state['diagnostico_activo'] = True
            # Resetear estado si se reinicia
            st.session_state['checklist_state'] = {} 
        else:
            st.error("Por favor ingresa el nombre y selecciona una actividad.")

# --- PASO 2: RESULTADOS Y CHECKLIST ---
if st.session_state['diagnostico_activo']:
    st.divider()
    
    # Datos derivados
    info_actividad = df_ciiu[df_ciiu['label'] == actividad_seleccionada].iloc[0]
    nivel_riesgo = info_actividad['riesgo']
    
    # Generar lista de requisitos
    lista_requisitos = generar_lista_requisitos(num_trabajadores, nivel_riesgo)
    total_items = len(lista_requisitos)
    
    # --- TARJETA DE RIESGO ---
    st.markdown("### 2. Tu Perfil de Riesgo Legal")
    
    bg_class = "risk-bajo"
    mensaje_riesgo = "Tus obligaciones son administrativas y de gestión básica. El foco es la prevención documental."
    
    if nivel_riesgo == "Medio": 
        bg_class = "risk-medio"
        mensaje_riesgo = "Debes demostrar gestión técnica. Se requieren mediciones y vigilancia de salud."
    if nivel_riesgo == "Alto": 
        bg_class = "risk-alto"
        mensaje_riesgo = "🔴 ALERTA: Requiere Técnico calificado y permisos de trabajo peligrosos. Inspección prioritaria."

    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f'<div class="risk-badge {bg_class}">{nivel_riesgo.upper()}</div>', unsafe_allow_html=True)
    with col2:
        st.info(f"**Análisis:** {mensaje_riesgo}")
        st.caption(f"Clasificación: {'Microempresa' if num_trabajadores <=9 else 'Pequeña/Mediana'}")

    # --- CHECKLIST INTERACTIVO ---
    st.divider()
    st.markdown("### 3. Lista de Verificación (Marca lo que SÍ tienes vigente)")
    st.caption("Sé honesto para calcular tu porcentaje real. 'Tenerlo' significa que está firmado y archivado.")

    # Agrupar por categoría para mostrar en acordeones
    df_reqs = pd.DataFrame(lista_requisitos)
    categorias = df_reqs['cat'].unique()

    items_cumplidos = 0
    
    for cat in categorias:
        with st.expander(f"📂 {cat.upper()}", expanded=True):
            items_cat = df_reqs[df_reqs['cat'] == cat]
            for index, row in items_cat.iterrows():
                label = row['item']
                # Creamos un checkbox único para cada item
                key = f"check_{index}"
                if st.checkbox(label, key=key):
                    items_cumplidos += 1

    # --- CÁLCULO DE PORCENTAJE ---
    porcentaje = int((items_cumplidos / total_items) * 100)
    
    st.divider()
    st.markdown(f"<h2 style='text-align: center'>NIVEL DE CUMPLIMIENTO: {porcentaje}%</h2>", unsafe_allow_html=True)
    st.progress(porcentaje / 100)
    
    if porcentaje < 100:
        color_alert = "red" if porcentaje < 50 else "orange"
        st.markdown(f"<p style='color:{color_alert}; text-align:center; font-weight:bold'>⚠️ Tienes {total_items - items_cumplidos} hallazgos pendientes que generan multa.</p>", unsafe_allow_html=True)
    else:
        st.success("¡Felicitaciones! Tu empresa parece estar en regla.")

    # --- PASO 4: CAPTURA DE CONTACTO Y ENVÍO ---
    st.markdown("### 4. Recibe tu Informe y Plan de Acción")
    with st.form("contact_form"):
        c_tel, c_mail = st.columns(2)
        telefono = c_tel.text_input("Número de Celular (WhatsApp)", placeholder="099...")
        email = c_mail.text_input("Correo Electrónico", placeholder="nombre@empresa.com")
        
        # Botón de envío dentro del form
        submitted = st.form_submit_button("📈 FINALIZAR AUDITORÍA")
        
        if submitted:
            if telefono:
                # Generar mensaje de WhatsApp
                msg = f"Hola, soy el Rep. Legal de *{nombre_empresa}*. Realicé la auto-auditoría. Mi resultado es *{porcentaje}% de cumplimiento* (Riesgo {nivel_riesgo}). Me faltan {total_items - items_cumplidos} documentos. Mi correo es {email}. ¿Cómo los soluciono?"
                
                # TU NÚMERO DE VENTAS AQUÍ
                mi_numero = "593987996831" 
                
                link_wa = f"https://wa.me/{mi_numero}?text={msg.replace(' ', '%20')}"
                
                st.markdown(f"""
                <a href="{link_wa}" class="whatsapp-btn" target="_blank">
                    📲 VER RESULTADOS Y SOLUCIONES EN WHATSAPP
                </a>
                """, unsafe_allow_html=True)
                st.caption("Al hacer clic, se abrirá WhatsApp para enviarte el informe preliminar.")
            else:
                st.error("Por favor ingresa un número de celular para enviarte el resultado.")

