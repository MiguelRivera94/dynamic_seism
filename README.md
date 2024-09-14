# Software Dynamic Seism

<p align="center">
    <img src="./resources/icons/iconapp.ico" alt="Icono del Software" width="500" height="500">
</p>

## Description

Interactive Software for Dynamic Magnification Calculation of Single Degree of Freedom Structures in the Elastic and Inelastic Range Based on the Predominant Frequency Content of Seismic Records.

## Functionalities

- Process Multiple Seismic Records (Baseline Correction and Filtering of Multiple Seismic Records).
- Plot time series of acceleration, velocity, and displacement from original and processed data.
- Plot the filter gain applied to the seismic record.
- Plot Arias intensity and calculate the significant duration of the seismic record.
- Comparative plot of seismic record acceleration vs. acceleration corresponding to significant duration.
- Plot the Fourier spectrum.
- Plot the frequency content analysis of the seismic record.
- Calculate dynamic magnification.
- Plot dynamic magnification curves.
- Generate bar charts that relate the seismic event energy, frequencies, and dynamic magnification calculated for the elastic and inelastic ranges when at least 11 seismic records are loaded into the software.
- Generates charts that overlay the probability density functions (PDFs) of frequencies and dynamic magnifications, along with grouped histograms for different damping values. Each chart includes means, standard deviations, and probabilities corresponding to the 16th, 50th, and 84th percentiles. This function is activated only after at least 11 seismic records have been loaded into the software.
- Generate reports in PDF format with all graphs.
- Generate reports in Excel.

<!--
## Installation Requirements

The software requires the following:
- Operating System: Windows 10 or higher.
- Recommended Processor: Intel Core i7.
- Available Disk Space: 530 MB.
- Recommended Screen Resolution: 1920x1080 pixels.
- Installation of External Tools: wkhtmltopdf.
-->

## Installer

Download the software installer by clicking on the following image:

<p align="center">
  <a href="https://puceeduec-my.sharepoint.com/:u:/g/personal/meriverabo_puce_edu_ec/EX8Twoe_aGpIqtDKmPnoF6MBTavRt1THmwoqVWpqfrq4Bg?download=1">
    <img src="./visual/download_dynamic_seism.png" alt="Descargar Dynamic Seism" />
  </a>
</p>


<!--
https://puceeduec-my.sharepoint.com/:u:/g/personal/meriverabo_puce_edu_ec/EX8Twoe_aGpIqtDKmPnoF6MBTavRt1THmwoqVWpqfrq4Bg?download=1
-->


## How Install and Configurate the External Tool wkhtmltopdf?
- Download the wkhtmltopdf tool from the link provided in the table below

<p align="center">
    <img src="./visual/wkhtml_image.png" alt="Administradorwkhtmltopdf" alt="Icono del Software" width="457.5" height="225">
</p>

<div align="center">

