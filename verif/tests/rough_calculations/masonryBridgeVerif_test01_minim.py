#-*- coding: utf-8 -*-

from __future__ import division
import math
import sys
import numpy as np
import pydoc
import rough_calculations.masonryVault as masonryVault

#Obtención de los coeficientes del polinomio a partir de 4 puntos del arco 
#(los 4 puntos que tomamos son los obtenidos como coordenadas de las rótulas 
#en el ejemplo de la tesis)
xA= 3.156
xC= 6.175
xD= 10.996
xB= 14.001

hA=6.019
hC=7.406
hD=6.659
hB=2.733

a = np.array([[pow(xA,4),pow(xA,3),pow(xA,2),xA], [pow(xB,4),pow(xB,3),pow(xB,2),xB],[pow(xC,4),pow(xC,3),pow(xC,2),xC],[pow(xD,4),pow(xD,3),pow(xD,2),xD]])
b = np.array([hA,hB,hC,hD])

arcGeom=masonryVault.archGeometry()
arcGeom.coefPolArch=np.linalg.solve(a, b) #[f,j,k,r] coefficients of polynomial y=fx^4+jx^3+kx^2+rx+u (u=0)
#arcGeom.XRot=[xA,xB,xC,xD]     #X coordinates rotules A,B,C,D [m]
arcGeom.arcThick=1             #arch thickness (m)
arcGeom.arcSpan=15             #arch span [m]


fillChar= masonryVault.FillingCharacteristics()
fillChar.angPhi= math.radians(30)   #angle de frottement interne
fillChar.cohesion=0                 #cohésion
fillChar.mp= 0.33                   #Correction factor.
fillChar.mc= 0.01                   #Correction factor.
fillChar.alpha= 0.726
fillChar.beta= 6.095
fillChar.swFill=18e3      #specific weight of filling material [N/m3]
fillChar.swSupStr=20e3    #specific weight or superstructure [N/m3]
fillChar.fillThick=9     #thickness of filling material in the endpoint of the arch [m]
fillChar.eqThickRoad=0.5  #equivalent thickness of road material [m]

trLoad=masonryVault.trafficLoad()
trLoad.delta= math.radians(30)
trLoad.fillThickKeys= 1.5 # Hauteur du remplissage sur la clé de la voûte (m).
trLoad.Q= 160000 # Charge ponctuelle due au trafic (N).
trLoad.qrep= 0.005e6 # Charge uniformément repartie due au trafic (Pa).


permLoadRes=masonryVault.permLoadResult(arcGeom,fillChar)

trafLoadRes=masonryVault.trafficLoadResult(arcGeom,trLoad)

Nadmis=-1.25e6 #Effort axial admisible
resist= masonryVault.resistance(Nadmis,arcGeom,fillChar,trLoad,permLoadRes,trafLoadRes)



res = resist.minimize()

#Results printing
#resist.printResults()

nTeor= 8.25829137054
n=resist.getSafCoef()
ratio1= abs(n-nTeor)/nTeor

# print 'n= ', n
# print 'nTeor= ', nTeor
# print 'ratio1= ', ratio1

import os
fname= os.path.basename(__file__)
if abs(ratio1)<0.06:
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."
