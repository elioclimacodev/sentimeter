import csv
import math
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import ArchivoAnalisis, ResultadoLinea, ResumenAnalisis
from .services import AnalizadorSentimiento

try:
    import plotly.graph_objects as go
except ImportError:
    go = None


def inicio(request):
    archivos = ArchivoAnalisis.objects.all()
    return render(request, 'sentiminer/inicio.html', {'archivos': archivos})


def subir_archivo(request):
    if request.method != 'POST':
        return redirect('inicio')

    archivo = request.FILES.get('archivo')

    if not archivo:
        messages.error(request, 'No se seleccionó ningún archivo.')
        return redirect('inicio')

    if not archivo.name.endswith('.txt'):
        messages.error(request, 'Solo se permiten archivos .txt')
        return redirect('inicio')

    try:
        contenido = archivo.read().decode('utf-8')
    except UnicodeDecodeError:
        try:
            archivo.seek(0)
            contenido = archivo.read().decode('latin-1')
        except Exception:
            messages.error(request, 'No se pudo leer el archivo. Verifique la codificación.')
            return redirect('inicio')

    if not contenido.strip():
        messages.error(request, 'El archivo está vacío.')
        return redirect('inicio')

    archivo_obj = ArchivoAnalisis.objects.create(
        nombre_original=archivo.name,
        contenido=contenido
    )

    try:
        analizador = AnalizadorSentimiento()
        analizador.procesar_archivo(archivo_obj.pk)
    except Exception as e:
        messages.error(request, f'Error al analizar el archivo: {str(e)}')
        return redirect('inicio')

    messages.success(request, 'Archivo analizado correctamente.')

    if request.headers.get('HX-Request'):
        response = HttpResponse()
        response['HX-Redirect'] = f'/resultados/{archivo_obj.pk}/'
        return response

    return redirect('resultados', archivo_id=archivo_obj.pk)


def resultados(request, archivo_id):
    """
    HU-04: Resumen cuantitativo con porcentajes.
    Muestra el dashboard completo con tarjetas de resumen,
    gráficos y tabla de resultados.
    """
    archivo = get_object_or_404(ArchivoAnalisis, pk=archivo_id)
    resumen = get_object_or_404(ResumenAnalisis, archivo=archivo)
    lineas = ResultadoLinea.objects.filter(archivo=archivo)

    return render(request, 'sentiminer/resultados.html', {
        'archivo': archivo,
        'resumen': resumen,
        'lineas': lineas,
    })


