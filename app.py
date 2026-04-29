import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

st.set_page_config(page_title="Test de Liderazgo", layout="centered")

st.title("🧠 Test de Liderazgo Blake & Mouton")
st.write("Selecciona un valor de 0 (Nunca) a 5 (Siempre).")

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
    st.markdown(f"**{i+1}. {p}**")
    val = st.radio("Selecciona:", [0,1,2,3,4,5], horizontal=True, key=f"q{i}")
    respuestas.append(val)

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

    # Guardar resultados
    df = pd.DataFrame([respuestas + [gente, tareas, estilo]],
                      columns=[f"P{i+1}" for i in range(18)] + ["Gente", "Tareas", "Estilo"])

    archivo = "resultados.csv"

    if not os.path.exists(archivo):
        df.to_csv(archivo, index=False)
    else:
        df.to_csv(archivo, mode='a', header=False, index=False)

    st.success("Respuesta guardada de forma anónima ✅")

    # Resultados
    st.subheader("📊 Tu resultado")
    st.write(f"Gente: {gente:.2f}")
    st.write(f"Tareas: {tareas:.2f}")
    st.write(f"Estilo: **{estilo}**")

    # 📈 Gráfica correcta
    fig, ax = plt.subplots(figsize=(6,6))

    ax.set_xlim(1, 9)
    ax.set_ylim(1, 9)

    # Cuadrantes
    ax.axhline(5)
    ax.axvline(5)

    # Etiquetas
    ax.text(3, 7, "Social", ha='center')
    ax.text(7, 7, "Líder de equipo", ha='center')
    ax.text(3, 3, "Ajeno", ha='center')
    ax.text(7, 3, "Autoritario", ha='center')

    # Ejes
    ax.set_xlabel("Tareas")
    ax.set_ylabel("Personas")

    ax.set_xticks(range(1,10))
    ax.set_yticks(range(1,10))

    # Punto
    ax.scatter(tareas, gente, s=120)

    # Líneas guía
    ax.axhline(y=gente, linestyle='--')
    ax.axvline(x=tareas, linestyle='--')

    ax.grid(True)

    st.pyplot(fig)
