import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from .models import ArchivoAnalisis, ResultadoLinea, ResumenAnalisis


class AnalizadorSentimiento:
    """
    HU-03: Clasificación de frases en positivas, negativas o neutras.
    
    Motor de análisis sentimental multilingüe con prioridad en español
    usando pysentimiento. Fallback a VADER para inglés y TextBlob como
    respaldo adicional.
    """

    def __init__(self):
        self._vader = None
        self._pysentimiento = None

    @property
    def vader(self):
        if self._vader is None:
            self._vader = SentimentIntensityAnalyzer()
        return self._vader

    @property
    def pysentimiento(self):
        if self._pysentimiento is None:
            from pysentimiento import create_analyzer
            self._pysentimiento = create_analyzer(task="sentiment", lang="es")
        return self._pysentimiento

    def _es_espanol(self, texto):
        """
        Heurística para detectar si un texto está en español.
        Busca caracteres propios del español: ñ, tildes, ¿, ¡
        """
        patron_espanol = re.compile(r'[ñáéíóúüÁÉÍÓÚÜ¿¡]')
        return bool(patron_espanol.search(texto))

    def analizar_texto(self, texto):
        """
        Analiza un texto y devuelve su clasificación sentimental.
        
        Prioriza pysentimiento para textos en español.
        Usa VADER como fallback para inglés.
        
        Retorna dict con: clasificacion, puntaje_polaridad, libreria_usada
        """
        if not texto or not texto.strip():
            return {
                'clasificacion': 'neutro',
                'puntaje_polaridad': 0.0,
                'libreria_usada': 'sin_texto'
            }

        if self._es_espanol(texto):
            return self._analizar_pysentimiento(texto)

        return self._analizar_vader(texto)

    def _analizar_pysentimiento(self, texto):
        """
        HU-03: Análisis con pysentimiento para español (mayor precisión).
        """
        try:
            resultado = self.pysentimiento.predict(texto)
            salida = resultado.output
            probabilidades = resultado.probas

            if salida == 'POS':
                clasificacion = 'positivo'
                puntaje = probabilidades.get('POS', 0.5)
            elif salida == 'NEG':
                clasificacion = 'negativo'
                puntaje = -probabilidades.get('NEG', 0.5)
            else:
                clasificacion = 'neutro'
                puntaje = 0.0

            return {
                'clasificacion': clasificacion,
                'puntaje_polaridad': round(puntaje, 4),
                'libreria_usada': 'pysentimiento'
            }
        except Exception:
            return self._analizar_vader(texto)

    def _analizar_vader(self, texto):
        """
        Análisis con VADER para inglés. Incluye puntuación compuesta.
        """
        puntajes = self.vader.polarity_scores(texto)
        compuesto = puntajes['compound']

        if compuesto >= 0.05:
            clasificacion = 'positivo'
        elif compuesto <= -0.05:
            clasificacion = 'negativo'
        else:
            clasificacion = 'neutro'

        return {
            'clasificacion': clasificacion,
            'puntaje_polaridad': round(compuesto, 4),
            'libreria_usada': 'vader'
        }

    def procesar_archivo(self, archivo_id):
        """
        HU-02, HU-03, HU-04: Procesa todas las líneas de un archivo y
        genera el resumen estadístico del análisis.
        
        Args:
            archivo_id: ID del ArchivoAnalisis a procesar
        
        Returns:
            dict con lineas_analizadas y resumen
        """
        archivo = ArchivoAnalisis.objects.get(pk=archivo_id)
        lineas = archivo.contenido.splitlines()

        ResultadoLinea.objects.filter(archivo=archivo).delete()

        lineas_analizadas = []
        for i, linea in enumerate(lineas, start=1):
            texto = linea.strip()
            if not texto:
                continue

            resultado = self.analizar_texto(texto)
            linea_obj = ResultadoLinea.objects.create(
                archivo=archivo,
                numero_linea=i,
                texto=texto,
                clasificacion=resultado['clasificacion'],
                puntaje_polaridad=resultado['puntaje_polaridad'],
                libreria_usada=resultado['libreria_usada']
            )
            lineas_analizadas.append(linea_obj)

        resumen = self.calcular_resumen(archivo, lineas_analizadas)

        return {
            'lineas': lineas_analizadas,
            'resumen': resumen
        }

    def calcular_resumen(self, archivo, lineas_analizadas):
        """
        HU-04: Calcula el resumen estadístico con porcentajes y
        sentimiento predominante.
        """
        total = len(lineas_analizadas)
        positivas = sum(1 for l in lineas_analizadas if l.clasificacion == 'positivo')
        negativas = sum(1 for l in lineas_analizadas if l.clasificacion == 'negativo')
        neutras = sum(1 for l in lineas_analizadas if l.clasificacion == 'neutro')

        pct_positivo = round((positivas / total) * 100, 1) if total > 0 else 0
        pct_negativo = round((negativas / total) * 100, 1) if total > 0 else 0
        pct_neutro = round((neutras / total) * 100, 1) if total > 0 else 0

        if positivas >= negativas and positivas >= neutras:
            predominante = 'positivo'
        elif negativas >= positivas and negativas >= neutras:
            predominante = 'negativo'
        else:
            predominante = 'neutro'

        ResumenAnalisis.objects.filter(archivo=archivo).delete()
        resumen = ResumenAnalisis.objects.create(
            archivo=archivo,
            total_lineas=total,
            positivas=positivas,
            negativas=negativas,
            neutras=neutras,
            porcentaje_positivo=pct_positivo,
            porcentaje_negativo=pct_negativo,
            porcentaje_neutro=pct_neutro,
            sentimiento_predominante=predominante
        )

        return resumen