def grafico_sentimientos(request, archivo_id):
    """
    HU-05: Genera gráfico de pastel con la distribución de sentimientos.
    Se carga vía HTMX para actualización asíncrona.
    """
    archivo = get_object_or_404(ArchivoAnalisis, pk=archivo_id)
    resumen = get_object_or_404(ResumenAnalisis, archivo=archivo)

    etiquetas = ['Positivo', 'Negativo', 'Neutro']
    valores = [resumen.positivas, resumen.negativas, resumen.neutras]
    colores = ['#2fb344', '#d63939', '#656d77']

    fig = go.Figure(data=[
        go.Pie(
            labels=etiquetas,
            values=valores,
            marker=dict(colors=colores),
            hole=0.3,
            textinfo='label+percent',
            textfont=dict(size=14)
        )
    ])

    fig.update_layout(
        margin=dict(t=10, b=10, l=10, r=10),
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    grafico_html = fig.to_html(full_html=False, config={'displayModeBar': False})

    return render(request, 'sentiminer/_grafico_sentimientos.html', {
        'grafico_html': grafico_html
    })


def grafico_tendencia(request, archivo_id):
    """
    HU-09: Variación sentimental a lo largo del texto.
    Gráfico de línea que muestra la evolución del sentimiento
    línea por línea para detectar patrones.
    """
    archivo = get_object_or_404(ArchivoAnalisis, pk=archivo_id)
    lineas = ResultadoLinea.objects.filter(archivo=archivo)

    numeros = [l.numero_linea for l in lineas]
    puntajes = [l.puntaje_polaridad for l in lineas]
    textos = [l.texto[:60] + '...' if len(l.texto) > 60 else l.texto for l in lineas]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=numeros,
        y=puntajes,
        mode='lines+markers',
        name='Polaridad',
        line=dict(color='#206bc4', width=2),
        marker=dict(size=6),
        text=textos,
        hovertemplate='Línea %{x}<br>%{text}<br>Polaridad: %{y}<extra></extra>'
    ))

    fig.add_hline(
        y=0, line_dash='dash', line_color='gray', opacity=0.5,
        annotation_text='Neutro'
    )

    fig.update_layout(
        # title='Evolución del sentimiento por línea',
        xaxis_title='Número de línea',
        yaxis_title='Polaridad',
        margin=dict(t=40, b=40, l=40, r=20),
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    grafico_html = fig.to_html(full_html=False, config={'displayModeBar': False})

    return render(request, 'sentiminer/_grafico_tendencia.html', {
        'grafico_html': grafico_html
    })


def tabla_resultados(request, archivo_id):
    archivo = get_object_or_404(ArchivoAnalisis, pk=archivo_id)
    lineas = ResultadoLinea.objects.filter(archivo=archivo)

    clasificacion = request.GET.get('clasificacion', '').strip()
    q = request.GET.get('q', '').strip()
    per_page = request.GET.get('per_page', '10')
    page = request.GET.get('page', '1')

    if clasificacion in ('positivo', 'negativo', 'neutro'):
        lineas = lineas.filter(clasificacion=clasificacion)

    if q:
        lineas = lineas.filter(texto__icontains=q)

    try:
        per_page = int(per_page)
        if per_page not in (5, 10, 25, 50, 100):
            per_page = 10
    except (ValueError, TypeError):
        per_page = 10

    try:
        page = int(page)
        if page < 1:
            page = 1
    except (ValueError, TypeError):
        page = 1

    total_registros = lineas.count()
    total_paginas = math.ceil(total_registros / per_page) if total_registros > 0 else 1

    if page > total_paginas:
        page = total_paginas

    inicio = (page - 1) * per_page
    fin = inicio + per_page
    lineas_pagina = lineas[inicio:fin]

    rango_inicio = inicio + 1
    rango_fin = min(fin, total_registros)

    paginas = []
    if total_paginas <= 7:
        paginas = list(range(1, total_paginas + 1))
    else:
        paginas.append(1)
        if page > 3:
            paginas.append('...')
        start = max(2, page - 1)
        end = min(total_paginas - 1, page + 1)
        paginas.extend(range(start, end + 1))
        if page < total_paginas - 2:
            paginas.append('...')
        paginas.append(total_paginas)

    return render(request, 'sentiminer/_tabla_resultados.html', {
        'lineas': lineas_pagina,
        'page': page,
        'per_page': per_page,
        'total_paginas': total_paginas,
        'total_registros': total_registros,
        'rango_inicio': rango_inicio,
        'rango_fin': rango_fin,
        'clasificacion': clasificacion,
        'q': q,
        'archivo_id': archivo_id,
        'paginas': paginas,
    })


def exportar_csv(request, archivo_id):
    """
    HU-11: Exportación básica de resultados.
    Genera un archivo CSV con el análisis detallado por línea.
    """
    archivo = get_object_or_404(ArchivoAnalisis, pk=archivo_id)
    resumen = get_object_or_404(ResumenAnalisis, archivo=archivo)
    lineas = ResultadoLinea.objects.filter(archivo=archivo)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = (
        f'attachment; filename="{archivo.nombre_original}_analisis.csv"'
    )

    writer = csv.writer(response)
    writer.writerow(['Número de Línea', 'Texto', 'Clasificación', 'Polaridad', 'Librería'])

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
    writer.writerow(['Positivas', f'{resumen.positivas} ({resumen.porcentaje_positivo}%)'])
    writer.writerow(['Negativas', f'{resumen.negativas} ({resumen.porcentaje_negativo}%)'])
    writer.writerow(['Neutras', f'{resumen.neutras} ({resumen.porcentaje_neutro}%)'])
    writer.writerow(['Sentimiento predominante', resumen.sentimiento_predominante])

    return response


def exportar_txt(request, archivo_id):
    """
    HU-11: Exportación básica de resultados.
    Genera un archivo TXT con el análisis detallado por línea.
    """
    archivo = get_object_or_404(ArchivoAnalisis, pk=archivo_id)
    resumen = get_object_or_404(ResumenAnalisis, archivo=archivo)
    lineas = ResultadoLinea.objects.filter(archivo=archivo)

    contenido = []
    contenido.append(f"SentiMiner - Análisis Sentimental")
    contenido.append(f"=" * 60)
    contenido.append(f"Archivo: {archivo.nombre_original}")
    contenido.append(f"Fecha: {archivo.fecha_subida.strftime('%d/%m/%Y %H:%M')}")
    contenido.append(f"Total líneas analizadas: {resumen.total_lineas}")
    contenido.append("")
    contenido.append("ANÁLISIS POR LÍNEA:")
    contenido.append("-" * 60)

    for linea in lineas:
        etiqueta = f"[{linea.clasificacion.upper()}]".ljust(12)
        contenido.append(f"  #{linea.numero_linea:<4} {etiqueta} {linea.texto}")

    contenido.append("")
    contenido.append("RESUMEN:")
    contenido.append("-" * 60)
    contenido.append(f"  Positivas: {resumen.positivas} ({resumen.porcentaje_positivo}%)")
    contenido.append(f"  Negativas: {resumen.negativas} ({resumen.porcentaje_negativo}%)")
    contenido.append(f"  Neutras:   {resumen.neutras} ({resumen.porcentaje_neutro}%)")
    contenido.append("")
    contenido.append(f"  Sentimiento predominante: {resumen.sentimiento_predominante.upper()}")
    contenido.append("=" * 60)

    response = HttpResponse(
        '\n'.join(contenido),
        content_type='text/plain'
    )
    response['Content-Disposition'] = (
        f'attachment; filename="{archivo.nombre_original}_analisis.txt"'
    )

    return response