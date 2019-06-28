#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 15:40:12 2018

@author: chalvidalm
"""

import numpy as np 
import pandas as pd
import scipy
import matplotlib.pyplot as plt
import sklearn


""" Data processing """

Data = pd.read_excel('./Database_RoadNoise_SupElec.xlsx',sheet_name=[3,4,5,6,7,8,9,10,11,12], header =0 )

cols = ['Colonne1', 'Mesures Rlt Ok/Nok', 'Mesures TMB Ok/Nok',
       'Subjectif\nOk/Nok', 'Renault/CAC',
       'Référence Complète du véhicule', 'Marque', 'Modèle',
       'Année Modèle', 'Génération', 'Doublon', 'Segment', 'Marché',
       'Référence du véhicule', 'Provenance', 'Cyindrée', 'Energie', 'BV',
       'Type TAV', 'Type TAR', 'Type Berceau Avant',
       'Berceau Avant Filtré ?', 'Type Caisse', 'Toit Ouvrant/Normal',
       'Matériau Roues', 'Taille Roues', 'Roue de Secours',
       'Manufacturier Pneus', 'Modèle Pneus',
       'Taille Pneus Indice Vitesse', 'PMC1\n(Hz)', 'PMC2\n(Hz)',
       'Niveau PMC/BTD\n(dBA)', 'DOT', 'pression AV', 'pression AR',
       "Complément d'info", 'Date mesures', 'Km', '°C', 'Météo', 'Piste',
       'Opérateur', 'BTD Global (dBA)', 'BTD TBF (dBA)', 'BTD BF (dBA)',
       'BTD MF (dBA)', 'BTD HF (dBA)', 'BTD TMB MAX (dBB)']


dic = {}
dic[3]='BTD'
dic[6]='BTK'
dic[7]='Accelero_avant_X'
dic[8]='Accelero_avant_Y'
dic[9]='Accelero_avant_Z'
dic[10]='Accelero_arrière_X'
dic[11]='Accelero_avant_Y'
dic[12]='Accelero_avant_Z'

for i in (3,6,7,8,9,10,11,12):
    #Data[i].set_index('Colonne1')
    new_col=[]
    for k in Data[i].columns:
        new_col.append(k+"_{}".format(dic[i]))
    Data[i].columns=new_col


Data_clean = pd.concat([Data[i] for i in (3,6,7,8,9,10,11,12)],axis=1)


Data_clean['Mesures Rlt Ok/Nok_BTD'] = (Data_clean['Mesures Rlt Ok/Nok_BTD'] == 'OK')
Data_clean['Mesures TMB Ok/Nok_BTD'] = (Data_clean['Mesures TMB Ok/Nok_BTD'] == 'OK')
Data_clean['Subjectif\nOk/Nok_BTD'] = (Data_clean['Subjectif\nOk/Nok_BTD'] == 'ok')
Data_clean['Renault/CAC_BTD'] = (Data_clean['Renault/CAC_BTD'] == 'Renault')

metrics_names = [] 
for i in (3,6,7,8,9,10,11,12):
    for j in range(500):
        metrics_names.append('{}\nRoulement Bandes Fines_{}'.format(j,dic[i]))
 
                       
Spectre_full = np.array(Data_clean[Data_clean['Mesures Rlt Ok/Nok_BTD']][metrics_names].dropna())
Spectral_full_mean = np.nanmean(Spectre_full, axis = 0) 
Spectre_full_centered = np.array([Spectre_full[i] - Spectral_full_mean for i in range(Spectre_full.shape[0])])

from sklearn.mixture import GaussianMixture
Gauss_model_pad = GaussianMixture(n_components=9)
Gauss_model.fit(Spectre_full_centered)
Spectre_full_centered['GMM class'] = Gauss_model.predict(Spectre_full_centered)

params = [i + "_BTD" for i in params_of_interest]

Class_composition_full = Spectre_clustered.groupby(['GMM class'])[params_of_interest].describe()


"""SVR """



