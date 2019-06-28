#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 14 09:22:04 2018

Clustering by micture model 

@author: chalvidalm
"""

""" Standard imports """

import numpy as np 
import pandas as pd
import scipy
import matplotlib.pyplot as plt
import sklearn

"""Data processing """


Data_DTB = pd.read_excel('./Database_RoadNoise_SupElec.xlsx',sheet_name=3, header =0 )
Data_BTD['Mesures Rlt Ok/Nok'] = (Data_BTD['Mesures Rlt Ok/Nok'] == 'OK')
Data_BTD['Mesures TMB Ok/Nok'] = (Data_BTD['Mesures TMB Ok/Nok'] == 'OK')
Data_BTD['Subjectif\nOk/Nok'] = (Data_BTD['Subjectif\nOk/Nok'] == 'ok')
Data_BTD['Renault/CAC'] = (Data_BTD['Renault/CAC'] == 'Renault')

Spectre_names = ['{}\nRoulement Bandes Fines'.format(i) for i in range(500)]
params_of_interest = ['Energie', 'Type TAV',
'Type TAR',
'Type Berceau Avant',
'Berceau Avant Filtré ?',
'Type Caisse',
'Toit Ouvrant/Normal',
'Matériau Roues',
'Taille Roues',
'Roue de Secours']
                         
Spectre = np.array(Data_BTD[Data_BTD['Mesures Rlt Ok/Nok']][Spectre_names])


""" Building Model """

from sklearn.mixture import GaussianMixture
Gauss_model_pad = GaussianMixture(n_components=9)
Gauss_model_pad.fit(padding)

Gauss_model = GaussianMixture(n_components=9)
Gauss_model.fit(Spectre_centered)

Spectre_clustered = Data_BTD[Data_BTD['Mesures Rlt Ok/Nok']]


Spectre_clustered['GMM class']=Gauss_model.predict(Spectre_centered)
Spectre_clustered['GMM class pad']=Gauss_model_pad.predict(padding)

Class_composition = Spectre_clustered.groupby(['GMM class'])[params_of_interest].describe()
Class_composition_pad = Spectre_clustered.groupby(['GMM class pad'])[params_of_interest].describe()


Class_densities=[]
for i in range(9):
    densities_pres = np.zeros((500,1000))
    for j in range(500):
        Spectre_kernel = KernelDensity(kernel='exponential',bandwidth=1).fit(np.array(Spectre_clustered[Spectre_clustered['GMM class']== i][Spectre_names])[:,j].reshape(-1, 1))
        log_density = Spectre_kernel.score_samples(np.linspace(0, 100, 1000)[:,np.newaxis])
        densities_pres[j] = np.exp(log_density)
    Class_densities.append(densities_pres)
    

""" Ploting """    
    
    
fig, ax = plt.subplots(3, 3, figsize=(16,16))
for i in range(9):
    ax[i//3,i%3].plot(np.array(Spectre_clustered[Spectre_clustered['GMM class']== i][Spectre_names]).T)
    ax[i//3,i%3].plot(np.array(Spectre_clustered[Spectre_clustered['GMM class']== i][Spectre_names].mean()),c='w')
    #ax[i//3,i%3].plot(Class_densities[i].argmax(axis=1)/10, c='w')
    ax[i//3,i%3].set_ylim([20,70])
    title = str(Class_composition[('Energie','top')][i]) + ' / Type TAR:' + str(Class_composition[('Type TAR','top')][i]) + "\n" + 'type Caisse:  ' + str(Class_composition[('Type Caisse','top')][i]) + ' / Berceau av filtré: ' + str(Class_composition[('Berceau Avant Filtré ?','top')][i]) + ' / Roue de secours:' + str(Class_composition[('Roue de Secours','top')][i])
    ax[i//3,i%3].set_title(title,fontsize=10)
plt.savefig("Clusters energy spectrums")    

fig, ax = plt.subplots(3, 3, figsize=(16,16))
for i in range(9):
    ax[i//3,i%3].plot(np.array(Spectre_clustered[Spectre_clustered['GMM class pad']== i][Spectre_names]).T)
    ax[i//3,i%3].plot(np.array(Spectre_clustered[Spectre_clustered['GMM class pad']== i][Spectre_names].mean()),c='w')
    #ax[i//3,i%3].plot(Class_densities[i].argmax(axis=1)/10, c='w')
    ax[i//3,i%3].set_ylim([20,70])
    title = str(Class_composition_pad[('Energie','top')][i]) + ' / Type TAR:' + str(Class_composition_pad[('Type TAR','top')][i]) + "\n" + 'type Caisse:  ' + str(Class_composition_pad[('Type Caisse','top')][i]) + ' / Berceau av filtré: ' + str(Class_composition_pad[('Berceau Avant Filtré ?','top')][i]) + ' / Roue de secours:' + str(Class_composition_pad[('Roue de Secours','top')][i])
    ax[i//3,i%3].set_title(title,fontsize=10)
plt.savefig("Clusters energy spectrums avec padding") 

