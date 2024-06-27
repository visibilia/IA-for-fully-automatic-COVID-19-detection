FADCIL: Fully Automatic Detection of Covid-19 cases in medical Images of the Lung
===============================================================================
.. figure:: ./images/fadcil_logo.png
   :alt: FADCIL official Logo. A product of Visibilia Ltda
   :align: center
   :width: 380px
   :height: 220px


Copyright (C) 2020-2024 `Visibilia`_

Welcome to the repository for **FADCIL** (Fully Automatic Detection of Covid-19 cases in medical Images of the Lung), a cutting-edge deep learning framework designed for the automatic detection of COVID-19 from chest CT scans. By integrating state-of-the-art architectures like **YOLOv4** and **3D U-Net**, FADCIL excels in accurately identifying and quantifying lung lesions caused by COVID-19, distinguishing them from other pulmonary diseases. This repository provides the source code and other materials for FADCIL as follows:

1. `Summary <#summary>`_
2. `Introduction <#introduction>`_
3. `System Overview <#system-overview>`_ 
4. `Performance Analysis <#performance-analysis>`_
5. `Running the Code <#running-the-code>`_
6. `Awards <#awards>`_
7. `Videos <#videos>`_
8. `Media Appearances <#media-appearances>`_
9. `Caution <#caution>`_
10. `Commercial Version <#commercial-version>`_
11. `Citation <#citation>`_


Summary
=========

The Coronavirus disease 2019 (COVID-19) pandemic has presented unprecedented challenges to global healthcare systems, urgently calling for innovative diagnostic solutions. This repository introduces the source code and other supplementary materials of **FADCIL** system, a cutting-edge deep learning framework designed for rapid and accurate COVID-19 diagnosis from chest computed tomography (CT) images. By leveraging an architecture based on **YOLO** and **3D U-Net**, FADCIL excels in identifying and quantifying lung injuries attributable to COVID-19, distinguishing them from other pathologies. In the real-world clinical environment of The Hospital das Clínicas de São Paulo (`HCFMUSP`_), Brazil, FADCIL achieved a DICE coefficient above 0.82. FADCIL also enhances the reliability of COVID-19 assessment, empowering healthcare professionals to make informed decisions and effectively manage patient care. Thus, this repository outlines the FADCIL source code, materials and presents an in-depth analysis of quantitative and qualitative evaluation results.



Introduction
============
The novel Coronavirus, SARS-CoV-2, emerged in late 2019, leading to a global pandemic with significant morbidity, mortality, and socioeconomic disruption. The virus's high contagion and severe respiratory effects posed major challenges to public health, requiring urgent responses from governments, healthcare institutions, and scientists. While RT-PCR tests are crucial for COVID-19 diagnosis, their reliability can vary. As a result, medical imaging, particularly chest CT scans, became a vital tool for COVID-19 detection due to their high sensitivity of up to 95%. This led to the integration of AI techniques for accurate and automated analysis of medical images. Deep learning, especially CNN-based models, has been highly effective in analyzing CT scans. However, models like YOLO and 3D U-Net have been less explored. 

At the beginning of the pandemic in Brazil, in April 2020, the São Paulo government and HCFMUSP launched a challenge to identify the best AI tool for diagnosing COVID-19 from medical images. The FADCIL system emerged as the leading solution, excelling in diagnosing COVID-19 from CT scans. FADCIL combines YOLOv4 and 3D U-Net architectures, enhanced through transfer learning, achieving competitive results. FADCIL performs precise lung segmentation and identifies COVID-19 lesions at various stages, distinguishing them from other conditions, mapping lesion locations, and quantifying lung impairment.

To ensure efficient cloud functioning, FADCIL uses a processing queue system and GPUs to minimize bottlenecks during real-time CT scan processing. Its exceptional performance and support to HCFMUSP’s medical teams during the pandemic gained significant attention and became the subject of an international case study.




System Overview
===============

FADCIL operates on the coronal, sagittal, and axial planes of patient data obtained from CT scans in  DICOM, NII, and NIfTI formats. FADCIL is structured into four main modules:  Preprocessing, Prediction, User Interface, and Feedback. The integration of these modules is illustrated in the following figure.

.. figure:: ./images/fadcil-modular-architecture-visibilia.png
   :alt: Basic modular architecture of FADCIL
   :align: center




