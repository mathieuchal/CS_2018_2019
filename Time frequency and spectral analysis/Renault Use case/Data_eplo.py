#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 12:22:34 2018

@author: chalvidalm
"""

import numpy as np 
import pandas as pd
import scipy
import matplotlib.pyplot as plt
import sklearn
import seaborn  as sns
import os

sns.set_context("paper")
sns.set_color_codes()
plot_kwds = {'alpha' : 0.25, 's' : 50, 'linewidths':0}
sns.set(rc={'figure.figsize':(16,8)})


""" Data processing """

os.chdir('/Users/chalvidalm/Documents/3A OMA/Projets OMA/Renault Noise database')
Data_BTD = pd.read_excel('./Database_RoadNoise_SupElec.xlsx', sheet_name=3, header =0 )
Data_BTD['Mesures Rlt Ok/Nok'] = (Data_BTD['Mesures Rlt Ok/Nok'] == 'OK')
Data_BTD['Mesures TMB Ok/Nok'] = (Data_BTD['Mesures TMB Ok/Nok'] == 'OK')
Data_BTD['Subjectif\nOk/Nok'] = (Data_BTD['Subjectif\nOk/Nok'] == 'ok')
Data_BTD['Renault/CAC'] = (Data_BTD['Renault/CAC'] == 'Renault')

params_of_interest = ['Energie', 'Type TAV',
'Type TAR',
'Type Berceau Avant',
'Berceau Avant Filtré ?',
'Type Caisse',
'Toit Ouvrant/Normal',
'Matériau Roues',
'Taille Roues',
'Roue de Secours']

Spectre_names = ['{}\nRoulement Bandes Fines'.format(i) for i in range(500)]
TMB_names = ['{}\nTambourinement'.format(i) for i in range(15,61)] 

Spectre_restricted = ['{}\nRoulement Bandes Fines'.format(i) for i in range(60,280)] 

Spectre_Unweighted_names = ['{}\nRoulement Bandes Fines en Pascal'.format(i) for i in range(10,500)] 
            
Spectre_HF_names = ['1/3 oct 500',
'1/3 oct 630',
'1/3 oct 800',
'1/3 oct 1000',
'1/3 oct 1250',
'1/3 oct 1600',
'1/3 oct 2000',
'1/3 oct 2500',
'1/3 oct 3150']


Pondération_dBA = pd.read_csv('pondération DBA.txt',delimiter=';')
plt.plot(Pondération_dBA['1/3 d’octave (Hz)'],Pondération_dBA['Pondération A (dB)'])
interpolation_DBA = scipy.interpolate.interp1d(np.array(Pondération_dBA['1/3 d’octave (Hz)']),np.array(Pondération_dBA['Pondération A (dB)']))
ponderation = np.array([-interpolation_DBA(np.linspace(10,500,490)) for i in range(170)])

Spectre_HF_freq = [500,630,800,1000,1250,1600,2000,2500,3150]


""" Inversion de la pondération du spectre """
                        
Spectre = np.array(Data_BTD[Data_BTD['Mesures Rlt Ok/Nok']][Spectre_names])
Spectre_HF = np.array(Data_BTD[Data_BTD['Mesures Rlt Ok/Nok']][Spectre_HF_names]) 
Spectre_Unweighted = np.exp((np.array(Data_BTD[Data_BTD['Mesures Rlt Ok/Nok']][Spectre_names])[:,10:500] - 2*np.ones((170,490)) + ponderation)/20)

Spectral_mean = np.nanmean(Spectre, axis = 0) 
Spectral_HF_mean = np.nanmean(Spectre_HF, axis = 0) 
Spectral_Unweighted_mean = np.nanmean(Spectre_Unweighted, axis = 0) 


Spectre_centered = np.array([Spectre[i] - Spectral_mean for i in range(Spectre.shape[0])])
Spectre_HF_centered = np.array([Spectre[i] - Spectral_mean for i in range(Spectre.shape[0])])
Spectre_Unweighted_centered = np.array([Spectre_Unweighted[i] - Spectral_Unweighted_mean for i in range(Spectre.shape[0])])

Tambourinement_target = np.array(Data_BTD[Data_BTD['Mesures TMB Ok/Nok']][Spectre_names])
Tambourinement = np.array(Data_BTD[Data_BTD['Mesures TMB Ok/Nok']][TMB_names])

plt.plot(Spectre_HF_freq, Spectre_HF.T)    
plt.ylim([0,80]) 
plt.savefig('spectre HF du dataset')


plt.plot(Spectre_Unweighted.T)
plt.plot(np.linspace(10,500,490),Spectre_Unweighted_centered.T)
plt.plot(Spectre_centered.T)
plt.savefig('Signature spectrale de 0 à 500Hz pondéré centré')




Data_clean = Data_BTD[Data_BTD['Mesures Rlt Ok/Nok']]
for i in range(10,490): 
    Data_clean['{}\nRoulement Bandes Fines en Pascal sans pondération'.format(i)]= pd.Series(Spectre_Unweighted.T[i], index=Data_clean.index)

spectre_non_pondérés_names = ['{}\nRoulement Bandes Fines en Pascal sans pondération'.format(i) for i in range(10,490)]
    
Data_clean = Data_clean[Data_clean['Type Caisse'].notna()]
    
Spectre_type_caisse = Data_clean.groupby(['Type Caisse'])[spectre_non_pondérés_names].mean()
Type_caisse = Spectre_type_caisse.index
Spectre_type_caisse = np.array(Spectre_type_caisse)
plt.plot(Spectre_type_caisse.T)
plt.legend(Type_caisse)    
    
    
    
""" Renault against others """

Spectre_Renault = np.exp((np.array(Data_BTD[Data_BTD['Mesures Rlt Ok/Nok'] & Data_BTD['Renault/CAC']][Spectre_names])[:,10:500] - 2*np.ones((64,490)) + np.array([-interpolation_DBA(np.linspace(10,500,490)) for i in range(64)]))/20)
Spectral_Renault_mean = np.nanmean(Spectre_Renault, axis = 0) 

Spectre_Other= np.array(Data_BTD[Data_BTD['Mesures Rlt Ok/Nok'] & ~Data_BTD['Renault/CAC']][Spectre_names])
Spectral_Other_mean = np.nanmean(Spectre_Other, axis = 0) 
  

plt.plot(Spectral_Other_mean)
plt.plot(Spectral_Renault_mean)
plt.legend(['Other','Renault'])
plt.ylim([30,60])  


""" Motorisation """

Spectre_essence = np.array(Data_BTD[Data_BTD['Mesures Rlt Ok/Nok'] & (Data_BTD['Energie'] == 'essence')][Spectre_names])
Spectral_essence_mean = np.nanmean(Spectre_essence, axis = 0) 

Spectre_diesel = np.array(Data_BTD[Data_BTD['Mesures Rlt Ok/Nok'] & (Data_BTD['Energie'] == 'diesel')][Spectre_names])
Spectral_diesel_mean = np.nanmean(Spectre_diesel, axis = 0) 

Spectre_elec = np.array(Data_BTD[Data_BTD['Mesures Rlt Ok/Nok'] & (Data_BTD['Energie'] == 'électrique')][Spectre_names])
Spectral_elec_mean = np.nanmean(Spectre_elec, axis = 0) 
  
plt.figure(figsize =(16,8))
plt.plot(Spectral_essence_mean)
plt.plot(Spectral_diesel_mean)
plt.plot(Spectral_elec_mean)
plt.legend(['essence','diesel','elec'])
plt.ylim([30,60])  
plt.savefig('spectre par motorisation')


""" Cylindrée """

plt.figure(figsize =(16,8))
Data_cylindrée = Data_BTD[Data_BTD['Mesures Rlt Ok/Nok']].groupby(['Cyindrée'])[Spectre_names].mean()
cylindrée = Data_cylindrée.index
Spectre_Cylindrée = np.array(Data_cylindrée)
plt.plot(Spectre_Cylindrée.T)
plt.legend(cylindrée)
plt.ylim([30,70])
plt.savefig('spectre par cylindrée')

""" Segment """

plt.figure(figsize =(16,8))
Data_segment = Data_BTD[Data_BTD['Mesures Rlt Ok/Nok']].groupby(['Segment'])[Spectre_names].mean()
segment = Data_segment.index
Spectre_segment = np.array(Data_segment)
plt.plot(Spectre_segment.T)
plt.legend(segment)
plt.ylim([30,70])
plt.savefig('spectre par segment')

""" Type de caisse """

Type_caisse = {}
Type_caisse['B']='Berline'
Type_caisse['K']='Breal'
Type_caisse['L']='Sedan'
Type_caisse['J']='Monospace'
Type_caisse['R']='Monospace long'
Type_caisse['C']='Coupé'
Type_caisse['E']='Cabriolet'
Type_caisse['H']='SUV'
Type_caisse['D']='D'
Type_caisse['F']='F'


plt.figure(figsize =(16,8))
Data_caisse = Data_BTD[Data_BTD['Mesures Rlt Ok/Nok']].groupby(['Type Caisse'])[Spectre_names].mean()
Caisse = Data_caisse.index
Spectre_caisse = np.array(Data_caisse)
plt.plot(Spectre_caisse.T)
plt.legend([Type_caisse[i] for i in Caisse])
plt.ylim([30,70])
plt.savefig('spectre par type de caisse')


""" Kernel density estimation """

from sklearn.neighbors.kde import KernelDensity
import seaborn

    """ estimation on Renault cars """"
    
densities = np.zeros((490,1000))
for i in range(490):
    Spectre_kernel = KernelDensity(kernel='gaussian',bandwidth=1).fit(Spectre_Renault[:,i].reshape(-1, 1))
    log_density = Spectre_kernel.score_samples(np.linspace(0, 100, 1000)[:,np.newaxis])
    densities[i] = np.exp(log_density)

sns.set(rc={'figure.figsize':(6,6)})
plt.plot(densities[200]) 
   
    
heatmap = sns.heatmap(-densities,xticklabels=False, yticklabels=False,cmap="YlGnBu",cbar=False)   
heatmap.get_figure().savefig("Estimation du spectre énergétique des véhicules Renault")  

plt.figure(figsize =(16,8))
plt.plot(Spectre_Renault.T)
plt.plot(densities.argmax(axis=1)/10, c='w')
plt.ylim([20,70])
plt.savefig('Estimation du spectre des véhicules Renault')


scipy.integrate.trapz(densities.argmax(axis=1)/10)
Data_BTD[Data_BTD['Mesures Rlt Ok/Nok']].groupby(['Renault/CAC'])['BTD TBF (dBA)','BTD BF (dBA)','BTD MF (dBA)'].mean()


    """ Precision of the estimation """

Spectre_Berline_diesel_essieu_H = np.array(Data_BTD[Data_BTD['Mesures Rlt Ok/Nok'] & (Data_BTD['Energie'] == 'diesel')  & (Data_BTD['Type TAR'] == 'H') & (Data_BTD['Type Caisse'] == 'B')][Spectre_names])

densities_pres = np.zeros((500,1000))    
for i in range(500):
    Spectre_kernel_essence = KernelDensity(kernel='exponential',bandwidth=1).fit(Spectre_Berline_diesel_essieuH[:,i].reshape(-1, 1))
    log_density = Spectre_kernel_essence.score_samples(np.linspace(0, 100, 1000)[:,np.newaxis])
    densities_pres[i] = np.exp(log_density)

#heatmap = sns.heatmap(-densities,xticklabels=False, yticklabels=False,cmap="YlGnBu",cbar=False)   

plt.plot(Spectre_Berline_diesel_essieuH.T)
plt.legend(Data_BTD[Data_BTD['Mesures Rlt Ok/Nok'] & (Data_BTD['Energie'] == 'diesel')  & (Data_BTD['Type TAR'] == 'H') & (Data_BTD['Type Caisse'] == 'B')]['Modèle'])
plt.plot(densities_pres.argmax(axis=1)/10, c='r')
#plt.plot(Spectral_essence_mean)
plt.ylim([20,70])

def movingaverage (values, window):
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'full')
    return sma

def distance(Spectre, Estimateur, padding):
    diff = Spectre - Estimateur
    #dist = np.zeros(len(diff))
    return movingaverage(diff,padding)   
    
plt.figure(figsize =(16,8))    
plt.plot(Spectre_Berline_diesel_essieuH[0])
plt.plot(densities_pres.argmax(axis=1)/10)
plt.legend(['spectre','estimation'])
plt.plot(distance(Spectre_Berline_diesel_essieuH[9],densities_pres.argmax(axis=1)/10, 5))
plt.legend(['spectre','estimation','distance','distance lissée'])
plt.ylim([-20,80])
plt.savefig("Spectre, Estimation et distance à l'estimation du spectre d'une Berline diesel à essieu souple H")

plt.figure(figsize =(16,8))
plt.plot(movingaverage(Spectre_Berline_diesel_essieuH[0] - densities_pres.argmax(axis=1)/10, 5))
plt.plot(Spectre_Berline_diesel_essieuH[0] - densities_pres.argmax(axis=1)/10)


""" Gaussian micture model """ 


#essai avec moyennage#
padding = []
for i in range(10,500,10):
    padding.append(np.mean(Spectre_centered.T[i:i+10], axis=0))
padding = np.array(padding.T)

plt.plot(padding.T)

""" Essai sur spectre total """

from sklearn.mixture import GaussianMixture
Gauss_model_pad = GaussianMixture(n_components=9)
Gauss_model_pad.fit(padding)

Gauss_model = GaussianMixture(n_components=9)
Gauss_model.fit(Spectre_centered)

Gauss_model_Unweighted = GaussianMixture(n_components=9)
Gauss_model_Unweighted.fit(Spectre_Unweighted_centered)

Gauss_model_Unweighted_restricted = GaussianMixture(n_components=9)
Gauss_model_Unweighted_restricted.fit(Spectre_Unweighted_centered[:,10:280])

Spectre_clustered = Data_BTD[Data_BTD['Mesures Rlt Ok/Nok']]
Pascal = pd.DataFrame(data=Spectre_Unweighted_centered, index=Spectre_clustered.index, columns=Spectre_Unweighted_names)
Spectre_clustered =pd.concat([Spectre_clustered, Pascal], axis=1)


Spectre_clustered['GMM class'] = Gauss_model.predict(Spectre_centered)
Spectre_clustered['GMM class pad']=Gauss_model_pad.predict(padding)
Spectre_clustered['GMM class Unweighted'] = Gauss_model_Unweighted.predict(Spectre_Unweighted_centered)
Spectre_clustered['GMM class Unweighted'] = Gauss_model_Unweighted.predict(Spectre_Unweighted_centered)
Spectre_clustered['GMM class Unweighted restricted'] = Gauss_model_Unweighted_restricted.predict(Spectre_Unweighted_centered[:,10:280])


Class_composition = Spectre_clustered.groupby(['GMM class'])[params_of_interest].describe()
Class_composition_pad = Spectre_clustered.groupby(['GMM class pad'])[params_of_interest].describe()
Class_composition_Unweighted = Spectre_clustered.groupby(['GMM class Unweighted'])[params_of_interest].describe()
Class_composition_Unweighted_restricted = Spectre_clustered.groupby(['GMM class Unweighted restricted'])[params_of_interest].describe()


Class_densities=[]
for i in range(9):
    densities_pres = np.zeros((500,1000))
    for j in range(500):
        Spectre_kernel = KernelDensity(kernel='exponential',bandwidth=1).fit(np.array(Spectre_clustered[Spectre_clustered['GMM class']== i][Spectre_names])[:,j].reshape(-1, 1))
        log_density = Spectre_kernel.score_samples(np.linspace(0, 100, 1000)[:,np.newaxis])
        densities_pres[j] = np.exp(log_density)
    Class_densities.append(densities_pres)
    

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

fig, ax = plt.subplots(3, 3, figsize=(16,16))
for i in range(9):
    ax[i//3,i%3].plot(np.array(Spectre_clustered[Spectre_clustered['GMM class Unweighted']== i][Spectre_Unweighted_names]).T)
    ax[i//3,i%3].plot(np.array(Spectre_clustered[Spectre_clustered['GMM class Unweighted']== i][Spectre_Unweighted_names].mean()),c='w')
    #ax[i//3,i%3].plot(Class_densities[i].argmax(axis=1)/10, c='w')
    #ax[i//3,i%3].set_ylim([20,70])
    title = str(Class_composition[('Energie','top')][i]) + ' / Type TAR:' + str(Class_composition[('Type TAR','top')][i]) + "\n" + 'type Caisse:  ' + str(Class_composition[('Type Caisse','top')][i]) + ' / Berceau av filtré: ' + str(Class_composition[('Berceau Avant Filtré ?','top')][i]) + ' / Roue de secours:' + str(Class_composition[('Roue de Secours','top')][i])
    ax[i//3,i%3].set_title(title,fontsize=10)
plt.savefig("Clusters unweighted energy spectrums centered") 

fig, ax = plt.subplots(3, 3, figsize=(16,16))
for i in range(9):
    ax[i//3,i%3].plot(np.array(Spectre_clustered[Spectre_clustered['GMM class Unweighted restricted']== i][Spectre_Unweighted_names]).T)
    ax[i//3,i%3].plot(np.array(Spectre_clustered[Spectre_clustered['GMM class Unweighted restricted']== i][Spectre_Unweighted_names].mean()),c='w')
    #ax[i//3,i%3].plot(Class_densities[i].argmax(axis=1)/10, c='w')
    #ax[i//3,i%3].set_ylim([20,70])
    title = str(Class_composition[('Energie','top')][i]) + ' / Type TAR:' + str(Class_composition[('Type TAR','top')][i]) + "\n" + 'type Caisse:  ' + str(Class_composition[('Type Caisse','top')][i]) + ' / Berceau av filtré: ' + str(Class_composition[('Berceau Avant Filtré ?','top')][i]) + ' / Roue de secours:' + str(Class_composition[('Roue de Secours','top')][i])
    ax[i//3,i%3].set_title(title,fontsize=10)
    ax[i//3,i%3].axvline(x=280,c='r')
plt.savefig("Clusters unweighted energy spectrums centered restricted ") 

#Class_composition = Spectre_clustered.groupby(['GMM class'])[params_of_interest].nunique()/item_per_variable
#Class_composition = Class_composition / Class_composition.sum()

Spectre_mean_clustered = np.array(Spectre_clustered.groupby(['GMM class'])[Spectre_names].mean())
plt.plot(Spectre_mean_clustered.T)
plt.legend([i for i in range(1,10)])
plt.savefig("GMM Clustering (Class=10)")


""" essai avec fenêtre """

for i in range(10,500,10):
    print('clustering on freq: {} to {}'.format(i,i+10))
    Gauss_model = GaussianMixture(n_components=5)
    Gauss_model.fit(Spectre_centered[:,i:i+10])
    Gauss_model.predict(Spectre_centered[:,i:i+10])

    Spectre_clustered = Data_BTD[Data_BTD['Mesures Rlt Ok/Nok']]
    Spectre_clustered['GMM class']=Gauss_model.predict(padding)

    Class_composition = Spectre_clustered.groupby(['GMM class'])[params_of_interest].count()
    Class_composition = Class_composition / Class_composition.sum()
    if np.var(Class_composition, )
    
    
    
Spectre_mean_clustered = np.array(Spectre_clustered.groupby(['GMM class'])[Spectre_names].mean())
plt.plot(Spectre_mean_clustered.T)
plt.legend([i for i in range(1,10)])
plt.savefig("GMM Clustering (Class=10)")

""" order selection """
order_AIC=[]
order_BIC=[]
for k in range(1,20):
    print("{} order".format(k))
    Gauss_model_order = GaussianMixture(n_components=i)
    Gauss_model_order.fit(Spectre_Unweighted_centered)
    order_AIC.append(Gauss_model_order.aic(Spectre_Unweighted_centered))
    order_BIC.append(Gauss_model_order.bic(Spectre_Unweighted_centered))

plt.plot(order_AIC)
plt.plot(order_BIC)



""" PCA Embedding """

from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D
pca = PCA(n_components=3)
Embedded = pca.fit_transform(Spectre_clustered[Spectre_names])

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'w','orange']
markers = ['o','v','^'	,'<','>','p','*'	,'h','H']

classes = [i for i in range(9)]
col = dict(zip(classes,colors ))
mark = dict(zip(classes,markers ))

color_labels = [col[i] for i in Spectre_clustered['GMM class Unweighted restricted']]
markers_labels = [mark[i] for i in Spectre_clustered['GMM class Unweighted restricted']]


fig = plt.figure(figsize=(16,16))
ax = fig.add_subplot(111, projection='3d')
ax.view_init(30, 60)
#ax.set_xticks([])
#ax.set_yticks([])
#ax.set_zticks([])
for i in range(170):
    ax.scatter(Embedded[i,0],Embedded[i,1],Embedded[i,2],s=70,color=color_labels[i], marker=markers_labels[i])
plt.savefig('PCA Embedding of classes in 3 dimensions vue 2')
ax.legend()

""" Histo """
from collections import Counter
Counter(Spectre_clustered)

Class_composition_Unweighted_hist = Spectre_clustered.groupby(['GMM class Unweighted'])[params_of_interest].count()
Spectre_clustered['GMM class Unweighted'].value_counts()


Class_composition_Unweighted_hist=[{} for i in range(9)]
lenghts=[{} for k in range(9)]
fig, ax = plt.subplots(3, 3, figsize=(16,16))
for i in range(9):
    count=0
    space=[]
    heights=[]
    for k in params_of_interest:
        Class_composition_Unweighted_hist[i][k]=Counter(Spectre_clustered[Spectre_clustered['GMM class Unweighted']==i][k].values).most_common(5)
        lenghts[i][k]=len(Class_composition_Unweighted_hist[i][k])
        count+=1
        space.append(np.arange(lenghts[i][k])+np.ones(lenghts[i][k])*10*count)
    space=np.concatenate(space)
    heights=[Class_composition_Unweighted_hist[i][m][l][1] for m in list(Class_composition_Unweighted_hist[i]) for l in range(len(Class_composition_Unweighted_hist[i][m]))]
    colors=[Class_composition_Unweighted_hist[i][m][l][0] for m in list(Class_composition_Unweighted_hist[i]) for l in range(len(Class_composition_Unweighted_hist[i][m]))]
    ax[i//3,i%3].bar(space, heights,label=colors)
    ax[i//3,i%3].set_title(i)
    plt.savefig("hist of specifications by GMM clusters (Class=9)")

        
""" Support vector regression """    
from sklearn.svm import SVR
Tambourinement_predicted = []
Tambourinement_predicted_rbf = []
scores=[]
for i in range(Tambourinement.shape[1]):
    svr_linear = SVR(kernel='linear', C=0.01)
    #svr_rbf = SVR(kernel='rbf', C=1000, gamma=1/60)
    Tambourinement_predicted.append(svr_linear.fit(Tambourinement_target[:100,15:60], Tambourinement[:100,i]).predict(Tambourinement_target[100:,15:60]))
    #Tambourinement_predicted_rbf.append(svr_rbf.fit(Tambourinement_target[:100,15:60], Tambourinement[:100,i]).predict(Tambourinement_target[100:,15:60]))
    scores.append(svr_linear.score(Tambourinement_target[100:,15:60], Tambourinement[100:,i]))

Tambourinement_predicted = np.array(Tambourinement_predicted).T
Tambourinement_predicted_rbf = np.array(Tambourinement_predicted_rbf).T


fig, ax = plt.subplots(4, 4, figsize=(16,16))
for i in range(16):
    ax[i//4,i%4].plot([j for j in range(15,61)],Tambourinement_predicted[i],c='b')
    #ax[i//4,i%4].plot([j for j in range(15,61)],Tambourinement_predicted_rbf[i],c='g')
    ax[i//4,i%4].plot([j for j in range(15,61)],Tambourinement[100+i],c='r')
    ax[i//4,i%4].legend(['predicted','predicted with eponential kernel' ,'mesured'],loc=3, prop={'size': 6})
    ax[i//4,i%4].set_title(Data_BTD[Data_BTD['Mesures TMB Ok/Nok']]['Marque'].iloc[i+100] + " " +  Data_BTD[Data_BTD['Mesures TMB Ok/Nok']]['Modèle'].iloc[i+100],fontsize=10)
    ax[i//4,i%4].set_ylim([35,85])
plt.savefig("Support Vector regression sur les mesures de Tambourinement pour 16 voitures ")

""" Grid Search """
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score
for i in range(Tambourinement.shape[1]):
    svr = GridSearchCV(SVR(kernel='rbf', gamma=0.1), cv=5, param_grid={"C": [1e0, 1e1, 1e2, 1e3],"gamma": np.logspace(-2, 2, 5)})
    svr.fit(Tambourinement_target[:100,15:60],Tambourinement[:100,i])
    print(svr.cv_results_)

""" correlation """
corr =[]
for i in range(Tambourinement.shape[1]):
    for j in range(Tambourinement.shape[1]):
        corr.append(scipy.stats.pearsonr(Tambourinement_target[:,15+i], Tambourinement[:,j])[0])   
corr=np.array(corr).reshape(Tambourinement.shape[1],Tambourinement.shape[1])    
sns.set(rc={'figure.figsize':(16,16)})
sns.heatmap(corr)  
plt.savefig('Correlation de la signature spectrale (15 à 60 Hz) sur piste lisse et tambourinante')
 