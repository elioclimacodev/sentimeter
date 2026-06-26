# SentiMiner - Exposicion al Directorio Ejecutivo

## Analisis de Sentimientos con Inteligencia Artificial

---

## 1. El Problema de Negocio

### Contexto

Las organizaciones generan y reciben diariamente grandes volumenes de texto: encuestas de satisfaccion, retroalimentacion de clientes, quejas y reclamaciones, comunicados de prensa, publicaciones en redes sociales, actas de reuniones, informes de campo, correspondencia institucional y documentos de inteligencia.

### El problema concreto

Actualmente, el analisis de sentimiento de estos documentos se realiza de forma **manual**. Un equipo de personas lee cada documento, clasifica el tono emocional y registra los resultados en hojas de calculo o bases de datos.

**Cuantificacion del impacto:**

| Metrica actual | Estimacion |
|----------------|------------|
| Tiempo promedio por documento (100 lineas) | 15 a 25 minutos de revision humana |
| Documentos analizados manualmente al mes (organizacion mediana) | 50 a 200 documentos |
| Horas-hombre dedicadas al mes | 25 a 100 horas |
| Costo estimado por hora de analista | S/ 4 a S/ 4.7 |
| Costo mensual estimado del analisis manual | S/ 1130.00|
| Errores de clasificacion humana por fatiga | 10% a 25% de los documentos |
| Tiempo de respuesta para tomar una decision | Dias a semanas |

### Consecuencias

- **Decisiones lentas**: La informacion llega a los directivos con retraso, cuando los problemas ya escalaron.
- **Sesgo subjetivo**: Diferentes analistas pueden interpretar el mismo texto de forma distinta.
- **Escalabilidad limitada**: Si el volumen de documentos se duplica, se necesita duplicar el personal.
- **Riesgos no detectados**: Tendencias negativas en la percepcion de clientes o ciudadanos pasan desapercibidas hasta que se convierten en crisis.
- **Costo oculto**: El tiempo dedicado a tareas repetitivas de lectura y clasificacion es tiempo que no se invierte en estrategia.

---

## 2. La Solucion: SentiMiner

### Que es

SentiMiner es un sistema de analisis sentimental basado en inteligencia artificial que procesa archivos de texto y clasifica automaticamente cada linea como **positiva**, **negativa** o **neutra**, asignando un puntaje de polaridad numerico y generando reportes visuales e interactivos.

### Como funciona (resumen ejecutivo)

1. El usuario sube un archivo de texto (.txt) a traves de la interfaz web o lo procesa desde la linea de comandos.
2. El sistema detecta automaticamente el idioma (espanol o ingles).
3. Utiliza modelos de IA pre-entrenados para clasificar cada linea del documento.
4. Genera un dashboard con graficos interactivos que muestran la distribucion de sentimientos y su evolucion a lo largo del texto.
5. Permite exportar los resultados a CSV o TXT para su uso en otras herramientas.

### Arquitectura tecnica

| Componente | Tecnologia | Funcion |
|------------|------------|---------|
| Backend | Django 6.0.5 | Logica de negocio, gestion de datos, endpoints |
| Analisis de sentimientos (espanol) | pysentimiento | Modelo de IA pre-entrenado para espanol |
| Analisis de sentimientos (ingles) | VADER | Reglas lexicales para ingles como respaldo |
| Visualizacion | Plotly | Graficos interactivos (pastel y tendencia) |
| Interfaz web | HTMX + Alpine.js + Tabler | Carga asincrona, interactividad ligera, diseno responsivo |
| Base de datos | SQLite | Almacenamiento local de resultados |
| Comando de consola | Python/Django management | Analisis desde terminal sin interfaz web |

**Nota importante**: El sistema opera de forma **local**. No se envian datos a servicios externos en la nube. Los modelos de IA se ejecutan en el servidor de la organizacion, garantizando la confidencialidad de la informacion.

---

## 3. Beneficios Estrategicos

### 3.1 Toma de decisiones basada en datos

SentiMiner transforma texto no estructurado en **datos cuantificables**. En lugar de opiniones subjetivas sobre como se sienten los clientes o ciudadanos, el directorio obtiene:

- **Porcentajes exactos**: "El 68% de los comentarios sobre el nuevo servicio son positivos, el 19% negativos y el 13% neutros."
- **Tendencias detectables**: El grafico de linea muestra si la percepcion mejora o empeora a lo largo del tiempo o del documento.
- **Puntajes numericos**: Cada linea recibe un valor de polaridad de -1 a +1, permitiendo comparaciones cuantitativas.
- **Sentimiento predominante**: Resumen automatico del tono general del documento.

### 3.2 Deteccion temprana de riesgos

El sistema identifica tendencias negativas **antes** de que se conviertan en problemas mayores:

