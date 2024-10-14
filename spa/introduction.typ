= Introducción

== _Motivación_

La industria de servicios financieros ha presenciado un cambio de paradigma hacia la personalización, impulsado por la evolución de las expectativas de los clientes y los avances en tecnología. Los servicios de asesoría financiera personalizados se han vuelto esenciales para atender los objetivos financieros únicos, apetitos de riesgo y circunstancias de vida de cada cliente. Sin embargo, los modelos de asesoría tradicionales luchan por ofrecer consejos personalizados a gran escala debido a su dependencia de procesos manuales y capacidades limitadas de integración de datos.

Al mismo tiempo, la proliferación de datos de diversas fuentes—incluyendo registros transaccionales, datos de mercado, redes sociales y actualizaciones regulatorias—presenta tanto una oportunidad como un desafío. Las instituciones financieras poseen grandes cantidades de datos estructurados y no estructurados que, si se aprovechan eficazmente, pueden mejorar significativamente la personalización de los servicios de asesoría. La integración e interpretación de estos datos heterogéneos excede las capacidades de los métodos convencionales de procesamiento y análisis de datos.

La Generación Aumentada por Recuperación (RAG, por sus siglas en inglés) ha surgido como un enfoque prometedor que combina las fortalezas de los grandes modelos de lenguaje (LLM) con sistemas de recuperación de información. Al aprovechar grafos de conocimiento o bases de datos gráficas, RAG puede acceder e integrar vastos conjuntos de datos interconectados para generar resultados contextualmente relevantes y personalizados. Los grafos de conocimiento proporcionan una representación estructurada de la información, capturando entidades y sus relaciones, lo cual es particularmente ventajoso para modelar dominios financieros complejos.

Esta tesis explora la aplicación de RAG sobre grafos de conocimiento para abordar los desafíos de ofrecer servicios de asesoría financiera personalizados a gran escala. La premisa central es que la integración de RAG con grafos de conocimiento puede permitir la generación de consejos financieros personalizados mediante la recuperación de datos relevantes específicos del cliente y la aplicación de técnicas sofisticadas de procesamiento de lenguaje natural.

== _Declaración del Problema_

A pesar de los posibles beneficios, varios obstáculos impiden la implementación efectiva de servicios de asesoría personalizados utilizando métodos tradicionales:

1. *Silos de Datos y Fragmentación*: Los datos financieros a menudo están dispersos en múltiples sistemas y formatos, lo que dificulta un análisis completo.
2. *Problemas de Escalabilidad*: La personalización manual requiere mucho trabajo y no es factible para grandes bases de clientes.
3. *Cumplimiento Regulatorio*: Asegurar que los consejos cumplan con regulaciones en constante cambio añade complejidad al proceso de asesoría.
4. *Transparencia y Explicabilidad*: Clientes y reguladores exigen explicaciones claras para los consejos, lo cual es un desafío con modelos de IA opacos.

== _Objetivos_

El objetivo principal de esta investigación es desarrollar un marco que utilice Generación Aumentada por Recuperación en grafos de conocimiento para mejorar los servicios de asesoría financiera personalizados. Los objetivos específicos incluyen:

- *Diseñar un Modelo de Grafo de Conocimiento*: Construir un grafo de conocimiento financiero que integre datos de clientes, productos financieros, tendencias del mercado e información regulatoria.
- *Implementar Técnicas de RAG*: Aplicar RAG para recuperar información relevante del grafo de conocimiento y generar consejos personalizados.
- *Asegurar Cumplimiento y Explicabilidad*: Incorporar mecanismos para producir consejos que cumplan con las regulaciones y sean explicables para los clientes.
- *Evaluar la Efectividad*: Evaluar el rendimiento del marco propuesto en términos de precisión de personalización, escalabilidad y satisfacción del usuario en comparación con métodos tradicionales.

== _Significado del Estudio_

Esta investigación contribuye a los campos de la inteligencia artificial y la tecnología financiera mediante:

- *Avanzar en Aplicaciones de IA en Finanzas*: Demostrar cómo técnicas avanzadas de IA pueden abordar desafíos reales de asesoría financiera.
- *Mejorar la Personalización*: Proporcionar una solución escalable para ofrecer consejos financieros personalizados a una amplia base de clientes.
- *Mejorar la Utilización de Datos*: Mostrar la integración efectiva de fuentes de datos financieras heterogéneas a través de grafos de conocimiento.
- *Facilitar el Cumplimiento Regulatorio*: Ofrecer un método para generar consejos alineados con los requisitos regulatorios y transparentes en su justificación.