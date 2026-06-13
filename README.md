# SentiMiner - Análisis Sentimental

## Objetivo del proyecto

SentiMiner es una herramienta web de análisis sentimental que permite a los usuarios subir archivos de texto plano (.txt) y obtener un análisis detallado de sentimientos línea por línea. El sistema clasifica cada línea como positiva, negativa o neutra, genera estadísticas agregadas con porcentajes, y visualiza los resultados mediante gráficos interactivos.

## Tecnología utilizada

- **Backend**: Django 6.0.5
- **Frontend**: HTMX 2.0.4, Alpine.js 3.x, Plotly 3.1.0
- **Análisis de sentimientos**:
  - **pysentimiento**: Librería principal para análisis en español (mayor precisión)
  - **VADER (vaderSentiment)**: Fallback para análisis en inglés
- **Base de datos**: SQLite
- **CSS Framework**: Tabler
- **Visualización**: Plotly (gráficos de pastel y tendencia)

## Historias de usuario

Las historias de usuario están documentadas en los comentarios del código fuente:

| ID | Descripción | Estado |
|----|-------------|--------|
| HU-01 | Carga de archivos .txt | Implementada |
| HU-02 | Lectura integral del contenido | Implementada |
| HU-03 | Clasificación de sentimientos (positivo, negativo, neutro) | Implementada |
| HU-04 | Resumen cuantitativo con porcentajes | Implementada |
| HU-05 | Generación de gráfico de pastel | Implementada |
| HU-06 | (No documentada en código) | - |
| HU-07 | Ejecución del sistema desde consola | Implementada |
| HU-08 | Interfaz minimalista | Implementada |
| HU-09 | Variación sentimental a lo largo del texto | Implementada |
| HU-10 | Pruebas con datasets simulados | Implementada |
| HU-11 | Exportación básica de resultados | Implementada |
| HU-12 | Manejo de errores con mensajes claros | Implementada |

## Funcionalidad

### Interfaz Web
1. **Subida de archivos**: Formulario para subir archivos .txt con validación de formato y codificación
2. **Dashboard de resultados**:
   - Tarjetas con resumen cuantitativo (total líneas, positivas, negativas, neutras con porcentajes)
   - Sentimiento predominante
   - Gráfico de pastel interactivo (distribución de sentimientos)
   - Gráfico de tendencia (variación sentimental por línea)
   - Tabla detallada con clasificación por línea
3. **Exportación**: Descarga de resultados en formato CSV o TXT
4. **Historial**: Lista de análisis anteriores con acceso rápido

### Análisis de sentimientos
- Detección automática de idioma (español/inglés) mediante heurísticas
- Para textos en español: utiliza pysentimiento (mayor precisión)
- Para textos en inglés: utiliza VADER como fallback
- Clasificación en tres categorías: positivo, negativo, neutro
- Cálculo de puntaje de polaridad para cada línea

### Comando de consola
```bash
python manage.py analizar <archivo.txt> [--exportar csv|txt] [--grafico]
```
- `--exportar csv|txt`: Exporta resultados a archivo
- `--grafico`: Abre gráfico de pastel en el navegador

### API REST (endpoints HTMX)
- `GET /`: Página principal con formulario
- `POST /subir/`: Sube y analiza un archivo
- `GET /resultados/<id>/`: Dashboard de resultados
- `GET /resultados/<id>/grafico/`: Gráfico de pastel
- `GET /resultados/<id>/tendencia/`: Gráfico de tendencia
- `GET /resultados/<id>/tabla/`: Tabla de resultados
- `GET /resultados/<id>/exportar/csv/`: Exportar CSV
- `GET /resultados/<id>/exportar/txt/`: Exportar TXT

## Cómo se hace funcionar

### Requisitos previos
- Python 3.8 o superior
- pip

### Instalación

1. **Clonar el repositorio** (si aplica) o navegar al directorio del proyecto

2. **Crear entorno virtual**:
   ```bash
   python -m venv venv
   ```

3. **Activar entorno virtual**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Ejecutar migraciones**:
   ```bash
   python manage.py migrate
   ```

6. **Crear superusuario (opcional)**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Ejecutar servidor de desarrollo**:
   ```bash
   python manage.py runserver
   ```

8. **Acceder a la aplicación**:
   - Aplicación web: http://127.0.0.1:8000/
   - Panel de administración: http://127.0.0.1:8000/admin/

### Ejecutar pruebas
```bash
python manage.py test sentiminer
```

### Uso del comando de consola
```bash
# Analizar un archivo
python manage.py analizar mi_archivo.txt

# Analizar y exportar a CSV
python manage.py analizar mi_archivo.txt --exportar csv

# Analizar y mostrar gráfico en navegador
python manage.py analizar mi_archivo.txt --grafico
```

## Modelos de análisis

El proyecto **NO se conecta a modelos en la nube**. Utiliza modelos locales que se ejecutan en el servidor:

1. **pysentimiento** (español): Modelo de análisis de sentimientos pre-entrenado para español. Se carga bajo demanda la primera vez que se analiza un texto en español.

2. **VADER** (inglés): Análisis de sentimientos basado en reglas léxicas. Se utiliza como fallback para textos en inglés.

### Flujo de análisis
1. El sistema detecta el idioma mediante heurísticas (presencia de caracteres como ñ, tildes, ¿, ¡)
2. Si detecta español, utiliza pysentimiento
3. Si detecta inglés u otro idioma, utiliza VADER
4. Guarda los resultados en la base de datos SQLite
5. Genera estadísticas y gráficos interactivos

## Estructura del proyecto

```
sentiminer/
├── config/              # Configuración de Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── sentiminer/          # Aplicación principal
│   ├── models.py        # Modelos: ArchivoAnalisis, ResultadoLinea, ResumenAnalisis
│   ├── views.py         # Vistas web y endpoints HTMX
│   ├── services.py      # Motor de análisis de sentimientos
│   ├── urls.py          # Rutas de la aplicación
│   ├── admin.py         # Configuración del panel de administración
│   ├── templates/       # Plantillas HTML
│   │   ├── base.html
│   │   ├── inicio.html
│   │   ├── resultados.html
│   │   └── _*.html      # Parciales HTMX
│   ├── static/          # Archivos estáticos (CSS)
│   ├── management/      # Comandos de gestión
│   │   └── commands/
│   │       └── analizar.py
│   └── tests/           # Pruebas y fixtures
│       └── fixtures/
│           ├── positivo.txt
│           ├── negativo.txt
│           └── mixto.txt
├── manage.py
├── requirements.txt
└── db.sqlite3
```
