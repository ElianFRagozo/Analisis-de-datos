from cmath import nan
from datetime import date
import streamlit as st
from helper import data, seconddata, match_elements, describe, outliers, drop_items, download_data, filter_data, num_filter_data, rename_columns, clear_image_cache, handling_missing_values, data_wrangling
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
     page_title="Análisis de Datos FonviSocial",
     page_icon="images/fonvi.png",
     layout="wide",
     initial_sidebar_state="expanded",
)

st.sidebar.title("Análisis de Datos FonviSocial")

file_format_type = ["csv", "txt", "xls", "xlsx", "ods", "odt"]
functions = ["Resumen", "Valores Atípicos", "Eliminar Columnas", "Eliminar Filas Categóricas", "Eliminar Filas Numéricas", "Renombrar Columnas", "Mostrar Gráfico", "Manejo de Datos Faltantes", "Transformación de Datos"]
excel_type = ["vnd.ms-excel", "vnd.openxmlformats-officedocument.spreadsheetml.sheet", "vnd.oasis.opendocument.spreadsheet", "vnd.oasis.opendocument.text"]

uploaded_file = st.sidebar.file_uploader("Sube tu archivo", type=file_format_type)

if uploaded_file is not None:

    file_type = uploaded_file.type.split("/")[1]
    
    if file_type == "plain":
        separator = st.sidebar.text_input("Por favor, ingresa el separador de tus datos: ", max_chars=5) 
        data = data(uploaded_file, file_type, separator)

    elif file_type in excel_type:
        data = data(uploaded_file, file_type)

    else:
        data = data(uploaded_file, file_type)
    
    describe, shape, columns, num_category, str_category, null_values, dtypes, unique, str_category, column_with_null_values = describe(data)

    multi_function_selector = st.sidebar.multiselect("Ingresa el nombre o selecciona la columna que deseas graficar: ", functions, default=["Resumen"])

    st.subheader("Vista Previa del Conjunto de Datos")
    st.dataframe(data)

    st.text(" ")
    st.text(" ")
    st.text(" ")

    if "Resumen" in multi_function_selector:
        st.subheader("Descripción del Conjunto de Datos")
        st.write(describe)

        st.text(" ")
        st.text(" ")
        st.text(" ")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.text("Información Básica")
            st.write("Nombre del Conjunto de Datos")
            st.text(uploaded_file.name)

            st.write("Tamaño del Conjunto de Datos (MB)")
            number = round((uploaded_file.size*0.000977)*0.000977, 2)
            st.write(number)

            st.write("Forma del Conjunto de Datos")
            st.write(shape)
            
        with col2:
            st.text("Columnas del Conjunto de Datos")
            st.write(columns)
        
        with col3:
            st.text("Columnas Numéricas")
            st.dataframe(num_category)
        
        with col4:
            st.text("Columnas de Texto")
            st.dataframe(str_category)
            

        col5, col6, col7, col8 = st.columns(4)

        with col6:
            st.text("Tipo de Datos de las Columnas")
            st.dataframe(dtypes)
        
        with col7:
            st.text("Valores Únicos Contados")
            st.write(unique)
        
        with col5:
            st.write("Valores Nulos Contados")
            st.dataframe(null_values)

# ==================================================================================================
    if "Valores Atípicos" in multi_function_selector:

        outliers_selection = st.multiselect("Ingresa o selecciona el nombre de las columnas para ver los valores atípicos:", num_category)
        outliers = outliers(data, outliers_selection)
        
        for i in range(len(outliers)):
            st.image(outliers[i])
# ===================================================================================================

    if "Eliminar Columnas" in multi_function_selector:
        
        multiselected_drop = st.multiselect("Por favor, escribe o selecciona una o varias columnas que deseas eliminar: ", data.columns)
        
        dropped = drop_items(data, multiselected_drop)
        st.write(dropped)
        
        drop_export = download_data(dropped, label="Eliminado(Editado)")

# =====================================================================================================================================
    if "Eliminar Filas Categóricas" in multi_function_selector:

        filter_column_selection = st.selectbox("Por favor, selecciona o ingresa un nombre de columna: ", options=data.columns)
        filtered_value_selection = st.multiselect("Ingresa el nombre o selecciona los valores que no deseas en tu columna {} (Puedes elegir múltiples valores): ".format(filter_column_selection), data[filter_column_selection].unique())
        
        filtered_data = filter_data(data, filter_column_selection, filtered_value_selection)
        st.write(filtered_data)
        
        filtered_export = download_data(filtered_data, label="filtrado")

