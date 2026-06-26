# Explicacion de Tecnologias - SentiMiner

## Indice

1. [Tecnologias utilizadas](#tecnologias-utilizadas)
2. [Motor de analisis de sentimientos](#motor-de-analisis-de-sentimientos)
3. [Visualizacion grafica](#visualizacion-grafica)
4. [Otros componentes](#otros-componentes)
5. [Que es la polaridad](#que-es-la-polaridad)
6. [Como interpretar los graficos estadisticos](#como-interpretar-los-graficos-estadisticos)

---

## Tecnologias utilizadas

El proyecto SentiMiner integra varias tecnologias especializadas en distintas capas de la aplicacion. A continuacion se describe cada una y donde se aplica.

### pysentimiento (libreria principal)

- **Archivo de uso**: `sentiminer/services.py` (lineas 29-30, 62-87)
- **Para que se usa**: Es el motor principal de analisis de sentimientos para textos en **espanol**. Se carga bajo demanda la primera vez que se detecta un texto en espanol mediante `create_analyzer(task="sentiment", lang="es")`.
- **Como funciona**: El metodo `predict()` devuelve una clasificacion (`POS`, `NEG` o `NEU`) y un diccionario de probabilidades (`probas`). A partir de eso se asigna:
  - Si el resultado es `POS` (positivo): la polaridad es la probabilidad de ser positivo (valor entre 0 y 1).
  - Si el resultado es `NEG` (negativo): la polaridad es la probabilidad de ser negativo, con signo negativo (valor entre -1 y 0).
  - Si el resultado es `NEU` (neutro): la polaridad es 0.0.
- **Precision**: Es la libreria con mayor precision para espanol en este proyecto. Si pysentimiento falla por alguna razon, el sistema recurre a VADER como respaldo.

### VADER (vaderSentiment)

- **Archivo de uso**: `sentiminer/services.py` (lineas 2, 89-107)
- **Para que se usa**: Sirve como **fallback** (respaldo) para textos en **ingles** y tambien para textos en espanol cuando pysentimiento produce un error.
- **Como funciona**: El metodo `polarity_scores()` devuelve un diccionario con cuatro valores:
  - `neg`: puntaje de negatividad (0 a 1)
  - `neu`: puntaje de neutralidad (0 a 1)
  - `pos`: puntaje de positividad (0 a 1)
  - `compound`: puntaje compuesto (-1 a +1), que es el valor que SentiMiner usa como polaridad.
- **Criterios de clasificacion**:
  - `compound >= 0.05` se clasifica como **positivo**
  - `compound <= -0.05` se clasifica como **negativo**
  - Entre -0.05 y 0.05 se clasifica como **neutro**
- **Ventaja**: Funciona sin modelos de machine learning, usa reglas lexicales (listas de palabras con pesos predefinidos), por lo que es rapido y no requiere entrenamiento.

### TextBlob

- **Archivo de uso**: `sentiminer/services.py` (linea 3, importacion)
- **Para que se usa**: Esta importada en el codigo y listada en `requirements.txt`, pero **no se utiliza activamente** en el flujo principal de analisis. Funciona como dependencia de respaldo reservada para uso futuro.
- **Estado actual**: Solo se importa. No se invoca ningun metodo de TextBlob en ningun archivo del proyecto.

### Re (expresiones regulares)

- **Archivo de uso**: `sentiminer/services.py` (lineas 1, 33-39)
- **Para que se usa**: Detectar si un texto esta en espanol. El metodo `_es_espanol()` busca caracteres propios del idioma como `ñ`, `á`, `é`, `í`, `ó`, `ú`, `ü`, `¿`, `¡` usando una expresion regular. Si encuentra alguno de estos caracteres, el texto se envia a pysentimiento; de lo contrario, se envia a VADER.

### Plotly

- **Archivos de uso**:
  - `sentiminer/views.py` (lineas 10-13, 88-170)
  - `sentiminer/management/commands/analizar.py` (lineas 5, 202-237)
  - `sentiminer/templates/sentiminer/base.html` (linea 9, CDN)
- **Para que se usa**: Generar los dos graficos estadisticos interactivos del proyecto:
  1. **Grafico de pastel (donut)**: Muestra la distribucion porcentual de sentimientos positivos, negativos y neutros.
  2. **Grafico de tendencia (linea con marcadores)**: Muestra como varia la polaridad linea por linea a lo largo del texto.
- **Detalles tecnicos**: Los graficos se generan en el servidor como HTML embebido (`fig.to_html(full_html=False)`) y se cargan en la interfaz web de forma asincrona via HTMX. Desde la linea de comandos, el grafico de pastel se escribe en un archivo temporal HTML y se abre en el navegador predeterminado.

### Django

- **Archivos de uso**: Todos los archivos del proyecto siguen la estructura de Django.
- **Para que se usa**: Framework backend que gestiona:
  - Rutas URL (`sentiminer/urls.py`)
  - Vistas/logica de negocio (`sentiminer/views.py`)
  - Modelos de base de datos (`sentiminer/models.py`)
  - Comandos de gestion (`sentiminer/management/commands/analizar.py`)
  - Plantillas HTML (`sentiminer/templates/`)
  - Panel de administracion (`sentiminer/admin.py`)
  - Base de datos SQLite (configuracion por defecto)

### HTMX

- **Archivo de uso**: `sentiminer/templates/sentiminer/base.html` (linea 10, CDN)
- **Archivos de plantilla**: `resultados.html`, `_tabla_resultados.html`
- **Para que se usa**: Cargar contenido de forma asincrona en la pagina sin recargar toda la interfaz. Por ejemplo, los graficos y la tabla de resultados se obtienen via peticiones HTMX cuando el usuario accede al dashboard.

### Alpine.js

- **Archivo de uso**: `sentiminer/templates/sentiminer/base.html` (linea 11, CDN)
- **Para que se usa**: Manejar comportamientos ligeros del lado del cliente, como el auto-cierre de alertas despues de unos segundos.

### Tabler

- **Archivo de uso**: `sentiminer/templates/sentiminer/base.html` (linea 8, CSS local)
- **Para que se usa**: Framework CSS que proporciona el diseno visual de la interfaz (tarjetas, botones, layout, tablas, badges de colores).

### Pandas y python-dotenv

- **Archivo de uso**: `requirements.txt` (lineas 4-5)
- **Estado actual**: Listadas como dependencias en `requirements.txt` pero **no se importan ni utilizan** en ningun archivo del codigo fuente.

---

## Motor de analisis de sentimientos

El corazon del proyecto es la clase `AnalizadorSentimiento` en `sentiminer/services.py`. Su flujo de operacion es:

```
Texto recibido
    │
    ▼
¿Es texto vacio? ──Si──▶ Clasificacion: neutro, Polaridad: 0.0
    │ No
    ▼
¿Contiene caracteres espanoles (ñ, á, é, etc)? ──Si──▶ pysentimiento
    │ No
    ▼
  VADER
```

Cada linea analizada se almacena en la base de datos con:
- `clasificacion`: positivo, negativo o neutro
- `puntaje_polaridad`: valor numerico float
- `libreria_usada`: "pysentimiento", "vader" o "sin_texto"

Despues de procesar todas las lineas, el metodo `calcular_resumen()` agrega los datos y calcula totales, porcentajes y el sentimiento predominante.

---

## Visualizacion grafica

### Grafico de pastel (Distribucion de sentimientos)

- **Funcion en views.py**: `grafico_sentimientos()` (lineas 88-122)
- **Funcion en analizar.py**: `_mostrar_grafico()` (lineas 202-237)
- **Tipo**: `go.Pie` con `hole=0.3` (estilo donut)
- **Datos**: Conteo de lineas positivas, negativas y neutras
- **Colores**:
  - Verde (`#2fb344`) para positivo
  - Rojo (`#d63939`) para negativo
  - Gris (`#656d77`) para neutro
- **Muestra**: Etiquetas con nombre y porcentaje (ej: "Positivo 60%")

### Grafico de tendencia (Variacion sentimental por linea)

- **Funcion en views.py**: `grafico_tendencia()` (lineas 125-170)
- **Tipo**: `go.Scatter` con `mode='lines+markers'`
- **Eje X**: Numero de linea (orden secuencial en el archivo)
- **Eje Y**: Puntaje de polaridad de cada linea
- **Linea de referencia**: Linea punteada horizontal en y=0 marcada como "Neutro"
- **Herramienta interactiva**: Al pasar el cursor se muestra el numero de linea, el texto (hasta 60 caracteres) y el puntaje de polaridad

---

## Otros componentes

### Modelos de base de datos (`sentiminer/models.py`)

- **ArchivoAnalisis**: Almacena el nombre del archivo, el contenido completo y la fecha de subida.
- **ResultadoLinea**: Almacena el resultado por linea: numero de linea, texto, clasificacion, puntaje de polaridad y libreria utilizada.
- **ResumenAnalisis**: Almacena el resumen estadistico: totales, conteos, porcentajes y sentimiento predominante.

### Exportacion de resultados

- **CSV** (`sentiminer/views.py`, lineas 244-278): Genera un archivo CSV con columnas: Numero de Linea, Texto, Clasificacion, Polaridad, Libreria, seguido de un bloque de resumen.
- **TXT** (`sentiminer/views.py`, lineas 281-322): Genera un archivo de texto plano con cada linea clasificada y un resumen al final.
- **Desde consola** (`analizar.py`, metodo `_exportar()`): Permite exportar desde la linea de comandos con el argumento `--exportar csv` o `--exportar txt`.

### Comando de consola (`analizar.py`)

Uso: `python manage.py analizar <archivo.txt> [--exportar csv|txt] [--grafico]`

- Analiza un archivo .txt desde la terminal
- Muestra resultados con colores (verde=positivo, rojo=negativo, amarillo=neutro)
- Puede exportar a CSV o TXT
- Puede abrir el grafico de pastel en el navegador con `--grafico`

### Pruebas (`sentiminer/tests.py`)

Suite de pruebas que valida:
- Analisis directo de textos positivos, negativos, neutros y vacios
- Deteccion de idioma espanol
- Procesamiento de archivos completos
- Porcentajes correctos en el resumen
- Todas las vistas web (inicio, resultados, graficos, tabla)
- Exportacion CSV y TXT
- Comando de consola con distintos argumentos
- Modelos de la base de datos

---

## Que es la polaridad

La **polaridad** es un valor numerico que representa la intensidad y direccion del sentimiento expresado en un texto. Es el dato fundamental que genera el motor de analisis.

### Rango de valores

| Polaridad | Significado |
|-----------|-------------|
| **+1.0** | Sentimiento positivo maximo |
| **0.0** | Sentimiento neutro (sin carga emocional) |
| **-1.0** | Sentimiento negativo maximo |

### Como se calcula segun la libreria

**Con pysentimiento** (espanol):
- El modelo devuelve probabilidades para cada clase (positivo, negativo, neutro).
- Si el texto es positivo: polaridad = probabilidad de POS (ej: 0.9818)
- Si el texto es negativo: polaridad = probabilidad de NEG, con signo negativo (ej: -0.9480)
- Si el texto es neutro: polaridad = 0.0

**Con VADER** (ingles):
- Se usa el puntaje `compound` directamente (rango -1 a +1).
- No requiere conversion adicional.

### Ejemplo real

Un archivo de 22 lineas de discurso politico peruano produjo estos resultados:
- Lineas positivas: polaridades de 0.5878, 0.7249, 0.6813 (valores positivos moderados a altos)
- Lineas negativas: polaridades de -0.4633 a -0.9823 (valores negativos de moderados a extremos)
- Todas las lineas fueron analizadas con pysentimiento (todas contenian caracteres espanoles)

---

## Como interpretar los graficos estadisticos

### Grafico de pastel (Distribucion de sentimientos)

Este grafico muestra **que proporcion** del texto pertenece a cada categoria de sentimiento.

**Que mirar**:
- **El tamano relativo de cada porcion**: Indica que sentimiento es mas frecuente en el texto.
- **Los porcentajes**: Muestran la participacion exacta de cada categoria.
- **La porcion mas grande**: Corresponde al sentimiento predominante del archivo.

**Ejemplo de interpretacion**:
- Si el grafico muestra "Positivo 65%, Negativo 20%, Neutro 15%", significa que el texto tiene un tono mayormente positivo, con una quinta parte de expresiones negativas y un porcentaje pequeno de expresiones sin carga emocional.

**Colores**:
- Verde = Positivo
- Rojo = Negativo
- Gris = Neutro

### Grafico de tendencia (Variacion sentimental por linea)

Este grafico muestra **como cambia** el sentimiento a lo largo del texto, linea por linea.

**Que mirar**:
- **Eje horizontal (X)**: Numero de linea del archivo (1, 2, 3, ...).
- **Eje vertical (Y)**: Puntaje de polaridad de esa linea.
- **Linea punteada en 0**: Marca la frontera entre sentimiento positivo (arriba) y negativo (abajo).
- **Puntos por encima de 0**: Lineas con sentimiento positivo.
- **Puntos por debajo de 0**: Lineas con sentimiento negativo.
- **Puntos sobre la linea 0**: Lineas neutras.

**Que buscar**:
- **Patrones de subida y bajada**: Un texto que empieza positivo y termina negativo (o viceversa) indica un cambio de tono.
- **Picos extremos**: Valores cercanos a +1 o -1 indican sentimientos muy intensos.
- **Zonas estables**: Varias lineas con valores similares indican consistencia en el tono del texto.
- **Cambios bruscos**: Un salto de positivo a negativo entre lineas consecutivas marca un punto de inflexion en el texto.

**Ejemplo de interpretacion**:
- Si las primeras 10 lineas estan por encima de 0 y las siguientes 10 por debajo, el texto tiene una primera mitad positiva y una segunda mitad negativa, lo que podria indicar un cambio de tema, de opinion o de contexto narrativo.

### Resumen del dashboard

El dashboard de resultados combina ambos graficos con tarjetas de resumen que muestran:
- Total de lineas analizadas
- Cantidad y porcentaje de lineas positivas, negativas y neutras
- El sentimiento predominante (el que tiene mayor cantidad)

Esto permite una vision completa: los graficos muestran la distribucion global y la evolucion temporal, mientras que las tarjetas dan los numeros exactos.
