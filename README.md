# Yenka IA1 Trading Assistant: Plataforma de Señales para la Bolsa de Valores

## Descripción General
Este proyecto tiene como objetivo desarrollar una aplicación de inteligencia artificial para facilitar el trading de acciones en la bolsa de valores de EE.UU. La aplicación integrará análisis técnico (indicadores financieros) y análisis fundamental (resúmenes generados por modelos de lenguaje grandes, LLMs) con capacidades predictivas y automatización a través de agentes inteligentes.

## Relevancia
La creciente necesidad de herramientas accesibles y automatizadas empodera a traders no profesionales al proporcionarles análisis avanzados y claros. Este proyecto impactará positivamente al democratizar el acceso a estrategias complejas de inversión.

## Público Objetivo
- Inversionistas individuales (retail traders).
- Traders novatos que buscan herramientas de apoyo visual y analítico.
- Estudiantes de finanzas interesados en estrategias de inversión.

## Objetivo del Proyecto
Diseñar una herramienta que combine modelos de lenguaje grandes (LLMs), algoritmos de machine learning y agentes inteligentes para:
- Analizar datos financieros históricos y métricas fundamentales.
- Generar señales de compra, venta y liquidación en tiempo real.
- Presentar resultados mediante una interfaz visual y accesible.

## Roadmap del Proyecto

### Nivel Esencial (MVP)
**Plazo estimado:** 3-4 días hábiles  
**Objetivo:** Crear un prototipo funcional que permita cargar datos, realizar análisis técnico básico y mostrar gráficos interactivos.

#### Actividades Principales
- **Carga y procesamiento de datos**
    - Conexión a APIs (p. ej., Alpha Vantage o Yahoo Finance) para descargar datos históricos de precios.
    - Limpieza y preprocesamiento de datos (formato CSV o JSON).
- **Análisis técnico básico**
    - Implementación de medias móviles simples (SMA) y exponenciales (EMA).
    - Generación de señales de compra/venta basadas en cruces de medias móviles (golden cross y death cross).
- **Visualización de datos**
    - Creación de gráficos de precios e indicadores técnicos usando Plotly.
    - Interfaz básica en Streamlit que permita seleccionar acciones y ver señales generadas.
- **Infraestructura básica**
    - Configuración del repositorio en GitHub y entorno de desarrollo (Docker o virtualenv).

**Resultado esperado:** Aplicación funcional con carga de datos, visualización de gráficos y generación de señales básicas.

### Nivel Medio
**Plazo estimado:** 4-5 días hábiles  
**Objetivo:** Ampliar el análisis técnico y agregar capacidades iniciales de análisis fundamental mediante LLMs.

#### Actividades Principales
- **Análisis técnico avanzado**
    - Incorporar indicadores adicionales como RSI, MACD y soporte/resistencia.
    - Personalización de parámetros para los indicadores.
- **Integración con LLMs**
    - Uso de LangChain para conectar un modelo LLM (como GPT-4).
    - Creación de prompts para:
        - Resumir reportes financieros.
        - Extraer métricas clave (p. ej., P/E ratio, EPS).
- **Interacción con el usuario**
    - Opciones para introducir tickers de acciones y consultar recomendaciones técnicas y fundamentales.
    - Descarga de gráficos y datos en formato CSV.
- **Infraestructura optimizada**
    - Migración a SQLite para consultas más rápidas de datos históricos.

**Resultado esperado:** Herramienta robusta con análisis técnico avanzado y resúmenes generados por LLMs.

### Nivel Avanzado
**Plazo estimado:** 5 días hábiles  
**Objetivo:** Incorporar capacidades predictivas, agentes inteligentes y optimización de la interfaz.

#### Actividades Principales
- **Modelo predictivo de Machine Learning**
    - Implementar un modelo como XGBoost o Prophet para predicción de precios.
    - Validación del modelo con datos históricos.
- **Optimización con agentes IA**
    - Configurar agentes con LangChain para:
        - Analizar datos en tiempo real.
        - Generar alertas automáticas con reglas definidas por el usuario.
- **Interfaz avanzada**
    - Dashboards interactivos para:
        - Comparar señales de múltiples acciones.
        - Mostrar métricas de rendimiento y proyecciones.
    - Personalización avanzada de parámetros del modelo.
- **Infraestructura final**
    - Implementación de contenedores Docker y migración a PostgreSQL si la carga de datos aumenta.
    - Despliegue en la nube (AWS, Heroku).

**Resultado esperado:** Aplicación predictiva y automatizada con una interfaz optimizada.

## Tecnologías Propuestas
- **Lenguajes:** Python, JavaScript (opcional para React).
- **Frameworks y Librerías:** LangChain, TensorFlow, Scikit-learn, Plotly, Streamlit/Django/React.
- **Bases de Datos:** SQLite (esencial), PostgreSQL (avanzado).
- **APIs:** Alpha Vantage, Yahoo Finance.
- **Infraestructura:** Docker, GitHub.I Trading Assistant: Plataforma de Señales para la Bolsa de Valores



---
# Plan de Acción Detallado para el Mínimo Producto Viable (Nivel Esencial)

**Duración Estimada Total:** 3-4 días hábiles (32 horas de trabajo efectivo)  
**Objetivo Principal:** Crear un prototipo funcional que permita cargar datos, realizar análisis técnico básico, generar señales de compra/venta y mostrar gráficos interactivos en una interfaz de usuario.

### Día 1: Configuración Inicial y Preparación de Entorno (6 horas)

**Actividades:**

