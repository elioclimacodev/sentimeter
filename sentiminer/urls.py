from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('subir/', views.subir_archivo, name='subir_archivo'),
    path('resultados/<int:archivo_id>/', views.resultados, name='resultados'),
    path('resultados/<int:archivo_id>/grafico/', views.grafico_sentimientos, name='grafico_sentimientos'),
    path('resultados/<int:archivo_id>/tendencia/', views.grafico_tendencia, name='grafico_tendencia'),
    path('resultados/<int:archivo_id>/tabla/', views.tabla_resultados, name='tabla_resultados'),
    path('resultados/<int:archivo_id>/exportar/csv/', views.exportar_csv, name='exportar_csv'),
    path('resultados/<int:archivo_id>/exportar/txt/', views.exportar_txt, name='exportar_txt'),
]