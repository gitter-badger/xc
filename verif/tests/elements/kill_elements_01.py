# -*- coding: utf-8 -*-
# home made test

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AOO)"
__copyright__= "Copyright 2015, LCPT and AOO"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

import xc_base
import geom
import xc
from model import predefined_spaces
from solution import predefined_solutions
from materials import typical_materials
from model import fix_node_6dof

E= 30e6 # Young modulus (psi)
l= 20*12 # Bar length in inches
h= 30 # Canto de la viga in inches.
A= 50.65 # Área de la viga in inches cuadradas
I= 7892 # Inercia de la viga in inches a la cuarta
F= 1000 # Fuerza

# Problem type
prueba= xc.ProblemaEF()
preprocessor=  prueba.getPreprocessor   
nodes= preprocessor.getNodeLoader
predefined_spaces.gdls_resist_materiales2D(nodes)
nodes.defaultTag= 1 #First node number.
nod= nodes.newNodeXY(0,0)
nod= nodes.newNodeXY(l,0.0)
nod= nodes.newNodeXY(2*l,0.0)
nod= nodes.newNodeXY(3*l,0.0)

# Geometric transformations
trfs= preprocessor.getTransfCooLoader
lin= trfs.newLinearCrdTransf2d("lin")

    
# Materials definition
scc= typical_materials.defElasticSection2d(preprocessor, "scc",A,E,I)


# Elements definition
elementos= preprocessor.getElementLoader
elementos.defaultTransformation= "lin"
elementos.defaultMaterial= "scc"
#  sintaxis: beam2d_02[<tag>] 
elementos.defaultTag= 1 #Tag for next element.
beam2d= elementos.newElement("elastic_beam_2d",xc.ID([1,2]))
beam2d.h= h
        
beam2d= elementos.newElement("elastic_beam_2d",xc.ID([3,4]))
beam2d.h= h
    
# Constraints
coacciones= preprocessor.getConstraintLoader
#
spc= coacciones.newSPConstraint(1,0,0.0) # Nodo 1
spc= coacciones.newSPConstraint(1,1,0.0)
spc= coacciones.newSPConstraint(1,2,0.0)
spc= coacciones.newSPConstraint(4,0,0.0) # Nodo 4
spc= coacciones.newSPConstraint(4,1,0.0)
spc= coacciones.newSPConstraint(4,2,0.0)


setTotal= preprocessor.getSets.getSet("total")
setTotal.killElements() # Desactivamos los elementos.

mesh= prueba.getDomain.getMesh
mesh.setDeadSRF(0.0)
mesh.freezeDeadNodes("congela")


# Loads definition
cargas= preprocessor.getLoadLoader
casos= cargas.getLoadPatterns
#Load modulation.
ts= casos.newTimeSeries("constant_ts","ts")
casos.currentTimeSeries= "ts"
#Load case definition
lp0= casos.newLoadPattern("default","0")
lp0.newNodalLoad(2,xc.Vector([F,F,F]))

#We add the load case to domain.
casos.addToDomain("0")

# Solution
analisis= predefined_solutions.simple_static_linear(prueba)
result= analisis.analyze(1)
    


nodes.calculateNodalReactions(True)
nodes= preprocessor.getNodeLoader
nod1= nodes.getNode(1)
deltax1= nod1.getDisp[0] 
deltay1= nod1.getDisp[1] 

nod2= nodes.getNode(2)
deltax2= nod2.getDisp[0] 
deltay2= nod2.getDisp[1] 

R1= nod1.getReaction[0] 
R2= nod2.getReaction[0] 


setTotal.aliveElements()
mesh.meltAliveNodes("congela") # Reactiva nodos inactivos.

# Solution
analisis= predefined_solutions.simple_static_linear(prueba)
result= analisis.analyze(1)


nodes.calculateNodalReactions(True)
nodes= preprocessor.getNodeLoader
nod1= nodes.getNode(1)
deltaxB1= nod1.getDisp[0] 
deltayB1= nod1.getDisp[1] 
nod2= nodes.getNode(2)
deltaxB2= nod2.getDisp[0] 
deltayB2= nod2.getDisp[1] 

RB1= nod1.getReaction[0] 
RB2= nod2.getReaction[0] 




ratio1= (R1)
ratio2= ((R2+F)/F)
ratio3= ((RB1+F)/F)
ratio4= (RB2)

''' 
print "R1= ",R1
print "R2= ",R2
print "dx2= ",deltax2
print "dy2= ",deltay2
print "RB1= ",RB1
print "RB2= ",RB2
print "dxB2= ",deltaxB2
print "dyB2= ",deltayB2
print "ratio1= ",ratio1
print "ratio2= ",ratio2
print "ratio3= ",ratio3
print "ratio4= ",ratio4
   '''

import os
fname= os.path.basename(__file__)
if (abs(ratio1)<1e-5) & (abs(ratio2)<1e-5) & (abs(ratio3)<1e-5) & (abs(ratio4)<1e-5):
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."

