# 🦟 Dashboard Plan de Contingencia Fiebre Amarilla

Dashboard interactivo para el seguimiento de indicadores del Plan de Contingencia para Alertas y Emergencia por Fiebre Amarilla en Colombia.

## 📊 Características

- **17 indicadores** distribuidos en 5 líneas estratégicas
- **Seguimiento temporal** de los últimos 3 meses (Marzo-Mayo 2025)
- **Visualización automática** de indicadores cualitativos y cuantitativos
- **Corrección automática** de porcentajes mal calculados
- **Interfaz responsiva** adaptable a diferentes dispositivos

## 🚀 Tecnologías

- **Streamlit** - Framework web para Python
- **Plotly** - Gráficos interactivos
- **Pandas** - Procesamiento de datos
- **PIL** - Procesamiento de imágenes

## 📁 Estructura del Proyecto

```
streamlit-fiebre-amarilla/
├── dashboard_indicadores.py    # Aplicación principal
├── requirements.txt           # Dependencias de Python
├── indicadores.xlsx          # Archivo de datos Excel
├── Logo_gobernacion.png      # Logo de la Gobernación
├── README.md                 # Este archivo
└── .streamlit/
    └── config.toml           # Configuración de Streamlit
```

## 🛠️ Instalación Local

1. **Clonar el repositorio:**
```bash
git clone <url-del-repositorio>
cd streamlit-fiebre-amarilla
```

2. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación:**
```bash
streamlit run dashboard_indicadores.py
```

## 📂 Archivos de Datos

### `indicadores.xlsx`
Archivo Excel que contiene:
- **Hoja:** `Ficha_indicadores`
- **Estructura:** 17 indicadores con datos de seguimiento mensual
- **Períodos:** Marzo, Abril, Mayo 2025
- **Formato:** Incluye numerador, denominador e ILE para cada período

### `Logo_gobernacion.png`
Logotipo oficial de la Gobernación del Tolima en formato PNG.

## 🎯 Uso del Dashboard

### Pestañas Principales:

1. **📈 Progreso Temporal**
   - Gráficos individuales por indicador
   - Agrupación por líneas estratégicas
   - Información detallada de cada indicador

2. **📊 Resumen Ejecutivo**
   - Métricas generales de seguimiento
   - Distribución por líneas estratégicas
   - Gráficos de resumen

3. **📋 Datos Detallados**
   - Tabla completa de todos los datos
   - Opción de descarga en CSV

### Filtros Disponibles:
- **Línea Estratégica:** Filtrar por línea específica
- **Tipo de Indicador:** Proceso-Trazador o Resultado-Trazador

## 🔧 Configuración

El dashboard detecta automáticamente:
- **Indicadores cualitativos** (SI/NO)
- **Indicadores cuantitativos** (numéricos)
- **Corrección de porcentajes** (multiplica por 100 cuando es necesario)

## 👨‍💻 Desarrollador

**Ing. José Miguel Santos**  
*Secretaría de Salud del Tolima*

Desarrollado para la Gobernación del Tolima como herramienta de seguimiento y rendición de cuentas del Plan de Contingencia de Fiebre Amarilla.

## 📄 Licencia

Este proyecto fue desarrollado para uso interno de la Secretaría de Salud del Tolima.

## 🚀 Deployment en Streamlit Cloud

Este dashboard está optimizado para ejecutarse en Streamlit Cloud con todos los archivos necesarios incluidos.

### Requisitos del Sistema:
- Python 3.8+
- Archivos de datos en el repositorio
- Configuración automática de dependencias

---

*Dashboard actualizado para mostrar datos de seguimiento de marzo a mayo 2025*