# =============================================================================================================================

    if "Eliminar Filas Numéricas" in multi_function_selector:

        option = st.radio(
        "¿Qué tipo de filtrado deseas?",
        ('Eliminar datos dentro del rango', 'Eliminar datos fuera del rango'))

        num_filter_column_selection = st.selectbox("Por favor, selecciona o ingresa un nombre de columna: ", options=num_category)
        selection_range = data[num_filter_column_selection].unique()

        for i in range(0, len(selection_range)):
            selection_range[i] = selection_range[i]
        selection_range.sort()

        selection_range = [x for x in selection_range if np.isnan(x) == False]

        start_value, end_value = st.select_slider(
        'Selecciona un rango de números que deseas editar o conservar',
        options=selection_range,
        value=(min(selection_range), max(selection_range)))
        
        if option == "Eliminar datos dentro del rango":
            st.write('Vamos a eliminar todos los valores entre ', int(start_value), 'y', int(end_value))
            num_filtered_data = num_filter_data(data, start_value, end_value, num_filter_column_selection, param=option)
        else:
            st.write('Vamos a conservar todos los valores entre', int(start_value), 'y', int(end_value))
            num_filtered_data = num_filter_data(data, start_value, end_value, num_filter_column_selection, param=option)

        st.write(num_filtered_data)
        num_filtered_export = download_data(num_filtered_data, label="num_filtrado")


# =======================================================================================================================================

    if "Renombrar Columnas" in multi_function_selector:

        if 'rename_dict' not in st.session_state:
            st.session_state.rename_dict = {}

        rename_dict = {}
        rename_column_selector = st.selectbox("Por favor, selecciona o ingresa un nombre de columna que deseas renombrar: ", options=data.columns)
        rename_text_data = st.text_input("Ingresa el nuevo nombre para la columna {} ".format(rename_column_selector), max_chars=50)


        if st.button("Guardar Borrador", help="Cuando quieras renombrar múltiples columnas/una sola columna, primero debes hacer clic en el botón Guardar Borrador. Esto actualiza los datos y luego presiona el botón Renombrar Columnas."):
            st.session_state.rename_dict[rename_column_selector] = rename_text_data
        st.code(st.session_state.rename_dict)

        if st.button("Aplicar Cambios", help="Toma tus datos y renombra la columna como desees."):
            rename_column = rename_columns(data, st.session_state.rename_dict)
            st.write(rename_column)
            export_rename_column = download_data(rename_column, label="renombrar_columna")
            st.session_state.rename_dict = {}

# ===================================================================================================================
    plot_columns = []
    if "Mostrar Gráfico" in multi_function_selector:

        plot_columns = st.multiselect("Selecciona columnas para graficar:", data.columns)

    if len(plot_columns) > 0:
        plot_type = st.selectbox("Selecciona el tipo de gráfico:", ["Barra", "Línea", "Dispersión", "Área", "Pastel", "Barra Horizontal", "Radar"])

        if plot_type == "Barra":
            fig = px.bar(data, x=plot_columns[0], y=plot_columns[1:])
        elif plot_type == "Línea":
            fig = px.line(data, x=plot_columns[0], y=plot_columns[1:])
        elif plot_type == "Dispersión":
            fig = px.scatter(data, x=plot_columns[0], y=plot_columns[1:])
        elif plot_type == "Área":
            fig = px.area(data, x=plot_columns[0], y=plot_columns[1:])
        elif plot_type == "Pastel":
            if len(plot_columns) > 1:
                pie_data = data.groupby(plot_columns[0])[plot_columns[1:]].sum().reset_index()
                fig = px.pie(pie_data, names=plot_columns[0], values=plot_columns[1])
            else:
                fig = px.pie(data, names=data.index, values=plot_columns[0])
        elif plot_type == "Barra Horizontal":
            fig = px.bar(data, x=plot_columns[1:], y=plot_columns[0], orientation='h')
        elif plot_type == "Radar":
            if len(plot_columns) >= 3:
                fig = go.Figure()

                for col in plot_columns[1:]:
                    fig.add_trace(go.Scatterpolar(
                        r=data[col],
                        theta=data[plot_columns[0]],
                        fill='toself',
                        name=col
                    ))

                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, data[plot_columns[1:]].max().max()]
                        )),
                    showlegend=True
                )
            else:
                st.warning("Por favor, selecciona al menos tres columnas para el gráfico Radar.")
                fig = None
        if fig is not None:
            st.plotly_chart(fig)
    else:
        st.warning("Por favor, selecciona al menos una columna para graficar.")

