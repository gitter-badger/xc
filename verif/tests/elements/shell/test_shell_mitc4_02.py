# -*- coding: utf-8 -*-
# home made test

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AOO)"
__copyright__= "Copyright 2015, LCPT and AOO"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

E= 2.1e6 # Módulo de Young del acero.
nu= 0.3 # Poisson's ratio.
h= 0.1 # Espesor.
dens= 1.33 # Densidad kg/m2.

import xc_base
import geom
import xc
from model import predefined_spaces
from materials import typical_materials
import math

prueba= xc.ProblemaEF()
preprocessor=  prueba.getPreprocessor
nodes= preprocessor.getNodeLoader

# Problem type
predefined_spaces.gdls_resist_materiales3D(nodes)
nodes.newNodeIDXYZ(1,0,0,0)
nodes.newNodeIDXYZ(2,2,0,0)
nodes.newNodeIDXYZ(3,2,1,1)
nodes.newNodeIDXYZ(4,0,1,1)


# Materials definition
memb1= typical_materials.defElasticPlateSection(preprocessor, "memb1",E,nu,0,h)

elementos= preprocessor.getElementLoader
elementos.defaultMaterial= "memb1"
elem= elementos.newElement("shell_mitc4",xc.ID([1,2,3,4]))

v1= xc.Vector([0,math.sqrt(2)/2,math.sqrt(2)/2])
v2= xc.Vector([0,-math.sqrt(2)/2,math.sqrt(2)/2])
ratio1= (elem.getCoordTransf.getG2Vector-v1).Norm()
ratio2= (elem.getCoordTransf.getG3Vector-v2).Norm()

''' 
print "ratio1= ",ratio1
print "ratio2= ",ratio2
 '''

import os
fname= os.path.basename(__file__)
if (ratio1 < 1e-12) & (ratio2 < 1e-12):
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."

