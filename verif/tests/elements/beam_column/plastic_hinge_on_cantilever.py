# -*- coding: utf-8 -*-
# home made test

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AOO)"
__copyright__= "Copyright 2015, LCPT and AOO"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

# Testing hinge development in a cantilever.

import xc_base
import geom
import xc

from materials.perfiles_metalicos.arcelor import perfiles_ipe_arcelor as ipe
from materials import aceros_estructurales as steel
from model import predefined_spaces
from model import fix_node_3dof
from solution import predefined_solutions

test= xc.ProblemaEF()
preprocessor=  test.getPreprocessor

S355JR= steel.S355JR
S355JR.gammaM= 1.05
epp= S355JR.getDesignElasticPerfectlyPlasticMaterial(preprocessor, "epp")
IPE200= ipe.IPEProfile(S355JR,'IPE_200')
fs3d= IPE200.getFiberSection3d(preprocessor,'epp')

L= 1.0
nodes= preprocessor.getNodeLoader
predefined_spaces.gdls_resist_materiales2D(nodes)
nodes.defaultTag= 1 #First node number.
nod= nodes.newNodeXY(0,0.0)
nod= nodes.newNodeXY(L,0.0)

# Geometric transformations
trfs= preprocessor.getTransfCooLoader
lin= trfs.newLinearCrdTransf2d("lin")

# Elements definition
elementos= preprocessor.getElementLoader
elementos.defaultTransformation= "lin" # Transformación de coordenadas para los nuevos elementos
elementos.defaultMaterial= IPE200.fiberSection3dName
beam2d= elementos.newElement("force_beam_column_2d",xc.ID([1,2]));

# Constraints
coacciones= preprocessor.getConstraintLoader
fix_node_3dof.fixNode000(coacciones,1)

# Loads definition
WzplTeor= IPE200.get('Wzpl')
M0Teor= -WzplTeor*S355JR.fyd()
F= M0Teor*0.87
cargas= preprocessor.getLoadLoader
casos= cargas.getLoadPatterns
#Load modulation.
ts= casos.newTimeSeries("constant_ts","ts")
casos.currentTimeSeries= "ts"
#Load case definition
lp0= casos.newLoadPattern("default","0")
lp0.newNodalLoad(2,xc.Vector([0,F,0]))
#We add the load case to domain.
casos.addToDomain("0")

# Procedimiento de solución
analisis= predefined_solutions.simple_static_modified_newton(test)
result= analisis.analyze(10)

elem1= elementos.getElement(0)
elem1.getResistingForce()
scc= elem1.getSections()[0]
M0= scc.getStressResultantComponent("Mz")
M= F*L
ratio1= (M0-M)/M
ratio2= (M0-M0Teor)/M0Teor

'''
print 'M0Teor= ', M0Teor/1e3, ' kNm'
print 'M0= ', M0/1e3, ' kNm'
print 'M= ', M/1e3, ' kNm'
print 'ratio1= ', ratio1
print 'ratio2= ', ratio2
'''

import os
fname= os.path.basename(__file__)
if (ratio1<1e-12) & (ratio2<0.2):
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."