**Preprocessing Module**

This module directly handles CT scans,  preparing them for inference using deep learning models.  To accommodate potential format variations in the voxel spacing of CT scans, this module begins by compressing all inputs to the NIfTI format. Then, scans and reference masks are resampled to 0.75 x 0.75 x 0.8 mm resolution using cubic and nearest neighbor interpolation, respectively. This process is shown in the following figure.

.. figure:: ./images/yolo-3dunet-integration-fadcil-1.PNG
   :alt: YOLOv4 and 3D U-net integration at FADCIL: resampling at uniform resolution
   :align: center




From the uniform resolution, two new images are resampled: low resolution images with $3.0 x 3.0 x 3.2 mm and medium resolution images with 1.5 x 1.5 x 1.6 mmas 

.. figure:: ./images/yolo-3dunet-integration-fadcil-2.PNG
   :alt: YOLOv4 and 3D U-net integration at FADCIL: resampling from the uniform resolution to low and medium resolution.
   :align: center




**Prediction Module**

This module combines YOLOv4 and 3D U-Net models to improve the accuracy of COVID-19 detection. Resampled images with low resolution are processed by 3D U-Net. If 3D U-Net identifies large lesions characteristic of COVID-19, the diagnosis is confirmed. For cases involving smaller lesions or uncertain, the final diagnosis is determined by processing images at medium resolution. This process is shown in the following figure.


.. figure:: ./images/yolo-3dunet-integration-fadcil-3.PNG
   :alt: YOLOv4 and 3D U-net integration at FADCIL: 3D U-net processing CT scans at low resolution as part of FADCIL prediction module
   :align: center


YOLO version 4 (YOLOv4) processes CT scans at medium resolution, focusing on work on identify the presence of the virus in small lesions or confirm the absence when there are no injuries. It is shown in the following figure.


.. figure:: ./images/yolo-3dunet-integration-fadcil-4.PNG
   :alt: YOLOv4 and 3D U-net integration at FADCIL: YOLOv4 processing CT scans at medium resolution as part of FADCIL prediction module
   :align: center


COVID-19 diagnosis is only confirmed if 3D U-Net identifies large characteristic lesions of the disease. However, in cases where lesions are minimal or absent, the diagnosis of COVID-19 relies on consensus, meaning confirmation occurs only when both 3D U-Net and YOLOv4 are in agreement as shown in the final fiagram of YOLO and 3D U-Net integration at FADCIL prediction module shown in the following figure.


.. figure:: ./images/yolo-3dunet-integration-fadcil-visibilia.PNG
   :alt: YOLOv4 and 3D U-net integration at FADCIL: YOLOv4 processing CT scans at medium resolution as part of FADCIL prediction module
   :align: center


**User Interface Module**

- **Integration**: FADCIL integrates seamlessly with PACS and other CT visualization systems via its API. It saves segmentation results in new scans and stores classification and meta-information in structured report (SR) files.

**Feedback Module**

- **Expert Input**: Captures feedback from radiologists to refine and retrain the model, improving its accuracy over time.


Performance Analysis
====================

FADCIL has been rigorously tested in real clinical environments, processing over 1,000 CT scans from HCFMUSP. It demonstrated outstanding performance, assisting medical teams in diagnosing COVID-19 efficiently.

**Performance Metrics**

- **Classification**:
  - Accuracy: 65%
  - Sensitivity: 86%
  - ROC-AUC: 0.719

- **Segmentation**:
  - DICE Score: 0.856

**Qualitative Evaluation**

- Radiologists rated the segmentations produced by FADCIL with an average score of 4.06 out of 5.

.. image:: ./images/segmentation_example.png
   :alt: Example of Segmentation
   :align: center
   :width: 600px
   :height: 400px

Running the Code
=================

To run the FADCIL code, you need to set up the appropriate programming environment. The source code is written in Python and R, and the necessary dependencies are listed in the following files:

- **Python Dependencies**: `requirements.txt`
- **R Dependencies**: `requirements-R.txt`

### Steps to Run the Code:

1. **Set Up Environment**:
   - Install the required Python packages using: 
     ```
     pip install -r requirements.txt
     ```
   - Install the necessary R packages and other software as specified in `requirements-R.txt`.

