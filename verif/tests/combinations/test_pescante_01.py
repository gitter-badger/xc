# -*- coding: utf-8 -*-

from __future__ import division

b= 0.4
h= 0.8
A= b*h
E= 200000*9.81/1e-4 # Elastic modulus aproximado del hormigón.
nu= 0.3 # Poisson's ratio
G= E/(2.0*(1+nu)) # Shear modulus
Iy= (1/12.0*h*b**3) # Cross section moment of inertia (m4)
Iz= (1/12.0*b*h**3) # Cross section moment of inertia (m4)
J= 0.721e-8 # Cross section torsion constant (m4)
densHorm= 2500 # Densidad del hormigón armado.

import xc_base
import geom
import xc
from solution import predefined_solutions
from model import predefined_spaces
from model import fix_node_6dof
from materials import typical_materials
from solution import resuelve_combinacion

#
#     3   2     4
#     ----|------
#         |
#         |
#         |
#         |1
#

# Problem type
prueba= xc.ProblemaEF()
preprocessor=  prueba.getPreprocessor
nodes= preprocessor.getNodeLoader
predefined_spaces.gdls_resist_materiales3D(nodes)
nodes.defaultTag= 1 #First node number.
nod= nodes.newNodeXYZ(2.0,0.0,0.0)
nod= nodes.newNodeXYZ(2.0,0.0,4.0)
nod= nodes.newNodeXYZ(0.0,0.0,4.0)
nod= nodes.newNodeXYZ(5.0,0.0,4.0)

trfs= preprocessor.getTransfCooLoader
lin= trfs.newLinearCrdTransf3d("lin")
lin.xzVector= xc.Vector([0,1,0])
    
# Materials definition
scc= typical_materials.defElasticSection3d(preprocessor, "scc",A,E,G,Iz,Iy,J)


# Elements definition
elementos= preprocessor.getElementLoader
elementos.defaultTransformation= "lin"
elementos.defaultMaterial= "scc"
elementos.defaultTag= 1
#  sintaxis: elastic_beam_3d[<tag>]
beam1= elementos.newElement("elastic_beam_3d",xc.ID([1,2]))
beam1.rho= densHorm*A
beam2= elementos.newElement("elastic_beam_3d",xc.ID([3,2])) 
beam2.rho= densHorm*A
beam3= elementos.newElement("elastic_beam_3d",xc.ID([2,4])) 
beam3.rho= densHorm*A

# Constraints
coacciones= preprocessor.getConstraintLoader

fix_node_6dof.fixNode6DOF(coacciones,1)

# Loads definition
cargas= preprocessor.getLoadLoader

casos= cargas.getLoadPatterns

#Load modulation.
ts= casos.newTimeSeries("constant_ts","ts")
casos.currentTimeSeries= "ts"

# Peso propio
lpG= casos.newLoadPattern("default","G") 
# Sobrecarga de uso
lpSC= casos.newLoadPattern("default","SC") 
# Viento
lpVT= casos.newLoadPattern("default","VT") 
# Nieve
lpNV= casos.newLoadPattern("default","NV") 

casos.currentLoadPattern= "G"
elementos= preprocessor.getSets.getSet("total").getElements
for e in elementos:
  pesoElem= (e.rho*(-10))
  e.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,pesoElem]))

beam2.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-22e3]))
beam3.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-22e3]))

casos.currentLoadPattern= "SC"

beam3.vector3dPointByRelDistLoadGlobal(0.99,xc.Vector([0.0,0.0,-100e3]))

casos.currentLoadPattern= "VT"
lpVT.newNodalLoad(3,xc.Vector([50e3,0.0,0.0,0.0,0.0,0.0]))

casos.currentLoadPattern= "NV"
beam2.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-10e3]))
beam3.vector3dUniformLoadGlobal(xc.Vector([0.0,0.0,-10e3]))

# Combinaciones
combs= cargas.getLoadCombinations
import os
pth= os.path.dirname(__file__)
#print "pth= ", pth
if(not pth):
  pth= "."
execfile(pth+"/../aux/def_hip_elu.py")

NMin1= 6.023e23
NMin2= 6.023e23

def procesResultVerif(nmbComb):
  elementos= preprocessor.getElementLoader
  elem1= elementos.getElement(1)
  elem1.getResistingForce()
  N1= elem1.getN1
  global NMin1
  NMin1=min(NMin1,N1)
  global NMin2
  NMin2=min(NMin2,elem1.getN2)



NMin1= 1e9
NMin2= 1e9
numSteps= 1

# Lanzamos la obtención de soluciones.
analysis= predefined_solutions.simple_static_linear(prueba)
from solution import resuelve_combinacion as rc

for key in combs.getKeys():
  rc.resuelveComb(preprocessor, key,analysis,numSteps)
  procesResultVerif(key)

NMin1Teor= 440.7e3
NMin2Teor= 397.5e3
ratio1= ((NMin1+NMin1Teor)/NMin1Teor)
ratio2= ((NMin2+NMin2Teor)/NMin2Teor)

''' 
print "NMin1= ",NMin1/1e3
print "NMin1Teor= ",NMin1Teor/1e3
print "ratio1= ",ratio1
print "NMin2= ",NMin2/1e3
print "NMin2Teor= ",NMin2Teor/1e3
print "ratio2= ",ratio2
 '''


import os
fname= os.path.basename(__file__)
if (abs(ratio1)<1e-8) & (abs(ratio2)<1e-8):
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."
