import os
import csv
import webbrowser
import tempfile
import plotly.graph_objects as go
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from sentiminer.models import ArchivoAnalisis, ResultadoLinea, ResumenAnalisis
from sentiminer.services import AnalizadorSentimiento


class Command(BaseCommand):
    """
    HU-07: Ejecución del sistema desde consola.
    
    Comando de gestión de Django para analizar archivos .txt desde terminal.
    Uso: python manage.py analizar <archivo.txt> [--exportar csv|txt]
    
    HU-12: Manejo de errores con mensajes claros en caso de archivos inválidos.
    """

    help = 'HU-07: Analiza un archivo .txt y muestra resultados en consola'

    def add_arguments(self, parser):
        parser.add_argument(
            'archivo',
            type=str,
            help='Ruta al archivo .txt a analizar'
        )
        parser.add_argument(
            '--exportar',
            choices=['csv', 'txt'],
            help='Exporta los resultados en el formato especificado'
        )
        parser.add_argument(
            '--grafico',
            action='store_true',
            help='Abre un gráfico de resultados en el navegador (HU-06)'
        )

    def handle(self, *args, **options):
        ruta_archivo = options['archivo']
        formato_exportar = options['exportar']
        mostrar_grafico = options['grafico']

        if not os.path.exists(ruta_archivo):
            raise CommandError(f'El archivo "{ruta_archivo}" no existe.')

        if not ruta_archivo.endswith('.txt'):
            raise CommandError('Solo se permiten archivos .txt')

        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
        except UnicodeDecodeError:
            try:
                with open(ruta_archivo, 'r', encoding='latin-1') as f:
                    contenido = f.read()
            except Exception:
                raise CommandError('No se pudo leer el archivo. Verifique la codificación.')

        if not contenido.strip():
            raise CommandError('El archivo está vacío.')

        nombre_archivo = os.path.basename(ruta_archivo)

        self.stdout.write(self.style.SUCCESS('=== SentiMiner - Análisis Sentimental ==='))
        self.stdout.write(f'Archivo: {nombre_archivo}')

        archivo_obj = ArchivoAnalisis.objects.create(
            nombre_original=nombre_archivo,
            contenido=contenido
        )

        self.stdout.write('Analizando...')

        try:
            analizador = AnalizadorSentimiento()
            resultado = analizador.procesar_archivo(archivo_obj.pk)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al analizar: {str(e)}'))
            return

        lineas = resultado['lineas']
        resumen = resultado['resumen']

        self.stdout.write(f'Total líneas: {resumen.total_lineas}')
        self.stdout.write('')

        self.stdout.write(self.style.SUCCESS('CLASIFICACIÓN POR LÍNEA:'))
        self.stdout.write('-' * 60)

        for linea in lineas:
            color = self._color_clasificacion(linea.clasificacion)
            etiqueta = f'[{linea.clasificacion.upper()}]'.ljust(12)
            texto_truncado = (
                linea.texto[:65] + '...' if len(linea.texto) > 65 else linea.texto
            )
            self.stdout.write(
                color(f'  #{linea.numero_linea:<4} {etiqueta} {texto_truncado}')
            )

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('RESUMEN:'))
        self.stdout.write('-' * 60)
        self.stdout.write(
            f"  Positivas: {resumen.positivas} ({resumen.porcentaje_positivo}%)"
        )
        self.stdout.write(
            f"  Negativas: {resumen.negativas} ({resumen.porcentaje_negativo}%)"
        )
        self.stdout.write(
            f"  Neutras:   {resumen.neutras} ({resumen.porcentaje_neutro}%)"
        )
        self.stdout.write('')

        predominante = resumen.sentimiento_predominante.upper()
        color_pred = self._color_clasificacion(resumen.sentimiento_predominante)
        self.stdout.write(color_pred(f'  Sentimiento predominante: {predominante}'))
        self.stdout.write('=' * 60)

        if formato_exportar:
            self._exportar(archivo_obj, formato_exportar)

        if mostrar_grafico:
            self._mostrar_grafico(archivo_obj)

    def _color_clasificacion(self, clasificacion):
        if clasificacion == 'positivo':
            return self.style.SUCCESS
        elif clasificacion == 'negativo':
            return self.style.ERROR
        return self.style.WARNING

    def _exportar(self, archivo_obj, formato):
        """
        HU-11: Exportación de resultados desde consola.
        """
        lineas = ResultadoLinea.objects.filter(archivo=archivo_obj)
        resumen = ResumenAnalisis.objects.get(archivo=archivo_obj)
        nombre_base = Path(archivo_obj.nombre_original).stem

        if formato == 'csv':
            ruta_salida = f'{nombre_base}_analisis.csv'
            with open(ruta_salida, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(
                    ['Número de Línea', 'Texto', 'Clasificación', 'Polaridad', 'Librería']
                )
                for linea in lineas:
                    writer.writerow([
                        linea.numero_linea,
                        linea.texto,
                        linea.clasificacion,
                        linea.puntaje_polaridad,
                        linea.libreria_usada
                    ])
                writer.writerow([])
                writer.writerow(['RESUMEN'])
                writer.writerow(['Total líneas', resumen.total_lineas])
                writer.writerow(
                    ['Positivas', f'{resumen.positivas} ({resumen.porcentaje_positivo}%)']
                )
                writer.writerow(
                    ['Negativas', f'{resumen.negativas} ({resumen.porcentaje_negativo}%)']
                )
                writer.writerow(
                    ['Neutras', f'{resumen.neutras} ({resumen.porcentaje_neutro}%)']
                )
                writer.writerow(
                    ['Sentimiento predominante', resumen.sentimiento_predominante]
                )
        elif formato == 'txt':
            ruta_salida = f'{nombre_base}_analisis.txt'
            contenido = []
            contenido.append("SentiMiner - Análisis Sentimental")
            contenido.append(f"Archivo: {archivo_obj.nombre_original}")
            contenido.append(f"Total líneas: {resumen.total_lineas}")
            contenido.append("")
            for linea in lineas:
                etiqueta = f"[{linea.clasificacion.upper()}]".ljust(12)
                contenido.append(f"  #{linea.numero_linea:<4} {etiqueta} {linea.texto}")
            contenido.append("")
            contenido.append(
                f"Positivas: {resumen.positivas} ({resumen.porcentaje_positivo}%)"
            )
            contenido.append(
                f"Negativas: {resumen.negativas} ({resumen.porcentaje_negativo}%)"
            )
            contenido.append(
                f"Neutras: {resumen.neutras} ({resumen.porcentaje_neutro}%)"
            )
            contenido.append(
                f"Sentimiento predominante: {resumen.sentimiento_predominante.upper()}"
            )

            with open(ruta_salida, 'w', encoding='utf-8') as f:
                f.write('\n'.join(contenido))

        self.stdout.write(self.style.SUCCESS(f'Resultados exportados a: {ruta_salida}'))

    def _mostrar_grafico(self, archivo_obj):
        """
        HU-06: Muestra un gráfico de pastel en el navegador.
        """
        lineas = ResultadoLinea.objects.filter(archivo=archivo_obj)
        resumen = ResumenAnalisis.objects.get(archivo=archivo_obj)

        etiquetas = ['Positivo', 'Negativo', 'Neutro']
        valores = [resumen.positivas, resumen.negativas, resumen.neutras]
        colores = ['#2fb344', '#d63939', '#656d77']

        fig = go.Figure(data=[
            go.Pie(
                labels=etiquetas,
                values=valores,
                marker=dict(colors=colores),
                hole=0.3,
                textinfo='label+percent'
            )
        ])

        fig.update_layout(
            title=f'Análisis: {archivo_obj.nombre_original}',
            height=500
        )

        with tempfile.NamedTemporaryFile(
            suffix='.html', delete=False, encoding='utf-8', mode='w'
        ) as f:
            f.write(fig.to_html(full_html=True))
            ruta_html = f.name

        webbrowser.open(ruta_html)
        self.stdout.write(
            self.style.SUCCESS(f'Gráfico abierto en el navegador.')
        )