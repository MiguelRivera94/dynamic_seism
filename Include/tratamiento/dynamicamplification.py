import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os
import scipy as sp
import pandas as pd
from statsmodels.tsa.tsatools import detrend
import pdfkit
import base64
from Include.tratamiento.record import TratamientoRecord
from openpyxl import Workbook

image_etiquetas = []
class DynamicAmplification:
    def __init__(self, proyectPath, tratamiento: TratamientoRecord):
        # Initialize an empty list to store image labels
        image_etiquetas = []
        # Assign the 'tratamiento' object to the instance variable 'self.tratamiento'
        self.tratamiento = tratamiento
        # Assign the project path to the instance variable 'self.proyectPath'
        self.proyectPath = proyectPath
         # Flatten the fregistros_90 attribute from the tratamiento instance and convert to a NumPy array
        self.fregistros_90 = np.array(
            self.tratamiento.fregistros_90, dtype=np.float64
        ).flatten()
        # Define paths for HTML, temporary HTML, and PDF files using the project path and file basename from tratamiento
        self.archivo_html = (
            f"{self.proyectPath}/results/html/da_{self.tratamiento.filebasename}.html"
        )
        # Define the path for the temporary HTML report file
        self.archivo_temporal_html = f"{self.proyectPath}/results/html/da_{self.tratamiento.filebasename}.temporal.html"
        # Define the path for the PDF report file
        self.archivo_pdf = (
            f"{self.proyectPath}/results/pdf/da_{self.tratamiento.filebasename}.pdf"
        )
        # Define the path for the Excel report file with suffix '_report_sr'
        self.datos_informe_df_sfc = (
            f"{self.proyectPath}/results/xlsx/{self.tratamiento.filebasename}_report_sr.xlsx"
        )
        # Define the path for the Excel report file with suffix '_report_dm'
        self.datos_informe_da = (
            f"{self.proyectPath}/results/xlsx/{self.tratamiento.filebasename}_report_dm.xlsx"
        )
        #self.datos_informe = (
        #    f"{self.proyectPath}/results/xlsx/{self.tratamiento.filebasename}_complete.xlsx"
        #)

        # Check if the dynamic amplification report file exists, and if so, delete it
        if os.path.exists(self.datos_informe_da):
            os.remove(self.datos_informe_da)
            print(f"Archivo '{self.datos_informe_da}' eliminado.")

        #if os.path.exists(self.datos_informe):
        #    os.remove(self.datos_informe)
        #    print(f"Archivo '{self.datos_informe}' eliminado.")
        # Initialize lists for HTML content output
        self.salidaHtml = []
        self.salidaTemporalHtml = []
        # Close all existing plots to ensure a clean state for generating new plots
        # limpieza de datos
        plt.close("all")

    def saveImages(self, plt):
        # Get a list of figure numbers
        fig_nums = plt.get_fignums()
        # Create a list of figure objects based on the figure numbers
        figs = [plt.figure(n) for n in fig_nums]
        # print(f"figs: {figs}")
        # Loop through each figure object
        for fig in figs:
            # Construct the file path for saving the image
            ruta_imagen = f"{self.proyectPath}/results/html/images/da_{self.tratamiento.filebasename}/{self.numImagesDynamic}.png"
            # print(ruta_imagen)
            # Save the figure as a PNG image at the constructed file path with 300 dpi resolution
            fig.savefig(
                ruta_imagen,
                dpi=300,
            )
            # Increment the counter for dynamic images
            self.numImagesDynamic = self.numImagesDynamic + 1

    def procesar(self):
        self.numImagesDynamic = 1
        # CALCULATE AN ARRAY FOR VARIOUS DAMPING VALUES "zeta"
        # The damping values 'zeta' are generated 
        # with various conditions of 'zeta1', 'zeta2', and 'deltazeta'
        if self.tratamiento.deltazeta == 0:
            if self.tratamiento.zeta1 >= 0 and self.tratamiento.zeta2 >= 0 and self.tratamiento.zeta1 <= self.tratamiento.zeta2:
                zeta = np.array([self.tratamiento.zeta1]).flatten()
            elif self.tratamiento.zeta1 >= 0 and self.tratamiento.zeta2 < 0:
                 zeta = np.array([self.tratamiento.zeta1]).flatten()
            elif self.tratamiento.zeta1 < 0 and self.tratamiento.zeta2 >= 0:
                zeta = np.array([self.tratamiento.zeta2]).flatten()
            else:
                zeta = np.array([0]).flatten()
        else:
            if self.tratamiento.zeta1 >= 0 and self.tratamiento.zeta2 >= 0:
                if self.tratamiento.zeta2 == self.tratamiento.zeta1:
                            zeta = np.array([self.tratamiento.zeta1]).flatten()
                elif self.tratamiento.zeta2 > self.tratamiento.zeta1:
                    if self.tratamiento.zeta1 + self.tratamiento.deltazeta <= self.tratamiento.zeta2:
                        zeta = np.arange(self.tratamiento.zeta1, self.tratamiento.zeta2, self.tratamiento.deltazeta).reshape(-1, 1).flatten()
                        zeta = np.append(zeta, [self.tratamiento.zeta2]).flatten()
                    else:
                        zeta = np.append([self.tratamiento.zeta1], [self.tratamiento.zeta2]).flatten() 
                else:
                    zeta = np.array([self.tratamiento.zeta1]).flatten()
            elif self.tratamiento.zeta1 >= 0 and self.tratamiento.zeta2 < 0:
                zeta = np.array([self.tratamiento.zeta1]).flatten()
            elif self.tratamiento.zeta1 < 0 and self.tratamiento.zeta2 >= 0:
                zeta = np.array([self.tratamiento.zeta2]).flatten()
            else:
                zeta = np.array([0]).flatten()
        if len(zeta) > 1 and np.isclose(zeta[-1], zeta[-2]):
            zeta = np.delete(zeta, -1)

        # Frequency Calculation
        festructura = 1 / self.tratamiento.Tevaluado  
        westructura = 2 * np.pi * festructura
        wregistros_90 = 2 * np.pi * self.fregistros_90

        # Calculation of the angular frequencies ratio W/Wn
        rw_90 = np.zeros((len(wregistros_90), 1))
        for i in range(len(wregistros_90)):
            rw_90[i] = wregistros_90[i] / westructura
            
        # Establish a domain based on the ratio of angular frequencies
        maxval_graficar = np.zeros(len(rw_90))
        for i in range(len(rw_90)):
            if max(rw_90[i]) < 2.5:
                maxval_graficar[i] = 2.5
            else:
                maxval_graficar[i] = rw_90[i][0] + 1
        # Specify the number of values each graph will have
        num_valores = 1000
        # Generate the W/Wn ratios for the graphs
        rw_grafico = np.zeros((num_valores, len(maxval_graficar)))
        for i in range(len(maxval_graficar)):
            rw_grafico[:, i] = np.linspace(0, maxval_graficar[i], num_valores)

        # Calculate dynamic magnification values in the linear range
        Rd_lineal = np.zeros((num_valores, len(zeta) * len(rw_grafico[0])))
        kkk = 0
        for i in range(len(rw_grafico[0])):
            for j in range(len(zeta)):
                Rd_lineal[:, kkk] = (
                    1
                    / (
                        ((1 - (rw_grafico[:, i]) ** 2) ** 2)
                        + (2 * zeta[j] * rw_grafico[:, i]) ** 2
                    )
                    ** 0.5
                )
                kkk = kkk + 1

        # Calculate dynamic magnification values in the nonlinear range
        Rd_nolineal = np.zeros((num_valores, len(zeta) * len(rw_grafico[0])))
        kkk = 0
        for i in range(len(rw_grafico[0])):
            for j in range(len(zeta)):
                Rd_nolineal[:, kkk] = (
                    (1 + (2 * zeta[j] * rw_grafico[:, i]) ** 2)
                    / (
                        ((1 - (rw_grafico[:, i]) ** 2) ** 2)
                        + (2 * zeta[j] * rw_grafico[:, i]) ** 2
                    )
                ) ** 0.5
                kkk = kkk + 1

        # Calculate dynamic magnification values based on the structure's period and 
        # predominant frequencies of the seismic record in the linear range
        Rd_calculo_lineal = []
        for i in range(len(rw_90)):
            newrow_lineal = []
            for k in range(len(zeta)):
                zeta_a = zeta[k]
                for j in range(len(rw_90[0])):
                    Rdd_lineal = (
                        1
                        / (
                            ((1 - (rw_90[i][j]) ** 2) ** 2)
                            + (2 * zeta_a * rw_90[i][j]) ** 2
                        )
                        ** 0.5
                    )
                    newrow_lineal.append(Rdd_lineal)
            Rd_calculo_lineal.append(newrow_lineal)
        Rd_calculo_lineal = np.array(Rd_calculo_lineal)

        Rd_calculo2_lineal = np.zeros((len(rw_90), len(Rd_calculo_lineal[0])))
        kk = 0
        for j in range(len(rw_90[0])):
            for i in range(len(zeta)):
                Rd_calculo2_lineal[:, kk] = Rd_calculo_lineal[
                    :, (len(rw_90[0]) * i + j)
                ]
                kk = kk + 1

        # Calculate dynamic magnification values based on the structure's period and 
        # predominant frequencies of the seismic record in the nonlinear range
        Rd_calculo_nolineal = []
        for i in range(len(rw_90)):
            newrow_nolineal = []
            for k in range(len(zeta)):
                zeta_a = zeta[k]
                for j in range(len(rw_90[0])):
                    Rdd_nolineal = (
                        (1 + (2 * zeta_a * rw_90[i][j]) ** 2)
                        / (
                            ((1 - (rw_90[i][j]) ** 2) ** 2)
                            + (2 * zeta_a * rw_90[i][j]) ** 2
                        )
                    ) ** 0.5
                    newrow_nolineal.append(Rdd_nolineal)
            Rd_calculo_nolineal.append(newrow_nolineal)
        Rd_calculo_nolineal = np.array(Rd_calculo_nolineal)

        Rd_calculo2_nolineal = np.zeros((len(rw_90), len(Rd_calculo_nolineal[0])))
        kk = 0
        for j in range(len(rw_90[0])):
            for i in range(len(zeta)):
                Rd_calculo2_nolineal[:, kk] = Rd_calculo_nolineal[
                    :, (len(rw_90[0]) * i + j)
                ]
                kk = kk + 1

        # Calculate the transpose of the previous matrices
        Rd_evaluado_lineal = Rd_calculo2_lineal.T
        Rd_evaluado_nolineal = Rd_calculo2_nolineal.T

        ################################################################### Graphs
        colormap1 = plt.cm.Blues.reversed()
        colormap2 = plt.cm.gray

        # Ruta del directorio donde quieres guardar las gráficas

        # Loop through each element in self.fregistros_90
        for j in range(len(self.fregistros_90)):
            # Create a label index
            iLabel = j + 1
            # Append a label to the image_etiquetas list
            image_etiquetas.append(f"Dynamic Magnification (&psi;) ({iLabel}) ")
            #plt.figure(figsize=(12, 16), dpi=300)
            #########################################################################################################################################################################################
            # Set the figure height for dynamic magnification
            hsize_dm = 5.7
            # Create a new figure with specified size and resolution
            plt.figure(figsize=(11, hsize_dm), dpi=300)
            # Calculate the vertical line position
            linea_vertical = self.fregistros_90[j] / (self.tratamiento.Tevaluado**-1)
            # Plot a vertical dotted line at the calculated position
            plt.axvline(x=linea_vertical, color='dimgray', linestyle='dotted',
                    label="Tn(s) = {:.2f};f(Hz) = {:.2f}".format(self.tratamiento.Tevaluado, self.fregistros_90[j]))
                    #label="Tn(s) = {:.3f};f(Hz) = {:.3f};W/Wn = {:.3f}".format(self.tratamiento.Tevaluado, self.fregistros_90[j], linea_vertical))
            # Loop through each damping ratio
            for i in range(len(zeta)):
                if i == 0:
                    # Set colors for the first damping ratio
                    color2 = mcolors.to_rgba("black", alpha=0.8)
                    color1 = mcolors.to_rgba("blue", alpha=0.8)
                else:
                    # Set colors for subsequent damping ratios
                    color2 = mcolors.to_rgba(
                        colormap2((i + 1) / Rd_nolineal.shape[1]), alpha=0.8
                    )
                    color1 = mcolors.to_rgba(
                        colormap1((i + 1) / Rd_lineal.shape[1]), alpha=0.8
                    )
                # Plot the linear dynamic magnification curve
                plt.plot(
                    rw_grafico[:, j],
                    Rd_lineal[:, j * len(zeta) + i],
                    label=(
                        "ζ = {:.2%}".format(zeta[i])
                        + "; "
                        + "ψ_L = {:.3}".format(Rd_evaluado_lineal[i, j])
                    ),
                    color=color2,
                )
                # Plot the nonlinear dynamic magnification curve
                plt.plot(
                    rw_grafico[:, j],
                    Rd_nolineal[:, j * len(zeta) + i],
                    label=(
                        "ζ = {:.2%}".format(zeta[i])
                        + "; "
                        + "ψ_NL = {:.3}".format(Rd_evaluado_nolineal[i, j])
                    ),
                    color=color1,
                )

            # Check if the vertical line position is within a specific range
            if 0.7 <= linea_vertical < 0.99:
                # Annotate the plot with a label for the vertical line
                plt.annotate(
                    "Dynamic Magnification for W/Wn = {:.2f}".format(linea_vertical),
                    # Position of the point to label
                    xy=(
                        linea_vertical,
                        plt.ylim()[1],
                    ),  
                    xytext=(-15, -15),  # Text offset
                    textcoords="offset points",  # Coordinate type for the offset
                    verticalalignment="top",
                    horizontalalignment="right",
                    color="dimgray",
                    fontsize=10,
                    rotation="vertical",
                )
            else:
                # Annotate the plot with a label for the vertical line (different format)
                plt.annotate(
                    "Dynamic Magnification for W/Wn = {:.3f}".format(linea_vertical),
                    xy=(
                        linea_vertical,
                        plt.ylim()[1],
                    ),  # Position of the point to label
                    xytext=(14, -15),  # Text offset
                    textcoords="offset points",  # Coordinate type for the offset
                    verticalalignment="top",
                    horizontalalignment="left",
                    color="dimgray",
                    fontsize=10,
                    rotation="vertical",
                )
            # Set the X-axis label
            plt.xlabel("W/Wn", fontsize=15)
            # Set the Y-axis label
            plt.ylabel("Dynamic Magnification ψ", fontsize=10)
            #Tn(s) = {:.3f};f(Hz) = {:.3f};W/Wn = {:.3f}".format(self.tratamiento.Tevaluado, self.fregistros_90[j], linea_vertical))
            # Format and set the plot title
            title_graph = "Dyn. Mag. for Tn(s)={:.2f};f(Hz)={:.2f};W/Wn={:.2f}".format(self.tratamiento.Tevaluado, self.fregistros_90[j], linea_vertical)
            plt.title(title_graph, fontsize=11)
            # Add the legend to the plot
            plt.legend(loc="upper left", bbox_to_anchor=(1, 1), fontsize=12)    ###############################################
            # Set the maximum number of labels to display on the legend for one column
            num_max_etiquetas = 40 # This value is adjusted based on hsize_dm by trial and error  (33)
            # This condition is used to avoid division by zero
            if self.tratamiento.deltazeta != 0:
                # Calculate the number of labels based on the given delta zeta value
                num_etiquetas = (2*(self.tratamiento.zeta2-self.tratamiento.zeta1)/self.tratamiento.deltazeta)+3
            else:
                # Default number of labels if delta zeta is zero
                num_etiquetas = 10 
            # Calculate the number of columns for the legend labels
            num_col_etiqueta = np.ceil(num_etiquetas/num_max_etiquetas)
            # Set the font size for the legend labels
            tamano_letra = 7
            # Add the legend to the plot with specified location, font size, and number of columns
            plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=tamano_letra, ncol=num_col_etiqueta)    ############ cambiar a 10
            # Set the X-axis limit slightly beyond the maximum value in rw_grafico
            plt.xlim(0,np.max(rw_grafico[:, j])+0.05)
            
            # Guardar la imagen en un archivo en el directorio destino
            # nombre_archivo = os.path.join(directorio_destino, f"grafico_{j}.png")
            # plt.savefig(nombre_archivo, bbox_inches="tight")
            # plt.close()
            # Ensures all plot elements fit within the figure area.
            plt.tight_layout()

        # Save generated images using matplotlib
        self.saveImages(plt)
        # Resultados para reporte de graficos
        # Calculate the index of the maximum value in maxval_graficar
        i_max = np.argmax(maxval_graficar)
        # Calculate the last index on axis 0 of the zeta array
        i_ultimo = zeta.shape[0] - 1
        # Extract a specific column from rw_grafico and reshape it into a single-column matrix
        rw_grafico_reporte = rw_grafico[:, i_max].reshape(-1, 1)
        # Build matrices for linear and nonlinear reports
        Reporte_graficas_lineales = np.hstack(
            (
                rw_grafico_reporte,
                Rd_lineal[
                    :, (i_max) * i_ultimo + i_max : (i_max + 1) * i_ultimo + (i_max + 1)
                ],
            )
        )
        Reporte_graficas_nolineales = np.hstack(
            (
                rw_grafico_reporte,
                Rd_nolineal[
                    :, (i_max) * i_ultimo + i_max : (i_max + 1) * i_ultimo + (i_max + 1)
                ],
            )
        )
        # Define column names for Excel reports
        column_name_reporte_graficas = [f"ζ={z*100:.2f}" for z in zeta]
        # Add the label "W/Wn" at the beginning of the list
        column_name_reporte_graficas.insert(0, "W/Wn")
        # Create a copy for column names
        nombres_columnas_reporte_graficas = []
        nombres_columnas_reporte_graficas.extend(column_name_reporte_graficas)

        # Labels for Excel report
        # Row and column names
        nombres_filas_factores = [f"f={f}Hz" for f in self.fregistros_90]
        nombres_columnas_factores = []
        # Generate labels for factor columns
        for j in range(len(zeta)):
            # Use Unicode for the Greek symbol "zeta"
            zeta_griego = "\u03B6"
            column_name_factores = "T={:.2f}s;{}={:.2f}%".format(
                self.tratamiento.Tevaluado, zeta_griego, zeta[j] * 100
            )
            nombres_columnas_factores.append(column_name_factores)

        # Create DataFrames for linear and non-linear graphs
        df_grafico_lineal = pd.DataFrame(
            Reporte_graficas_lineales, columns=nombres_columnas_reporte_graficas
        )
        df_grafico_nolineal = pd.DataFrame(
            Reporte_graficas_nolineales, columns=nombres_columnas_reporte_graficas
        )

        # Create DataFrames for both matrices
        df_lineal = pd.DataFrame(
            Rd_calculo2_lineal,
            index=nombres_filas_factores,
            columns=nombres_columnas_factores,
        )
        df_nolineal = pd.DataFrame(
            Rd_calculo2_nolineal,
            index=nombres_filas_factores,
            columns=nombres_columnas_factores,
        )

        ruta_excel = self.datos_informe_da
        # Create an ExcelWriter object
        with pd.ExcelWriter(ruta_excel, engine="openpyxl") as excel_writer:
            # Convert DataFrames to separate sheets in the Excel file
            df_grafico_lineal.to_excel(
                excel_writer, sheet_name="Linear Dynamic M. Curves", index=False
            )
            df_grafico_nolineal.to_excel(
                excel_writer, sheet_name="Nonlinear Dynamic M. Curves", index=False
            )
            df_lineal.to_excel(excel_writer, sheet_name="Dynamic Magn. Fact. - L")
            df_nolineal.to_excel(
                excel_writer, sheet_name="Dynamic Magn. Fact. - NL"
            )

            # Get the ExcelWriter object
            workbook = excel_writer.book

            # Get the sheets in the Excel file
            sheets = workbook.sheetnames

            # Auto-adjust the width of columns for each sheet
            # Iterate over each sheet name (sheet_name) in the list of sheets (sheets)
            for sheet_name in sheets:
                # Get the specific sheet object from the workbook
                sheet = workbook[sheet_name]
                # Iterate over each set of column cells in the current sheet
                for column_cells in sheet.columns:
                    # Initialize the maximum cell length to 0
                    max_length = 0
                    # Create a list of cells for the current column
                    column = [cell for cell in column_cells]
                    # Iterate over each cell in the current column cell list
                    for cell in column:
                        try:
                            # Attempt to get the length of the cell value as a string
                            if len(str(cell.value)) > max_length:
                                # Update the maximum length if the current string length is greater
                                max_length = len(cell.value)
                        except:
                            # Catch exceptions that may occur when attempting to get the cell length
                            pass
                    # Calculate the adjusted width for the current column (maximum length + 2)
                    adjusted_width = max_length + 2
                    # Get the column letter of the first cell in the column cell set
                    column_letter = column_cells[0].column_letter
                    # Set the width of the column dimensions for the current sheet
                    sheet.column_dimensions[column_letter].width = adjusted_width

        # Paths to the two Excel files you want to concatenate
        archivo1 = self.datos_informe_df_sfc
        archivo2 = self.datos_informe_da

        # Read all sheets from the first file into a dictionary of DataFrames
        hojas_archivo1 = pd.read_excel(archivo1, sheet_name=None)

        # Read all sheets from the second file into a dictionary of DataFrames
        hojas_archivo2 = pd.read_excel(archivo2, sheet_name=None)

        # Crear un nuevo archivo Excel para almacenar el resultado
        #with pd.ExcelWriter(self.datos_informe, engine='openpyxl') as writer:
        #    for nombre_hoja, df in hojas_archivo1.items():
        #        df.to_excel(writer, sheet_name=nombre_hoja, index=False)
        #    for nombre_hoja, df in hojas_archivo2.items():
        #        df.to_excel(writer, sheet_name=nombre_hoja, index=False)   

        self.tratamiento.numImagesDynamic = self.numImagesDynamic
        self.tratamiento.Rd_evaluado_lineal = Rd_evaluado_lineal
        self.tratamiento.Rd_evaluado_nolineal = Rd_evaluado_nolineal
        self.tratamiento.zeta = zeta
        self.RenderFiles()

    def RenderFiles(self):
        # Define a HTML tag for page break in rendered HTML output
        salto_linea = (
            '<div style = "display:block; clear:both; page-break-after:always;"></div>'
        )        
        # Append filename header to main HTML output
        self.salidaHtml.append(
            f"<h3 style='font-size:18px'>Filename: {self.tratamiento.filebasename}</h3><hr>"
        )
        # Start a new div container for images in main HTML output
        self.salidaHtml.append('<div>')
        # Iterate through each image index
        for i in range(self.numImagesDynamic):
            if i != 0:
                #self.salidaHtml.append(f"<center><h3>{image_etiquetas[i-1]}</h3></center>") adfsdgfadsfadsfasdfasdfasdfadfasdfsadfadsf
                # Append image tag with source path and styling to main HTML output
                self.salidaHtml.append(
                    f"<img src='images/da_{self.tratamiento.filebasename}/{i}.png' style=\"margin-bottom: 20px; border: 2px solid #000000; padding: 10px;\" width='98%'>" #cambio de 100 a 98 para indicar el borde
                )
        # Close the div container for images in main HTML output
        self.salidaHtml.append("</div>")
        # Combine all HTML elements into a single string for main HTML output
        self.htmlText = " ".join(self.salidaHtml)

        # Append filename header to temporary HTML output
        self.salidaTemporalHtml.append(
            f"<h3 style='font-size:18px'>Filename: {self.tratamiento.filebasename}</h3><hr>"
        )
        # Iterate through each image index for temporary HTML output
        for i in range(self.numImagesDynamic):
            if i != 0:
                # self.salidaTemporalHtml.append(f"<img src='file://{self.proyectPath}/results/html/images/{self.tratamiento.filebasename}/{i}.png' width='100%'><hr>")
                # Open image file in binary mode to read image data
                with open(
                    f"{self.proyectPath}/results/html/images/da_{self.tratamiento.filebasename}/{i}.png",
                    "rb",
                ) as image_file:
                    # Read image data from file
                    image_data = image_file.read()
                
                #if i != 1 :
                
                #self.salidaTemporalHtml.append(f"<center><h3>{image_etiquetas[i-1]}</h3></center>")   fgsfdgdsfgsfdgsdgfsdfgsdfgsdfgsdfgsdgfsfdg
                # Convert image data to Base64 format
                image_base64 = base64.b64encode(image_data).decode("utf-8")
                # Append image tag with Base64-encoded source to temporary HTML output
                self.salidaTemporalHtml.append(
                    f'<img src="data:image/png;base64,{image_base64}" width="100%">'
                )
                # Add a page break after each image except the last one in temporary HTML output
                ultimo_numero = list(range(self.numImagesDynamic))[-1]
                if(i < ultimo_numero):
                    self.salidaTemporalHtml.append(salto_linea)
        # Combine all HTML elements into a single string for temporary HTML output
        self.temporalhtmlText = " ".join(self.salidaTemporalHtml)

        # Write the main HTML content to a text file
        with open(self.archivo_html, "w") as archivo:
            archivo.write(
                f"<html><head><title>Análisis {self.tratamiento.filebasename}</title></head><body>"
            )
            archivo.write(self.htmlText)
            archivo.write("</body></html>")
        # Write the temporary HTML content to a separate text file
        with open(self.archivo_temporal_html, "w") as archivo:
            archivo.write(
                f"<html><head><title>Análisis {self.tratamiento.filebasename}</title></head><body>"
            )
            archivo.write(self.temporalhtmlText)
            archivo.write("</body></html>")

        # Configure options for PDFKit
        opciones = {
            "page-size": "A4",
            "margin-top": "30mm",
            "margin-right": "30mm",
            "margin-bottom": "30mm",
            "margin-left": "30mm",
            "orientation": 'Landscape',
        }
        try:
            # Convert temporary HTML file to PDF using PDFKit
            pdfkit.from_file(
                self.archivo_temporal_html, self.archivo_pdf, options=opciones
            )
            print(f"Archivo PDF guardado en: {self.archivo_pdf}")
        except Exception as e:
            print(f"Error al convertir a PDF: {str(e)}")
