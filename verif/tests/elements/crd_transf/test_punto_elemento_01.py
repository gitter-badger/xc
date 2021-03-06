# -*- coding: utf-8 -*-

from __future__ import division
import xc_base
import geom
import xc
from solution import predefined_solutions
from model import predefined_spaces
from model import fix_node_6dof
from materials import typical_materials

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AOO)"
__copyright__= "Copyright 2015, LCPT and AOO"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

b= 0.4
h= 0.8
A= b*h
E= 200000*9.81/1e-4 # Elastic modulus aproximado del hormigón.
nu= 0.3 # Poisson's ratio
G= E/(2*(1+nu)) # Shear modulus
Iy= (1/12.0*h*b**3) # Cross section moment of inertia (m4)
Iz= (1/12.0*b*h**3) # Cross section moment of inertia (m4)
J= 0.721e-8 # Cross section torsion constant (m4)
L= 5 # Longitud del elmento expresada en metros.

# Problem type
prueba= xc.ProblemaEF()
preprocessor=  prueba.getPreprocessor
nodes= preprocessor.getNodeLoader
predefined_spaces.gdls_resist_materiales3D(nodes)
nodes.defaultTag= 1 #First node number.
nod= nodes.newNodeXYZ(1.0,2.0,0.0)
nod= nodes.newNodeXYZ(1.0,2.0,L)


trfs= preprocessor.getTransfCooLoader
lin= trfs.newLinearCrdTransf3d("lin")
lin.xzVector= xc.Vector([0,1,0])

# Elements definition
elementos= preprocessor.getElementLoader

# Materials
caracMecSeccion= xc.CrossSectionProperties3d()
caracMecSeccion.A= A; caracMecSeccion.E= E; caracMecSeccion.G= G;
caracMecSeccion.Iz= Iz; caracMecSeccion.Iy= Iy; caracMecSeccion.J= J
seccion= typical_materials.defElasticSectionFromMechProp3d(preprocessor, "seccion",caracMecSeccion)

elementos.defaultTransformation= "lin"
#  sintaxis: elastic_beam_3d[<tag>] 
elementos.defaultMaterial= "seccion"
elementos.defaultTag= 1 #Tag for the next element.
beam3d= elementos.newElement("elastic_beam_3d",xc.ID([1,2]));



crdTransf= beam3d.getCoordTransf
P1= crdTransf.getPointGlobalCoordFromLocal(xc.Vector([0.5,0.0,0.0]))
P2= crdTransf.getPointGlobalCoordFromBasic(0.5)

ratio1= (P1-xc.Vector([1,2,0.5])).Norm()
ratio2= (P2-xc.Vector([1,2,2.5])).Norm()

''' 
print "P1: ",P1
print "P2: ",P2
print "ratio1= ",ratio1
print "ratio2= ",ratio2
  '''

import os
fname= os.path.basename(__file__)
if (ratio1 < 1e-15) & (ratio2 < 1e-15):
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."
