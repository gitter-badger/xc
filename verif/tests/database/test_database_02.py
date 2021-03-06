# -*- coding: utf-8 -*-
# home made test
# Comprobación de los comandos save y restore.

import xc_base
import geom
import xc
from model import predefined_spaces
from solution import predefined_solutions
from materials import typical_materials
from model import fix_node_6dof

# Material properties
E= 2.1e6*9.81/1e-4 # Elastic modulus (Pa)
nu= 0.3 # Poisson's ratio
G= E/(2*(1+nu)) # Shear modulus

# Cross section properties (IPE-80)
A= 7.64e-4 # Cross section area (m2)
Iy= 80.1e-8 # Cross section moment of inertia (m4)
Iz= 8.49e-8 # Cross section moment of inertia (m4)
J= 0.721e-8 # Cross section torsion constant (m4)

# Geometry
L= 1.5 # Bar length (m)

# Load
F= 1.5e3 # Load magnitude (kN)

prueba= xc.ProblemaEF()
preprocessor=  prueba.getPreprocessor   
nodes= preprocessor.getNodeLoader

# Problem type
predefined_spaces.gdls_resist_materiales3D(nodes)
nodes.defaultTag= 1 #First node number.
nod= nodes.newNodeXYZ(0,0.0,0.0)
nod= nodes.newNodeXYZ(L,0.0,0.0)

trfs= preprocessor.getTransfCooLoader
lin= trfs.newLinearCrdTransf3d("lin")
lin.xzVector= xc.Vector([0,1,0])
    
# Materials definition
scc= typical_materials.defElasticSection3d(preprocessor, "scc",A,E,G,Iz,Iy,J)


elementos= preprocessor.getElementLoader
elementos.defaultTransformation= "lin"
elementos.defaultMaterial= "scc"
#  sintaxis: elastic_beam_3d[<tag>] 
elementos.defaultTag= 1 #Tag for next element.
beam3d= elementos.newElement("elastic_beam_3d",xc.ID([1,2]));

coacciones= preprocessor.getConstraintLoader

fix_node_6dof.fixNode6DOF(coacciones,1)

cargas= preprocessor.getLoadLoader

casos= cargas.getLoadPatterns

#Load modulation.
ts= casos.newTimeSeries("constant_ts","ts")
casos.currentTimeSeries= "ts"
#Load case definition
lp0= casos.newLoadPattern("default","0")
lp0.newNodalLoad(2,xc.Vector([F,0,0,0,0,0]))
#We add the load case to domain.
casos.addToDomain("0")


import os
os.system("rm -f /tmp/test02.db")
db= prueba.newDatabase("SQLite","/tmp/test02.db")
db.save(100)
prueba.clearAll()
db.restore(100)

# Solution
analisis= predefined_solutions.simple_static_linear(prueba)
result= analisis.analyze(1)


nodes= preprocessor.getNodeLoader
 
nod2= nodes.getNode(2)
delta= nod2.getDisp[0] # Node 2 xAxis displacement

elem1= elementos.getElement(1)
elem1.getResistingForce()
N1= elem1.getN1

deltateor= (F*L/(E*A))
ratio1= (delta/deltateor)
ratio2= (N1/F)

''' 
print "delta= ",delta
print "deltateor= ",deltateor
print "ratio1= ",ratio1
print "N1= ",N1
print "ratio2= ",ratio2
   '''

fname= os.path.basename(__file__)
if (abs(ratio1-1.0)<1e-5) & (abs(ratio2-1.0)<1e-5):
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."

os.system("rm -f /tmp/test02.db") # Your garbage you clean it
