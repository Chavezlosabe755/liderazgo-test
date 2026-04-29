import streamlit as st
import pandas as pd
import os

st.title("Test de Liderazgo Blake & Mouton")

st.write("Responde cada pregunta de 0 (Nunca) a 5 (Siempre).")

preguntas = [
"1. Animo a los miembros de mi equipo a participar en la toma de decisiones.",
"2. Nada es más importante que completar un objetivo o tarea.",
"3. Monitoreo muy de cerca la duración de las tareas.",
"4. Me gusta ayudar a los demás a realizar nuevas tareas.",
"5. Cuanto más desafiante es la tarea, más lo disfruto.",
"6. Animo a mis colaboradores a ser creativos.",
"7. Me aseguro de todos los detalles en tareas complejas.",
"8. Me es fácil llevar varias tareas complicadas.",
"9. Leo sobre liderazgo y lo aplico.",
"10. Cuando corrijo errores no me preocupan las relaciones.",
"11. Administro mi tiempo con efectividad.",
"12. Me gusta explicar tareas complejas.",
"13. Divido proyectos en tareas manejables.",
"14. Desarrollar un gran equipo es clave.",
"15. Me gusta analizar problemas.",
"16. Respeto los límites de los demás.",
"17. Aconsejo a mis empleados.",
"18. Aplico lo que aprendo en mi profesión."
]

respuestas = []

for i, p in enumerate(preguntas):
    val = st.slider(p, 0, 5, 3)
    respuestas.append(val)

if st.button("Enviar"):
    
    # Índices (0-based)
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

    # Guardado anónimo
    df = pd.DataFrame([respuestas + [gente, tareas, estilo]],
                      columns=[f"P{i+1}" for i in range(18)] + ["Gente", "Tareas", "Estilo"])

    archivo = "resultados.csv"

    if not os.path.exists(archivo):
        df.to_csv(archivo, index=False)
    else:
        df.to_csv(archivo, mode='a', header=False, index=False)

    st.success("Respuesta guardada de forma anónima ✅")

    st.subheader("Tu resultado:")
    st.write(f"Gente: {gente:.2f}")
    st.write(f"Tareas: {tareas:.2f}")
    st.write(f"Estilo: **{estilo}**")
    

