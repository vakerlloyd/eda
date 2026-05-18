import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import io
  

class DataAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df_original = df
        self.df_limpio , self.log_limpieza = self.limpiar_transformar_dataframes(None, excluir_patron="id")  # Limpiamos al inicializar, excluyendo columnas con "id"

    def log_limpieza_dataframe(self):
        if hasattr(self, "log_limpieza"):
            return pd.DataFrame(self.log_limpieza)
        else:
            return pd.DataFrame(columns=["columna", "accion", "nulos_nuevos"])
        
    def info_general(self, limpiar=False):
        buffer = io.StringIO()
        (self.df_limpio if limpiar else self.df_original).info(buf=buffer)
        return buffer.getvalue()

    def tipos_datos(self, limpiar=False):
        return (self.df_limpio if limpiar else self.df_original).dtypes

    def valores_nulos(self, limpiar=False):
        return (self.df_limpio if limpiar else self.df_original).isnull().sum()

    def clasificar_variables(self, limpiar=False):
        df = self.df_limpio if limpiar else self.df_original
        numericas = df.select_dtypes(include=np.number).columns.tolist()
        categoricas = df.select_dtypes(exclude=np.number).columns.tolist()
        return numericas, categoricas
    
    def variables_filtradas(self, tipo="categoricas", excluir_patron="id",limpiar=False):
        """
        Devuelve variables filtradas según tipo (numericas o categoricas).
        Excluye columnas cuyo nombre:
        - sea exactamente igual al patrón
        - termine con el patrón
        - empiece con el patrón
        (case-insensitive)
        """
        num, cat = self.clasificar_variables(limpiar=limpiar)
        variables = num if tipo == "numericas" else cat

        patron = excluir_patron.lower()
        filtradas = [
            c for c in variables
            if not (
                c.lower() == patron or
                c.lower().endswith(patron) or
                c.lower().startswith(patron)
            )
        ]
        return filtradas

    def estadisticas_descriptivas(self, limpiar=False):
        df = self.df_limpio if limpiar else self.df_original
        return df.describe(include="all")

    def resumen_estadistico(self, limpiar=False):
        resultados = {}
        interpretaciones = {}
        numericas, _ = self.clasificar_variables(limpiar=limpiar)
        for col in numericas:
        #for col in self.df.select_dtypes(include=[np.number]).columns:
            serie = (self.df_limpio if limpiar else self.df_original)[col].dropna()
            media = serie.mean()
            desv_std = serie.std()
            varianza = serie.var()
            cv = desv_std / media if media != 0 else None

            # --- Primer DataFrame: métricas generales ---
            resultados[col] = {
                "media": round(media, 2),
                "mediana": round(serie.median(), 2),
                "min": round(serie.min(), 2),
                "max": round(serie.max(), 2),
                "rango": round(serie.max() - serie.min(), 2),
                "p25": round(serie.quantile(0.25), 2),
                "p75": round(serie.quantile(0.75), 2)
            }

            # --- Interpretaciones diferenciadas ---
            # Varianza
            if varianza < 100:
                int_var = "Varianza baja: poca dispersión cuadrática"
            elif varianza < 1000:
                int_var = "Varianza moderada"
            else:
                int_var = "Varianza alta: gran dispersión"

            # Desviación estándar
            if desv_std < media * 0.2:
                int_std = "Desviación baja: valores cercanos a la media"
            elif desv_std < media * 0.5:
                int_std = "Desviación moderada"
            else:
                int_std = "Desviación alta: valores muy dispersos"

            # Coeficiente de variación
            if cv is None:
                int_cv = "No se puede calcular CV (media=0)"
                conclusion = "Interpretación limitada"
            elif cv < 0.2:
                int_cv = "CV bajo: datos homogéneos"
                conclusion = "Baja variabilidad"
            elif 0.2 <= cv <= 0.5:
                int_cv = "CV moderado: cierta dispersión"
                conclusion = "Variabilidad moderada"
            else:
                int_cv = "CV alto: datos heterogéneos"
                conclusion = "Alta variabilidad"

            # --- Segundo DataFrame: dispersión + interpretaciones ---
            interpretaciones[col] = {
                "varianza": round(varianza, 2),
                "interpretacion_var": int_var,
                "desv_std": round(desv_std, 2),
                "interpretacion_std": int_std,
                "coef_var": round(cv, 2) if cv is not None else None,
                "interpretacion_cv": int_cv,
                "conclusion": conclusion
            }

        df_general = pd.DataFrame(resultados).T
        df_dispersion = pd.DataFrame(interpretaciones).T

        return df_general, df_dispersion

    def histograma(self, columna, limpiar=False, bins=30):
        """
        Genera un histograma para la columna seleccionada.
        - Usa df_limpio si limpiar=True, de lo contrario df_original.
        - bins: número de intervalos del histograma.
        """
        df = self.df_limpio if limpiar else self.df_original

        fig, ax = plt.subplots(figsize=(8, 5))
        sns.histplot(df[columna], bins=bins, kde=True, color="skyblue", ax=ax)

        ax.set_title(f"Distribución de {columna}", fontsize=14)
        ax.set_xlabel(columna)
        ax.set_ylabel("Frecuencia")

        return fig

    def grafico_barras(self, columna, limpiar=False):
        """
        Genera gráfico de barras para una columna categórica.
        Incluye conteos absolutos y proporciones relativas.
        """
        df = self.df_limpio if limpiar else self.df_original

        # Conteos y proporciones
        conteos = df[columna].value_counts()
        proporciones = (df[columna].value_counts(normalize=True) * 100).round(2)

        # Crear figura
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x=conteos.index, y=conteos.values, palette="viridis", ax=ax)

        # Etiquetas y título
        ax.set_title(f"Distribución de {columna}", fontsize=14)
        ax.set_xlabel(columna)
        ax.set_ylabel("Frecuencia")

        # Mostrar valores encima de las barras
        for i, v in enumerate(conteos.values):
            ax.text(i, v + 0.5, f"{v}\n({proporciones.iloc[i]:.2f}%)", 
                    ha="center", va="bottom", fontsize=9, color="black")

        return fig, conteos, proporciones


    def bivariado_num_cat(self, num_col, cat_col, limpiar=False, tipo="boxplot"):
        """
        Análisis bivariado: variable numérica vs categórica.
        - tipo="box": gráfico de caja
        - tipo="violin": gráfico violin
        - tipo="bar": gráfico de barras con medias
        - tipo="strip": gráfico de puntos individuales
        """
        df = self.df_limpio if limpiar else self.df_original
        fig, ax = plt.subplots(figsize=(8, 5))

        if tipo == "boxplot":
            sns.boxplot(x=df[cat_col], y=df[num_col], palette="Set2", ax=ax)
        elif tipo == "violin":
            sns.violinplot(x=df[cat_col], y=df[num_col], palette="Set2", ax=ax)
        elif tipo == "barplot":
            sns.barplot(x=df[cat_col], y=df[num_col], palette="Set2", ci="sd", ax=ax)
        elif tipo == "stripplot":
            sns.stripplot(x=df[cat_col], y=df[num_col], palette="Set2", jitter=True, ax=ax)

        ax.set_title(f"{num_col} vs {cat_col}", fontsize=14)
        ax.set_xlabel(cat_col)
        ax.set_ylabel(num_col)

        return fig



    def bivariado_cat_cat(self, col1, col2, limpiar=False, tipo="stacked"):
        """
        Análisis bivariado: categórico vs categórico.
        - tipo="stacked": gráfico de barras apiladas con proporciones
        - tipo="heatmap": mapa de calor con frecuencias
        """
        df = self.df_limpio if limpiar else self.df_original

        # Tabla de contingencia
        tabla_abs = pd.crosstab(df[col1], df[col2])
        tabla_prop = pd.crosstab(df[col1], df[col2], normalize="index").round(2)

        fig, ax = plt.subplots(figsize=(8, 5))

        if tipo == "stacked":
            tabla_prop.plot(kind="bar", stacked=True, ax=ax, colormap="viridis")
            ax.set_ylabel("Proporción")
        elif tipo == "heatmap":
            sns.heatmap(tabla_abs, annot=True, fmt="d", cmap="Blues", ax=ax)
            ax.set_ylabel(col1)
            ax.set_xlabel(col2)

        ax.set_title(f"{col1} vs {col2}", fontsize=14)

        return fig, tabla_abs, tabla_prop

    def analisis_dinamico(self, var1, tipo_var1, var2, tipo_var2, limpiar=False, tipo_grafico="boxplot"):

        df = self.df_limpio if limpiar else self.df_original
        resumen = None
        fig = None
        estadoNumCat= True
        estadoNumNum= True

        #Primera variable numerica
        if tipo_var1 == "numerica":
            # Numérica vs Categórica
            if tipo_var2 == "categorica":
                fig = self.bivariado_num_cat(var1, var2, limpiar=limpiar, tipo=tipo_grafico)
                resumen = df.groupby(var2)[var1].agg(["mean", "median", "std"]).round(2)
            # Numérica vs Numérica
            elif tipo_var2 == "numerica":
                fig, ax = plt.subplots(figsize=(8, 5))
                if tipo_grafico == "scatterplot":
                    sns.scatterplot(x=df[var2], y=df[var1], ax=ax)
                    ax.set_title(f"{var1} vs {var2} (scatterplot)")
                else:
                    ax.text(0.5, 0.5, f"Solo scatterplot soportado para numéricas", ha="center", va="center")
                    estadoNumNum= False

                if estadoNumNum:
                    resumen = df[[var1, var2]].corr().round(2)

        elif tipo_var1 == "categorica":
            # Categórica vs Categórica (solo heatmap o stacked)
            if tipo_var2 == "categorica":
                fig, tabla_abs, tabla_prop = self.bivariado_cat_cat(
                    var1, var2, limpiar=limpiar,
                    tipo="heatmap" if tipo_grafico == "heatmap" else "stacked"
                )
                resumen = {"abs": tabla_abs, "prop": tabla_prop}
            elif tipo_var2 == "numerica":
                fig = self.bivariado_num_cat(var2, var1, limpiar=limpiar, tipo=tipo_grafico)
                resumen = df.groupby(var1)[var2].agg(["mean", "median", "std"]).round(2)
        else:
            # Fallback
            fig, ax = plt.subplots()
            ax.text(0.5, 0.5, "Combinación no soportada", ha="center", va="center")
            resumen = None

        return fig, resumen


   
    def resumen_insights(self, limpiar=False):
        df = self.df_limpio if limpiar else self.df_original
        insights = {}   # 🔑 ahora es un diccionario
        graficos = {}

        # Tamaño del dataset
        insights["dataset_info"] = f"📊 El dataset contiene {df.shape[0]} registros y {df.shape[1]} columnas."

        # Variables con más valores faltantes
        missing = df.isnull().sum().sort_values(ascending=False)
        top_missing = missing[missing > 0].head(5)
        if not top_missing.empty:
            insights["missing_values"] = {
                "texto": [f"- {col}: {val} valores nulos" for col, val in top_missing.items()],
                "resumen": "❓ Variables con más valores faltantes"
            }

            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(x=top_missing.index, y=top_missing.values, palette="Reds", ax=ax)
            ax.set_title("Top variables con valores faltantes")
            ax.set_ylabel("Cantidad de nulos")
            graficos["missing_values"] = fig

        # Distribución de churn
        if "Churn" in df.columns:
            churn_counts = df["Churn"].value_counts(normalize=True).round(2) * 100
            insights["churn"] = {
                "texto": [f"- {cat}: {val:.1f}%" for cat, val in churn_counts.items()],
                "resumen": "📉 Distribución de Churn"
            }

            fig, ax = plt.subplots(figsize=(6, 6))
            ax.pie(churn_counts, labels=churn_counts.index, autopct="%1.1f%%", colors=["skyblue", "salmon"])
            ax.set_title("Distribución de Churn")
            graficos["churn"] = fig

        # Correlaciones numéricas
        num_cols = df.select_dtypes(include=["number"]).columns
        if len(num_cols) > 1:
            corr = df[num_cols].corr()

            # Heatmap
            fig, ax = plt.subplots(figsize=(10, 8))
            sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
            ax.set_title("Correlaciones entre variables numéricas")
            graficos["correlaciones"] = fig

            # Interpretación automática
            corr_pairs = corr.unstack().dropna()

            # 🔑 Eliminar duplicados (mantener solo un orden)
            corr_pairs = corr_pairs.reset_index()
            corr_pairs.columns = ["var1", "var2", "valor"]
            corr_pairs = corr_pairs[corr_pairs["var1"] != corr_pairs["var2"]]
            corr_pairs["pair"] = corr_pairs.apply(lambda x: tuple(sorted([x["var1"], x["var2"]])), axis=1)
            corr_pairs = corr_pairs.drop_duplicates(subset="pair").set_index("pair")["valor"]

            # Clasificación por fuerza
            insights["correlaciones"] = {
                "resumen": "📈 Correlaciones entre variables numéricas",
                "fuertes": [f"- {v1} y {v2}: {val:.2f}" for (v1, v2), val in corr_pairs.items() if abs(val) >= 0.8],
                "moderadas": [f"- {v1} y {v2}: {val:.2f}" for (v1, v2), val in corr_pairs.items() if 0.3 <= abs(val) < 0.8],
                "débiles": [f"- {v1} y {v2}: {val:.2f}" for (v1, v2), val in corr_pairs.items() if abs(val) < 0.3]
            }


        return insights, graficos

    def analisis_num_vs_churn(self, limpiar=False):
        df = self.df_limpio if limpiar else self.df_original
        resultados = {}
        graficos = {}
        conclusiones = {"positivos": [], "negativos": []}

        # Validar que exista la columna Churn
        if "Churn" not in df.columns:
            return {"error": "No existe la columna Churn"}, {}, conclusiones

        # Crear columna binaria de churn
        df = df.copy()
        df["Churn_bin"] = df["Churn"].map({"No": 0, "Yes": 1})

        # Estadísticas descriptivas por grupo
        num_cols = df.select_dtypes(include="number").columns
        stats = df.groupby("Churn")[num_cols].agg(["mean", "median", "std"]).round(2)
        resultados["estadisticas"] = stats

        # Correlaciones con churn
        resultados["correlaciones"] = None
        if "Churn_bin" in df.columns and len(num_cols) > 1:
            corr = df[num_cols].corr()
            if "Churn_bin" in corr.columns:
                corr_churn = corr["Churn_bin"].drop("Churn_bin").sort_values(ascending=False)
                resultados["correlaciones"] = corr_churn

                # Clasificación automática de drivers
                for var, val in corr_churn.items():
                    if val >= 0.3:  # correlación positiva moderada/fuerte
                        conclusiones["positivos"].append(
                            f"📈 La variable **{var}** está asociada positivamente con Churn (r={val:.2f}). Clientes con valores más altos tienden a abandonar."
                        )
                    elif val <= -0.3:  # correlación negativa moderada/fuerte
                        conclusiones["negativos"].append(
                            f"📉 La variable **{var}** está asociada negativamente con Churn (r={val:.2f}). Clientes con valores más altos tienden a permanecer."
                        )

        # Gráficos: boxplot para cada variable numérica vs churn
        for col in num_cols:
            if col != "Churn_bin":
                fig, ax = plt.subplots(figsize=(6, 4))
                sns.boxplot(x=df["Churn"], y=df[col], palette="Set2", ax=ax)
                ax.set_title(f"{col} vs Churn")
                graficos[col] = fig

                # Conclusión simple por variable
                mean_churn = df[df["Churn"] == "Yes"][col].mean()
                mean_nochurn = df[df["Churn"] == "No"][col].mean()
                if mean_churn > mean_nochurn:
                    conclusiones["positivos"].append(
                        f"➡️ Los clientes con churn tienen valores más altos en **{col}** (promedio {mean_churn:.2f}) que los que permanecen ({mean_nochurn:.2f})."
                    )
                else:
                    conclusiones["negativos"].append(
                        f"➡️ Los clientes con churn tienen valores más bajos en **{col}** (promedio {mean_churn:.2f}) que los que permanecen ({mean_nochurn:.2f})."
                    )

        return resultados, graficos, conclusiones

    def analisis_cat_vs_churn(self, limpiar=False):
        df = self.df_limpio if limpiar else self.df_original
        resultados = {}
        graficos = {}
        conclusiones = {"positivos": [], "negativos": []}

        if "Churn" not in df.columns:
            return {"error": "No existe la columna Churn"}, {}, conclusiones

        cat_cols = df.select_dtypes(exclude="number").columns

        for col in cat_cols:
            if col == "Churn":
                continue

            # Tabla de proporciones
            tabla = pd.crosstab(df[col], df["Churn"], normalize="index").round(2)
            resultados[col] = tabla

            # Gráfico de barras apiladas
            fig, ax = plt.subplots(figsize=(7, 4))
            tabla.plot(kind="bar", stacked=True, ax=ax, colormap="Set2")
            ax.set_title(f"{col} vs Churn")
            graficos[col] = fig

            # Conclusiones automáticas
            if "Yes" in tabla.columns:
                churn_rates = tabla["Yes"].sort_values(ascending=False)
                top_cat = churn_rates.head(1)
                low_cat = churn_rates.tail(1)

                for categoria, val in top_cat.items():
                    conclusiones["positivos"].append(
                        f"📈 En la categoría **{col} = {categoria}**, el churn es más alto ({val*100:.1f}%)."
                    )
                for categoria, val in low_cat.items():
                    conclusiones["negativos"].append(
                        f"📉 En la categoría **{col} = {categoria}**, el churn es más bajo ({val*100:.1f}%)."
                    )

        return resultados, graficos, conclusiones



    # Método genérico para formatear resultados
    def formatear_resultado(self, resultado, columnas, incluir_tipo=False, limpiar=False):
        """
        Convierte Series, dict o lista en DataFrame con columnas personalizadas.
        Si incluir_tipo=True y resultado es lista de columnas, añade tipo de dato.
        """
        if isinstance(resultado, (pd.Series, dict)):
            df_res = pd.DataFrame(resultado).reset_index()
            df_res.columns = columnas
        elif isinstance(resultado, list):
            if incluir_tipo:
                # Creamos DataFrame con nombre de columna + tipo de dato
                tipos = (self.df_limpio if limpiar else self.df_original)[resultado].dtypes.reset_index()
                # Usamos los nombres pasados en 'columnas'
                tipos.columns = columnas
                df_res = tipos
            else:
                df_res = pd.DataFrame(resultado, columns=columnas)
        else:
            df_res = pd.DataFrame([resultado], columns=columnas)
        return df_res
    
    def limpiar_transformar_dataframes(self, dataframe=None, excluir_patron=None):
        """
        Devuelve una copia del DataFrame con:
        - Columnas binarias (0/1) transformadas a categóricas (No/Sí).
        - Columnas tipo object que deberían ser numéricas convertidas a float,
          reemplazando espacios en blanco por NaN.
        """
        df_preparado = dataframe.copy() if dataframe is not None else self.df_original.copy()
        log_limpieza = []

        # --- Excluir columnas según patrón ---
        if excluir_patron:
            patron = excluir_patron.lower()
            cols_excluir = [
                c for c in df_preparado.columns
                if (
                    c.lower() == patron or
                    c.lower().startswith(patron) or
                    c.lower().endswith(patron)
                )
            ]
            df_preparado = df_preparado.drop(columns=cols_excluir)
            for col in cols_excluir:
                log_limpieza.append({"columna": col, "accion": f"Excluida por patrón '{patron}'", "nulos_nuevos": 0})

        # --- Transformar binarios (0/1 → No/Sí) ---
        for col in df_preparado.select_dtypes(include=[int, float]).columns:
            valores_unicos = df_preparado[col].dropna().unique()
            if set(valores_unicos) == {0, 1}:
                df_preparado[col] = df_preparado[col].map({0: "No", 1: "Sí"}).astype("category")
                log_limpieza.append({"columna": col, "accion": "Binario → categórico (No/Sí)", "nulos_nuevos": 0})

        # --- Limpiar solo campos object que parecen numéricos ---
        for col in df_preparado.select_dtypes(include=["object"]).columns:
            # Si todos los valores son dígitos o espacios, intentamos convertir
            if df_preparado[col].str.strip().str.match(r"^\d*\.?\d*$").all():
                nulos_antes = df_preparado[col].isna().sum()
                df_preparado[col] = df_preparado[col].str.strip()
                df_preparado[col] = pd.to_numeric(df_preparado[col], errors="coerce")
                nulos_despues = df_preparado[col].isna().sum()
                nuevos_nulos = nulos_despues - nulos_antes
                log_limpieza.append({"columna": col, "accion": "Object → numérico (espacios → NaN)", "nulos_nuevos": nuevos_nulos})
            else:
                # Se conserva como categórica
                df_preparado[col] = df_preparado[col].astype("category")
                log_limpieza.append({"columna": col, "accion": "Mantiene tipo categórico", "nulos_nuevos": 0})

        df_log = pd.DataFrame(log_limpieza)
        return df_preparado, df_log
    
