import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

# PDF
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="Test de Liderazgo", layout="centered")

st.title("Test de Liderazgo Blake & Mouton")

st.write("Responde de 0 (nunca) a 5 (siempre)")

# -------------------------
# DESCRIPCIONES ORIGINALES
# -------------------------
descripciones = {
    "Ajeno": {
        "emoji": "⚪",
        "texto": """Tu estilo de liderazgo tiende a mantenerse al margen tanto de las personas como de las tareas. 
Es probable que no te involucres activamente en la dirección del equipo ni en el seguimiento de objetivos.

Esto puede hacer que tu equipo perciba falta de guía o apoyo, lo que impacta en la motivación y en los resultados. 
Tampoco sueles involucrarte en las preocupaciones o expectativas del equipo, lo cual puede limitar el desempeño colectivo.

Desarrollar mayor involucramiento tanto en las personas como en los objetivos puede ayudarte a generar mayor impacto como líder."""
    },
    "Autoritario": {
        "emoji": "🔴",
        "texto": """Tu estilo de liderazgo está fuertemente orientado al cumplimiento de tareas y objetivos. 
Tiendes a tomar el control, dirigir, y asegurarte de que el trabajo se realice de forma eficiente y correcta.

Probablemente confías en tu criterio para tomar decisiones importantes y priorizas la rapidez y precisión, especialmente en situaciones urgentes.

Sin embargo, este enfoque puede hacer que descuides el aspecto humano del equipo. 
Fortalecer tus habilidades en relaciones interpersonales puede ayudarte a potenciar aún más tu liderazgo."""
    },
    "Social": {
        "emoji": "🟡",
        "texto": """Tu estilo de liderazgo está centrado en las personas. 
Te preocupas por el bienestar de tu equipo, fomentas un ambiente positivo y das libertad para que cada quien trabaje a su manera.

Es probable que generes confianza y buenas relaciones dentro del equipo, lo cual es clave para un ambiente saludable.

Sin embargo, este enfoque puede hacer que en ocasiones los resultados o la ejecución de tareas no sean la prioridad. 
Encontrar un mejor balance entre personas y objetivos puede llevar tu liderazgo al siguiente nivel."""
    },
    "Líder de equipo": {
        "emoji": "🟢",
        "texto": """Tu estilo de liderazgo logra un equilibrio sólido entre las personas y las tareas. 
No solo te enfocas en alcanzar objetivos, sino también en construir un ambiente positivo y colaborativo.

Entiendes que un equipo motivado y bien dirigido es clave para lograr resultados sostenibles. 
Te preocupas por prevenir conflictos, mantener la satisfacción del equipo y asegurar que todos estén alineados.

Este es uno de los estilos más efectivos de liderazgo, ya que combina productividad con bienestar organizacional."""
    }
}

color_map = {
    "Ajeno": "gray",
    "Autoritario": "red",
    "Social": "orange",
    "Líder de equipo": "green"
}

# -------------------------
# PREGUNTAS
# -------------------------
preguntas = [
"Animo a los miembros de mi equipo a participar en la toma de decisiones.",
"Nada es más importante que completar un objetivo o tarea.",
"Monitoreo muy de cerca la duración de las tareas.",
"Me gusta ayudar a los demás a realizar nuevas tareas.",
"Cuanto más desafiante es la tarea, más lo disfruto.",
"Animo a mis colaboradores a ser creativos.",
"Me aseguro de todos los detalles en tareas complejas.",
"Me es fácil llevar varias tareas complicadas.",
"Leo sobre liderazgo y lo aplico.",
"Cuando corrijo errores no me preocupan las relaciones.",
"Administro mi tiempo con efectividad.",
"Me gusta explicar tareas complejas.",
"Divido proyectos en tareas manejables.",
"Desarrollar un gran equipo es clave.",
"Me gusta analizar problemas.",
"Respeto los límites de los demás.",
"Aconsejo a mis empleados.",
"Aplico lo que aprendo en mi profesión."
]

respuestas = []

for i, p in enumerate(preguntas):
    val = st.radio(f"{i+1}. {p}", [0,1,2,3,4,5], horizontal=True, key=i)
    respuestas.append(val)

# -------------------------
# PDF
# -------------------------
def generar_pdf(estilo, gente, tareas, descripcion):
    archivo = "reporte.pdf"
    doc = SimpleDocTemplate(archivo)
    styles = getSampleStyleSheet()

    contenido = []
    contenido.append(Paragraph("Reporte de Liderazgo", styles["Title"]))
    contenido.append(Spacer(1, 10))

    contenido.append(Paragraph(f"Estilo: {estilo}", styles["Heading2"]))
    contenido.append(Paragraph(f"Personas: {gente:.2f}", styles["Normal"]))
    contenido.append(Paragraph(f"Tareas: {tareas:.2f}", styles["Normal"]))

    contenido.append(Spacer(1, 10))
    contenido.append(Paragraph("Descripción:", styles["Heading3"]))
    contenido.append(Paragraph(descripcion, styles["Normal"]))

    contenido.append(Spacer(1, 10))
    contenido.append(Paragraph(f"Fecha: {datetime.now()}", styles["Normal"]))

    doc.build(contenido)
    return archivo

# -------------------------
# LOGICA
# -------------------------
if st.button("Enviar"):

    gente_idx = [0,3,5,8,9,11,13,15]
    tareas_idx = [1,2,4,6,7,10,12,14,16,17]

    gente = sum(respuestas[i] for i in gente_idx) * 0.2
    tareas = sum(respuestas[i] for i in tareas_idx) * 0.2

    def clasificar(g, t):
        if g <= 3 and t <= 3:
            return "Ajeno"
        elif g <= 3 and t > 3:
            return "Autoritario"
        elif g > 3 and t <= 3:
            return "Social"
        else:
            return "Líder de equipo"

    estilo = clasificar(gente, tareas)
    info = descripciones[estilo]

    # -------------------------
    # RESULTADO
    # -------------------------
    st.divider()
    st.markdown(f"## {info['emoji']} Estilo: {estilo}")

    st.markdown(f"""
    <div style="background-color:#f5f5f5; padding:20px; border-radius:10px;">
    <h4>🧠 Descripción</h4>
    <p>{info["texto"]}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col1.metric("Personas", f"{gente:.2f}")
    col2.metric("Tareas", f"{tareas:.2f}")

    # -------------------------
    # GRAFICA
    # -------------------------
    fig, ax = plt.subplots()
    ax.set_xlim(0.5, 9.5)
    ax.set_ylim(0.5, 9.5)
    ax.axhline(5)
    ax.axvline(5)
    ax.scatter(tareas, gente, s=150, color=color_map[estilo])
    ax.set_xlabel("Tareas")
    ax.set_ylabel("Personas")
    st.pyplot(fig)

    # -------------------------
    # PDF
    # -------------------------
    archivo_pdf = generar_pdf(estilo, gente, tareas, info["texto"])

    with open(archivo_pdf, "rb") as f:
        st.download_button(
            label="📥 Descargar reporte PDF",
            data=f,
            file_name="reporte_liderazgo.pdf",
            mime="application/pdf"
        )
