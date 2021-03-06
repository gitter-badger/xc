# -*- coding: utf-8 -*-

#Test from Ansys manual
#Reference:  Strength of Materials, Part I, Elementary Theory and Problems, pg. 26, problem 10

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

E= 30e6 #Young modulus (psi)
l= 10 #Bar length in inches
a= 0.3*l #Longitud del tramo a
b= 0.3*l #Longitud del tramo b
F1= 1000 #Force magnitude 1 (pounds)
F2= 1000/2 #Force magnitude 2 (pounds)

prueba= xc.ProblemaEF()
preprocessor=  prueba.getPreprocessor
nodes= preprocessor.getNodeLoader

predefined_spaces.gdls_elasticidad2D(nodes)
nodes.defaultTag= 1 #El número del próximo nodo será 1.
nodes.newNodeXYZ(0,0,0)
nodes.newNodeXYZ(0,l-a-b,0)
nodes.newNodeXYZ(0,l-a,0)
nodes.newNodeXYZ(0,l,0)

elast= typical_materials.defElasticMaterial(preprocessor, "elast",E)

# Se definen nodos en los puntos de aplicación de
# la carga. Puesto que no se van a determinar tensiones
# se emplea una sección arbitraria de área unidad
elements= preprocessor.getElementLoader
elements.dimElem= 2 #Las barras se definen e un espacio bidimensional.
elements.defaultMaterial= "elast"
elements.defaultTag= 1 #Tag for the next element.
truss= elements.newElement("truss",xc.ID([1,2]));
truss.area= 1
truss= elements.newElement("truss",xc.ID([2,3]));
truss.area= 1
truss= elements.newElement("truss",xc.ID([3,4]));
truss.area= 1

coacciones= preprocessor.getConstraintLoader
#Impedimos el movimiento del nodo 1.
spc= coacciones.newSPConstraint(1,0,0.0)
spc= coacciones.newSPConstraint(1,1,0.0)
#Impedimos el movimiento del nodo 4.
spc= coacciones.newSPConstraint(4,0,0.0)
spc= coacciones.newSPConstraint(4,1,0.0)
#Impedimos el movimiento del nodo 2 según X (gdl 0).
spc= coacciones.newSPConstraint(2,0,0.0)
#Impedimos el movimiento del nodo 3 según X (gdl 0).
spc= coacciones.newSPConstraint(3,0,0.0)

cargas= preprocessor.getLoadLoader
#Contenedor de hipótesis de carga:
casos= cargas.getLoadPatterns
#modulación de la carga en el tiempo:
ts= casos.newTimeSeries("constant_ts","ts")
casos.currentTimeSeries= "ts"
#Load case definition
lp0= casos.newLoadPattern("default","0")
lp0.newNodalLoad(2,xc.Vector([0,-F2]))
lp0.newNodalLoad(3,xc.Vector([0,-F1]))

#Agregamos el caso de carga al dominio.
casos.addToDomain("0")

# Solution
analisis= predefined_solutions.simple_static_linear(prueba)
result= analisis.analyze(1)

nodes.calculateNodalReactions(True)
R1= nodes.getNode(4).getReaction[1]
R2= nodes.getNode(1).getReaction[1]

ratio1= (R1-900)/900
ratio2= (R2-600)/600

#print "R1= ",R1
#print "R2= ",R2
#print "ratio1= ",ratio1
#print "ratio2= ",ratio2

import os
fname= os.path.basename(__file__)
if abs(ratio1)<1e-5 and abs(ratio2)<1e-5:
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."


