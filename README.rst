IA for fully automatic COVID-19 detection
==========================================
Copyright (C) 2020 `Visibilia`_

.. _Visibilia: https://visibilia.net.br 

This repository shows the full source code of the algorithms for automatic detection of the presence of COVID-19 in medical images of computed tomography (ct) scans of the lung with high precision. This system identifies the areas of the lung with lesions caused by the disease with high precision, quantifying them in relation to the total lung parenchyma. Moreover, this system aproperly distinguishes lessions caused by COVID-19 from such caused by other diseases.


Awarded
========
Visibilia participated in the challenge launched by the Sao Paulo State Government through the public call nº 03/2020: "*Como o uso de algoritmos de Inteligência Artificial pode auxiliar médicos radiologistas no diagnóstico do COVID-19 através de imagem de tomografia computadorizada e raios-X de tórax?*" and organized by the innovation hub `IdeiaGov`_ . The Sao Paulo state is the richest Brazilian state and a major industrial complex, often dubbed the "locomotive of Brazil" and since the beginning of the pandemic it has been highlighted by the implementation of several actions moved to contain the progress of COVID-19.

.. _IdeiaGov: https://ideiagov.sp.gov.br/desafios/diagnostico-atraves-de-imagens-de-tomografia-computadorizada-e-raio-x-de-torax/

Therefore, after weeks of hard work, Visibilia was chosen as winner of this challenge. Visibilia's selection in the aforementioned competition had been officially approved by the Official Press of the Sao Paulo State Government, according to a `publication on August 15, 2020`_.

.. _publication on August 15, 2020: https://www.imprensaoficial.com.br/DO/BuscaDO2001Documento_11_4.aspx?link=%2f2020%2fexecutivo%2520secao%2520i%2fagosto%2f15%2fpag_0028_0f4ec73d9ce98efebbb9ba398e36dc0e.pdf&pagina=28&data=15/08/2020&caderno=Executivo%20I&paginaordenacao=100028


Commitment
==========
In compliance with the commitment assumed by Visibilia during its participation in the aforementioned contest, this repository is made available under the MIT license. It is important to note that the code available in this repository corresponds to the code developed by Visibilia up to the third (final) stage of the contest.


Getting Started
================

Our source code is in Python and R programming languages. Because we use several data and image processing, machine learning and deep learning algorithms, you will need install an appropriate programming enviromment. Therefore, the packages needed for make out code work are specified in the following files:

- ``requirements.txt`` list of Python packages and their required versions.
- ``requirements-R.txt`` list of packages and other softwares, and their required versions, needed to make run our source code in R. 


Running
========

The source code developed by Visibilia up to the third (final) stage of the contest is formed by the following files:

- ``unet3D_keras_segmentation.py`` Full code implementing segmentation algorithms for detecting lungs and COVID-19 lessions from CT scans. This code is fully implemented in Python.
- ``yolov4-covid_classification.cfg`` Configuration file maintaining the parameter values for all the deep nets used in ``unet3D_keras_segmentation.py``.
- ``final-classification.R`` Full code using classification algorithms for compute the probability of presence of COVID-19. This file use as input some feaures pre-computed in ``unet3D_keras_segmentation.py``. This code is fully implemented in R.


What you will get
=================

For each input CT scan you will get: 

- A binary classification output: Prediction results labeled with **1** (is COVID-19) or **0** (is not COVID-19). In case the prediction result is COVID-19, the probability value between 0 and 1 will be indicated. It is important to note that cases not being COVID-19 does not imply that the patient is totally healthy, as he may still have some other lung disease.

- A segmentation output: Segmentation results represented by a (binary) mask indicating the positions of the curve adjusted to the lessions limits. One or more lessions can be identified. COVID-19 lessions are distinguished from injuries caused by other diseases as well as tomographic findings (e.g. opacity).


What else do you need to do
===========================

Some pieces of code are not considered in this repository and the implementation is under the responsibility of whoever will use the available code. These pieces of code are:

- Input reading: necessary to read the CT scan(s) from the format in which the image to be analyzed is, e.g. DICOM, NII, NIfTI, etc.
- Pre-processing: optionally, in case you need to do any cleaning or other task according to the problem requirements.
- Post-processing: optionally, in case you need to adjust the results to some format or specification.
- Visualization: optionally, in case you need to graphically view the results.


Caution
========

The results obtained by the source code provided here should not be used in a clinical environment.


Updates
=======

Visibilia does not undertake to carry out updates to the source code available in this repository.


Commercial Version
==================

Complementary source code pieces were built to constitute a software product capable of meeting the real-world needs of a clinical environment. Also, rigorous training of our deep neural networks and other machine learning models was performed to improve the quality of our results. This entire package constitutes FADCIL, software licensed by Visibilia and whose pilot version worked at Clinics Hospital of Sao Paulo, the largest and most reputable hospital in Latin America.


.. image:: https://visibilia.net.br/wp-content/uploads/2020/11/fadcil-lung-covid19-visibilia-winner.png
   :width: 600


