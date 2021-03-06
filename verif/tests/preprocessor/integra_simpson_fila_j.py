# -*- coding: utf-8 -*-
import xc_base
import geom
import xc
from solution import predefined_solutions
from model import predefined_spaces
from materials import typical_materials
import integra_simpson as isimp

# Problem type
prueba= xc.ProblemaEF()
preprocessor=  prueba.getPreprocessor
nodes= preprocessor.getNodeLoader
predefined_spaces.gdls_elasticidad3D(nodes)

# Definimos materiales
elast= typical_materials.defElasticMaterial(preprocessor, "elast",3000)

nodes.newSeedNode()
seedElemLoader= preprocessor.getElementLoader.seedElemLoader
seedElemLoader.defaultMaterial= "elast"
seedElemLoader.dimElem= 3
seedElemLoader.defaultTag= 1 #Tag for the next element.
truss= seedElemLoader.newElement("truss",xc.ID([0,0]));
truss.area= 10.0

unifGrids= preprocessor.getCad.getUniformGrids
uGrid= unifGrids.newUniformGrid()

uGrid.org= geom.Pos3d(3.0,0.0,0.0)
uGrid.Lx= 3
uGrid.Ly= 1
uGrid.Lz= 1
uGrid.nDivX= 3
uGrid.nDivY= 0
uGrid.nDivZ= 0

total= preprocessor.getSets.getSet("total")
total.genMesh(xc.meshDir.I)

abscissae= []
gridNodes= uGrid.getNodeLayers
nNodes= uGrid.nDivX+1
for j in range(1,nNodes+1):
  n= gridNodes.getAtIJK(1,j,1)
  abscissae.append(n.getInitialPos3d.x)


def func(x):
  return x-1.0

#pesos= uGrid.getSimpsonWeights("j",'x-1.0',1,1,10)
pesos= isimp.getSimpsonWeights(abscissae,func,10)
suma= pesos[0]+pesos[1]+pesos[2]+pesos[3]

import os
fname= os.path.basename(__file__)
if abs(suma-(9/8.0+3+4+19/8.0))<1e-5:
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."