# ====================================================================================================================    

    if "Manejo de Datos Faltantes" in multi_function_selector:
        handling_missing_value_option = st.radio("Selecciona lo que deseas hacer", ("Eliminar Valores Nulos", "Rellenar Valores Faltantes"))

        if handling_missing_value_option == "Eliminar Valores Nulos":

            drop_null_values_option = st.radio("Elige tu opción adecuada: ", ("Eliminar todas las filas con valores nulos", "Eliminar solo las filas que contienen todos valores nulos"))
            dropped_null_value = handling_missing_values(data, drop_null_values_option)
            st.write(dropped_null_value)
            export_rename_column = download_data(dropped_null_value, label="rellenar_columna")
        
        elif handling_missing_value_option == "Rellenar Valores Faltantes":
            
            if 'missing_dict' not in st.session_state:
                st.session_state.missing_dict = {}
            
            fillna_column_selector = st.selectbox("Por favor, selecciona o ingresa un nombre de columna que deseas rellenar con valores NaN: ", options=column_with_null_values)
            fillna_text_data = st.text_input("Ingresa el nuevo valor para la columna {} con valor NaN".format(fillna_column_selector), max_chars=50)

            if st.button("Guardar Borrador", help="Cuando quieras rellenar múltiples columnas/una sola columna con valores nulos, primero debes hacer clic en el botón Guardar Borrador. Esto actualiza los datos y luego presiona el botón Aplicar Cambios."):     
                
                if fillna_column_selector in num_category:
                    try:
                        st.session_state.missing_dict[fillna_column_selector] = float(fillna_text_data)
                    except:
                        st.session_state.missing_dict[fillna_column_selector] = int(fillna_text_data)
                else:
                    st.session_state.missing_dict[fillna_column_selector] = fillna_text_data

            st.code(st.session_state.missing_dict)

            if st.button("Aplicar Cambios", help="Toma tus datos y rellena los valores NaN en las columnas como desees."):

                fillna_column = handling_missing_values(data, handling_missing_value_option, st.session_state.missing_dict)
                st.write(fillna_column)
                export_rename_column = download_data(fillna_column, label="rellenar_columna")
                st.session_state.missing_dict = {}

# ==========================================================================================================================================

    if "Transformación de Datos" in multi_function_selector:
        data_wrangling_option = st.radio("Elige tu opción adecuada: ", ("Fusión por Índice", "Concatenación por Eje"))

        if data_wrangling_option == "Fusión por Índice":
            data_wrangling_merging_uploaded_file = st.file_uploader("Sube tu segundo archivo que deseas fusionar", type=uploaded_file.name.split(".")[1])

            if data_wrangling_merging_uploaded_file is not None:

                second_data = seconddata(data_wrangling_merging_uploaded_file, file_type=data_wrangling_merging_uploaded_file.type.split("/")[1])
                same_columns = match_elements(data, second_data)
                merge_key_selector = st.selectbox("Selecciona una columna por la cual deseas fusionar los dos conjuntos de datos", options=same_columns)
                
                merge_data = data_wrangling(data, second_data, merge_key_selector, data_wrangling_option)
                st.write(merge_data)
                download_data(merge_data, label="fusión_por_índice")

        if data_wrangling_option == "Concatenación por Eje":

            data_wrangling_concatenating_uploaded_file = st.file_uploader("Sube tu segundo archivo que deseas concatenar", type=uploaded_file.name.split(".")[1])

            if data_wrangling_concatenating_uploaded_file is not None:

                second_data = seconddata(data_wrangling_concatenating_uploaded_file, file_type=data_wrangling_concatenating_uploaded_file.type.split("/")[1])
                concatenating_data = data_wrangling(data, second_data, None, data_wrangling_option)
                st.write(concatenating_data)
                download_data(concatenating_data, label="concatenación_por_eje")
        
# ==========================================================================================================================================
    st.sidebar.info("Después de usar esta aplicación, por favor haz clic en el botón Borrar Caché para que todos tus datos sean eliminados de la carpeta.")
    if st.sidebar.button("Borrar Caché"):
        clear_image_cache()

else:
    with open('samples/sample.zip', 'rb') as f:
        st.sidebar.download_button(
                label="Descargar Datos de Muestra y Usarlos",
                data=f,
                file_name='datos_muestra.zip',
                help="Descarga algunos datos de muestra y úsalos para explorar esta aplicación web."
            )