- Una encuesta de satisfaccion donde el 40% de las respuestas son negativas genera una alerta automatica.
- Un documento de inteligencia con picos negativos en el grafico de tendencia indica un punto de crisis.
- La comparacion entre documentos permite detectar deterioro en la percepcion a lo largo del tiempo.

### 3.3 Ahorro de tiempo

| Proceso | Sin SentiMiner | Con SentiMiner | Reduccion |
|---------|---------------|----------------|-----------|
| Analisis de 100 lineas | 15-25 min | 2-3 segundos | 99.8% |
| Analisis de 1,000 lineas | 2.5-4 horas | 5-8 segundos | 99.9% |
| Analisis de 10,000 lineas | 25-40 horas | 30-50 segundos | 99.97% |
| Generacion de reporte | 30-60 min adicionales | Automatico e inmediato | 100% |

### 3.4 Escalabilidad

El sistema puede analizar cientos o miles de documentos **sin aumentar personal**. La capacidad de procesamiento depende del hardware del servidor, no del numero de analistas. Esto permite:

- Procesar encuestas masivas de ciudadanos en minutos.
- Analizar redes sociales a gran escala.
- Revisar historiales completos de atencion al cliente.

### 3.5 Transformacion digital

SentiMiner incorpora inteligencia artificial en procesos institucionales de forma practica y tangible:

- No requiere conocimientos tecnicos avanzados para usarlo.
- Los resultados se presentan de forma visual e intuitiva.
- Integra IA sin depender de servicios externos o costos recurrentes de licencias.
- Sirve como base para futuros proyectos de inteligencia artificial en la organizacion.

---

## 4. Reduccion de Riesgos

### Riesgos mitigados

| Riesgo | Como SentiMiner lo mitiga |
|--------|---------------------------|
| Perdida de oportunidades por no detectar insatisfaccion | Clasificacion automatica y alerta por porcentajes negativos |
| Crisis reputacional por respuesta tardia | Analisis en segundos, no en dias |
| Decisiones basadas en percepciones, no en datos | Porcentajes y graficos objetivos |
| Dependencia de personal especializado | Sistema automatizado que no requiere expertos en analisis textual |
| Sujecion a sesgo individual del analista | Modelo de IA consistente y replicable |
| Sobrecosto operativo por aumento de volumen | Escalabilidad sin aumento de personal |

---

## 5. Casos de Uso

### 5.1 Recursos Humanos

**Encuestas de clima laboral**: Analizar automaticamente las respuestas abiertas de las encuestas de satisfaccion interna para identificar areas de mejora y detectar desmotivacion antes de que aumente la rotacion.

**Retroalimentacion de desempeño**: Clasificar comentarios de evaluaciones 360 para obtener una vision objetiva del tono general hacia cada colaborador o departamento.

**Buzon de quejas**: Procesar miles de comentarios anónimos para identificar patrones de insatisfaccion en areas especificas.

### 5.2 Gobierno

**Percepcion ciudadana**: Analizar respuestas de consultas publicas, encuestas de satisfaccion con servicios gubernamentales o comentarios en plataformas de participacion ciudadana.

**Inteligencia de comunicados**: Procesar notas de prensa, documentos de oposición o comunicaciones para detectar el tono predominante hacia politicas publicas.

**Seguimiento a interventiones**: Medir como cambia la percepcion ciudadana despues de la implementacion de un programa o politica publica.

**Atencion al ciudadano**: Clasificar automaticamente las quejas y sugerencias que llegan por canales digitales para priorizar las mas urgentes.

### 5.3 Empresas Privadas

**Experiencia del cliente (CX)**: Analizar reseñas, encuestas NPS, comentarios de redes sociales y correos de soporte para medir la satisfaccion del cliente a escala.

**Investigacion de mercado**: Procesar retroalimentacion de focus groups o entrevistas para identificar sentimientos hacia productos o marcas.

**Monitoreo de marca**: Analizar menciones en redes sociales o foros para detectar crisis reputacionales en tiempo real.

**Soporte al cliente**: Clasificar tickets de soporte por tono emocional para priorizar los casos mas urgentes o delicados.

**Ventas**: Analizar comunicaciones con clientes para identificar oportunidades de mejora en el proceso comercial.

---

## 6. Retorno de la Inversión (ROI)

### Inversion estimada (MVP actual)

| Concepto | Costo estimado |
|----------|----------------|
| Desarrollo del sistema (MVP funcional) | Inversion en tiempo de desarrollo |
| Infraestructura de servidor | Servidor existente o $50-$200/mes (cloud) |
| Licencias de software | $0 (tecnologias de codigo abierto) |
| Costo recurrente de IA | $0 (modelos locales, sin APIs externas) |
| Mantenimiento anual estimado | $200-$500 (soporte tecnico) |

### Retorno calculado

**Escenario conservador** (organizacion mediana, 100 documentos/mes):

