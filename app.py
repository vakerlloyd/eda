import streamlit as st
import pandas as pd
import numpy as np
from libreria_clases import DataAnalyzer #importando la clase DataAnalyzer desde el archivo clases.py

def validar_id(id_input, max_id):  
    if id_input < 1 or id_input > max_id:
        return False
    return True


def home():
 
    # Usando HTML para centrar
    st.markdown("<h1 style='text-align: center;'>Especialización en Python</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Módulo 2 - Python for Analytics</h2>", unsafe_allow_html=True)
   
    #Centrar imagen con streamlit
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("logo_personal.png", width=300)

   
    st.header("🏠 Bienvenido")       
    st.subheader("Autor: Lloyd Ramírez del Aguila")  

    st.markdown("""
    Hola, soy Ingeniero de sistemas egresado de la UNMSM.
    Apasionado por la programación y el desarrollo de software, asi como la gestion de tecnologías de la información.
    Me encanta aprender nuevas tecnologías y compartir mis conocimientos con la comunidad.
    """)
    st.subheader("Descripción del Análisis") 
    st.markdown("""
    - En esta aplicación se realiza un análisis exploratorio de datos (EDA) utilizando el dataset de Telco Customer Churn, con el objetivo de identificar patrones, tendencias y relaciones significativas entre las variables presentes en el dataset.
    - El análisis se divide en varias secciones, cada una enfocada en un aspecto específico del EDA, como la información general del dataset, la clasificación de variables, las estadísticas descriptivas, el análisis de valores faltantes, la distribución de variables numéricas, el análisis de variables categóricas, el análisis bivariado entre variables numéricas y categóricas, entre otros.
    - Se presentan insights y análisis de resultados basados en los datos del dataset, con el objetivo de identificar patrones, tendencias y relaciones significativas entre las variables.
    - Se pueden generar insights generales sobre el dataset, así como análisis específicos de variables numéricas y categóricas en relación con la variable de interés "Churn".
    - Se puede seleccionar entre usar el dataset original o el dataset limpio (si se ha realizado la limpieza previamente) para comparar los resultados y observar cómo la limpieza de datos puede afectar los insights obtenidos.
    """)

    st.subheader("Tecnologías usadas")  
    st.markdown("""
    - Esta aplicación se ha desarrollado utilizando Streamlit, una biblioteca de Python que permite crear aplicaciones web interactivas de manera sencilla y rápida.
    - Se utilizan otras bibliotecas como Pandas para el manejo de datos, Numpy, IO, Matplotlib y Seaborn para la visualización de datos.
    - Se creo la clase DataAnalyzer para encapsular las funciones de análisis de datos y graficos, a fin de facilitar su uso en la aplicación.
    """)

    st.subheader("Explicación del DataSet") 
    st.markdown("""
    - En la presente aplicacion se va hacer uso del dataset de Telco Customer Churn, el cual contiene información sobre clientes de una empresa de telecomunicaciones, se tiene detalle sobre 
    los clientes, sus servicios contratados, facturación mensual, tiempo de permanencia y estado actual en la empresa. 
    - Puede descargar el dataset desde el botón de descarga en la sección de carga de dataset.
    - A continuación se muestra una descripción de las columnas presentes en el dataset:
    """)
    # Diccionario con variables y descripciones
    variables = {
        "customerID": "Identificador único del cliente",
        "gender": "Género del cliente",
        "SeniorCitizen": "Si el cliente es adulto mayor",
        "Partner": "Si el cliente tiene pareja",
        "Dependents": "Si el cliente tiene dependientes",
        "tenure": "Meses de permanencia",
        "PhoneService": "Si el cliente tiene servicio telefónico",
        "MultipleLines": "Si tiene múltiples líneas",
        "InternetService": "Tipo de servicio de internet",
        "OnlineSecurity": "Si posee seguridad en línea",
        "OnlineBackup": "Si posee respaldo en línea",
        "DeviceProtection": "Protección del dispositivo",
        "TechSupport": "Soporte técnico",
        "StreamingTV": "Servicio de TV",
        "StreamingMovies": "Servicio de películas",
        "Contract": "Tipo de contrato",
        "PaperlessBilling": "Facturación electrónica",
        "PaymentMethod": "Método de pago",
        "MonthlyCharges": "Cargo mensual",
        "TotalCharges": "Cargo total",
        "Churn": "Si el cliente abandonó la empresa (“Yes”/“No”)"
    }

    # Convertir a DataFrame
    df_variables = pd.DataFrame(list(variables.items()), columns=["Variable", "Descripción"])

    # Mostrar en Streamlit
    st.table(df_variables)
    


    st.subheader("Año: 2026")  
    #Centrar imagen con streamlit
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("logo_dmc.png", width=300)


