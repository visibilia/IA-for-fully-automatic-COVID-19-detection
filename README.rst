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


What you will find in this repository
======================================

The source code developed by Visibilia up to the third (final) stage of the contest is formed by two main files:

- ``unet3D_keras_segmentation.py`` Full code implementing segmentation algorithms for detecting lungs and COVID-19 lessions from CT scans. This code is fully implemented in Python.
- ee

