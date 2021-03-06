# -*- coding: utf-8 -*-

# Test from Ansys manual
# Reference:  Strength of Material, Part I, Elementary Theory and Problems, pg. 10, problem 2

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AOO)"
__copyright__= "Copyright 2015, LCPT and AOO"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

import xc_base
import geom
import xc
from solution import predefined_solutions
from model import predefined_spaces
from materials import typical_materials
import math


E= 30e6 #Young modulus (psi)
l= 15*12 #Bar length (15 pies) expresada in inches}
theta= math.radians(30) #angle between bars
F= 5000 #Force magnitude (pounds)}
A= 0.5 #Área in inches cuadradas}
a= 2*l*math.cos(theta) #Distancia entre nodos extremos}
b= l*math.sin(theta) #Distancia entre nodos extremos}

prb= xc.ProblemaEF()
preprocessor=  prb.getPreprocessor
nodes= preprocessor.getNodeLoader

# Problem type
predefined_spaces.gdls_elasticidad2D(nodes)

nodes.defaultTag= 1 #First node number.
nodes.newNodeXYZ(0,0,0)
nodes.newNodeXYZ(a/2,-b,0)
nodes.newNodeXYZ(a,0,0)

# Materials definition
elast= typical_materials.defElasticMaterial(preprocessor, "elast",E)
elast.E= E


# Element definition.
elementos= preprocessor.getElementLoader
elementos.dimElem= 2 #Bidimensional space.
elementos.defaultMaterial= "elast"
elementos.defaultTag= 1 #Next element number.
truss= elementos.newElement("truss",xc.ID([1,2]));
truss.area= A
truss= elementos.newElement("truss",xc.ID([2,3]))
truss.area= A

coacciones= preprocessor.getConstraintLoader
#Zerp movement for node 1.
spc= coacciones.newSPConstraint(1,0,0.0)
spc= coacciones.newSPConstraint(1,1,0.0)
#Zerp movement for node 1.
spc= coacciones.newSPConstraint(3,0,0.0)
spc= coacciones.newSPConstraint(3,1,0.0)

cargas= preprocessor.getLoadLoader
#Load case container:
casos= cargas.getLoadPatterns
#Load modulation.
ts= casos.newTimeSeries("constant_ts","ts")
casos.currentTimeSeries= "ts"
#Load case definition
lp0= casos.newLoadPattern("default","0")
lp0.newNodalLoad(2,xc.Vector([0,-F]))
#We add the load case to domain.
casos.addToDomain("0")

# Solution
analisis= predefined_solutions.simple_static_linear(prb)
result= analisis.analyze(1)

delta= nodes.getNode(2).getDisp[1]
stress= elementos.getElement(1).getMaterial().getStress()

ratio1= delta/(-0.12)
ratio2= stress/10000

import os
fname= os.path.basename(__file__)
if abs(ratio1-1)<1e-5 and abs(ratio2-1)<1e-5:
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."