| Name                  | Description                                                                                   | Website                                                      |
|-----------------------|-----------------------------------------------------------------------------------------------|---------------------------------------------------------------|
| wkhtmltopdf           | Convert the files from HTML format to PDF                                                      | [https://wkhtmltopdf.org/index.html](https://wkhtmltopdf.org/index.html) |

</div>

- Run the wkhtmltopdf tool as an administrator and install it

<p align="center">
  <img src="./visual/Ejecutar_como_administrador_wkhtmltopdf.png" alt="Administradorwkhtmltopdf" />
</p>

- Read and accept the license agreement, then click 'I Agree'

<p align="center">
  <img src="./visual/Acuerdo_de_Licencia_de_la_herramienta_wkhtmltopdf.png" alt="Acuerdowkhtmltopdf" />
</p>

- Choose an installation path, then click "Install"

<p align="center">
<img src="./visual/ruta_de_instalacion_de_la_herramienta_wkhtmltopdf.png" alt="Eutawkhtmpltopdf" />
</p>

- Once the installation is complete, click 'Close'
<p align="center">
<img src="./visual/finalizacion_de_la_instalacion.png" alt="Finalizacionwkhtmltopdf" />
</p>


- Copy the path of the "bin" folder located within the wkhtmltopdf installation directory, which by default is "C:\Program Files\wkhtmltopdf\bin"

<p align="center">
<img src="./visual/ruta_de_la_carpeta_bin.png" alt="copiarrutabinwkhtmltopdf" />
</p>




- Open the Environment Variables editor. Press Windows + S, then search for "Edit the System Environment Variables" and open it
<p align="center">
<img src="./visual/abrir_editar_variables_de_entorno.png" alt="copiarrutabinwkhtmltopdf" />
</p>

- Clic on "Environment Variables"
  
<p align="center">
<img src="./visual/clic_en_environment_variables.png" alt="copiarrutabinwkhtmltopdf" />
</p>

- Edit the Path variable, either for system variables or for a specific user.
<p align="center">
<img src="./visual/edit_variable_path.png" alt="copiarrutabinwkhtmltopdf" />
</p>


- Clic on "New"
<p align="center">
<img src="./visual/Clic_on_new.png" alt="copiarrutabinwkhtmltopdf" />
</p>


- Paste the path of the "bin" folder. If the path is set to the default, it will be: "C:\Program Files\wkhtmltopdf\bin". Then click "Ok" on all subsequent windows to apply the changes.
<p align="center">
<img src="./visual/paste_binpath.png" alt="copiarrutabinwkhtmltopdf" />
</p>

## Installation Steps for Dynamic Seism:

- Install and configure the tool wkhtmltopdf. This step has been explained previously and it is recommended to review the section **"How to Install and Configure the External Tool wkhtmltopdf?"**


- Run the Dynamic Seism software as an administrator
<p align="center">
<img src="./visual/run_as_administrator_dynamicseism.png" alt="copiarrutabinwkhtmltopdf" />
</p>

- Select the installation folder path for the software and click on Next

<p align="center">
<img src="./visual/select_path_installation_dynamicseism.png" alt="copiarrutabinwkhtmltopdf" />
</p>

- Check the option labeled "Create a desktop shortcut" then click Next.

<p align="center">
<img src="./visual/create_icon_deskop_dynamicseism.png" alt="copiarrutabinwkhtmltopdf" />
</p>

- Verify that the installation path is correct and that an icon is created on the desktop, then click Next.
  
<p align="center">
<img src="./visual/Clic_Install_dynamicseism.png" alt="copiarrutabinwkhtmltopdf" />
</p>

- Wait while the installation proceeds

<p align="center">
<img src="./visual/wait_for_installation_dynamicseism.png" alt="copiarrutabinwkhtmltopdf" />
</p>

- A window will appear notifying you that the software has been installed. Then, click on Finish

<p align="center">
<img src="./visual/Notification_installation_end_dynamicseism.png" alt="copiarrutabinwkhtmltopdf" />
</p>

## Main Windows

<p align="center">
<img src="./visual/principal_main_and_presentation.png" alt="copiarrutabinwkhtmltopdf" />
</p>


## How to Create a New Project?

- Click on the File menu

<p align="center">
<img src="./visual/How_Create_a_New_Project/1clic_on_file.png" alt="copiarrutabinwkhtmltopdf" />
</p>

- Click on New
<p align="center">
<img src="./visual/How_Create_a_New_Project/2clic_on_new.png" alt="copiarrutabinwkhtmltopdf" />
</p>

- Select the folder that will host the new project
<p align="center">
<img src="./visual/How_Create_a_New_Project/3select_newproject_folder.png" alt="copiarrutabinwkhtmltopdf" />
</p>

- Assign a name to the project
<p align="center">
<img src="./visual/How_Create_a_New_Project/4write_name_project.png" alt="copiarrutabinwkhtmltopdf" />
</p>

## How to load, process, and analyze the frequency content of the project's seismic records?
It is important to note that before loading the records, a new project must be created. To do this, refer to the section **"How to Create a New Project?"**

The steps to load seismic records into a project, process them by correcting the baseline or applying filters, and analyze their frequency content are as follows:

- Clic on "Load Seismic Records"

<p align="center">
<img src="./visual/How_load_process_analyze_sr/1clic_on_load_seismic_record_2.png" alt="copiarrutabinwkhtmltopdf" />
</p>

- Clic on "Select Files"

<p align="center">
<img src="./visual/How_load_process_analyze_sr/2clic_on_select_files.png" alt="copiarrutabinwkhtmltopdf" />
</p>

- Select the seismic project's seismic records
Select the project's seismic records. Keep in mind that you can choose both .txt and .AT2 files. To select .txt files, check the "text files" option, and for .AT2 files, check the "information files" option. A project in the software can include seismic records in both formats.

<p align="center">
<img src="./visual/How_load_process_analyze_sr/3select_seismic_records.png" alt="copiarrutabinwkhtmltopdf" />
</p>


- Enter the data to process and analyze the frequency content of the seismic records.
  
The data to be entered for analyzing and processing the seismic records are as follows:

**Data Presentation:** Seismic records can commonly be presented in three types: Simple Column, Multiple Column, and Time Acceleration.

**Useless Rows:** Seismic records often contain information that should be ignored to focus on acceleration data. Useless rows refer to those that the software should omit to capture the acceleration data in the seismic record. The user should enter a natural number for this.

**Acceleration Units:** Refers to the units in which accelerations are expressed in the seismic record. The user has the option to work in two units: fraction of gravity (g) and centimeters per second squared (cm/s²).

**Conversion Factor:** This factor allows the user to convert the acceleration units in the seismic record and to scale the seismic record. The user can enter a decimal number.

**Time Interval Between Acceleration Measurements (Dt):** Typically, the first lines of text in the seismic record contain information on the time interval between each acceleration measurement. The user should enter this data after reviewing these informational lines. A positive decimal number is allowed.

**Baseline Correction:** The user has the option to correct the baseline to remove a trend in the seismic record. The user can choose between Yes or No.

**Baseline Correction Polynomial Degree:** The user must enter the degree of polynomial regression for baseline correction in the seismic record. The user should enter a natural number.

**Filter Type:** Filters are applied to remove noise from the seismic record. The software uses a Butterworth filter, offering the user three options: Highpass, Lowpass, and Bandpass. There is also an option for "None" to apply no filter to the seismic record.

**Cutoff Frequency 1 and 2:** Cutoff Frequency 1 refers to the minimum frequency allowed through in the case of a bandpass filter, while Cutoff Frequency 2 represents the maximum frequency allowed with minimal attenuation. These two frequencies define a range of interest in the signal. Decimal numbers are allowed.

**Filter Order:** Refers to how quickly the filter attenuates frequencies outside a passband. The software only allows the entry of a natural number for this data entry.

**Number of Windows:** The number of windows in which the Fourier Spectrum is divided helps identify the most representative frequencies of the seismic record, which assists in determining which frequencies contain 90% of the earthquake's energy. The user should enter a natural number.

**For example 1:**

<p align="center">
<img src="./visual/How_load_process_analyze_sr/5Enter_the_data_to_process_and_analyze_the_frequency_content_of the_seismic_records_2.png" alt="copiarrutabinwkhtmltopdf" />
</p>

Once the data is entered, click on Apply

**For example 2:**

<p align="center">
<img src="./visual/How_load_process_analyze_sr/6Enter_the_data_to_process_and_analyze_the_frequency_content_of the_seismic_records.png" alt="copiarrutabinwkhtmltopdf" />
</p>



Once the data is entered, click on Apply



- After entering the data for all seismic records in the project, click OK.

<p align="center">
<img src="./visual/How_load_process_analyze_sr/7_clic_on_ok.png" alt="copiarrutabinwkhtmltopdf" />
</p>

- Wait for the software to display a window with the message: "File processing has finished," and then click OK.

<p align="center">
<img src="./visual/How_load_process_analyze_sr/8_process_analyze_results_view.png" alt="copiarrutabinwkhtmltopdf" />
</p>

- To view the corresponding results, click on the tab "Seismic Record Processing and Signal Frequency Content Charts".

<p align="center">
<img src="./visual/How_load_process_analyze_sr/pestana_seismicrecordprocessing.png" alt="copiarrutabinwkhtmltopdf" />
</p>

- Click on the names of the records listed on the left side. With the corresponding tab active, their results will be displayed

<p align="center">
<img src="./visual/How_load_process_analyze_sr/finally_first results.png" alt="copiarrutabinwkhtmltopdf" />
</p>

## How to Calculate Dynamic Magnification?

A project must be created in the software, as outlined in the section: **How to Create a New Project?.**
Additionally, seismic records must be processed and their frequency content analyzed, as detailed in the section: **How to load, process, and analyze the frequency content of the project's seismic records?.**
Next, follow these steps:


- Click on "Calculate Dynamic Magnification"

<p align="center">
<img src="./visual/How_calculate_dynamic_magnification/01_clic_on_calculate_dynamic_magnification.png" alt="copiarrutabinwkhtmltopdf" />
</p>


- Click on "Calculate Dynamic Magnification"

<p align="center">
<img src="./visual/How_calculate_dynamic_magnification/02_empty_windows.png" alt="copiarrutabinwkhtmltopdf" />
</p>

- Enter the data for calculating dynamic amplification.

Note the following:

**Initial and Final Damping Coefficients (Zeta 1 and Zeta 2):** The software allows plotting dynamic amplification curves for various damping values. The initial damping (Zeta 1) sets the lower limit, while the final damping (Zeta 2) defines the upper limit of a range of values.

**Damping Coefficient Variation (Delta Zeta):** The user must specify an increment in the damping values to create a sequence of values, gradually ranging from the initial to the final damping.

**Period:** This refers to the period of the structure and is used to calculate dynamic amplification values based on the predominant frequency content of the seismic records and the range of damping values entered by the user.

For Example:
<p align="center">
<img src="./visual/How_calculate_dynamic_magnification/03_entrythedata_dynmagn.png" alt="copiarrutabinwkhtmltopdf" />
</p>
Once the data has been entered, click OK

- Wait until a window appears with the message: "File processing has finished," and then click OK.

<p align="center">
<img src="./visual/How_calculate_dynamic_magnification/04_message_dynmagn.png" alt="copiarrutabinwkhtmltopdf" />
</p>

- Click on the tab "Dynamic Magnification Charts" to view the charts

<p align="center">
<img src="./visual/How_calculate_dynamic_magnification/05_dynmagn_charts.png" alt="copiarrutabinwkhtmltopdf" />
</p>

- Click on the names of the records listed on the left side. With the corresponding tab active, the dynamic amplification results will be displayed.

<p align="center">
<img src="./visual/How_calculate_dynamic_magnification/06_finally_dynmagn.png" alt="copiarrutabinwkhtmltopdf" />
</p>

## What Files and Folders Make Up a Project?

A project consists of two folders named file and results, and another file called _sismoanalyticsproject with the extension .sisproj. The file folder contains the seismic records loaded into the project.

<p align="center">
<img src="./visual/poject_content/1_all_files_project.png" alt="copiarrutabinwkhtmltopdf" />
</p>

The file folder contains the seismic records loaded into the project.

<p align="center">
<img src="./visual/poject_content/2_files_folder.png" alt="copiarrutabinwkhtmltopdf" />
</p>

The results folder contains three subfolders named html, pdf, and xlsx. The html subfolder also contains a folder called images, where the images displayed in the graphical interface are stored, along with all the HTML files generated by the software. The pdf folder contains the results in PDF format as a report. Lastly, the xlsx folder contains the results obtained in the software.

<p align="center">
<img src="./visual/poject_content/3_results_folder.png" alt="copiarrutabinwkhtmltopdf" />
</p>

The .sisproj file contains all the necessary information to reopen a project in the software. This file includes all the data entered by the user and the files loaded into the project.
## How to Open an Existing Project?

- Click on Open in the File menu

<p align="center">
<img src="./visual/How to Open an Existing Project/1_clic_on_open.png" alt="copiarrutabinwkhtmltopdf" />
</p>

- Navigate to the folder path containing an existing project and open the "_sismoanalyticsproject.sisproj"" file

<p align="center">
<img src="./visual/How to Open an Existing Project/2_open_file_sisproj.png" alt="copiarrutabinwkhtmltopdf" />
</p>



## How to Review the Reports and Results of a Project in the Software?

Locate the folder containing a project developed with the software and open the results subfolder. There, you will find:

- Reports with charts in PDF format

<p align="center">
<img src="./visual/View_Results/1_pdf_results.png" alt="copiarrutabinwkhtmltopdf" />
</p>

- Reports of the results in XLSX format

<p align="center">
<img src="./visual/View_Results/02xlsx_results.png" alt="copiarrutabinwkhtmltopdf" />
</p>

- All the images displayed in the graphical interface

<p align="center">
<img src="./visual/View_Results/3_all_images.png" alt="copiarrutabinwkhtmltopdf" />
</p>

## Charts Displayed in the Software

- Original Record for: Acceleration, Velocity and Displacement

<p align="center">
<img src="./visual/Charts_Displayed_in_the_Software/1_original_acceleration_velocity_displacement.png" alt="copiarrutabinwkhtmltopdf" />
</p>


- Comparison of Original and Corrected Records for: Acceleration, Velocity, and Displacement

<p align="center">
<img src="./visual/Charts_Displayed_in_the_Software/2_comparisson_original_and_corrected_acceleration_velocity_displacement.png" alt="copiarrutabinwkhtmltopdf" />
</p>

- Corrected Record for: acceleration, velocity, and displacement

<p align="center">
<img src="./visual/Charts_Displayed_in_the_Software/03_corrected_acceleration.png" alt="copiarrutabinwkhtmltopdf" />
</p>


- Filter Gain

<p align="center">
<img src="./visual/Charts_Displayed_in_the_Software/04_Filter_Gain.png" alt="copiarrutabinwkhtmltopdf" />
</p>


- Arias Intensity

<p align="center">
<img src="./visual/Charts_Displayed_in_the_Software/05_AriaIntensity.png" alt="copiarrutabinwkhtmltopdf" />
</p>


- Comparison between corrected acceleration and acceleration for the significant duration

<p align="center">
<img src="./visual/Charts_Displayed_in_the_Software/06_Correctedacceleration_vs_accelerationforsignificantduration.png" alt="copiarrutabinwkhtmltopdf" />
</p>

- Fourier Spectrum and Frequency Content Analysis of the Entire Corrected Seismic Record

<p align="center">
<img src="./visual/Charts_Displayed_in_the_Software/07_Fourier_Spectrum.png" alt="copiarrutabinwkhtmltopdf" />
</p>

<p align="center">
<img src="./visual/Charts_Displayed_in_the_Software/08_Frequency_Content_Analysis.png" alt="copiarrutabinwkhtmltopdf" />
</p>


- Dynamic Magnification Curves

<img src="./visual/Charts_Displayed_in_the_Software/09_Dynamic_Magnification_Curves.png" alt="copiarrutabinwkhtmltopdf" />
</p>

## User Manual

You can download the User Manual by clicking on the following link:

- [Download the User Manual]()

## Video for Installation

You can view and download the software installation video at the following link:
[Video](https://drive.google.com/file/d/1CZogRnWWqlSv9tIE6zEUN0bcUSwRPpmZ/view?usp=drive_link)