2. **Execute the Scripts**:
   - **Segmentation**:
     - Run `unet3D_keras_segmentation.py` to segment lungs and detect COVID-19 lesions from CT scans.
   - **Classification**:
     - Use `final-classification.R` to compute the probability of COVID-19 presence based on features extracted by the segmentation script.
   - **Configuration**:
     - Ensure `yolov4-covid_classification.cfg` is configured with the correct parameter values for the deep nets used in the segmentation script.

### Expected Outputs:

- **Binary Classification**: Outputs labeled with **1** (COVID-19) or **0** (not COVID-19), along with a probability score.
- **Segmentation**: Binary mask indicating the positions of the lesions.

### Additional Tasks:

- **Input Reading**: Implement necessary code to read CT scans in formats like DICOM, NII, or NIfTI.
- **Pre-processing**: Optionally, add code to clean or prepare the data according to specific requirements.
- **Post-processing**: Optionally, adjust the results to match specific formats or specifications.
- **Visualization**: Optionally, add code to visualize the results graphically.






Awards
========

FADCIL was developed as part of the `Challenge nº 03/2020 <https://ideiagov.sp.gov.br/desafios/diagnostico-atraves-de-imagens-de-tomografia-computadorizada-e-raio-x-de-torax/>`_ launched by the São Paulo State Government, aimed at finding AI solutions to assist radiologists in diagnosing COVID-19 from CT and X-ray images. After rigorous evaluation, **Visibilia** was selected as the winner of this challenge. This recognition was officially published in the `Official Press of the Sao Paulo State Government <https://www.imprensaoficial.com.br/DO/BuscaDO2001Documento_11_4.aspx?link=%2f2020%2fexecutivo%2520secao%2520i%2fagosto%2f15%2fpag_0028_0f4ec73d9ce98efebbb9ba398e36dc0e.pdf&pagina=28&data=15/08/2020&caderno=Executivo%20I&paginaordenacao=100028>`_ on August 15, 2020.




Videos
========

Watch FADCIL in action on our YouTube channel:

- `Overview of FADCIL <https://www.youtube.com/watch?v=5MC5czxMdQM&list=PLxCzFuDeosTlrlphQ8-oZyMpYCLmMy4bA&index=1>`_
- `Demonstration Video 1 <https://www.youtube.com/watch?v=example_video_1>`_
- `Demonstration Video 2 <https://www.youtube.com/watch?v=example_video_2>`_

.. image:: https://img.youtube.com/vi/5MC5czxMdQM/0.jpg
   :target: https://www.youtube.com/watch?v=5MC5czxMdQM




Media Appearances
==================

FADCIL has been featured in various media outlets and publications:

- `Visibilia Blog - FADCIL Overview <https://visibilia.net.br/category/fadcil/>`_
- `Interview with Visibilia on the Development of FADCIL <https://www.example.com/interview>`_
- `Feature Article in Local News <https://www.example.com/news-article>`_

Caution
=========

The results generated by FADCIL should not be used directly in clinical settings without appropriate validation and approval by medical professionals.



Commercial Version
==================
Visibilia offers a commercial version of FADCIL, enhanced for clinical use. The commercial version includes additional features such as low refusal rate, high-speed processing, DICOM structured report files, and secure integration with existing clinical platforms.

- For more information, visit our `FADCIL product page <https://visibilia.net.br/fadcil>`_.

.. image:: https://visibilia.net.br/wp-content/uploads/2020/11/fadcil-lung-covid19-visibilia-winner.png
   :width: 600px
   :align: center





Citation
=========

If you use FADCIL in your research, please cite our paper:

.. code-block:: bibtex

    @inproceedings{valverde2024integrating,
      title={Integrating YOLO and 3D U-Net for COVID-19 Diagnosis on Chest CT Scans},
      author={Valverde-Rebaza, Jorge and Andreis, Guilherme R and Shiguihara, Pedro and Paucar, Sebastián and Mano, Leandro Y and Góes, Fabiana and Noguez, Julieta and Da Silva, Nathalia C},
      booktitle={Proceedings of the IEEE 37th International Symposium on Computer-Based Medical Systems (CBMS)},
      year={2024},
      organization={IEEE}
    }


.. _Visibilia: https://visibilia.net.br 
.. _HCFMUSP: https://www.hc.fm.usp.br/hc/portal/