1. **Configuración del Control de Versiones (GitHub)**
    - Crear un repositorio en GitHub.
    - Configurar un archivo `.gitignore` que excluya archivos sensibles como claves de API y entornos virtuales.
    - Establecer las ramas `main` y `development` para manejar el flujo de trabajo.
    - **Duración estimada:** 1 hora.

2. **Configuración del Entorno de Desarrollo (Conda)**
    - Crear un entorno virtual usando Conda.
    - Instalar librerías esenciales: `pandas`, `plotly`, `streamlit`, `requests`, `pytest`.
    - Generar un archivo `environment.yml` para documentar las dependencias del entorno.
    - **Duración estimada:** 2 horas.

3. **Documentación Inicial**
    - Crear un archivo `README.md` con los siguientes apartados:
        - Descripción del proyecto.
        - Objetivos iniciales.
        - Instrucciones para clonar el repositorio y configurar el entorno con Conda.
    - **Duración estimada:** 2 horas.

4. **Preparación de Claves y APIs**
    - Registrar cuentas en APIs de datos financieros (Alpha Vantage, Yahoo Finance).
    - Configurar variables de entorno para almacenar claves API en un archivo `.env`.
    - **Duración estimada:** 1 hora.

### Día 2: Procesamiento de Datos y Generación de Señales Básicas (8 horas)

**Actividades:**

1. **Descarga y Limpieza de Datos**
    - Crear un módulo en Python para conectarse a la API financiera.
    - Descargar datos históricos de precios en formato JSON/CSV.
    - Implementar funciones para limpiar y preprocesar los datos: manejo de valores nulos, formateo de fechas y generación de columnas adicionales (p. ej., variación porcentual).
    - **Duración estimada:** 3 horas.

2. **Implementación de Indicadores Técnicos**
    - Calcular medias móviles simples (SMA) y exponenciales (EMA) usando `pandas`.
    - Implementar lógica para detectar cruces de medias móviles (golden cross y death cross).
    - **Duración estimada:** 2 horas.

3. **Pruebas Unitarias del Procesamiento de Datos**
    - Crear casos de prueba con `pytest` para validar la limpieza y el cálculo de indicadores técnicos.
    - Documentar las pruebas en el repositorio con ejemplos de entradas y salidas esperadas.
    - **Duración estimada:** 2 horas.

4. **Documentación del Módulo de Procesamiento**
    - Actualizar el `README.md` con los siguientes apartados:
        - Estructura del módulo: funciones principales y su propósito.
        - Ejemplo de uso con capturas de pantalla o salidas generadas.
        - Limitaciones actuales y posibles mejoras.
    - **Duración estimada:** 1 hora.

### Día 3: Interfaz Básica y Visualización de Datos (8 horas)

**Actividades:**

1. **Creación de la Interfaz en Streamlit**
    - Configurar un archivo principal (`app.py`) que permita:
        - Cargar datos desde el módulo desarrollado.
        - Seleccionar una acción específica para análisis.
    - **Duración estimada:** 3 horas.

2. **Visualización Gráfica**
    - Usar `plotly` para graficar precios históricos con las SMA y EMA.
    - Superponer las señales generadas (golden cross y death cross) en el gráfico.
    - **Duración estimada:** 3 horas.

3. **Pruebas de la Interfaz**
    - Validar la funcionalidad básica de la aplicación en diferentes navegadores.
    - Documentar cualquier error encontrado y las soluciones implementadas.
    - **Duración estimada:** 1 hora.

4. **Documentación de la Interfaz**
    - Añadir al `README.md` los siguientes apartados:
        - Capturas de pantalla de la interfaz funcional.
        - Guía para usar la aplicación y explorar las funcionalidades básicas.
        - Limitaciones actuales.
    - **Duración estimada:** 1 hora.

### Día 4: Revisión Final y Actualización en GitHub (8 horas)

**Actividades:**

1. **Revisión y Optimización**
    - Revisar y limpiar el código: eliminar redundancias y optimizar funciones clave.
    - Comentar funciones críticas para facilitar la comprensión del código.
    - **Duración estimada:** 2 horas.

2. **Pruebas Finales**
    - Ejecutar pruebas unitarias y de integración en todo el proyecto para validar que las funciones del MVP operan correctamente.
    - **Duración estimada:** 2 horas.

3. **Actualización del Repositorio en GitHub**
    - Subir la versión final del MVP a la rama `main`.
    - Añadir etiquetas y actualizar la estructura del `README.md` para reflejar el estado actual del proyecto.
    - **Duración estimada:** 1 hora.

4. **Planificación para el Siguiente Nivel**
    - Documentar tareas pendientes y mejoras necesarias para el nivel medio.
    - Crear issues en GitHub para organizar las funcionalidades que se implementarán posteriormente.
    - **Duración estimada:** 1 hora.

5. **Actualización Final de Documentación**
    - Revisar que el `README.md` incluya:
        - Un resumen completo del MVP.
        - Explicación de los módulos desarrollados.
        - Instrucciones claras para ejecutar el MVP localmente.
    - **Duración estimada:** 2 horas.

### Resumen de Tiempo

| Día  | Actividad Principal                  | Horas  |
|------|--------------------------------------|--------|
| Día 1| Configuración inicial                | 6 horas|
| Día 2| Procesamiento de datos y señales     | 8 horas|
| Día 3| Interfaz y visualización de datos    | 8 horas|
| Día 4| Revisión final y documentación       | 8 horas|
| **Total** |                                  | **32 horas** |
