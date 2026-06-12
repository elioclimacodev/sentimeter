from django.db import models


class ArchivoAnalisis(models.Model):
    """
    HU-01: Carga de archivos .txt
    HU-02: Lectura integral del contenido
    
    Almacena el archivo subido por el usuario y su contenido completo
    para su posterior análisis sentimental.
    """
    nombre_original = models.CharField(max_length=255)
    contenido = models.TextField()
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Archivo de Análisis"
        verbose_name_plural = "Archivos de Análisis"
        ordering = ['-fecha_subida']

    def __str__(self):
        return self.nombre_original


class ResultadoLinea(models.Model):
    """
    HU-03: Clasificación de sentimientos (positivo, negativo, neutro)
    HU-09: Variación sentimental a lo largo del texto
    
    Resultado del análisis sentimental para cada línea del archivo procesado.
    """
    CLASIFICACIONES = [
        ('positivo', 'Positivo'),
        ('negativo', 'Negativo'),
        ('neutro', 'Neutro'),
    ]

    archivo = models.ForeignKey(
        ArchivoAnalisis,
        on_delete=models.CASCADE,
        related_name='lineas'
    )
    numero_linea = models.IntegerField()
    texto = models.TextField()
    clasificacion = models.CharField(max_length=10, choices=CLASIFICACIONES)
    puntaje_polaridad = models.FloatField()
    libreria_usada = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Resultado por Línea"
        verbose_name_plural = "Resultados por Línea"
        ordering = ['numero_linea']

    def __str__(self):
        return f"Línea {self.numero_linea} - {self.clasificacion}"


class ResumenAnalisis(models.Model):
    """
    HU-04: Resumen cuantitativo con porcentajes
    
    Agregación estadística del análisis sentimental de un archivo.
    Calcula totales, porcentajes y sentimiento predominante.
    """
    archivo = models.OneToOneField(
        ArchivoAnalisis,
        on_delete=models.CASCADE,
        related_name='resumen'
    )
    total_lineas = models.IntegerField()
    positivas = models.IntegerField()
    negativas = models.IntegerField()
    neutras = models.IntegerField()
    porcentaje_positivo = models.FloatField()
    porcentaje_negativo = models.FloatField()
    porcentaje_neutro = models.FloatField()
    sentimiento_predominante = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Resumen de Análisis"
        verbose_name_plural = "Resúmenes de Análisis"

    def __str__(self):
        return f"Resumen: {self.archivo.nombre_original}"