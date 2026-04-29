import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="Test de Liderazgo", layout="centered")

st.title("Test de Liderazgo Blake & Mouton")
st.write("Es un cuestionario de 18 preguntas, divididas en dos dimensiones: preguntas 
orientadas a personas y preguntas orientadas a tareas. 
El resultado nos puede decir si somos líderes orientados más a tareas o a las 
personas. 
Se debe contestar cada pregunta asignándole un valor de 0 a 5, donde 0 el más bajo o 
nunca y 5 el más alto o siempre. 
Abajo encontrarás una lista de declaraciones acerca de la conducta de un líder. Lee 
cada una cuidadosamente, luego utilizando la escala provista decide qué conducta se 
aplica más a ti. Para lograr los mejores resultados, trata de responder lo más honesto 
posible.")

# Preguntas
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

# Formulario
for i, p in enumerate(preguntas):
    st.markdown(f"**{i+1}. {p}**")
    val = st.radio("Selecciona:", [0,1,2,3,4,5], horizontal=True, key=f"q{i}")
    respuestas.append(val)

# Descripciones
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

    # Guardar resultados (local)
    df = pd.DataFrame([respuestas + [gente, tareas, estilo]],
                      columns=[f"P{i+1}" for i in range(18)] + ["Gente", "Tareas", "Estilo"])

    archivo = "resultados.csv"

    if not os.path.exists(archivo):
        df.to_csv(archivo, index=False)
    else:
        df.to_csv(archivo, mode='a', header=False, index=False)

    st.success("Respuesta guardada de forma anónima ✅")

    # Mostrar resultado
    info = descripciones[estilo]

    st.markdown(f"## {info['emoji']} Estilo: {estilo}")
    st.info(info["texto"])

    col1, col2 = st.columns(2)
    col1.metric("Personas", f"{gente:.2f}")
    col2.metric("Tareas", f"{tareas:.2f}")

    # Interpretación
    st.markdown("### 📌 Interpretación")

    if estilo == "Líder de equipo":
        st.success("Perfil balanceado, ideal para liderazgo efectivo.")
    elif estilo == "Autoritario":
        st.warning("Gran enfoque en resultados, mejora relaciones.")
    elif estilo == "Social":
        st.warning("Buen manejo de personas, refuerza ejecución.")
    else:
        st.error("Desarrolla enfoque en personas y tareas.")

    # 📈 Gráfica estilo Blake & Mouton
    fig, ax = plt.subplots(figsize=(6,6))

    ax.set_xlim(0.5, 9.5)
    ax.set_ylim(0.5, 9.5)

    ax.axhline(5)
    ax.axvline(5)

    ax.text(3, 7, "Social", ha='center')
    ax.text(7, 7, "Líder de equipo", ha='center')
    ax.text(3, 3, "Ajeno", ha='center')
    ax.text(7, 3, "Autoritario", ha='center')

    ax.set_xlabel("Tareas")
    ax.set_ylabel("Personas")

    ax.set_xticks(range(1,10))
    ax.set_yticks(range(1,10))

    ax.scatter(tareas, gente, 
               s=150, 
               color=color_map[estilo], 
               edgecolors='black')

    ax.axhline(y=gente, linestyle='--')
    ax.axvline(x=tareas, linestyle='--')

    ax.grid(True)

    st.pyplot(fig)
