# -*- coding: utf-8 -*-
# home made test

import xc_base
import geom
import xc
import math
from model import predefined_spaces
from materials import typical_materials
from model import fix_node_6dof


E= 2.1e6 # Módulo de Young del acero en kg/cm2.
nu= 0.3 # Poisson's ratio.
h= 0.1 # Espesor.
dens= 1.33 # Densidad kg/m2.


v1= xc.Vector([0,math.sqrt(2)/2,math.sqrt(2)/2])
v2= xc.Vector([0,-math.sqrt(2)/2,math.sqrt(2)/2])

# Problem type
prueba= xc.ProblemaEF()
preprocessor=  prueba.getPreprocessor
nodes= preprocessor.getNodeLoader
predefined_spaces.gdls_resist_materiales3D(nodes)
nodes.newNodeIDXYZ(1,0,0,0)
nodes.newNodeIDXYZ(2,2,0,0)
nodes.newNodeIDXYZ(3,2,1,1)
nodes.newNodeIDXYZ(4,0,1,1)


# Materials definition

memb1= typical_materials.defElasticMembranePlateSection(preprocessor, "memb1",E,nu,dens,h)


elementos= preprocessor.getElementLoader
elementos.defaultMaterial= "memb1"
elem= elementos.newElement("shell_mitc4",xc.ID([1,2,3,4]))

import os
os.system("rm -f /tmp/test04.db")
db= prueba.newDatabase("SQLite","/tmp/test04.db")
db.save(100)
prueba.clearAll()
db.restore(100)

elementos= preprocessor.getElementLoader
elem= elementos.getElement(0)
ratio1= (elem.getCoordTransf.getG2Vector-v1).Norm()
ratio2= (elem.getCoordTransf.getG3Vector-v2).Norm()
#ratio1= abs((abs(elem.getCoordTransf.getG2Vector-v1)))
#ratio2= abs((abs(elem.getCoordTransf.getG3Vector-v2)))




''' 
print "v1= ",v1
print "v2= ",v2
print "ratio1= ",ratio1
print "ratio2= ",ratio2
 '''

import os
fname= os.path.basename(__file__)
if (ratio1 < 1e-12) & (ratio2 < 1e-12):
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."
os.system("rm -f /tmp/test04.db") # Your garbage you clean it

