# SentiMiner

## Análisis de Sentimientos con Inteligencia Artificial

### Exposición al Directorio Ejecutivo

---

## Resumen Ejecutivo

Las organizaciones reciben y generan diariamente miles de textos: encuestas, quejas, retroalimentación de clientes, comunicados, actas y documentos internos. Actualmente, analizar el tono emocional de estos documentos es un proceso **manual, lento y costoso** que genera decisiones atrasadas y riesgos no detectados.

**SentiMiner** es una herramienta de inteligencia artificial que procesa texto automáticamente, clasificando cada línea como positiva, negativa o neutra en **segundos**. Opera completamente **de forma local**, sin enviar datos a la nube, garantizando la confidencialidad de la información. Está desarrollada con **tecnologías de código abierto**, eliminando costos de licencias.

**El resultado:** ahorro de hasta **$147,000 USD anuales**, decisiones basadas en datos reales, detección temprana de riesgos y una base tecnológica sólida para la transformación digital de la organización.

---

## 1. Contexto

### El volumen de texto es creciente e inmanejable

| Fuente de datos | Volumen típico |
|-----------------|----------------|
| Encuestas de satisfacción | 200-2,000 respuestas abiertas por ciclo |
| Quejas y reclamaciones | 100-500 documentos mensuales |
| Redes sociales y reseñas | Miles de menciones diarias |
| Actas y comunicados internos | 50-200 documentos mensuales |
| Evaluaciones de desempeño | 100-1,000 comentarios por evaluación |

### El problema actual

Este análisis se realiza de forma **manual**. Un equipo de personas lee cada documento, clasifica el tono y registra resultados en hojas de cálculo.

**Cuantificación del impacto actual:**

| Métrica | Estimación |
|---------|------------|
| Tiempo por documento (100 líneas) | 15 a 25 minutos |
| Documentos analizados al mes | 50 a 200 |
| Horas-hombre dedicadas al mes | 25 a 100 horas |
| Errores de clasificación por fatiga humana | 10% a 25% |
| Tiempo para tomar una decisión | Días a semanas |

---

## 2. Objetivo del Proyecto

Desarrollar un sistema de análisis sentimental basado en inteligencia artificial que:

- Procese automáticamente grandes volúmenes de texto
- Clasifique sentimientos de forma objetiva y consistente
- Genere reportes visuales para la toma de decisiones
- Opere de forma local protegiendo la confidencialidad
- Funcione sin costos recurrentes de licencias o servicios externos

---

## 3. Problemas que Resuelve

### Dolor que enfrenta la organización

| Problema | Impacto en el negocio |
|----------|----------------------|
| **Lentitud en el análisis** | Los problemas de clientes o ciudadanos se detectan cuando ya son crisis |
| **Sesgo subjetivo** | Diferentes analistas interpretan el mismo texto de forma distinta |
| **Escalabilidad limitada** | Si el volumen se duplica, se debe duplicar el personal |
| **Costo oculto** | El tiempo en tareas repetitivas es tiempo que no se invierte en estrategia |
| **Información dispersa** | No existe una visión consolidada del sentimiento general |

### Consecuencias de no actuar

- **Pérdida de clientes** por no detectar insatisfacción a tiempo
- **Crisis reputacionales** que escalan por respuesta tardía
- **Decisiones basadas en percepciones**, no en datos objetivos
- **Dependencia de personal especializado** que puede rotar o ausentarse
- **Sobrecosto operativo** que crece proporcionalmente al volumen

---

## 4. La Solución: SentiMiner

### ¿Qué es?

SentiMiner es un sistema de análisis sentimental que utiliza inteligencia artificial para procesar archivos de texto y clasificar automáticamente cada línea como **positiva**, **negativa** o **neutra**, asignando un puntaje numérico y generando reportes visuales interactivos.

### ¿Cómo funciona?

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUJO DE PROCESAMIENTO                   │
└─────────────────────────────────────────────────────────────┘

  ┌──────────┐    ┌──────────────┐    ┌──────────────────┐
  │  ARCHIVO │───▶│  DETECCIÓN   │───▶│   ANÁLISIS DE    │
  │  .TXT    │    │  DE IDIOMA   │    │   SENTIMIENTOS   │
  └──────────┘    └──────────────┘    └──────────────────┘
                         │                      │
                         ▼                      ▼
                  ┌──────────────┐    ┌──────────────────┐
                  │   ESPAÑOL    │    │    CLASIFICA     │
                  │  pysentim.   │    │  Positivo/Negat. │
                  └──────────────┘    │    /Neutro       │
                                      └──────────────────┘
                         │                      │
                         ▼                      ▼
                  ┌──────────────┐    ┌──────────────────┐
                  │    INGLÉS    │    │   GUARDA EN      │
                  │    VADER     │    │   BASE DATOS     │
                  └──────────────┘    └──────────────────┘
                                                 │
                                                 ▼
                                      ┌──────────────────┐
                                      │   GENERA         │
                                      │   • Porcentajes  │
                                      │   • Gráficos     │
                                      │   • Reportes     │
                                      └──────────────────┘
