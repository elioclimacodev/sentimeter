import os
import tempfile
from io import BytesIO
from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.core.management.base import CommandError
from .models import ArchivoAnalisis, ResultadoLinea, ResumenAnalisis
from .services import AnalizadorSentimiento


FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'tests', 'fixtures')


class ArchivoValidoTxtTest(TestCase):
    """
    HU-01: Verifica que el sistema acepta archivos .txt válidos.
    HU-10: Pruebas con datasets simulados para validar el MVP.
    """

    def test_archivo_valido_txt(self):
        archivo = SimpleUploadedFile(
            "positivo.txt",
            b"Este proyecto es excelente.\nMe siento muy feliz.",
            content_type="text/plain"
        )
        response = self.client.post(
            reverse('subir_archivo'),
            {'archivo': archivo}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse(
            'resultados', kwargs={'archivo_id': 1}
        ))

    def test_archivo_invalido_no_txt(self):
        archivo = SimpleUploadedFile(
            "documento.pdf",
            b"contenido falso",
            content_type="application/pdf"
        )
        response = self.client.post(
            reverse('subir_archivo'),
            {'archivo': archivo}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('inicio'))

    def test_sin_archivo(self):
        response = self.client.post(reverse('subir_archivo'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('inicio'))


class AnalisisSentimientoTest(TestCase):
    """
    HU-03: Verifica la clasificación de sentimientos.
    HU-10: Validación con datos de prueba simulados.
    """

    def setUp(self):
        self.analizador = AnalizadorSentimiento()

    def test_analisis_positivo_espanol(self):
        resultado = self.analizador.analizar_texto(
            "Me encanta este proyecto, es maravilloso y fantástico"
        )
        self.assertEqual(resultado['clasificacion'], 'positivo')

    def test_analisis_negativo_espanol(self):
        resultado = self.analizador.analizar_texto(
            "Odio este proyecto, es horrible y espantoso, me enfurece"
        )
        self.assertEqual(resultado['clasificacion'], 'negativo')

    def test_analisis_neutro(self):
        resultado = self.analizador.analizar_texto("La reunión es a las tres de la tarde")
        self.assertEqual(resultado['clasificacion'], 'neutro')

    def test_analisis_texto_vacio(self):
        resultado = self.analizador.analizar_texto("")
        self.assertEqual(resultado['clasificacion'], 'neutro')
        self.assertEqual(resultado['puntaje_polaridad'], 0.0)

    def test_deteccion_espanol(self):
        self.assertTrue(self.analizador._es_espanol("¿Cómo estás?"))
        self.assertTrue(self.analizador._es_espanol("mañana"))
        self.assertTrue(self.analizador._es_espanol("él"))
        self.assertFalse(self.analizador._es_espanol("Hello world"))
        self.assertFalse(self.analizador._es_espanol(""))


class ProcesamientoArchivoTest(TestCase):
    """
    HU-02: Verifica que se procesa el 100% de líneas.
    HU-04: Verifica porcentajes y resumen.
    """

    def setUp(self):
        self.archivo = ArchivoAnalisis.objects.create(
            nombre_original="prueba.txt",
            contenido="Me siento feliz.\nEsto es terrible.\nUna frase neutra."
        )
        self.analizador = AnalizadorSentimiento()
        self.analizador.procesar_archivo(self.archivo.pk)

    def test_procesa_todas_las_lineas(self):
        self.archivo.refresh_from_db()
        lineas = self.archivo.lineas.all()
        self.assertEqual(lineas.count(), 3)

    def test_resumen_creado(self):
        resumen = ResumenAnalisis.objects.get(archivo=self.archivo)
        self.assertEqual(resumen.total_lineas, 3)
        self.assertAlmostEqual(
            resumen.porcentaje_positivo + resumen.porcentaje_negativo + resumen.porcentaje_neutro,
            100.0,
            delta=0.5
        )

    def test_archivo_completo_positivo(self):
        with open(os.path.join(FIXTURES_DIR, 'positivo.txt'), 'r', encoding='utf-8') as f:
            contenido = f.read()

        archivo = ArchivoAnalisis.objects.create(
            nombre_original="positivo.txt",
            contenido=contenido
        )
        self.analizador.procesar_archivo(archivo.pk)

        lineas = archivo.lineas.all()
        self.assertEqual(lineas.count(), 5)
        resumen = ResumenAnalisis.objects.get(archivo=archivo)
        self.assertGreaterEqual(resumen.positivas, 3)

    def test_archivo_completo_negativo(self):
        with open(os.path.join(FIXTURES_DIR, 'negativo.txt'), 'r', encoding='utf-8') as f:
            contenido = f.read()

        archivo = ArchivoAnalisis.objects.create(
            nombre_original="negativo.txt",
            contenido=contenido
        )
        self.analizador.procesar_archivo(archivo.pk)

        lineas = archivo.lineas.all()
        self.assertEqual(lineas.count(), 5)
        resumen = ResumenAnalisis.objects.get(archivo=archivo)
        self.assertEqual(resumen.sentimiento_predominante, 'negativo')

    def test_archivo_completo_mixto(self):
        with open(os.path.join(FIXTURES_DIR, 'mixto.txt'), 'r', encoding='utf-8') as f:
            contenido = f.read()

        archivo = ArchivoAnalisis.objects.create(
            nombre_original="mixto.txt",
            contenido=contenido
        )
        self.analizador.procesar_archivo(archivo.pk)

        lineas = archivo.lineas.all()
        self.assertEqual(lineas.count(), 10)


class VistasTest(TestCase):
    """
    HU-08: Verifica que la interfaz carga correctamente.
    HU-04, HU-06, HU-09: Verifica las vistas de resultados y gráficos.
    """

    def setUp(self):
        self.archivo = ArchivoAnalisis.objects.create(
            nombre_original="prueba.txt",
            contenido="Feliz y contento.\nTriste y enojado.\nNormal."
        )
        self.analizador = AnalizadorSentimiento()
        self.analizador.procesar_archivo(self.archivo.pk)

    def test_inicio_carga(self):
        response = self.client.get(reverse('inicio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sentiminer/inicio.html')

    def test_resultados_carga(self):
        response = self.client.get(
            reverse('resultados', kwargs={'archivo_id': self.archivo.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sentiminer/resultados.html')

    def test_grafico_sentimientos_carga(self):
        response = self.client.get(
            reverse('grafico_sentimientos', kwargs={'archivo_id': self.archivo.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_grafico_tendencia_carga(self):
        response = self.client.get(
            reverse('grafico_tendencia', kwargs={'archivo_id': self.archivo.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_tabla_resultados_carga(self):
        response = self.client.get(
            reverse('tabla_resultados', kwargs={'archivo_id': self.archivo.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_resultados_inexistentes(self):
        response = self.client.get(
            reverse('resultados', kwargs={'archivo_id': 999})
        )
        self.assertEqual(response.status_code, 404)


class ExportacionTest(TestCase):
    """
    HU-11: Verifica la exportación de resultados en CSV y TXT.
    """

    def setUp(self):
        self.archivo = ArchivoAnalisis.objects.create(
            nombre_original="exportar.txt",
            contenido="Me siento feliz.\nEs terrible."
        )
        self.analizador = AnalizadorSentimiento()
        self.analizador.procesar_archivo(self.archivo.pk)

    def test_exportar_csv(self):
        response = self.client.get(
            reverse('exportar_csv', kwargs={'archivo_id': self.archivo.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('Número de Línea', response.content.decode('utf-8-sig'))

    def test_exportar_txt(self):
        response = self.client.get(
            reverse('exportar_txt', kwargs={'archivo_id': self.archivo.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')
        self.assertIn('SentiMiner', response.content.decode('utf-8'))


class ModelosTest(TestCase):
    """
    HU-01, HU-02, HU-03, HU-04: Verifica la correcta creación de modelos.
    """

    def test_crear_archivo_analisis(self):
        archivo = ArchivoAnalisis.objects.create(
            nombre_original="test.txt",
            contenido="Prueba de contenido"
        )
        self.assertEqual(archivo.nombre_original, "test.txt")
        self.assertIsNotNone(archivo.fecha_subida)

    def test_crear_resultado_linea(self):
        archivo = ArchivoAnalisis.objects.create(
            nombre_original="test.txt",
            contenido="Prueba"
        )
        linea = ResultadoLinea.objects.create(
            archivo=archivo,
            numero_linea=1,
            texto="Prueba",
            clasificacion="positivo",
            puntaje_polaridad=0.8,
            libreria_usada="pysentimiento"
        )
        self.assertEqual(linea.clasificacion, "positivo")
        self.assertEqual(linea.numero_linea, 1)

    def test_crear_resumen_analisis(self):
        archivo = ArchivoAnalisis.objects.create(
            nombre_original="test.txt",
            contenido="Prueba"
        )
        resumen = ResumenAnalisis.objects.create(
            archivo=archivo,
            total_lineas=10,
            positivas=5,
            negativas=3,
            neutras=2,
            porcentaje_positivo=50.0,
            porcentaje_negativo=30.0,
            porcentaje_neutro=20.0,
            sentimiento_predominante="positivo"
        )
        self.assertEqual(resumen.total_lineas, 10)
        self.assertEqual(resumen.sentimiento_predominante, "positivo")

    def test_str_modelos(self):
        archivo = ArchivoAnalisis.objects.create(
            nombre_original="test.txt",
            contenido="Prueba"
        )
        self.assertEqual(str(archivo), "test.txt")

        linea = ResultadoLinea.objects.create(
            archivo=archivo,
            numero_linea=1,
            texto="Prueba",
            clasificacion="positivo",
            puntaje_polaridad=0.8,
            libreria_usada="pysentimiento"
        )
        self.assertIn("1", str(linea))
        self.assertIn("positivo", str(linea))

        resumen = ResumenAnalisis.objects.create(
            archivo=archivo,
            total_lineas=1,
            positivas=1,
            negativas=0,
            neutras=0,
            porcentaje_positivo=100.0,
            porcentaje_negativo=0.0,
            porcentaje_neutro=0.0,
            sentimiento_predominante="positivo"
        )
        self.assertIn("test.txt", str(resumen))


class ComandoConsolaTest(TestCase):
    """
    HU-07: Verifica el comando de consola.
    HU-12: Verifica manejo de errores en consola.
    """

    def setUp(self):
        self.archivo_valido = os.path.join(FIXTURES_DIR, 'positivo.txt')
        self.archivo_invalido = os.path.join(FIXTURES_DIR, 'no_existe.txt')
        self.archivo_no_txt = os.path.join(FIXTURES_DIR, '..', 'admin.py')

    def test_comando_consola_valido(self):
        try:
            call_command('analizar', self.archivo_valido)
        except Exception as e:
            self.fail(f'El comando falló: {e}')

        self.assertTrue(
            ArchivoAnalisis.objects.filter(nombre_original='positivo.txt').exists()
        )

    def test_comando_consola_archivo_inexistente(self):
        with self.assertRaises(CommandError):
            call_command('analizar', self.archivo_invalido)

    def test_comando_consola_archivo_no_txt(self):
        with self.assertRaises(CommandError):
            call_command('analizar', self.archivo_no_txt)

    def test_comando_consola_con_exportar_csv(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            call_command(
                'analizar',
                self.archivo_valido,
                exportar='csv'
            )

        self.assertTrue(
            ArchivoAnalisis.objects.filter(nombre_original='positivo.txt').exists()
        )

    def test_comando_consola_con_exportar_txt(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            call_command(
                'analizar',
                self.archivo_valido,
                exportar='txt'
            )

        self.assertTrue(
            ArchivoAnalisis.objects.filter(nombre_original='positivo.txt').exists()
        )