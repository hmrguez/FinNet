== Conclusiones

Esta tesis exploró el desarrollo de un sistema de preguntas y respuestas para la planificación financiera impulsado por un sistema de generación aumentada por recuperación (RAG) basado en grafos. Las etapas de investigación e implementación destacaron el potencial del sistema para transformar la planificación financiera al combinar técnicas avanzadas de recuperación con la generación de lenguaje natural. Se pueden extraer las siguientes conclusiones de este estudio:

El uso de sistemas RAG basados en grafos demostró ser eficaz para gestionar las complejidades de los datos financieros. Las estructuras de grafos permitieron la representación de relaciones matizadas entre conceptos financieros, mientras que la recuperación basada en incrustaciones garantizó la flexibilidad semántica en el manejo de diversas consultas de los usuarios. Este enfoque híbrido abordó desafíos específicos del dominio, como la relevancia contextual, la representación precisa de las dependencias financieras y la comprensión de la intención del usuario.

La integración de Neo4j para el almacenamiento de grafos y MongoDB para la recuperación basada en incrustaciones permitió una consulta y una gestión del conocimiento eficientes. La capacidad de extraer subgrafos relevantes para las consultas de los usuarios demostró la capacidad del sistema para ofrecer respuestas precisas y contextualmente apropiadas, lo que lo hace particularmente adecuado para tareas de planificación financiera personal.

La adopción de la ingeniería de prompts zero-shot a través de la API de Gemini permitió al sistema generar respuestas en lenguaje natural de alta calidad sin un entrenamiento extenso en datos específicos del dominio. Este enfoque no solo redujo los costos de desarrollo, sino que también proporcionó adaptabilidad a la evolución del conocimiento financiero y las necesidades de los usuarios.

El rendimiento del sistema, medido por la precisión, la corrección fáctica, la eficiencia y la robustez, validó la viabilidad de los sistemas RAG basados en grafos para aplicaciones fintech. Las pruebas destacaron áreas de mejora, particularmente en el manejo de consultas ambiguas y la optimización de estrategias de recuperación, allanando el camino para futuras mejoras.

Este estudio contribuye al creciente cuerpo de investigación sobre soluciones fintech inteligentes al presentar un marco modular, impulsado por grafos, para el desarrollo de sistemas de preguntas y respuestas. Su metodología, que enfatiza la escalabilidad, la riqueza semántica y la rentabilidad, puede servir como base para una mayor innovación en este dominio.

= Limitaciones y trabajo futuro

A pesar de sus prometedores resultados, este estudio enfrentó limitaciones que presentan oportunidades para una mayor exploración:
- Desafíos de escalabilidad: A medida que crece el grafo de conocimiento, la eficiencia computacional y la velocidad de recuperación pueden necesitar optimización.
- Adaptación al dominio: Si bien es eficaz en la planificación financiera, la adaptabilidad del sistema a otros dominios aún debe probarse.
- Métricas de evaluación mejoradas: La incorporación de la satisfacción del usuario y el compromiso a largo plazo en el marco de evaluación proporcionaría información más profunda sobre la aplicabilidad en el mundo real.

La investigación futura podría centrarse en refinar las técnicas de extracción de subgrafos, explorar la integración de datos multimodales y mejorar la personalización del asesoramiento financiero al proporcionar información sensible al contexto del usuario. Además, extender el sistema para manejar datos y transacciones en tiempo real aumentaría su utilidad práctica.

Al integrar técnicas avanzadas de recuperación y generación, esta tesis demuestra cómo un sistema RAG basado en grafos puede brindar asesoramiento financiero personalizado, ofreciendo un paso prometedor en la evolución de las aplicaciones fintech inteligentes.