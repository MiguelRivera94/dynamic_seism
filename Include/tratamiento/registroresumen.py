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
# Tags to name the graphics within an HTML file.
image_etiquetas = [
    "Original Record for: Acceleration, Velocity and Displacement",
    "Comparison of Original and Corrected Records for: Acceleration, Velocity, and Displacement",
    "Corrected Record for: acceleration, velocity, and displacement",
    "Filter Gain",
    "Arias Intensity",
    "Comparison between corrected acceleration and acceleration for the significant duration",
    "Fourier Spectrum and Frequency Content Analysis of the Entire Corrected Seismic Record",
]


class RegistroResumen:
    def __init__(self, proyectPath, tratamiento: TratamientoRecord):
        self.tratamiento = tratamiento # Assigning the TratamientoRecord instance to self.tratamiento
        self.proyectPath = proyectPath # Assigning the project path to self.proyectPath
        # Setting file paths based on tratamiento.filebasename
        self.archivo_html = (
            f"{self.proyectPath}/results/html/{self.tratamiento.filebasename}.html"
        )
        self.archivo_temporal_html = f"{self.proyectPath}/results/html/{self.tratamiento.filebasename}.temporal.html"
        self.archivo_pdf = (
            f"{self.proyectPath}/results/pdf/{self.tratamiento.filebasename}.pdf"
        )
        self.datos_informe = (
            f"{self.proyectPath}/results/xlsx/{self.tratamiento.filebasename}_report_sr.xlsx"
        )

        self.salidaHtml = []
        self.salidaTemporalHtml = []

        # Data cleanup
        plt.close("all") # Closing all matplotlib figures

    def saveImages(self, plt):
        fig_nums = plt.get_fignums() # Getting the list of figure numbers from matplotlib
        figs = [plt.figure(n) for n in fig_nums] # Creating a list of figure objects based on their numbers
        # print(f"figs: {figs}")
        for fig in figs:
            ruta_imagen = f"{self.proyectPath}/results/html/images/{self.tratamiento.filebasename}/{self.numImages}.png"
            # Constructing the image path based on proyectoPath, tratamiento.filebasename, and self.numImages
            # print(ruta_imagen)
            # Saving the figure as a PNG image to ruta_imagen
            fig.savefig(
                ruta_imagen,
                dpi=300,
            )
            self.numImages = self.numImages + 1

    def procesar(self):
        # Initializing self.numImages to 1
        self.numImages = 1 
        # Printing the basename of self.tratamiento.ruta_registro
        print("Nombre del Registro:", os.path.basename(self.tratamiento.ruta_registro)) 
         # Reads seismic record data based on self.tratamiento.presentacion_datos
         # The acceleration data is "datosregistro"
        if self.tratamiento.presentacion_datos == "Simple Column": # For simple-column seismic records 
            # Constructs the full path to the record file
            # Skips specified number of rows at the beginning
            datosregistro = np.loadtxt(
                f"{self.proyectPath}/{self.tratamiento.ruta_registro}",
                skiprows=self.tratamiento.filas_inutiles,
            )
        elif self.tratamiento.presentacion_datos == "Multiple Column": # For multiple-column seismic records
            # Constructs the full path to the record file
            # Skips specified number of rows at the beginning
            datosregistro = self.getDataFromFile(
                f"{self.proyectPath}/{self.tratamiento.ruta_registro}",
                self.tratamiento.filas_inutiles,
            )
            # datosregistro = np.genfromtxt(f"{self.proyectPath}/{self.tratamiento.ruta_registro}", skip_header=self.tratamiento.filas_inutiles, delimiter=None, invalid_raise=False)
        elif self.tratamiento.presentacion_datos == "Time Acceleration": # For time-acceleration seismic records
            # Constructs the full path to the record file
            # Skips specified number of rows at the beginning
            datosregistro = np.loadtxt(
                f"{self.proyectPath}/{self.tratamiento.ruta_registro}",
                skiprows=self.tratamiento.filas_inutiles,
            )
            datosregistro = datosregistro[:, 1]
        else:
            print("revisar como estan organizados los datos en el registro")
            exit()
        # ACCELERATION OF THE SEISMIC RECORD
        # Definition of record units
        if self.tratamiento.unidades_aceleracion == "g": # For Record units in fraction of gravity
            fescala_unidades = 981
        elif self.tratamiento.unidades_aceleracion == "cm/s^2": # For Record units in (cm/s^2)
            fescala_unidades = 1
        else:
            print("Unidades no válidas. Debe ser 'g' o 'cm/s2'.")
            exit()
        # Change of record units or scaling of the record
        aceleracionoriginal = (
            self.tratamiento.factor_conversion * datosregistro.reshape(-1, 1).flatten()
        )
        # Creation of the time matrix
        total_valores = aceleracionoriginal.size
        matriz_itiempo = np.arange(total_valores) * self.tratamiento.dt
        matriz_itiempo = matriz_itiempo.reshape(-1, 1).flatten()
        # THE ORIGINAL VELOCITY OF THE SEISMIC RECORD
        # Integrating the acceleration
        velocidadoriginal = sp.integrate.cumtrapz(
            fescala_unidades * aceleracionoriginal,
            matriz_itiempo.flatten(),
            initial=0,
            dx=self.tratamiento.dt,
        )
        # THE ORIGINAL DISPLACEMENT OF THE SEISMIC RECORD
        # Integrating the velocity
        desplazamientooriginal = sp.integrate.cumtrapz(
            velocidadoriginal,
            matriz_itiempo.flatten(),
            initial=0,
            dx=self.tratamiento.dt,
        )
        # PLOTS OF ACCELERATION, VELOCITY, AND DISPLACEMENT FROM THE ORIGINAL RECORD DATA.
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 6), dpi=300)
        # Plot of the original acceleration
        ax1.plot(
            matriz_itiempo,
            aceleracionoriginal,
            color="blue",
            linewidth=0.7,
            label="Original Acceleration",
        )
        ax1.set_xlabel("Time (s)")
        ax1.set_ylabel(
            "Acceleration" + " (" + self.tratamiento.unidades_aceleracion + ")"
        )
        ax1.set_title("Accelerogram")
        ax1.legend(fontsize=8)
        ax1.set_xlim(min(matriz_itiempo), max(matriz_itiempo))
        # Plot of the original velocity
        ax2.plot(
            matriz_itiempo,
            velocidadoriginal,
            color="royalblue",
            linewidth=0.7,
            label="Original Velocity",
        )
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("Velocity (cm/s)")
        ax2.set_title("Velocity")
        ax2.legend(fontsize=8)
        ax2.set_xlim(min(matriz_itiempo), max(matriz_itiempo))
        # Plot of the original displacement
        ax3.plot(
            matriz_itiempo,
            desplazamientooriginal,
            color="dodgerblue",
            linewidth=0.7,
            label="Original Displacement",
        )
        ax3.set_xlabel("Time (s)")
        ax3.set_ylabel("Displacement (cm)")
        ax3.set_title("Displacement")
        ax3.legend(fontsize=8.5)
        ax3.set_xlim(min(matriz_itiempo), max(matriz_itiempo))
        plt.tight_layout()
    # SEISMIC RECORDS PROCESSING
        # BASELINE CORRECTION OF THE SEISMIC RECORD
        if self.tratamiento.realiza_correccion == "Yes":
            if self.tratamiento.grado_cbaseline == 0:
                aceleracion_cbaseline = sp.signal.detrend(
                    aceleracionoriginal, type="constant"
                )
            elif self.tratamiento.grado_cbaseline == 1:
                aceleracion_cbaseline = sp.signal.detrend(
                    aceleracionoriginal, type="linear"
                )
            elif self.tratamiento.grado_cbaseline == 2:
                aceleracion_cbaseline = detrend(aceleracionoriginal, order=2)
            elif self.tratamiento.grado_cbaseline == 3:
                aceleracion_cbaseline = detrend(aceleracionoriginal, order=3)
            elif self.tratamiento.grado_cbaseline == 4:
                aceleracion_cbaseline = detrend(aceleracionoriginal, order=4)
            else:
                print("agregar mas condicionales con el grado requerido")
        elif self.tratamiento.realiza_correccion == "No":
            aceleracion_cbaseline = aceleracionoriginal
        else:
            print("revisar")
            exit()
        # FILTERING OF THE SEISMIC RECORD
        # High-pass filter
        fmuestreo = 1 / self.tratamiento.dt
        if self.tratamiento.type_filtro == "Highpass":
            fnyquist = 0.5 * fmuestreo
            fcortenormalizada = self.tratamiento.fcorte1 / fnyquist
            bhigh, ahigh = sp.signal.butter(
                self.tratamiento.grado_filtro,
                fcortenormalizada,
                "highpass",
                analog=False,
            )
            aceleracionfiltrada = sp.signal.filtfilt(
                bhigh, ahigh, aceleracion_cbaseline
            )
        # Low-pass filter
        elif self.tratamiento.type_filtro == "Lowpass":
            fnyquist = 0.5 * fmuestreo
            fcortenormalizada = self.tratamiento.fcorte1 / fnyquist
            blow, alow = sp.signal.butter(
                self.tratamiento.grado_filtro,
                fcortenormalizada,
                "lowpass",
                analog=False,
            )
            aceleracionfiltrada = sp.signal.lfilter(blow, alow, aceleracion_cbaseline)
        # Bandpass filter
        elif self.tratamiento.type_filtro == "Bandpass":
            fnyquist = 0.5 * fmuestreo
            flow = self.tratamiento.fcorte1 / fnyquist
            fhigh = self.tratamiento.fcorte2 / fnyquist
            b_bandpass, a_bandpass = sp.signal.butter(
                self.tratamiento.grado_filtro, [flow, fhigh], "bandpass"
            )
            aceleracionfiltrada = sp.signal.lfilter(
                b_bandpass, a_bandpass, aceleracion_cbaseline
            )
        # No filtering
        elif self.tratamiento.type_filtro == "None":
            aceleracionfiltrada = aceleracion_cbaseline
        else:
            print("revisar")
            exit()
        # VELOCITIES AND DISPLACEMENTS CORRECTED TO THE BASELINE
        velocidad_cbaseline = sp.integrate.cumtrapz(
            fescala_unidades * aceleracion_cbaseline,
            matriz_itiempo.flatten(),
            initial=0,
            dx=self.tratamiento.dt,
        )
        desplazamiento_cbaseline = sp.integrate.cumtrapz(
            velocidad_cbaseline,
            matriz_itiempo.flatten(),
            initial=0,
            dx=self.tratamiento.dt,
        )
        # FILTERED VELOCITIES AND DISPLACEMENTS
        velocidadfiltrada = sp.integrate.cumtrapz(
            fescala_unidades * aceleracionfiltrada,
            matriz_itiempo.flatten(),
            initial=0,
            dx=self.tratamiento.dt,
        )
        desplazamientofiltrada = sp.integrate.cumtrapz(
            velocidadfiltrada,
            matriz_itiempo.flatten(),
            initial=0,
            dx=self.tratamiento.dt,
        )
        # COMPARATIVE GRAPH BETWEEN THE ORIGINAL AND PROCESSED RECORD FOR: ACC, VEL AND DIS.
        # Original Acceleration vs Processed Acceleration
        fig, (ax4, ax5, ax6) = plt.subplots(3, 1, figsize=(12, 6), dpi=300)
        ax4.plot(
            matriz_itiempo,
            aceleracionoriginal,
            color="black",
            linewidth=0.7,
            label="Original Acceleration",
        )
        ax4.plot(
            matriz_itiempo,
            aceleracionfiltrada,
            color="dodgerblue",
            linewidth=0.7,
            label="Acceleration Corrected and Filtered",
        )
        ax4.set_xlabel("Time (s)")
        ax4.set_ylabel(
            "Acceleration" + " (" + self.tratamiento.unidades_aceleracion + ")"
        )
        ax4.set_title("Accelerogram")
        ax4.legend(fontsize=8.5)
        ax4.set_xlim(min(matriz_itiempo), max(matriz_itiempo))
        # Original Velocity vs Processed Velocity
        ax5.plot(
            matriz_itiempo,
            velocidadoriginal,
            color="black",
            linewidth=0.7,
            label="Original Velocity",
        )
        ax5.plot(
            matriz_itiempo,
            velocidadfiltrada,
            color="dodgerblue",
            linewidth=0.7,
            label="Velocity Corrected and Filtered",
        )
        ax5.set_xlabel("Time (s)")
        ax5.set_ylabel("Velocity (cm/s)")
        ax5.set_title("Velocity")
        ax5.legend(fontsize=8.5)
        ax5.set_xlim(min(matriz_itiempo), max(matriz_itiempo))
        # Original Displacement vs Processed Displacement
        ax6.plot(
            matriz_itiempo,
            desplazamientooriginal,
            color="black",
            linewidth=0.7,
            label="Original Displacement",
        )
        ax6.plot(
            matriz_itiempo,
            desplazamientofiltrada,
            color="dodgerblue",
            linewidth=0.7,
            label="Displacement Corrected and Filtered",
        )
        ax6.set_xlabel("Time (s)")
        ax6.set_ylabel("Displacement (cm)")
        ax6.set_title("Displacement")
        ax6.legend(fontsize=8.5)
        ax6.set_xlim(min(matriz_itiempo), max(matriz_itiempo))
        plt.tight_layout()
        # 
        fig, (ax7, ax8, ax9) = plt.subplots(3, 1, figsize=(12, 6), dpi=300)
        # GRAPH OF PROCESSED ACC. - PROCESSED VEL - PROCESSED DIS.
        # Processed acceleration
        ax7.plot(
            matriz_itiempo,
            aceleracionfiltrada,
            color="blue",
            linewidth=0.7,
            label="Corrected Acceleration",
        )
        ax7.set_xlabel("Time (s)")
        ax7.set_ylabel(
            "Acceleration" + " (" + self.tratamiento.unidades_aceleracion + ")"
        )
        ax7.set_title("Accelerogram")
        ax7.legend(fontsize=8)
        ax7.set_xlim(min(matriz_itiempo), max(matriz_itiempo))
        # Processed velocity
        ax8.plot(
            matriz_itiempo,
            velocidadfiltrada,
            color="royalblue",
            linewidth=0.7,
            label="Corrected Velocity",
        )
        ax8.set_xlabel("Time (s)")
        ax8.set_ylabel("Velocity (cm/s)")
        ax8.set_title("Velocity")
        ax8.legend(fontsize=8)
        ax8.set_xlim(min(matriz_itiempo), max(matriz_itiempo))
        # Processed displacement
        ax9.plot(
            matriz_itiempo,
            desplazamientofiltrada,
            color="dodgerblue",
            linewidth=0.7,
            label="Corrected Displacement",
        )
        ax9.set_xlabel("Time (s)")
        ax9.set_ylabel("Displacement (cm)")
        ax9.set_title("Displacement")
        ax9.legend(fontsize=8.5)
        ax9.set_xlim(min(matriz_itiempo), max(matriz_itiempo))
        plt.tight_layout()
        # GRAPHS OF FILTER GAIN
        # Filter gain graph for a high-pass 
        if self.tratamiento.type_filtro == "Highpass":
            w, h = sp.signal.freqz(bhigh, ahigh, worN=20000)
            fig, ax10 = plt.subplots(figsize=(12,6), dpi=300)
            ax10.plot ((fmuestreo * 0.5 / np.pi) * w, abs(h), color='royalblue')
            ax10.set_xlabel('Frequency (Hz)')
            ax10.set_ylabel('Gain')
            ax10.grid(False)
            ax10.set_title('Filter Gain')
            ax10.set_xlim(min((fmuestreo * 0.5 / np.pi) * w), max((fmuestreo * 0.5/np.pi)*w))
            plt.tight_layout()
        # Filter gain graph for a low-pass
        elif self.tratamiento.type_filtro == "Lowpass":
            w, h = sp.signal.freqz(blow, alow, worN=20000)
            fig, ax10 = plt.subplots(figsize=(12,6), dpi=300)
            ax10.plot ((fmuestreo * 0.5 / np.pi) * w, abs(h), color='royalblue')
            ax10.set_xlabel('Frequency (Hz)')
            ax10.set_ylabel('Gain')
            ax10.grid(False)
            ax10.set_title('Filter Gain')
            ax10.set_xlim(min((fmuestreo * 0.5 / np.pi) * w), max((fmuestreo * 0.5/np.pi)*w))
            plt.tight_layout()
        # Filter gain graph for a bandpass
        elif self.tratamiento.type_filtro == "Bandpass":
            w, h = sp.signal.freqz(b_bandpass, a_bandpass, worN=20000)
            fig, ax10 = plt.subplots(figsize=(12,6), dpi=300)
            ax10.plot ((fmuestreo * 0.5 / np.pi) * w, abs(h), color='royalblue')
            ax10.set_xlabel('Frequency (Hz)')
            ax10.set_ylabel('Gain')
            ax10.grid(False)
            ax10.set_title('Filter Gain')
            ax10.set_xlim(min((fmuestreo * 0.5 / np.pi) * w), max((fmuestreo * 0.5/np.pi)*w))
            plt.tight_layout()
        # When unfiltered
        elif self.tratamiento.type_filtro == "None":
            fig, ax10 = plt.subplots(figsize=(14.45, 6), dpi=300)
            ax10.set_xticks([])
            ax10.set_yticks([])
            ax10.set_xlabel('Frequency (Hz)')  
            ax10.set_ylabel('Gain') 
            ax10.set_title('Filter Gain')
            ax10.text(0.5, 0.5, 'This chart does not apply', horizontalalignment='center', verticalalignment='center', fontsize=16, transform=ax10.transAxes)
            # fig.canvas.manager.set_window_title("Figura 4")
            #plt.show()
        else:
            exit()

    # ARIA INTENSITY
        iaria = (np.pi / (2 * fescala_unidades)) * sp.integrate.cumtrapz(
            (np.square(fescala_unidades * aceleracionfiltrada)),
            matriz_itiempo,
            initial=0,
            dx=self.tratamiento.dt,
        )
        iaria_end = iaria[-1]
        iaria_porcentaje = 100 * iaria / iaria_end
        # TIME FOR 5% OF ENERGY RELEASED
        # The utilization of interpolation
        porcentaje_5 = 5
        indice1_5 = np.argmax(iaria_porcentaje >= porcentaje_5) - 1
        indice2_5 = np.argmax(iaria_porcentaje >= porcentaje_5)
        x1_5 = matriz_itiempo[indice1_5]
        x2_5 = matriz_itiempo[indice2_5]
        y1_5 = iaria_porcentaje[indice1_5]
        y2_5 = iaria_porcentaje[indice2_5]
        t_5 = x1_5 + ((porcentaje_5 - y1_5) * (x2_5 - x1_5)) / (y2_5 - y1_5)
        # TIME FOR 95% OF ENERGY RELEASED
        # The utilization of interpolation
        porcentaje_95 = 95
        indice1_95 = np.argmax(iaria_porcentaje >= porcentaje_95) - 1
        indice2_95 = np.argmax(iaria_porcentaje >= porcentaje_95)
        x1_95 = matriz_itiempo[indice1_95]
        x2_95 = matriz_itiempo[indice2_95]
        y1_95 = iaria_porcentaje[indice1_95]
        y2_95 = iaria_porcentaje[indice2_95]
        t_95 = x1_95 + ((porcentaje_95 - y1_95) * (x2_95 - x1_95)) / (y2_95 - y1_95)
        # SIGNIFICAN DURATION
        duracion_significativa = t_95 - t_5
        # Select time and Acceleration Vaues between 5% and 95% of Released Energy
        condicion_duracion = (iaria_porcentaje >= 5) & (iaria_porcentaje <= 95)
        t_duracion = matriz_itiempo[condicion_duracion]
        a_duracion = aceleracionfiltrada[condicion_duracion]
        iaria_duracion = iaria_porcentaje[condicion_duracion]
        # Graph of Arias Intensity
        fig, ax11 = plt.subplots(figsize=(12,6), dpi=300)
        ax11.plot(matriz_itiempo, iaria_porcentaje, color='skyblue')
        ax11.plot(t_duracion, iaria_duracion, label='Significant Duration', color='royalblue')
        ax11.axvline(x=t_5, color='gray', linestyle='--', label = f'Time 5% = {t_5:.3f}')
        ax11.axvline(x=t_95, color='black', linestyle='--', label = f'Time 95% = {t_95:.3f}')
        ax11.plot([], [], ' ', label=f'Dₛ (s) = {duracion_significativa:.2f}')
        ax11.set_xlabel('Time (s)')
        ax11.set_ylabel('Aria Intensity %')
        ax11.legend(fontsize=8.5)
        ax11.grid(False)
        ax11.set_title('Aria Intensity')
        ax11.set_xlim(min(matriz_itiempo), max(matriz_itiempo))
        plt.tight_layout()
        # PGA for Processed Seismic Record
        indice_max_acceleration = np.argmax(np.abs(aceleracionfiltrada))
        valor_a_max = aceleracionfiltrada[indice_max_acceleration]
        valor_t_for_a_max = matriz_itiempo[indice_max_acceleration]
        # Comparative graph between processed acceleration and acceleration for significant duration over time
        fig, ax12 = plt.subplots(figsize=(12,6), dpi=300)
        ax12.plot(matriz_itiempo, aceleracionfiltrada, label='Corrected Acceleration', color='skyblue',linewidth=0.7)
        ax12.plot(t_duracion, a_duracion, label='Acceleration for Significant Duration', color='royalblue',linewidth=0.7)
        ax12.axvline(x=valor_t_for_a_max, color='lightgray', linestyle='--')
        ax12.scatter(valor_t_for_a_max, valor_a_max, color='black', marker='o', facecolor='none', label=f'Max. Acceleracion = {valor_a_max:.2f}' + ' (' + self.tratamiento.unidades_aceleracion + ')')
        ax12.set_xlabel('Time (s)')
        ax12.set_ylabel('Acceleration' + ' (' + self.tratamiento.unidades_aceleracion + ')')
        ax12.legend(fontsize=8.5)
        ax12.grid(False)
        ax12.set_title('Corrected Acceleration and Acceleration for Significant Duration')
        ax12.set_xlim(min(matriz_itiempo), max(matriz_itiempo))
        plt.tight_layout()
    # APPLICATION OF FAST FOURIER TRANSFORM TO SEISMIC RECORD
        amplitud_fourier = np.fft.fft(aceleracionfiltrada)
        # Calculate the frequencies for the FFT
        frecuencias_fourier = np.fft.fftfreq(
            len(matriz_itiempo), self.tratamiento.dt
        )  
        # Select positive frquencies. The lower half of Spectrum
        frecuencias_positivas = frecuencias_fourier[: len(frecuencias_fourier) // 2]
        amplitud_positivo = np.abs(amplitud_fourier[: len(amplitud_fourier) // 2])
        # PROCEDURE TO ANALYZE THE FREQUENCY CONTENT OF A SEISMIC SIGNAL
        # Calculate the width of each frequency window
        Δf = (
            np.max(frecuencias_positivas) - np.min(frecuencias_positivas)
        ) / self.tratamiento.num_ventanas
        # Define the boundaries of the frequency windows
        intervalos = []
        for i in range(self.tratamiento.num_ventanas):
            limite_inferior = np.min(frecuencias_positivas) + i * Δf
            limite_superior = np.min(frecuencias_positivas) + (i + 1) * Δf
            intervalos.append((limite_inferior, limite_superior))
        resultados = []
        # Code for calculate the maximum amplitude and corresponding frequency
        for limite_inferior, limite_superior in intervalos:
            amplitudes_intervalo = []
            frecuencias_intervalo = []
            # Select the frequencies and amplitudes belonging to each interval
            for frecuencia, amplitud in zip(frecuencias_positivas, amplitud_positivo):
                if limite_inferior <= frecuencia <= limite_superior:
                    amplitudes_intervalo.append(amplitud)
                    frecuencias_intervalo.append(frecuencia)
            # Select the maximum amplitude and corresponding frequency
            if amplitudes_intervalo:
                indice_amplitud_maxima = amplitudes_intervalo.index(
                    max(amplitudes_intervalo)
                )
                frecuencia_amplitud_maxima = frecuencias_intervalo[
                    indice_amplitud_maxima
                ]
                amplitud_maxima = max(amplitudes_intervalo)
            else:
                frecuencia_amplitud_maxima = None
                amplitud_maxima = None
            # Add the results of the current interval analysis to the 'resultsados' list.
            resultados.append(
                (
                    limite_inferior,
                    limite_superior,
                    amplitud_maxima,
                    frecuencia_amplitud_maxima,
                )
            )
        amplitudes_maximas_maximas = np.zeros((self.tratamiento.num_ventanas, 1))
        frecuencia_amplitud_maxima_maximas = np.zeros(
            (self.tratamiento.num_ventanas, 1)
        )
        # Record the results in the arrays
        # Fill arrays with maximum amplitudes and corresponding frequencies obtained.
        for i, (
            limite_inferior,
            limite_superior,
            amplitud_maxima,
            frecuencia_amplitud_maxima,
        ) in enumerate(resultados):
            amplitudes_maximas_maximas[i] = amplitud_maxima.flatten()
            frecuencia_amplitud_maxima_maximas[i] = frecuencia_amplitud_maxima.flatten()

        amplitudes_maximas_maximas = amplitudes_maximas_maximas.flatten()
        frecuencia_amplitud_maxima_maximas = (
            frecuencia_amplitud_maxima_maximas.flatten()
        )
        # Calculate the cumulative percentage of the maximum amplitudes
        acum_amplitudesmax = (
            100 * amplitudes_maximas_maximas / np.sum(amplitudes_maximas_maximas)
        )
        frecuencias_90 = []
        energy_90 = []
        acumulado = 0
        for a, b in zip(frecuencia_amplitud_maxima_maximas,acum_amplitudesmax):
            acumulado += b
            frecuencias_90.append(a)
            energy_90.append(b)
            if acumulado >= 90:
                break
        
        
        # Plots
        hsize = 12
        fig, (ax13, ax14) = plt.subplots(2, 1, figsize=(12, hsize), dpi=300)
        fig.subplots_adjust(hspace=2.5)
        # Fourier Spectrum Plot
        ax13.plot(
            frecuencias_positivas,
            amplitud_positivo,
            color="royalblue",
            linewidth=0.9,
            label="Fourier Spectrum",
        )
        #ax13.set_xlim([np.log10(frecuencias_positivas[0]), np.log10(frecuencias_positivas[-1])])
        # Add vertical lines passing through the maximum amplitudes 
        # for each interval and their corresponding frequencies to the plot.
        for i, frecuencia in enumerate(frecuencia_amplitud_maxima_maximas):
            random_color = "gray"
            label_text = f"f{i+1} = {frecuencia:.2f} Hz"
            ax13.axvline(
                x=frecuencia, color=random_color, linestyle="--", label=label_text, linewidth=1,
            )#######################
        ax13.set_xlabel("Frecuency (Hz)")
        ax13.set_xscale("log")
        ax13.set_xlim([frecuencias_positivas.min(), frecuencias_positivas.max()])
        ax13.legend(fontsize=8.5)
        if self.tratamiento.unidades_aceleracion == 'g':
            ax13.set_ylabel('Amplitude')
        else:
            ax13.set_ylabel('Amplitude')
        ax13.set_yticks([])
        ax13.set_title("Fourier Spectrum")
        # Bar chart of the frequency content analysis of the seismic record
        x_histograma = np.arange(1, self.tratamiento.num_ventanas + 1)
        ax14.bar(
            x_histograma,
            acum_amplitudesmax,
            width=0.5,
            color="royalblue",
            label="Amplitude",
        )
        # Add the line dividing the frequencies containing 90% 
        # of the seismic energy released
        x_90_i = len(frecuencias_90)
        x_90_j = len(frecuencias_90)+1
        x_90_prom = (x_90_i+x_90_j)/2
        
        ax14.bar(
            x_histograma,
            frecuencia_amplitud_maxima_maximas,
            bottom=acum_amplitudesmax,
            width=0.5,
            color="skyblue",
            label="Frequency (Hz)",
        )
        for i, frecuencia in enumerate(frecuencia_amplitud_maxima_maximas):
            ax14.text(
                x_histograma[i],
                acum_amplitudesmax[i] + frecuencia + 1,
                f"{frecuencia:.2f} Hz",
                ha="center",
                va="bottom",
                fontsize=9,
                color="black",
            )
        ax14.axvline(x_90_prom, color='lightgray', linestyle='--', linewidth=1)
        max_sum_comb = float(max([acum + freq for acum, freq in zip(acum_amplitudesmax, frecuencia_amplitud_maxima_maximas)]))
        ax14.set_ylim(0, max_sum_comb*1.25)
        y_lim_graph = ax14.get_ylim()
        y_text = y_lim_graph[0] + 0.70 * (y_lim_graph[1] - y_lim_graph[0])
        ax14.text(x_90_prom, y_text, "Energy/Pulse >= 90%", rotation=90, va='bottom', ha='right', color='black',fontsize=8)
        ax14.set_xlabel("Windows")
        ax14.set_ylabel("% Percentage")
        ax14.set_title("Frequency and Amplitude Variation")
        ax14.set_xticks(x_histograma)
        ax14.legend(fontsize=8.5)
        plt.tight_layout()
        
        # Calculate the maximum length
        maxima_longitud = max(
                len(frecuencias_positivas),
                len(aceleracionoriginal),
                len(aceleracionfiltrada),
                len(velocidadfiltrada),
                len(desplazamientofiltrada),
                len(iaria_porcentaje),
                len(a_duracion),
                len(amplitud_positivo),
                len(amplitudes_maximas_maximas),
                len(frecuencia_amplitud_maxima_maximas),
                len(matriz_itiempo),
            )
        
        # Function to pad lists with NaN until they reach the maximum length
        def llenado(listas, longi, llena=np.nan):
            return np.concatenate([listas, [llena] * (longi - len(listas))])

        # Pad lists with NaN to equalize their lengths
        tiempo_reporte = llenado(matriz_itiempo, maxima_longitud)
        frecuencias_positivas_reporte = llenado(frecuencias_positivas, maxima_longitud)
        aceleracion_original_reporte = llenado(aceleracionoriginal, maxima_longitud)
        aceleracion_filtrada_reporte = llenado(aceleracionfiltrada, maxima_longitud)
        velocidad_filtrada_reporte = llenado(velocidadfiltrada, maxima_longitud)
        desplazamiento_filtrada_reporte = llenado(desplazamientofiltrada, maxima_longitud)
        iaria_porcentaje_reporte = llenado(iaria_porcentaje, maxima_longitud)
        a_duracion_reporte = llenado(a_duracion, maxima_longitud)
        amplitud_positivo_reporte = llenado(amplitud_positivo, maxima_longitud)
        amplitudes_maximas_maximas_reporte = llenado(
            amplitudes_maximas_maximas, maxima_longitud
        )
        frecuencia_amplitud_maxima_maximas_reporte = llenado(
            frecuencia_amplitud_maxima_maximas, maxima_longitud
        )
        acum_amplitudesmax_reporte = llenado(acum_amplitudesmax, maxima_longitud)
        frecuencias_90_reporte = llenado(frecuencias_90, maxima_longitud)
        # Create the DataFrame from the lists
        lista_exportar = pd.DataFrame(
            {
            "Time [s]": tiempo_reporte,
            "Original Acceleration ("
            + self.tratamiento.unidades_aceleracion
            + ")": aceleracion_original_reporte,
            "Corrected Acceleration ("
            + self.tratamiento.unidades_aceleracion
            + ")": aceleracion_filtrada_reporte,
            "Corrected Velocity (cm/s)": velocidad_filtrada_reporte,
            "Corrected Displacement (cm)": desplazamiento_filtrada_reporte,
            "Aria Intensity %": iaria_porcentaje_reporte,
            "Acceleration for Significant Duration ("
            + self.tratamiento.unidades_aceleracion
            + ")": a_duracion_reporte,
            "Frequency [Hz]": frecuencias_positivas_reporte,
            "Fourier Amplitudes": amplitud_positivo_reporte,
            "Maximum Amplitudes": amplitudes_maximas_maximas_reporte,
            "Predominant Frequencies [Hz]": frecuencia_amplitud_maxima_maximas_reporte,
            "Energy/Pulse [%]": acum_amplitudesmax_reporte,
            "Frequencies for accumulated Energy/Pulse >=90 [Hz]": frecuencias_90_reporte,
            }
        )
        # guardar el DataFrame en un archivo Excel
        # nombre_informe =  + '_report.xlsx'
        # Exporting 'lista_exportar' dataframe to an Excel file specified by 'self.datos_informe',
        # with the sheet name 'Seismic Record Report' and without including the index.
        lista_exportar.to_excel(self.datos_informe, sheet_name='Seismic Record Report', index=False)
        # Load the workbook and select the sheet
        print(frecuencias_90)
        print(energy_90)
        # Assigning the value of 'frecuencias_90' to 'self.tratamiento.fregistros_90'.
        self.tratamiento.fregistros_90 = frecuencias_90
        self.tratamiento.energy_90 = energy_90
        # Calling the 'saveImages' method with the 'plt' object.
        self.saveImages(plt)
        # Calling the 'RenderFiles' method.
        self.RenderFiles()
        # Assigning the value of 'self.numImages' to 'self.tratamiento.numImages'.
        self.tratamiento.numImages = self.numImages

    def RenderFiles(self):
        # Define HTML tag for page break
        # This is used to force a page break when rendering to PDF.
        salto_linea = (
            '<div style = "display:block; clear:both; page-break-after:always;"></div>'
        )
        # Append filename header to HTML output
        self.salidaHtml.append(
            f"<h3 style='font-size:18px'>Filename: {self.tratamiento.filebasename}</h3><hr>"
        )
        # Open HTML div tag
        self.salidaHtml.append('<div>')
        # Loop through each image to render in HTML
        # Iterates through each image specified by self.numImages.
        for i in range(self.numImages): 
            # Skips the first image (assuming images are indexed starting from 1).
            if i != 0:
                # Append image label
                # tag for each image, specifying the path 
                self.salidaHtml.append(f"<center><h3>{image_etiquetas[i-1]}</h3></center>")
                # Append image tag with path and styling
                self.salidaHtml.append(
                    f"<img src='images/{self.tratamiento.filebasename}/{i}.png' style=\"margin-bottom: 20px; border: 2px solid #000000; padding: 10px;\" width='100%'>"
                )
               
        # Close HTML div tag       
        self.salidaHtml.append("</div>")
        # Join HTML list into a single string
        # Joins all elements in the self.salidaHtml list into a single string (self.htmlText).
        self.htmlText = " ".join(self.salidaHtml)
        # Append filename header to temporal HTML output
        self.salidaTemporalHtml.append(
            f"<h3 style='font-size:18px'>Filename: {self.tratamiento.filebasename}</h3><hr>"
        )
        # Loop through each image to render in temporal HTML
        # Iterates through each image specified by self.numImages.
        for i in range(self.numImages):
            if i != 0:
                # self.salidaTemporalHtml.append(f"<img src='file://{self.proyectPath}/results/html/images/{self.tratamiento.filebasename}/{i}.png' width='100%'><hr>")
                # Open the images of the treatment performed in this file to the seismic records in binary format to read them
                with open(
                    f"{self.proyectPath}/results/html/images/{self.tratamiento.filebasename}/{i}.png",
                    "rb",
                ) as image_file:
                    # Read the image data
                    image_data = image_file.read()
                # Add page break for specific images
                if i == 3 or i == 5 or i == 7:
                    self.salidaTemporalHtml.append(salto_linea)
                # Append image label
                self.salidaTemporalHtml.append(f"<center><h3>{image_etiquetas[i-1]}</h3></center>")
                # Convert image data to Base64 string and append to temporal HTML output
                image_base64 = base64.b64encode(image_data).decode("utf-8")
                self.salidaTemporalHtml.append(
                    f'<img src="data:image/png;base64,{image_base64}" width="100%">'
                )
        # Join temporal HTML list into a single string
        self.temporalhtmlText = " ".join(self.salidaTemporalHtml)

        # Write HTML content to file
        # Save the string in the text file
        with open(self.archivo_html, "w", encoding="utf-8") as archivo:
            archivo.write(
                f"<html><head><title>Análisis {self.tratamiento.filebasename}</title></head><body style=\"padding:20px\">"
            )
            archivo.write(self.htmlText)
            archivo.write("</body></html>")
        # Convert HTML temporal content to file
        with open(self.archivo_temporal_html, "w", encoding="utf-8") as archivo:
            archivo.write(
                f"<html><head><title>Análisis {self.tratamiento.filebasename}</title></head><body>"
            )
            archivo.write(self.temporalhtmlText)
            archivo.write("</body></html>")

        # Configure PDFKit options
        opciones = {
            "page-size": "A4",
            "margin-top": "30mm",
            "margin-right": "30mm",
            "margin-bottom": "30mm",
            "margin-left": "30mm",
        }
        try:
            # Convert temporal HTML to PDF
            pdfkit.from_file(
                self.archivo_temporal_html, self.archivo_pdf, options=opciones
            )
            print(f"Archivo PDF guardado en: {self.archivo_pdf}")
        except Exception as e:
            # Displays an error message when converting to pdf to notify the user
            print(f"Error al convertir a PDF: {str(e)}")
    def getEtiquetaFourier(self):
        # Return Fourier amplitude label based on units of acceleration
        if self.tratamiento.unidades_aceleracion == "g":
            return "Fourier Amplitudes"
        else:    
            return "Fourier Amplitudes cm/s^2"            

    def getMaximumAmplitude(self):
        # Return maximum amplitude label based on units of acceleration
        if self.tratamiento.unidades_aceleracion == "g":
            return "Maximum Amplitude"
        else:    
            return "Maximum Amplitude cm/s^2"

    def contadorLineas(self, archivo):
        # Initialize the maximum number of lines to zero
        max_lines = 0

        # Open the file and count the lines
        with open(archivo, "r") as file:
            for line in file:
                max_lines += 1
        return max_lines

    def getDataFromFile(
        self, ruta_registro, filas_inutiles, delimiter=None, invalid_raise=False
    ):
        # Load data from file with options
        datosregistro = np.genfromtxt(
            ruta_registro,
            skip_header=filas_inutiles,
            delimiter=delimiter,
            invalid_raise=invalid_raise,
            skip_footer=1,
        )
        # Reshape data for processing
        datosregistro = datosregistro.reshape(-1, 1).flatten()
        # Get data from the last row of the file for further processing
        datosregistroLastRow = np.genfromtxt(
            ruta_registro,
            skip_header=self.contadorLineas(ruta_registro) - 1,
            delimiter=delimiter,
            invalid_raise=invalid_raise,
        )
        datosregistroLastRow = datosregistroLastRow.reshape(-1, 1).flatten()
        # Concatenate both arrays for final processing
        return np.concatenate((datosregistro, datosregistroLastRow), axis=0)
