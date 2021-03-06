# -*- coding: utf-8 -*-
''' Tomado de la página 114 del artículo Development of Membrane, Plate and
 Flat Shell Elements in Java '''
''' El error obtenido es próximo al 15% (muy alto) parece que el elemento funciona mal
cuando el "aspect ratio" está lejos del cuadrado. '''

L= 6.0 # Longitud de la viga expresada in inches.
h= 0.8 # Canto de la viga expresado in inches.
t= 1 # Ancho de la viga expresado in inches.
E= 30000 # Módulo de Young del material expresado en ksi.
nu= 0.3 # Poisson's ratio.
# Load
F= 10 # Load magnitude en kips

import xc_base
import geom
import xc
from model import predefined_spaces
from solution import predefined_solutions
from materials import typical_materials
from model import fix_node_6dof
# Problem type
prueba= xc.ProblemaEF()
preprocessor=  prueba.getPreprocessor
nodes= preprocessor.getNodeLoader
predefined_spaces.gdls_resist_materiales3D(nodes)
nodes.newNodeIDXYZ(1,0,0,0)
nodes.newNodeIDXYZ(2,L/3,0,0)
nodes.newNodeIDXYZ(3,2*L/3,0,0)
nodes.newNodeIDXYZ(4,L,0,0)
nodes.newNodeIDXYZ(5,0,h,0)
nodes.newNodeIDXYZ(6,L/3,h,0)
nodes.newNodeIDXYZ(7,2*L/3,h,0)
nodes.newNodeIDXYZ(8,L,h,0)


# Materials definition
nmb1= typical_materials.defElasticMembranePlateSection(preprocessor, "memb1",E,nu,0.0,h)

elementos= preprocessor.getElementLoader
elementos.defaultMaterial= "memb1"
elementos.defaultTag= 1
elem= elementos.newElement("shell_mitc4",xc.ID([1,2,6,5]))

elem= elementos.newElement("shell_mitc4",xc.ID([2,3,7,6]))
elem= elementos.newElement("shell_mitc4",xc.ID([3,4,8,7]))

# Constraints
coacciones= preprocessor.getConstraintLoader

fix_node_6dof.Nodo6DOFGirosLibres(coacciones, 1)
spc= coacciones.newSPConstraint(2,2,0.0)
spc= coacciones.newSPConstraint(3,2,0.0)
spc= coacciones.newSPConstraint(4,2,0.0)
fix_node_6dof.Nodo6DOFGirosLibres(coacciones, 5)
spc= coacciones.newSPConstraint(6,2,0.0)
spc= coacciones.newSPConstraint(7,2,0.0)
spc= coacciones.newSPConstraint(8,2,0.0)

# Loads definition
cargas= preprocessor.getLoadLoader

casos= cargas.getLoadPatterns

#Load modulation.
ts= casos.newTimeSeries("constant_ts","ts")
casos.currentTimeSeries= "ts"
#Load case definition
lp0= casos.newLoadPattern("default","0")
lp0.newNodalLoad(8,xc.Vector([0,-F,0,0,0,0]))
#We add the load case to domain.
casos.addToDomain("0")



ele1= elementos.getElement(1)
mat= ele1.getPhysicalProperties.getVectorMaterials[0]
K11A= mat.getTangentStiffness().at(1,1)
import os
os.system("rm -f /tmp/test06.db")
db= prueba.newDatabase("SQLite","/tmp/test06.db")
db.save(2120)
prueba.clearAll()
db.restore(2120)

# Solution
analisis= predefined_solutions.simple_static_linear(prueba)
result= analisis.analyze(1)

elementos= preprocessor.getElementLoader
ele1= elementos.getElement(1)
mat= ele1.getVectorMaterials[0]
K11D= mat.getTangentStiffness().at(1,1)


nodes= preprocessor.getNodeLoader
nod8= nodes.getNode(8)
UX8= nod8.getDisp[0] # Node 8 xAxis displacement
UY8= nod8.getDisp[1] # Node 8 yAxis displacement

nod3= nodes.getNode(3)
UX3= nod3.getDisp[0] # Node 3 xAxis displacement
UY3= nod3.getDisp[1] # Node 3 yAxis displacement

UX8SP2K= 0.016110
UY8SP2K= -0.162735
UX3SP2K= -0.014285
UY3SP2K= -0.084652


# Diferencias respecto a los resultados que, en dicho artículo, atribuyen a SAP-2000
ratio1= abs(((UX8-UX8SP2K)/UX8SP2K))
ratio2= abs(((UY8-UY8SP2K)/UY8SP2K))
ratio3= abs(((UX3-UX3SP2K)/UX3SP2K))
ratio4= abs(((UY3-UY3SP2K)/UY3SP2K))
ratio5= abs(((K11D-K11A)/K11A))

''' 
print "UX8= ",UX8
print "UX8SP2K= ",UX8SP2K
print "UY8= ",UY8
print "UY8SP2K= ",UY8SP2K
print "UX3= ",UX3
print "UY3= ",UY3

print "ratio1= ",ratio1
print "ratio2= ",ratio2
print "ratio3= ",ratio3
print "ratio4= ",ratio4
print "ratio5= ",ratio5
  '''

fname= os.path.basename(__file__)
if (abs(ratio1)<0.15) & (abs(ratio2)<0.15) & (abs(ratio3)<0.15) & (abs(ratio4)<0.15) & (abs(ratio5)<1e-15):
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."
os.system("rm -f /tmp/test06.db") # Your garbage you clean it