```

### Pasos del proceso

1. **Subida**: El usuario carga un archivo .txt desde la web o consola
2. **Detección**: El sistema identifica automáticamente el idioma
3. **Análisis**: Modelos de IA clasifican cada línea del documento
4. **Visualización**: Se genera un dashboard con gráficos interactivos
5. **Exportación**: Los resultados se descargan en CSV o TXT

---

## 5. Cuánto Vale para la Empresa

### Ahorro de tiempo

| Proceso | Sin SentiMiner | Con SentiMiner | Reducción |
|---------|---------------|----------------|-----------|
| 100 líneas | 15-25 minutos | 2-3 segundos | **99.8%** |
| 1,000 líneas | 2.5-4 horas | 5-8 segundos | **99.9%** |
| 10,000 líneas | 25-40 horas | 30-50 segundos | **99.97%** |
| Generación de reporte | 30-60 min adicionales | Automático e inmediato | **100%** |

### Ahorro económico

**Escenario conservador** (100 documentos/mes):

| Concepto | Sin SentiMiner | Con SentiMiner |
|----------|---------------|----------------|
| Horas de analista | 50 horas/mes | 2 horas/mes |
| Costo mensual | $1,250 USD | $50 USD |
| **Ahorro anual** | - | **$14,400 USD** |

**Escenario escalado** (1,000 documentos/mes):

| Concepto | Sin SentiMiner | Con SentiMiner |
|----------|---------------|----------------|
| Horas de analista | 500 horas/mes | 10 horas/mes |
| Costo mensual | $12,500 USD | $250 USD |
| **Ahorro anual** | - | **$147,000 USD** |

---

## 6. Beneficios Estratégicos

### Toma de decisiones basada en datos

SentiMiner transforma texto no estructurado en **datos cuantificables**:

- **Porcentajes exactos**: "El 68% de los comentarios son positivos, el 19% negativos"
- **Tendencias detectables**: Gráficos que muestran si la percepción mejora o empeora
- **Puntajes numéricos**: Cada línea recibe un valor de -1 a +1
- **Sentimiento predominante**: Resumen automático del tono general

### Detección temprana de riesgos

- Encuesta con 40% de respuestas negativas → **alerta automática**
- Picos negativos en gráfico de tendencia → **punto de crisis identificado**
- Comparación entre documentos → **deterioro detectado a tiempo**

### Ahorro de tiempo

- De horas a segundos por documento
- Personal liberado para tareas de mayor valor estratégico

### Escalabilidad

- Analiza cientos o miles de documentos **sin contratar personal adicional**
- Capacidad limitada solo por el hardware del servidor

### Transformación digital

- Incorpora IA en procesos institucionales de forma práctica
- No requiere conocimientos técnicos avanzados
- Base para futuros proyectos de automatización

### Reducción de riesgos

| Riesgo | Cómo SentiMiner lo mitiga |
|--------|---------------------------|
| Pérdida de oportunidades | Clasificación automática y alertas |
| Crisis reputacional | Análisis en segundos, no en días |
| Decisiones subjetivas | Datos objetivos y porcentajes |
| Dependencia de personal | Sistema automatizado y replicable |
| Sobrecosto por volumen | Escalabilidad sin costo variable |

---

## 7. Privacidad y Confidencialidad

### Ventaja competitiva: operación 100% local

A diferencia de soluciones que envían datos a la nube (OpenAI API, Google Cloud AI, AWS Comprehend), **SentiMiner ejecuta todos los modelos de inteligencia artificial en el servidor de la organización**.

| Característica | Soluciones en la nube | SentiMiner |
|----------------|----------------------|------------|
| Ubicación de los datos | Servidores externos | **Servidor local** |
| Riesgo de fuga de información | Alto | **Mínimo** |
| Cumplimiento de políticas de seguridad | Complejo | **Simple** |
| Costo recurrente por uso | Sí (por API call) | **No** |
| Funcionamiento sin internet | No | **Sí** |

**Beneficio clave**: Entrevistas sensibles, quejas de clientes, información estratégica y documentos internos **nunca salen de la organización**.

---

## 8. Ahorro en Licencias de Software

### Todo se desarrolló con software libre

| Componente | Tecnología | Costo de licencia |
|------------|------------|-------------------|
| Backend | Django (Python) | **$0** |
| Análisis de sentimientos | pysentimiento | **$0** |
| Análisis en inglés | VADER | **$0** |
| Visualización de datos | Plotly | **$0** |
| Interfaz web | HTMX + Alpine.js | **$0** |
| Base de datos | SQLite | **$0** |
| Framework CSS | Tabler | **$0** |

**Costo total de licencias: $0 USD**

Compare con soluciones comerciales que cobran entre $500 y $5,000 mensuales por licencias de software de análisis de sentimientos.

---

## 9. Casos de Uso

### Empresas Privadas

- **Experiencia del cliente (CX)**: Analizar reseñas, encuestas NPS, comentarios de redes sociales
- **Investigación de mercado**: Procesar retroalimentación de focus groups y entrevistas
- **Monitoreo de marca**: Detectar crisis reputacionales en tiempo real
- **Soporte al cliente**: Clasificar tickets por urgencia emocional
- **Ventas**: Identificar oportunidades de mejora en el proceso comercial

### Recursos Humanos

- **Encuestas de clima laboral**: Detectar desmotivación antes de que aumente la rotación
- **Evaluaciones 360**: Obtener visión objetiva del tono hacia cada colaborador
- **Buzón de quejas**: Identificar patrones de insatisfacción en áreas específicas

### Gobierno

- **Percepción ciudadana**: Analizar respuestas de consultas públicas y encuestas
- **Inteligencia comunicacional**: Detectar tono hacia políticas públicas
- **Seguimiento a intervenciones**: Medir cambios de percepción post-implementación
- **Atención al ciudadano**: Priorizar quejas y sugerencias por urgencia

---

## 10. Inversión Estimada (MVP Actual)

| Concepto | Costo |
|----------|-------|
| Desarrollo del sistema (MVP funcional) | Inversión en tiempo de desarrollo |
| Infraestructura | Servidor existente o $50-$200/mes (nube) |
| Licencias de software | **$0** (código abierto) |
| Costo recurrente de IA | **$0** (modelos locales) |
| Mantenimiento anual | $200-$500 (soporte técnico) |

---

## 11. Línea de Tiempo de Implementación

### Fase 1: MVP Funcional ✅ COMPLETADA

- Análisis de archivos .txt línea por línea
- Clasificación positivo/negativo/neutro
- Detección automática de idioma
- Dashboard web con gráficos interactivos
- Exportación a CSV y TXT
- Comando de consola
- Suite de pruebas automatizadas

### Fase 2: Integración y Escalamiento (3-6 meses)

- Conexión con bases de datos de atención al cliente
- Importación desde Excel, CSV o APIs internas
- Soporte para PDF y Word
- Autenticación y control de accesos
- Despliegue en servidor de producción

### Fase 3: Análisis Avanzado (6-12 meses)

- Análisis por temas o categorías
- Detección de emociones específicas
- Alertas automáticas por umbrales
- API REST para integración con otros sistemas

### Fase 4: Inteligencia Institucional (12-24 meses)

- Modelos de predicción de tendencias
- Procesamiento de audio (transcripción + análisis)
- Integración con dashboards ejecutivos en tiempo real
- Plataforma de IA reutilizable para otros proyectos

---

## 12. Arquitectura Técnica

| Componente | Tecnología | Función |
|------------|------------|---------|
| Backend | Django 6.0.5 | Lógica de negocio y endpoints |
| IA (español) | pysentimiento | Modelo pre-entrenado para español |
| IA (inglés) | VADER | Reglas léxicas como respaldo |
| Visualización | Plotly | Gráficos interactivos |
| Interfaz | HTMX + Alpine.js + Tabler | Carga asíncrona y diseño responsivo |
| Base de datos | SQLite | Almacenamiento local |
| Consola | Django management | Análisis desde terminal |

**Nota**: Todos los componentes son de código abierto y operan de forma local.

---

## 13. Valor Económico para la Organización

| Beneficio | Descripción | Impacto |
|-----------|-------------|---------|
| **Menor tiempo de análisis** | De horas a segundos | Reducción del 99% |
| **Menor costo operativo** | Menos horas en tareas repetitivas | $14,400-$147,000 USD/año |
| **Decisiones más rápidas** | Información en tiempo real | Reacción oportuna |
| **Mayor capacidad** | Miles de documentos sin más personal | Escalabilidad |
| **IA institucional** | Inteligencia artificial en procesos reales | Base para futuro |
| **Confidencialidad** | Modelos locales sin nube | Cumplimiento de seguridad |
| **Consistencia** | Modelo que clasifica igual siempre | Sin sesgo subjetivo |
| **Sin licencias** | Todo es código abierto | $0 en licencias |

---

## 14. Conclusión

### La pregunta que debe responder el directorio

SentiMiner resuelve un problema real de negocio: la imposibilidad de procesar manualmente el creciente volumen de texto que generan y reciben las organizaciones.

Con una inversión inicial en una solución de código abierto, se obtiene:

- **Ahorro recurrente significativo** ($14,400 a $147,000 USD anuales)
- **Reducción de riesgos** por detección temprana de problemas
- **Base tecnológica sólida** para la transformación digital
- **Confidencialidad total** de la información sensible
- **Cero costos de licencias** de software

> **La pregunta no es si la organización puede permitirse implementar esta solución. La pregunta es si puede permitirse NO tenerla.**

---

*Grupo 3*
*Curso: Proyectos de Disrupción Tecnológica*
*UPN*
