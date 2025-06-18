import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import warnings
from PIL import Image
warnings.filterwarnings('ignore')

# Configuración de la página
st.set_page_config(
    page_title="Dashboard - Plan Contingencia Fiebre Amarilla",
    page_icon="🦟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal (sin logo aquí)
st.title("🦟 Plan de Contingencia para Alertas y Emergencia por Fiebre Amarilla")
st.markdown("### 📊 **Seguimiento de Indicadores - Rendición de Cuentas**")
st.markdown("**Secretaría de Salud del Tolima**")
st.markdown("---")

@st.cache_data
def load_and_process_data():
    """
    Carga y procesa el archivo Excel de indicadores
    """
    try:
        # Leer el archivo Excel
        df = pd.read_excel('indicadores.xlsx', sheet_name='Ficha_indicadores', header=None)
        
        # Identificar las filas de encabezados
        header_row = 1  # Fila 2 (índice 1)
        subheader_row = 3  # Fila 4 (índice 3)
        data_start_row = 4  # Datos empiezan en fila 5 (índice 4)
        
        # Extraer datos de indicadores
        indicadores_data = []
        
        # Solo últimos 3 meses: Marzo, Abril, Mayo 2025
        periodos = [
            ("Mar 2025", [23, 24, 25]),  # Columnas X, Y, Z
            ("Abr 2025", [26, 27, 28]),  # Columnas AA, AB, AC
            ("May 2025", [29, 30, 31]),  # Columnas AD, AE, AF
        ]
        
        # Procesar cada fila de indicadores (empezando desde la fila 5)
        for row_idx in range(data_start_row, min(data_start_row + 25, len(df))):
            try:
                # Verificar si hay un número de indicador
                if pd.isna(df.iloc[row_idx, 0]) or df.iloc[row_idx, 0] == '':
                    continue
                    
                numero = df.iloc[row_idx, 0]
                linea = str(df.iloc[row_idx, 1]) if not pd.isna(df.iloc[row_idx, 1]) else ""
                nombre = str(df.iloc[row_idx, 2]) if not pd.isna(df.iloc[row_idx, 2]) else ""
                tipo = str(df.iloc[row_idx, 3]) if not pd.isna(df.iloc[row_idx, 3]) else ""
                definicion = str(df.iloc[row_idx, 4]) if not pd.isna(df.iloc[row_idx, 4]) else ""
                
                # Si el número no es numérico, continuar
                try:
                    numero = int(float(numero))
                except:
                    continue
                
                # Extraer número de línea estratégica para ordenamiento
                linea_numero = 999  # Valor por defecto
                try:
                    if linea.strip():
                        linea_numero = int(linea.split('.')[0])
                except:
                    pass
                
                # Extraer datos de cada período
                datos_periodos = {}
                for periodo_name, cols in periodos:
                    try:
                        if len(cols) >= 3 and all(col < len(df.columns) for col in cols):
                            numerador = df.iloc[row_idx, cols[0]]
                            denominador = df.iloc[row_idx, cols[1]]
                            ile = df.iloc[row_idx, cols[2]]
                            
                            # Limpiar datos
                            numerador = str(numerador).strip() if not pd.isna(numerador) else ""
                            denominador = str(denominador).strip() if not pd.isna(denominador) else ""
                            ile = str(ile).strip() if not pd.isna(ile) else ""
                            
                            datos_periodos[periodo_name] = {
                                'numerador': numerador,
                                'denominador': denominador,
                                'ile': ile
                            }
                    except Exception as e:
                        datos_periodos[periodo_name] = {
                            'numerador': "",
                            'denominador': "",
                            'ile': ""
                        }
                
                indicadores_data.append({
                    'numero': numero,
                    'linea': linea,
                    'linea_numero': linea_numero,
                    'nombre': nombre,
                    'tipo': tipo,
                    'definicion': definicion,
                    'datos': datos_periodos
                })
                
            except Exception as e:
                continue
        
        # Ordenar por línea estratégica y luego por número de indicador
        indicadores_data.sort(key=lambda x: (x['linea_numero'], x['numero']))
        
        return indicadores_data
        
    except Exception as e:
        st.error(f"Error al cargar el archivo: {str(e)}")
        return []

def detect_indicator_type(indicador_data, periodos):
    """
    Detecta si un indicador es cualitativo (SI/NO) o cuantitativo (numérico)
    """
    valores_ile = []
    
    for periodo in periodos:
        if periodo in indicador_data['datos']:
            ile = indicador_data['datos'][periodo]['ile']
            if ile and ile.strip():
                valores_ile.append(ile.strip().upper())
    
    if not valores_ile:
        return "sin_datos"
    
    # Verificar si todos los valores son SI/NO
    valores_si_no = ['SI', 'NO']
    es_cualitativo = all(val in valores_si_no for val in valores_ile if val)
    
    if es_cualitativo:
        return "cualitativo"
    else:
        return "cuantitativo"

def corregir_porcentaje(valor):
    """
    Corrige porcentajes que vienen como decimales del Excel multiplicando por 100
    """
    try:
        num = float(valor.replace(',', '.'))
        # Si es un decimal entre 0 y 1 (inclusive), probablemente es un porcentaje mal calculado
        if 0 <= num <= 1:
            return num * 100
        return num
    except:
        return valor

def create_progress_chart(indicador_data, periodos):
    """
    Crea gráfico de progreso para un indicador específico
    """
    valores = []
    etiquetas = []
    valores_originales = []
    valores_display = []
    
    for periodo in periodos:
        if periodo in indicador_data['datos']:
            ile = indicador_data['datos'][periodo]['ile']
            etiquetas.append(periodo)
            
            if ile and ile.strip() and ile.strip() != "":
                # Intentar convertir a número si es posible
                try:
                    if ile.upper() == 'SI':
                        valores.append(1)
                        valores_originales.append('SI')
                        valores_display.append(1)
                    elif ile.upper() == 'NO':
                        valores.append(0)
                        valores_originales.append('NO')
                        valores_display.append(1)
                    else:
                        # Intentar como número y corregir porcentaje si es necesario
                        numero = corregir_porcentaje(ile)
                        valores.append(numero)
                        # Mostrar el valor corregido en el gráfico
                        if isinstance(numero, float):
                            valores_originales.append(f"{numero:.1f}")
                        else:
                            valores_originales.append(str(numero))
                        valores_display.append(numero)
                except:
                    valores.append(None)
                    valores_originales.append('Pendiente')
                    valores_display.append(None)
            else:
                valores.append(None)
                valores_originales.append('Pendiente')
                valores_display.append(None)
    
    if not valores or all(v is None for v in valores):
        return None
    
    # Detectar tipo de indicador
    tipo_indicador = detect_indicator_type(indicador_data, periodos)
    
    # Crear gráfico
    fig = go.Figure()
    
    if tipo_indicador == "cualitativo":
        # Gráfico de barras para indicadores SI/NO
        colores = []
        textos = []
        valores_barras = []
        
        for i, val in enumerate(valores):
            if val == 1 and valores_originales[i] == 'SI':
                colores.append('#28a745')  # Verde para SI
                textos.append('SI')
                valores_barras.append(1)
            elif val == 0 and valores_originales[i] == 'NO':
                colores.append('#dc3545')  # Rojo para NO
                textos.append('NO')
                valores_barras.append(1)
            else:
                colores.append('#6c757d')  # Gris para pendiente
                textos.append('Pendiente')
                valores_barras.append(0.5)
        
        fig.add_trace(go.Bar(
            x=etiquetas,
            y=valores_barras,
            marker_color=colores,
            text=textos,
            textposition='inside',
            textfont=dict(color='white', size=14)
        ))
        
        fig.update_layout(
            yaxis=dict(tickvals=[0, 0.5, 1], ticktext=['', 'Pendiente', 'Cumplido']),
            height=350
        )
        
    else:
        # Gráfico de línea para indicadores cuantitativos
        fig.add_trace(go.Scatter(
            x=etiquetas,
            y=valores_display,
            mode='lines+markers+text',
            line=dict(color='#007bff', width=3),
            marker=dict(size=10, color='#007bff'),
            text=valores_originales,
            textposition='top center',
            connectgaps=False
        ))
        
        fig.update_layout(height=350)
    
    fig.update_layout(
        title=f"Indicador {indicador_data['numero']}: {indicador_data['nombre'][:50]}...",
        xaxis_title="Período",
        showlegend=False,
        template="plotly_white",
        font=dict(size=12),
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig

def get_linea_estrategica_nombre(linea_texto):
    """
    Extrae el nombre de la línea estratégica
    """
    if not linea_texto or linea_texto.strip() == "":
        return "Sin clasificar"
    
    # Mapeo de líneas estratégicas conocidas
    lineas_map = {
        "1.": "1. Gestión integral de la contingencia",
        "2.": "2. Intensificación de la vigilancia",
        "3.": "3. Promoción de la salud y prevención",
        "4.": "4. Atención integral de casos",
        "5.": "5. Comunicación del riesgo y comunitaria"
    }
    
    linea_num = linea_texto.split('.')[0] + '.'
    return lineas_map.get(linea_num, linea_texto[:50])

def main():
    # Cargar datos
    with st.spinner("Cargando datos del archivo Excel..."):
        indicadores = load_and_process_data()
    
    if not indicadores:
        st.error("No se pudieron cargar los datos. Asegúrate de que el archivo 'indicadores.xlsx' esté en el directorio correcto.")
        return
    
    st.success(f"✅ Datos cargados exitosamente: **{len(indicadores)} indicadores** | **Últimos 3 meses: Mar-May 2025**")
    
    # Sidebar para filtros y logo
    with st.sidebar:
        # Logo en el sidebar - Más pequeño
        try:
            logo = Image.open("Logo_gobernacion.png")
            st.image(logo, width=150)
            st.markdown("---")
        except:
            st.markdown("🏛️ **Gobernación del Tolima**")
            st.markdown("---")
        
        st.header("🔧 Configuración")
        
        # Filtro por línea estratégica
        lineas_unicas = list(set([get_linea_estrategica_nombre(ind['linea']) for ind in indicadores]))
        lineas_unicas.sort()
        
        linea_seleccionada = st.selectbox(
            "Seleccionar Línea Estratégica:",
            options=["Todas"] + lineas_unicas,
            index=0
        )
        
        # Filtro por tipo de indicador
        tipos_unicos = list(set([ind['tipo'] for ind in indicadores if ind['tipo']]))
        tipo_seleccionado = st.selectbox(
            "Tipo de Indicador:",
            options=["Todos"] + tipos_unicos,
            index=0
        )
        
        st.markdown("---")
        st.markdown("### 📋 Resumen")
        st.markdown(f"**Total indicadores:** {len(indicadores)}")
        st.markdown(f"**Períodos:** 3 meses")
        st.markdown(f"**Líneas estratégicas:** 5")
        
        st.markdown("---")
        st.markdown("### 👨‍💻 Información del Sistema")
        st.markdown("**Desarrollado por:**")
        st.markdown("**Ing. José Miguel Santos**")
        st.markdown("*Secretaría de Salud del Tolima*")
    
    # Filtrar indicadores
    indicadores_filtrados = indicadores.copy()
    
    if linea_seleccionada != "Todas":
        indicadores_filtrados = [ind for ind in indicadores_filtrados 
                               if get_linea_estrategica_nombre(ind['linea']) == linea_seleccionada]
    
    if tipo_seleccionado != "Todos":
        indicadores_filtrados = [ind for ind in indicadores_filtrados 
                               if ind['tipo'] == tipo_seleccionado]
    
    # Períodos definidos (últimos 3 meses)
    periodos = ["Mar 2025", "Abr 2025", "May 2025"]
    
    # Pestañas principales
    tab1, tab2, tab3 = st.tabs(["📈 Progreso Temporal", "📊 Resumen Ejecutivo", "📋 Datos Detallados"])
    
    with tab1:
        st.header("📈 Progreso Temporal de Indicadores")
        st.markdown("*Últimos 3 meses: Marzo - Abril - Mayo 2025*")
        
        if not indicadores_filtrados:
            st.warning("No hay indicadores que coincidan con los filtros seleccionados.")
            return
        
        # Agrupar por línea estratégica
        indicadores_por_linea = {}
        for indicador in indicadores_filtrados:
            linea_nombre = get_linea_estrategica_nombre(indicador['linea'])
            if linea_nombre not in indicadores_por_linea:
                indicadores_por_linea[linea_nombre] = []
            indicadores_por_linea[linea_nombre].append(indicador)
        
        # Mostrar por línea estratégica
        for linea_nombre in sorted(indicadores_por_linea.keys()):
            st.subheader(f"🎯 {linea_nombre}")
            
            indicadores_linea = indicadores_por_linea[linea_nombre]
            
            for indicador in indicadores_linea:
                # Usar expanders como antes, pero mejorados
                with st.expander(f"**{indicador['numero']}. {indicador['nombre']}**", expanded=False):
                    
                    # Layout responsive con columnas
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Tipo:** {indicador['tipo']}")
                        st.markdown(f"**Línea:** {indicador['linea']}")
                        
                        # Definición operacional con toggle para ver completa
                        st.markdown("**Definición operacional:**")
                        if len(indicador['definicion']) > 200:
                            mostrar_def_completa = st.checkbox(
                                "Ver definición completa", 
                                key=f"def_{indicador['numero']}"
                            )
                            if mostrar_def_completa:
                                st.info(indicador['definicion'])
                            else:
                                definicion_corta = indicador['definicion'][:200] + "..."
                                st.info(definicion_corta)
                        else:
                            st.info(indicador['definicion'])
                    
                    with col2:
                        # Calcular seguimiento
                        total_periodos = len(periodos)
                        reportados = sum(1 for p in periodos 
                                       if indicador['datos'].get(p, {}).get('ile', '').strip())
                        seguimiento = (reportados / total_periodos) * 100
                        st.metric("Seguimiento", f"{seguimiento:.0f}%")
                        
                        # Mostrar tipo de indicador detectado
                        tipo_detected = detect_indicator_type(indicador, periodos)
                        if tipo_detected == "cualitativo":
                            st.info("📊 Cualitativo")
                        elif tipo_detected == "cuantitativo":
                            st.info("📈 Cuantitativo")
                        else:
                            st.info("⚪ Sin datos")
                    
                    # Gráfico de progreso
                    fig = create_progress_chart(indicador, periodos)
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No hay datos suficientes para generar el gráfico.")
                    
                    # Tabla de datos responsive
                    st.markdown("**Datos por período:**")
                    datos_tabla = []
                    for periodo in periodos:
                        if periodo in indicador['datos']:
                            datos = indicador['datos'][periodo]
                            ile_corregido = datos['ile']
                            
                            # Aplicar corrección de porcentaje si es necesario
                            if datos['ile'] and datos['ile'].strip():
                                try:
                                    if datos['ile'].upper() not in ['SI', 'NO']:
                                        ile_value = corregir_porcentaje(datos['ile'])
                                        if isinstance(ile_value, float):
                                            ile_corregido = f"{ile_value:.1f}"
                                except:
                                    pass
                            
                            datos_tabla.append({
                                'Período': periodo,
                                'Numerador': datos['numerador'] or 'Pendiente',
                                'Denominador': datos['denominador'] or 'N/A',
                                'ILE': ile_corregido or 'Pendiente'
                            })
                    
                    if datos_tabla:
                        df_tabla = pd.DataFrame(datos_tabla)
                        st.dataframe(df_tabla, use_container_width=True)
    
    with tab2:
        st.header("📊 Resumen Ejecutivo")
        st.markdown("*Últimos 3 meses: Marzo - Abril - Mayo 2025*")
        
        # Métricas generales - Layout responsive
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Indicadores", len(indicadores_filtrados))
        
        with col2:
            # Calcular promedio de seguimiento
            seguimientos = []
            for ind in indicadores_filtrados:
                reportados = sum(1 for p in periodos 
                               if ind['datos'].get(p, {}).get('ile', '').strip())
                seguimientos.append((reportados / len(periodos)) * 100)
            promedio_seguimiento = sum(seguimientos) / len(seguimientos) if seguimientos else 0
            st.metric("Seguimiento Promedio", f"{promedio_seguimiento:.1f}%")
        
        with col3:
            # Indicadores con datos completos
            completos = sum(1 for seg in seguimientos if seg == 100)
            st.metric("Indicadores Completos", completos)
        
        with col4:
            # Último período reportado
            st.metric("Último Período", "May 2025")
        
        st.markdown("---")
        
        # Gráfico de seguimiento por línea estratégica
        st.subheader("🎯 Seguimiento por Línea Estratégica")
        
        seguimiento_por_linea = {}
        for ind in indicadores_filtrados:
            linea_key = get_linea_estrategica_nombre(ind['linea'])
            if linea_key not in seguimiento_por_linea:
                seguimiento_por_linea[linea_key] = []
            
            reportados = sum(1 for p in periodos 
                           if ind['datos'].get(p, {}).get('ile', '').strip())
            seguimiento_por_linea[linea_key].append((reportados / len(periodos)) * 100)
        
        if seguimiento_por_linea:
            lineas = list(seguimiento_por_linea.keys())
            promedios = [sum(vals) / len(vals) for vals in seguimiento_por_linea.values()]
            
            fig_seguimiento = go.Figure(data=[
                go.Bar(x=lineas, y=promedios, 
                      marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57'][:len(lineas)])
            ])
            fig_seguimiento.update_layout(
                title="Seguimiento Promedio por Línea Estratégica (%)",
                xaxis_title="Línea Estratégica",
                yaxis_title="Seguimiento (%)",
                template="plotly_white",
                height=400,
                margin=dict(l=20, r=20, t=60, b=20)
            )
            st.plotly_chart(fig_seguimiento, use_container_width=True)
        
        # Layout responsive para gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribución de tipos de indicadores
            st.subheader("📊 Distribución de Tipos")
            tipos_count = {}
            for ind in indicadores_filtrados:
                tipo = ind['tipo']
                tipos_count[tipo] = tipos_count.get(tipo, 0) + 1
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=list(tipos_count.keys()),
                values=list(tipos_count.values()),
                hole=0.4
            )])
            fig_pie.update_layout(
                title="Tipos de Indicadores", 
                height=400,
                margin=dict(l=20, r=20, t=60, b=20)
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Tabla de resumen por línea
            st.subheader("📋 Resumen por Línea")
            resumen_lineas = []
            for linea_key, seguimientos_linea in seguimiento_por_linea.items():
                nombre_corto = linea_key.split('.')[1].strip() if '.' in linea_key else linea_key
                resumen_lineas.append({
                    'Línea': nombre_corto[:20] + "..." if len(nombre_corto) > 20 else nombre_corto,
                    'Indicadores': len(seguimientos_linea),
                    'Seguimiento (%)': f"{sum(seguimientos_linea) / len(seguimientos_linea):.1f}%"
                })
            
            if resumen_lineas:
                df_resumen = pd.DataFrame(resumen_lineas)
                st.dataframe(df_resumen, use_container_width=True)
    
    with tab3:
        st.header("📋 Datos Detallados")
        st.markdown("*Últimos 3 meses: Marzo - Abril - Mayo 2025*")
        
        # Tabla completa de todos los indicadores
        tabla_completa = []
        for ind in indicadores_filtrados:
            for periodo in periodos:
                if periodo in ind['datos']:
                    datos = ind['datos'][periodo]
                    
                    # Aplicar corrección de porcentaje
                    ile_corregido = datos['ile'] or 'Pendiente'
                    if datos['ile'] and datos['ile'].strip():
                        try:
                            if datos['ile'].upper() not in ['SI', 'NO']:
                                ile_value = corregir_porcentaje(datos['ile'])
                                if isinstance(ile_value, float):
                                    ile_corregido = f"{ile_value:.1f}"
                        except:
                            pass
                    
                    tabla_completa.append({
                        'Indicador': ind['numero'],
                        'Nombre': ind['nombre'],
                        'Línea': get_linea_estrategica_nombre(ind['linea']),
                        'Tipo': ind['tipo'],
                        'Definición': ind['definicion'],
                        'Período': periodo,
                        'Numerador': datos['numerador'] or 'Pendiente',
                        'Denominador': datos['denominador'] or 'N/A',
                        'ILE': ile_corregido
                    })
        
        if tabla_completa:
            df_completa = pd.DataFrame(tabla_completa)
            st.dataframe(df_completa, use_container_width=True, height=600)
            
            # Opción de descarga
            csv = df_completa.to_csv(index=False)
            st.download_button(
                label="📥 Descargar datos como CSV",
                data=csv,
                file_name="indicadores_fiebre_amarilla_mar_may_2025.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()