| Concepto | Sin SentiMiner | Con SentiMiner |
|----------|---------------|----------------|
| Horas de analista al mes | 50 horas | 2 horas (supervision) |
| Costo de analista al mes ($25/hr) | $1,250 | $50 |
| Ahorro mensual | - | $1,200 |
| Ahorro anual | - | **$14,400** |
| ROI primer anual | - | **Elevado** (inversion unica vs. ahorro recurrente) |

**Escenario escalado** (organizacion grande, 1,000 documentos/mes):

| Concepto | Sin SentiMiner | Con SentiMiner |
|----------|---------------|----------------|
| Horas de analista al mes | 500 horas | 10 horas |
| Costo de analista al mes ($25/hr) | $12,500 | $250 |
| Ahorro mensual | - | $12,250 |
| Ahorro anual | - | **$147,000** |

---

## 7. Linea de Tiempo de Implementacion

### Fase 1: MVP Funcional (Completada)

**Duracion**: Fase actual
**Estado**: Implementada y operativa

- Analisis de archivos .txt linea por linea
- Clasificacion en positivo, negativo y neutro
- Deteccion automatica de idioma (espanol/ingles)
- Dashboard web con graficos interactivos
- Exportacion a CSV y TXT
- Comando de consola para analisis desde terminal
- Suite de pruebas automatizadas

### Fase 2: Integracion y Escalamiento (3 a 6 meses)

**Objetivo**: Conectar SentiMiner con los flujos de datos reales de la organizacion.

- Conexion con bases de datos de atencion al cliente (tickets, encuestas)
- Importacion automatica desde archivos Excel, CSV o APIs internas
- Soporte para archivos PDF y Word
- Autenticacion y control de accesos por rol
- Despliegue en servidor de produccion con acceso por red interna
- Integracion con herramientas de reportes existentes

### Fase 3: Analisis Avanzado (6 a 12 meses)

**Objetivo**: Agregar capacidades analiticas mas profundas.

- Analisis de sentimientos por temas o categorias (no solo por linea)
- Deteccion de emociones especificas (alegria, enojo, miedo, sorpresa)
- Comparacion entre documentos o periodos
- Alertas automaticas cuando los indicadores negativos superan un umbral
- Reportes programados (diarios, semanales, mensuales)
- API REST para integracion con otros sistemas de la organizacion

### Fase 4: Inteligencia Institucional (12 a 24 meses)

**Objetivo**: Consolidar una plataforma de inteligencia artificial para la organizacion.

- Modelos de prediccion de tendencias (tono futuro basado en historial)
- Si la organización planea expandirse internacinalmente, se puede implementar el análisis multilingue expandido a otros idiomas.
- Procesamiento de audio (transcripcion + analisis de sentimiento en voz)
- Integracion con dashboards ejecutivos en tiempo real
- Capacitacion de modelos propios con datos historicos de la organizacion
- Plataforma de IA reutilizable para otros proyectos institucionales

---

## 8. Valor Economico para la Organizacion

### Que gana la organizacion

| Beneficio | Descripcion | Impacto |
|-----------|-------------|---------|
| **Menor tiempo de analisis** | De horas a segundos por documento | Reduccion del 99% en tiempo de procesamiento |
| **Menor costo operativo** | Menos horas de personal dedicado a tareas repetitivas | Ahorro de $14,400 a $147,000 USD anuales segun escala |
| **Decisiones mas rapidas** | Informacion disponible en tiempo real, no en dias | Reaccion oportuna ante crisis y oportunidades |
| **Mayor capacidad de procesamiento** | Miles de documentos sin contratar personal adicional | Escalabilidad sin costo variable proporcional |
| **Incorporacion de IA institucional** | Inteligencia artificial funcionando en procesos reales | Base para futuros proyectos de automatizacion |
| **Base tecnologica para futuros proyectos** | Arquitectura modular y extensible | Plataforma reutilizable para otros usos de IA |
| **Confidencialidad de datos** | Modelos locales sin envio a la nube | Cumplimiento de politicas de seguridad de la informacion |
| **Consistencia en el analisis** | Modelo de IA que clasifica igual siempre | Eliminacion del sesgo subjetivo del analista humano |

### Resumen ejecutivo

SentiMiner resuelve un problema real de negocio: la imposibilidad de procesar manualmente el creciente volumen de texto que generan y reciben las organizaciones. Con una inversion inicial en una solucion de codigo abierto, se obtiene un ahorro recurrente significativo, se reducen riesgos por deteccion tardia de problemas, y se construye la base tecnologica para futuros proyectos de inteligencia artificial.

La pregunta no es si la organizacion puede permitirse implementar esta solucion. La pregunta es si puede permitirse **no** tenerla.

---

*Grupo 3* - 
*Curso: Proyectos de Disrupción Tecnológica* -
*UPN*