def resumen_cargar_dataset(df):
    # Mostrar primeras filas
    st.subheader("👀 Vista previa de los datos")
    st.dataframe(df.head())

    # Información general
    st.subheader("📏 Dimensiones del dataset")
    st.write(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")

def cargar_csv_coma(archivo):
    if archivo is not None:
            try:
                df = pd.read_csv(archivo)

                st.session_state.dataset = df

                st.success("✅ Archivo cargado correctamente")
                resumen_cargar_dataset(df)

            except Exception as e:
                st.error(f"Error al cargar el archivo: {e}")
    else:
            st.info("No se ha seleccionado ningún archivo.")   

def cargar_csv(archivo, sep):
    if archivo is not None:
        try:
            df = pd.read_csv(archivo, sep=sep)

            st.session_state.dataset = df

            st.success(f"✅ Archivo cargado correctamente con separador '{sep}'")
            resumen_cargar_dataset(df)

        except Exception as e:
            st.error(f"Error al cargar el archivo: {e}")
    else:
        st.info("No se ha seleccionado ningún archivo.")

#Cargar dataset para el EDA:
def cargar_dataset():

    st.markdown("""
    - En esta sección puedes usar el dataset sugerido o cargar tu propio dataset en formato CSV para realizar un análisis exploratorio de datos (EDA).    
    - Si deseas usar el dataset sugerido simplemente descargalo desde el botón de descarga y luego selecciona el archivo desde tu computadora para cargarlo.  
    - Si optas por usar tu propio dataset, asegúrate de que esté en formato CSV y que tenga una estructura adecuada para el análisis, en ese caso cargalo de frente usando la copcion Upload.   
    - Al cargar el dataset se mostrará una vista previa de los datos, junto con información general sobre las dimensiones del dataset.
    - Se recomienda usar el dataset sugerido, pues algunos items son especificos para ese dataset, aunque la mayoria de los ejercicios se pueden realizar con cualquier dataset que tenga una estructura similar (variables numéricas y categóricas).
    """)
    # --- Cargar CSV fijo desde el proyecto ---
    with open("TelcoCustomerChurn.csv", "rb") as f:
        csv_bytes = f.read()

    # Botón de descarga
    st.download_button(
        label="⬇️ Descargar dataset de Telco Customer Churn",
        data=csv_bytes,
        file_name="TelcoCustomerChurn.csv",
        mime="text/csv"
    )

    if "dataset" not in st.session_state:
        st.info("Puedes usar el dataset de ejemplo o cargar tu propio archivo CSV.")
        #Subir un archivo CSV
        archivo = st.file_uploader("Selecciona un archivo CSV", type="csv")      
        # Selector de separador
        sep = st.selectbox("Selecciona el separador de columnas", [",", ";", "|", "\t"], index=0)  
        cargar_csv(archivo, sep)   
    else:
        st.success("✅ Dataset cargado en la sesión. Puedes navegar a la sección de EDA para analizarlo.")
        resumen_cargar_dataset(st.session_state.dataset)
        
        #st.info("Si desea puede volver a cargar su archivo csv.")
        #archivo = st.file_uploader("Selecciona un archivo CSV", type="csv")   
        #if archivo is not None:
        #    st.session_state.dataset = None # Limpiar el dataset actual para permitir cargar uno nuevo     
        #    cargar_csv(archivo, sep) 
        
        
    


#Ejercicio 4:
def eda():      
    
    if "dataset" not in st.session_state:
        st.warning("No se ha cargado ningún dataset. Por favor, carga un dataset para realizar el análisis.")
        return
    else:
        #df = st.session_state.dataset
        #analizador = DataAnalyzer(df)
        #st.session_state.limpiarDataframe = False # Variable para controlar si se ha limpiado el DataFrame
        # ✅ Crear el analizador solo una vez y guardarlo en session_state
        if "analizador" not in st.session_state:
            st.session_state.analizador = DataAnalyzer(st.session_state.dataset)
        # Flag de limpieza inicial
        if "limpiarDataframe" not in st.session_state:
            st.session_state.limpiarDataframe = False

    analizador = st.session_state.analizador
    
    # Crear pestañas
    item1, item2, item3,item4, item5, item6,item7,item8,item9,item10, Conclusiones = st.tabs(["📚 Item1", "🗂️ Item2", "🧮 Item3", "❓ Item4", "📊 Item5", "📋 Item6", "🔍 Item7", "🧩 Item8", "⚙️ Item9", "💡 Item10", "📈 Conclusiones"])
    
    with item1:
        st.header("Información general del dataset")
        st.markdown("""
        - En esta sección se muestra información general sobre el dataset, incluyendo las columnas presentes, la cantidad de valores nulos en cada columna y los tipos de datos asociados a cada columna.  
        - No se aplico ninguna limpieza o transformación a los datos, por lo que se muestra la información tal como se encuentra en el dataset original.
        """)
        st.markdown(
            "<span style='color:red; font-weight:bold;'>⚠️ Para un mejor análisis de los datos, se recomienda realizar una limpieza y transformación previa del dataset, lo cual se puede hacer usando el botón de limpieza y transformación que se encuentra a continuación.</span>",
            unsafe_allow_html=True
        )

        if st.button("Limpiar y transformar DataFrame"):
            # Recrear el analizador con el dataset actual
            st.session_state.analizador = DataAnalyzer(st.session_state.dataset)
            st.session_state.limpiarDataframe = True

            analizador = st.session_state.analizador
            st.success("✅ DataFrame limpiado y transformado correctamente.")
            st.dataframe(analizador.df_limpio.head())
            st.subheader("Acciones de limpieza realizadas:")
            st.dataframe(analizador.log_limpieza) # Mostrar el log de limpieza
            
            #df_limpio = analizador.limpiar_transformar_dataframes()
            #st.success("✅ DataFrame limpiado y transformado correctamente.")
            #st.dataframe(df_limpio.head())

    
        st.subheader("📌 .info()-> columnas,valores nulos, tipos de datos")
        st.text(analizador.info_general(limpiar=st.session_state.limpiarDataframe))

        # Tipos de datos
        tipos = analizador.formatear_resultado(
            analizador.tipos_datos(limpiar=st.session_state.limpiarDataframe),
            ["Columna", "Tipo de dato"],
            incluir_tipo=False, 
            limpiar=st.session_state.limpiarDataframe)
        st.subheader("📌 Tipos de datos")
        st.dataframe(tipos)

        # Valores nulos
        nulos = analizador.formatear_resultado(
            analizador.valores_nulos(limpiar=st.session_state.limpiarDataframe), 
            ["Columna", "Cantidad de valores nulos"], 
            incluir_tipo=False, 
            limpiar=st.session_state.limpiarDataframe)
        st.subheader("📌 Valores nulos")
        st.dataframe(nulos)


    with item2:

        st.header("Clasificación de variables")
        
        st.markdown("""
        - A continuacion se muestra la clasificación de las variables del dataset en numéricas y categóricas, asi como la cantidad de cada una.
        - Las variables numéricas son aquellas que representan cantidades o medidas, y pueden ser continuas o discretas. Estas variables permiten realizar operaciones matemáticas y estadísticas, como calcular promedios, desviaciones estándar, entre otros.
        - Las variables categóricas son aquellas que representan categorías o grupos, y pueden ser nominal
        - Para un análisis más preciso, se recomienda realizar una limpieza y transformación previa del dataset, lo cual se puede hacer usando el botón de limpieza y transformación que se encuentra en la sección de información general del dataset Item1.
        """)
        num, cat = analizador.clasificar_variables(limpiar=st.session_state.limpiarDataframe)

        st.subheader(f"🔢 Numéricas:  {len(num)}")
        var_numericas = analizador.formatear_resultado(num, ["Variables numéricas", "Tipo de dato"], incluir_tipo=True,limpiar=st.session_state.limpiarDataframe)
        st.dataframe(var_numericas)

        st.subheader(f"🏷️ Categóricas:  {len(cat)}")
        var_categoricas = analizador.formatear_resultado(cat, ["Variables categóricas", "Tipo de dato"], incluir_tipo=True,limpiar=st.session_state.limpiarDataframe)
        st.dataframe(var_categoricas)


    with item3:
        st.header("Estadísticas descriptivas")
        st.markdown(""" 
        - En esta sección se muestra un resumen de las principales estadísticas descriptivas del dataset utilizando la función describe().  
        - Se presentan estadísticas como la media, mediana, desviación estándar, valores mínimos y máximos, entre otros, para las variables numéricas del dataset.
        - Para un análisis más preciso, se recomienda realizar una limpieza y transformación previa del dataset, lo cual se puede hacer usando el botón de limpieza y transformación que se encuentra en la sección de información general del dataset Item1.
        """)
        st.subheader("📊 Se muestra un resumen de las principales estadisticas usando la funcion describe().")
        st.dataframe(analizador.estadisticas_descriptivas(st.session_state.limpiarDataframe))

        st.subheader("📉 Resumen estadístico de Variables numéricas")
        df_general, df_dispersion = analizador.resumen_estadistico(st.session_state.limpiarDataframe)
        st.dataframe(df_general)
        st.subheader("📑 Interpretación de resultados de estadisticos del paso anterior")
        st.dataframe(df_dispersion)

        st.header("📐 Conceptos claves:")
        st.markdown("""
            1. **Varianza**
            - **Qué es:** mide cuánto se alejan los valores respecto a la media, pero en escala cuadrática.  
            - **Interpretación:**  
                - Alta varianza → los datos están muy dispersos, hay gran variabilidad.  
                - Baja varianza → los datos están concentrados cerca de la media.  

            2. **Desviación estándar**
            - **Qué es:** raíz cuadrada de la varianza, expresada en la misma unidad que la variable.  
            - **Interpretación:**  
                - Alta desviación estándar → valores muy dispersos, difícil predecir un valor típico.  
                - Baja desviación estándar → valores homogéneos, más consistencia.  

            3. **Coeficiente de variación (CV)**
            - **Qué es:** relación entre desviación estándar y media.  
            - **Interpretación:** mide la variabilidad relativa respecto al promedio.  
                - CV < 0.2 (20%) → baja variabilidad, datos muy estables.  
                - CV entre 0.2 y 0.5 → variabilidad moderada.  
                - CV > 0.5 (50%) → alta variabilidad, datos muy heterogéneos.  
        """)


    with item4:
        st.header("Análisis de valores faltantes")
        st.markdown("""
        - En esta sección se muestra un análisis detallado de los valores faltantes presentes en el dataset. 
        - Se presenta una tabla con la cantidad de valores nulos por columna, así como un gráfico de barras que visualiza las columnas que contienen valores nulos. 
        - Si no se encuentran valores nulos en el dataset, se mostrará un mensaje indicando que no se han detectado valores faltantes.
        - Para un análisis más preciso, se recomienda realizar una limpieza y transformación previa del dataset, lo cual se puede hacer usando el botón de limpieza y transformación que se encuentra en la sección de información general del dataset Item1.
        """)

        nulos = analizador.valores_nulos(limpiar=st.session_state.limpiarDataframe)

        # Formatear resultado con nombres de columnas personalizados
        nulos_df = analizador.formatear_resultado(
            nulos,
            ["Columna", "Valores nulos"],
            incluir_tipo=False,
            limpiar=st.session_state.limpiarDataframe
        )

        st.subheader("📋 Tabla de valores nulos")
        st.dataframe(nulos_df)

        # Filtrar solo columnas con nulos > 0
        nulos_filtrados = nulos_df[nulos_df["Valores nulos"] > 0]

        if not nulos_filtrados.empty:
            st.subheader("📊 Gráfico de columnas con valores nulos")
            st.bar_chart(nulos_filtrados.set_index("Columna"))
        else:
            st.info("✅ No se encontraron valores nulos en el dataset.")


    with item5:
        st.header("Distribución de variables numéricas")
        st.markdown("""
        - En esta sección se muestra la distribución de las variables numéricas presentes en el dataset.
        - Se presenta un histograma para cada variable numérica, lo que permite visualizar la forma de la distribución, la presencia de sesgos, la cantidad de valores atípicos, entre otros aspectos relevantes para el análisis exploratorio de datos.
        - Para un análisis más preciso, se recomienda realizar una limpieza y transformación previa del dataset, lo cual se puede hacer usando el botón de limpieza y transformación que se encuentra en la sección de información general del dataset Item1.
        """)

        num_filtradas = analizador.variables_filtradas(tipo="numericas", excluir_patron="id", limpiar=st.session_state.limpiarDataframe)
        columna = st.selectbox("Selecciona variable:", num_filtradas)

        # Control adicional: slider para bins
        bins = st.slider("Número de intervalos (bins)", min_value=10, max_value=100, value=30, step=5)

        if st.button("Histograma"):
            with st.spinner(f"Generando histograma para {columna}..."):
                fig = analizador.histograma(columna, limpiar=st.session_state.limpiarDataframe, bins=bins)
                st.pyplot(fig)
            st.success("✅ Histograma generado correctamente.")

    with item6:
        st.header("Análisis de variables categóricas")
        st.markdown("""
        - En esta sección se muestra un análisis detallado de las variables categóricas presentes en el dataset.
        - Se presenta un gráfico de barras para cada variable categórica, lo que permite visualizar la frecuencia de cada categoría, identificar categorías predominantes, detectar posibles desequilibrios en la distribución de las categorías, entre otros aspectos relevantes para el análisis exploratorio de datos.
        - Para un análisis más preciso, se recomienda realizar una limpieza y transformación previa del dataset, lo cual se puede hacer usando el botón de limpieza y transformación que se encuentra en la sección de información general del dataset Item1.
        """)
        # Usamos el método filtrado para obtener solo las variables categóricas relevantes que no contengan 'id'
        cat_filtradas = analizador.variables_filtradas(tipo="categoricas", excluir_patron="id", limpiar=st.session_state.limpiarDataframe)
        columna = st.selectbox("Selecciona variable:", cat_filtradas)

        if st.button("Gráfico de barras"):
            with st.spinner(f"Generando gráfico para {columna}..."):
                fig, conteos, proporciones = analizador.grafico_barras(
                    columna, limpiar=st.session_state.limpiarDataframe
                )
                st.pyplot(fig)

            st.subheader("📊 Conteos absolutos")
            st.dataframe(conteos.rename("Frecuencia"))

            st.subheader("📈 Proporciones relativas (%)")
            st.dataframe(proporciones.rename("Porcentaje"))

    with item7:
        st.header("Análisis bivariado (numérico vs categórico)")
        st.markdown("""
        - En esta sección se realiza un análisis bivariado entre una variable numérica y una variable categórica.
        - Para un análisis más preciso, se recomienda realizar una limpieza y transformación previa del dataset, lo cual se puede hacer usando el botón de limpieza y transformación que se encuentra en la sección de información general del dataset Item1.
        - Puedes elegir el tipo de gráfico para visualizar la relación:
            - **Boxplot** → compara medianas y dispersión.
            - **Violin plot** → muestra la forma completa de la distribución.
            - **Barplot** → compara medias con barras de error.
            - **Stripplot** → muestra todos los puntos individuales.
        """)

        num_filtradas = analizador.variables_filtradas(
            tipo="numericas", excluir_patron="id", limpiar=st.session_state.limpiarDataframe
        )
        cat_filtradas = analizador.variables_filtradas(
            tipo="categoricas", excluir_patron="id", limpiar=st.session_state.limpiarDataframe
        )

        num_col = st.selectbox("Variable numérica", num_filtradas)
        cat_col = st.selectbox("Variable categórica", cat_filtradas)

        tipo_grafico = st.radio("Tipo de gráfico", ["Boxplot", "Violin", "Barplot", "Stripplot"])

        if st.button("Generar gráfico num vs cat"):
            with st.spinner(f"Generando {tipo_grafico} para {num_col} vs {cat_col}..."):
                fig = analizador.bivariado_num_cat(
                    num_col, cat_col, limpiar=st.session_state.limpiarDataframe,
                    tipo=tipo_grafico.lower()
                )
                st.pyplot(fig)
            st.success("✅ Gráfico generado correctamente.")


        
    with item8:
        st.header("Análisis bivariado (categórico vs categórico) ")
        st.markdown("""
        - En esta sección se realiza un análisis bivariado entre dos variables categóricas.
        - Para un análisis más preciso, se recomienda realizar una limpieza y transformación previa del dataset, lo cual se puede hacer usando el botón de limpieza y transformación que se encuentra en la sección de información general del dataset Item1.
        - Puedes elegir el tipo de gráfico para visualizar la relación: 
        """)
        cat_filtradas = analizador.variables_filtradas(tipo="categoricas", excluir_patron="id", limpiar=st.session_state.limpiarDataframe)
        col1 = st.selectbox("Variable categórica 1", cat_filtradas)
        col2 = st.selectbox("Variable categórica 2", cat_filtradas)
        tipo_grafico = st.radio("Tipo de gráfico", ["Barras apiladas", "Heatmap"])

        if st.button("Generar gráfico cat vs cat"):
            with st.spinner(f"Generando gráfico {tipo_grafico.lower()} para {col1} vs {col2}..."):
                fig, tabla_abs, tabla_prop = analizador.bivariado_cat_cat(
                    col1, col2, limpiar=st.session_state.limpiarDataframe,
                    tipo="stacked" if tipo_grafico == "Barras apiladas" else "heatmap"
                )
                st.pyplot(fig)

            st.subheader("📊 Tabla de frecuencias absolutas")
            st.dataframe(tabla_abs)

            st.subheader("📈 Tabla de proporciones relativas")
            st.dataframe(tabla_prop)

    with item9:
        st.header("Análisis dinámico basado en parámetros seleccionados")
        st.markdown("""
        - En esta sección se realiza un análisis dinámico entre dos variables seleccionadas por el usuario, donde el tipo de gráfico se adapta automáticamente según la combinación de tipos de variables elegidas. 
        - Para un análisis más preciso, se recomienda realizar una limpieza y transformación previa del dataset, lo cual se puede hacer usando el botón de limpieza y transformación que se encuentra en la sección de información general del dataset Item1. 
        - El análisis dinámico permite explorar diferentes relaciones entre variables de manera flexible, facilitando la identificación de patrones y tendencias en los datos.
        """)
        num_filtradas = analizador.variables_filtradas("numericas", excluir_patron="id", limpiar=st.session_state.limpiarDataframe)
        cat_filtradas = analizador.variables_filtradas("categoricas", excluir_patron="id", limpiar=st.session_state.limpiarDataframe)


         # Primera variable flexible
        tipo_var1 = st.radio("Tipo de la primera variable", ["Numerica", "Categorica"])
        if tipo_var1 == "Numerica":
            var1 = st.selectbox("Selecciona variable numérica (Var1)", num_filtradas)
        else:
            var1 = st.selectbox("Selecciona variable categórica (Var1)", cat_filtradas)

        # Segunda variable flexible
        tipo_var2 = st.radio("Tipo de la segunda variable", ["Numerica", "Categorica"])
        if tipo_var2 == "Numerica":
            var2 = st.selectbox("Selecciona variable numérica (Var2)", num_filtradas)
        else:
            var2 = st.selectbox("Selecciona variable categórica (Var2)", cat_filtradas)


        if tipo_var1 == "Numerica" and tipo_var2 == "Categorica":
            opciones_grafico = ["Boxplot", "Violin", "Barplot", "Stripplot"]
        elif tipo_var1 == "Categorica" and tipo_var2 == "Numerica":
            opciones_grafico = ["Boxplot", "Violin", "Barplot", "Stripplot"]
        elif tipo_var1 == "Numerica" and tipo_var2 == "Numerica":
            opciones_grafico = ["Scatterplot"]
        elif tipo_var1 == "Categorica" and tipo_var2 == "Categorica":
            opciones_grafico = ["Heatmap", "Stacked"]
        else:
            opciones_grafico = []

        tipo_grafico = st.radio("Tipo de gráfico", opciones_grafico, key="tipo_grafico")

        if st.button("Ejecutar análisis dinámico"):
            if opciones_grafico :
                fig, resumen = analizador.analisis_dinamico(
                #var1, "numerica", var2, tipo_var2.lower(),
                var1, tipo_var1.lower(), var2, tipo_var2.lower(),
                limpiar=st.session_state.limpiarDataframe,
                tipo_grafico=tipo_grafico.lower()
                )

                # ✅ Siempre pasamos fig explícito
                st.pyplot(fig)

                # Mostrar resumen
                if isinstance(resumen, dict):  # categórico vs categórico
                    st.subheader("📊 Tabla de frecuencias absolutas")
                    st.dataframe(resumen["abs"])
                    st.subheader("📈 Tabla de proporciones relativas")
                    st.dataframe(resumen["prop"])
                elif resumen is not None:
                    st.subheader("📊 Resumen estadístico")
                    st.dataframe(resumen)

        
    with item10:
        st.header("Insights y analisis de resultados")
        st.subheader("El siguiente análisis se basa en los datos del dataset de Telco Customer Churn. Si usa otro dataset los resultados pueden variar o no ser relevantes, en el peor de los casos generar errores si la estructura del dataset es muy diferente.")
        st.markdown("""
        - En esta sección se presentan insights y análisis de resultados basados en los datos del dataset, con el objetivo de identificar patrones, tendencias y relaciones significativas entre las variables.
        - Se pueden generar insights generales sobre el dataset, así como análisis específicos de variables numéricas en relación con la variable de interés "Churn", y análisis de variables categóricas también en relación con "Churn".
        - Se puede seleccionar entre usar el dataset original o el dataset limpio (si se ha realizado la limpieza previamente) para comparar los resultados y observar cómo la limpieza de datos puede afectar los insights obtenidos.
                        
        """)
        usar_limpio = st.radio("Selecciona el DataFrame a analizar:", ["Original", "Limpio"], key="df_item10")
        limpiar = True if usar_limpio == "Limpio" else False

        # Switch dinámico
        opcion = st.selectbox("Selecciona el tipo de análisis:", 
                ["Insights generales", "Numéricas vs Churn","Categóricas vs Churn"], key="opcion_item10")
        

    
        if st.button("Generar resumen de insights"):
            if opcion == "Insights generales":
                insights, graficos = analizador.resumen_insights(limpiar=limpiar)

                # Ejemplo: mostrar solo dataset info
                st.subheader("📊 Información del dataset")
                st.write(insights["dataset_info"])

                # Mostrar missing values
                if "missing_values" in insights:
                    st.subheader(insights["missing_values"]["resumen"])
                    for line in insights["missing_values"]["texto"]:
                        st.write(line)
                    st.pyplot(graficos["missing_values"])

                # Mostrar churn
                if "churn" in insights:
                    st.subheader(insights["churn"]["resumen"])
                    for line in insights["churn"]["texto"]:
                        st.write(line)
                    st.pyplot(graficos["churn"])

                # Mostrar correlaciones
                if "correlaciones" in insights:
                    st.subheader(insights["correlaciones"]["resumen"])
                    # Mostrar heatmap
                    st.pyplot(graficos["correlaciones"])

                    # Fuertes
                    if insights["correlaciones"]["fuertes"]:
                        st.write("🔴 Correlaciones fuertes (≥ 0.8):")
                        for line in insights["correlaciones"]["fuertes"]:
                            st.write(line)

                    # Moderadas
                    if insights["correlaciones"]["moderadas"]:
                        st.write("🟡 Correlaciones moderadas (0.3 – 0.8):")
                        for line in insights["correlaciones"]["moderadas"]:
                            st.write(line)

                    # Débiles
                    if insights["correlaciones"]["débiles"]:
                        st.write("🔵 Correlaciones débiles (< 0.3):")
                        for line in insights["correlaciones"]["débiles"]:
                            st.write(line)
                    st.markdown("""
                                **¿Qué significa?** 
                                Correlación mide la fuerza y dirección de la relación lineal entre dos variables numéricas. 
                                - Valores cercanos a +1 → relación positiva fuerte (cuando una sube, la otra también). 
                                - Valores cercanos a -1 → relación negativa fuerte (cuando una sube, la otra baja). 
                                - Valores cercanos a 0 → poca o ninguna relación lineal. 

                                **En el heatmap:** 
                                - Los colores cálidos (rojo) indican correlaciones positivas altas. 
                                - Los colores fríos (azul) indican correlaciones negativas altas. 
                                - Los tonos intermedios (blanco o gris) indican correlaciones débiles o nulas. 

                                **Ejemplo aplicado al dataset de churn** 
                                - tenure (tiempo de permanencia del cliente). 
                                - MonthlyCharges (cargos mensuales). 
                                 - TotalCharges (cargos totales). 

                                **En el mapa de correlaciones podrías ver:** 
                                - tenure vs TotalCharges → correlación positiva alta (clientes con más tiempo acumulan más cargos). 
                                - MonthlyCharges vs TotalCharges → correlación positiva moderada (los cargos mensuales influyen en el total, pero también depende del tiempo). 
                                - tenure vs MonthlyCharges → correlación baja (el tiempo de permanencia no necesariamente afecta cuánto paga mensualmente).
                                """)
                    
            elif opcion == "Numéricas vs Churn":
                resultados, graficos, conclusiones = analizador.analisis_num_vs_churn(limpiar=limpiar)

                # Estadísticas descriptivas
                st.subheader("📊 Estadísticas descriptivas por Churn")
                st.dataframe(resultados["estadisticas"])

                # Correlaciones con churn
                if resultados["correlaciones"] is not None:
                    st.subheader("📈 Correlaciones de variables numéricas con Churn")
                    st.dataframe(resultados["correlaciones"])

                # Gráficos por variable
                st.subheader("📉 Distribución de variables numéricas vs Churn")
                for col, fig in graficos.items():
                    st.write(f"Variable: {col}")
                    st.pyplot(fig)

                # Conclusiones automáticas
                st.subheader("📝 Conclusiones del análisis Numéricas vs Churn")
                if conclusiones["positivos"]:
                    st.write("🔴 **Drivers positivos (factores que aumentan churn):**")
                    for c in conclusiones["positivos"]:
                        st.write(c)
                if conclusiones["negativos"]:
                    st.write("🟢 **Drivers negativos (factores que reducen churn):**")
                    for c in conclusiones["negativos"]:
                        st.write(c)

            elif opcion == "Categóricas vs Churn":
                resultados, graficos, conclusiones = analizador.analisis_cat_vs_churn(limpiar=limpiar)

                # Tablas de proporciones
                st.subheader("📊 Distribución de Churn por categoría")
                for col, tabla in resultados.items():
                    st.write(f"Variable: {col}")
                    st.dataframe(tabla)

                # Gráficos
                st.subheader("📉 Gráficos categóricos vs Churn")
                for col, fig in graficos.items():
                    st.write(f"Variable: {col}")
                    st.pyplot(fig)

                # Conclusiones
                st.subheader("📝 Conclusiones del análisis Categóricas vs Churn")
                if conclusiones["positivos"]:
                    st.write("🔴 **Drivers positivos (categorías con mayor churn):**")
                    for c in conclusiones["positivos"]:
                        st.write(c)
                if conclusiones["negativos"]:
                    st.write("🟢 **Drivers negativos (categorías con menor churn):**")
                    for c in conclusiones["negativos"]:
                        st.write(c)
   
    with Conclusiones:
        st.header("Conclusiones generales del análisis exploratorio de datos (EDA)")  
       
        st.markdown("""
        - El análisis exploratorio de datos (EDA) es una etapa fundamental en cualquier proyecto de ciencia de datos, ya que permite comprender la estructura, características y relaciones presentes en el dataset antes de aplicar modelos predictivos o realizar análisis más avanzados.
        - A través del EDA se pueden identificar patrones, tendencias, valores atípicos, valores faltantes y relaciones entre variables, lo que facilita la toma de decisiones informadas sobre cómo abordar el análisis posterior.
        - En este análisis se han explorado diferentes aspectos del dataset, desde la información general y clasificación de variables, hasta análisis bivariados y generación de insights específicos relacionados con la variable de interés "Churn".
        - Es importante destacar que la limpieza y transformación de datos es un paso crucial para obtener insights más precisos y confiables, ya que los datos sin procesar pueden contener inconsistencias, valores faltantes o errores que afectan la calidad del análisis.
        - En resumen, el EDA es una herramienta poderosa para descubrir la historia que cuentan los datos, y es esencial para guiar las siguientes etapas del proyecto de ciencia de datos, como la selección de características, modelado y evaluación.
        """)   

        st.subheader("Las siguientes conclusiones se basan en el análisis exploratorio de datos realizado sobre el dataset de Telco Customer Churn. Si usa otro dataset, las conclusiones pueden variar dependiendo de las características específicas de ese dataset. Se recomienda realizar un análisis similar para obtener insights relevantes en cada caso particular.")     
        
        st.subheader("📌 Posibles causas de la fuga de clientes (Churn):")
        st.markdown("""
                **Altos costos mensuales (MonthlyCharges):** 
                - Los clientes con cargos mensuales más elevados tienden a presentar mayor probabilidad de churn. 
                - Esto sugiere que la percepción de precio alto sin un valor diferencial claro impulsa la salida. 

                **Baja permanencia (Tenure):** 
                - Los clientes con menor tiempo de permanencia en la compañía son más propensos a abandonar. 
                - Indica que la fidelización en los primeros meses es crítica. 

                **Servicios contratados limitados:** 
                - Clientes que solo tienen servicios básicos (ej. solo internet o solo teléfono) muestran mayor churn. 
                - La falta de paquetes integrados o beneficios adicionales reduce el compromiso. 

                **Problemas en contratos y métodos de pago** 
                - Contratos mensuales y pagos electrónicos automáticos se asocian con mayor churn. 
                - Los contratos a largo plazo y pagos más tradicionales tienden a retener mejor. 

                **TotalCharges bajos** 
                - Clientes con cargos acumulados bajos (relacionados con poco tiempo de permanencia) también presentan mayor churn. 
                - Refleja que la fuga ocurre temprano en la relación con la empresa.

        """)
        st.subheader("🎯 Conclusiones sobre la fuga de clientes:")      
        st.markdown("""
                - La fuga de clientes (churn) es un desafío crítico para las empresas, ya que retener a los clientes existentes suele ser más rentable que adquirir nuevos. 
                - El análisis exploratorio de datos ha permitido identificar factores clave asociados con el churn, como altos costos mensuales, baja permanencia, servicios limitados, problemas en contratos y métodos de pago, y cargos acumulados bajos. 
                - Estos insights pueden guiar estrategias de retención más efectivas, como ofrecer paquetes integrados, mejorar la experiencia del cliente en los primeros meses, implementar programas de fidelización y revisar políticas de precios y contratos. 
                - En última instancia, comprender las causas del churn es esencial para diseñar intervenciones que reduzcan la fuga de clientes y mejoren la rentabilidad a largo plazo.
        """)          
        st.subheader("✅ En Resumen:")  
        st.markdown("""
                **La fuga de clientes está impulsada principalmente por precio elevado, baja fidelización inicial y contratos poco atractivos. 
                Las estrategias de retención deben enfocarse en mejorar la experiencia temprana, ofrecer paquetes con beneficios claros y diseñar planes competitivos que incentiven la permanencia.**
        """)



#Aplicación Principal

# Configuración de la página de la aplicacion con streamlit
st.set_page_config(page_title="EDA en Python", page_icon="logo_personal.png", layout="wide")

# Menú lateral
menu = st.sidebar.selectbox(
    "Navegación",
    ["Home", "Cargar Dataset", "EDA"]
)

# Contenido según la opción seleccionada
if menu == "Home":
   home()

elif menu == "Cargar Dataset":
    st.header("Cargar Dataset")
    cargar_dataset()

elif menu == "EDA":
    st.header("Análisis Exploratorio de Datos - EDA \n 📊 Caso de Estudio: Telco Customer Churn 📈")
    st.subheader("Opciones de análisis:")

    eda()



