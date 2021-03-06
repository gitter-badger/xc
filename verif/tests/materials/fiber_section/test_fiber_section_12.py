# -*- coding: utf-8 -*-
# Test de funcionamiento de una sección de hormigón pretensado.
from __future__ import division

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AOO)"
__copyright__= "Copyright 2015, LCPT and AOO"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"

# prueba.logFileName= "/tmp/borrar.log"  #Para no imprimir mensajes de advertencia.
# Macros
import xc_base
import geom
import xc
from misc import banco_pruebas_scc3d


from materials.ehe import EHE_concrete
from materials.ehe import aceroPretEHE
from materials.fiber_section import createFiberSets
from model import fix_node_6dof
from solution import predefined_solutions

MzDato= 0.0
NDato= 0.0 # La única acción es el pretensado

prueba= xc.ProblemaEF()
preprocessor=  prueba.getPreprocessor
# Materials definition
tag= aceroPretEHE.Y1860S7.defDiagD(preprocessor, aceroPretEHE.Y1860S7.tInic())
tag= EHE_concrete.HP45.defDiagD(preprocessor)
import os
pth= os.path.dirname(__file__)
if(not pth):
  pth= "."
#print "pth= ", pth
execfile(pth+"/secc_hormigon_pret_01.py")
materiales= preprocessor.getMaterialLoader
secHP= materiales.newMaterial("fiber_section_3d","secHP")
fiberSectionRepr= secHP.getFiberSectionRepr()
fiberSectionRepr.setGeomNamed("geomSecHormigonPret01")
secHP.setupFibers()

elem= banco_pruebas_scc3d.modeloSecc3d(preprocessor, "secHP")

# Constraints
coacciones= preprocessor.getConstraintLoader

fix_node_6dof.fixNode6DOF(coacciones,1)
fix_node_6dof.Nodo6DOFMovXGiroZLibres(coacciones,2)

# Loads definition
cargas= preprocessor.getLoadLoader

casos= cargas.getLoadPatterns

#Load modulation.
ts= casos.newTimeSeries("constant_ts","ts")
casos.currentTimeSeries= "ts"
#Load case definition
lp0= casos.newLoadPattern("default","0")
lp0.newNodalLoad(2,xc.Vector([NDato,0,0,0,0,MzDato]))

#We add the load case to domain.
casos.addToDomain("0")


# Procedimiento de solución
analisis= predefined_solutions.simple_newton_raphson(prueba)
analOk= analisis.analyze(10)


nodes= preprocessor.getNodeLoader
nodes.calculateNodalReactions(True)

RN= nodes.getNode(1).getReaction[0] 
RM= nodes.getNode(1).getReaction[5] 
RN2= nodes.getNode(2).getReaction[0] 

elementos= preprocessor.getElementLoader
ele1= elementos.getElement(1)
scc= ele1.getSection()
esfN= scc.getStressResultantComponent("N")
esfMy= scc.getStressResultantComponent("My")
esfMz= scc.getStressResultantComponent("Mz")
defMz= scc.getSectionDeformationByName("defMz")
defN= scc.getSectionDeformationByName("defN")
concrFibers= createFiberSets.FiberSet(scc,"hormigon",EHE_concrete.HP45.matTagD)
fibraCEpsMin= concrFibers.getFiberWithMinStrain()
epsCMin= fibraCEpsMin.getMaterial().getStrain() # Deformación mínima en el hormigón.
fibraCEpsMax= concrFibers.getFiberWithMaxStrain()
epsCMax= fibraCEpsMax.getMaterial().getStrain() # Deformación máxima en el hormigón.
reinfFibers= createFiberSets.FiberSet(scc,"reinforcement",aceroPretEHE.Y1860S7.matTagD)
fibraSEpsMax= reinfFibers.getFiberWithMaxStrain()
epsSMax= fibraSEpsMax.getMaterial().getStrain() # Deformación máxima en el acero

from materials import regimenSeccion
from materials.ehe import comprobTnEHE
tipoSolic= regimenSeccion.tipoSolicitacion(epsCMin,epsSMax)
strTipoSolic= regimenSeccion.strTipoSolicitacion(tipoSolic)
cumpleFT= comprobTnEHE.cumpleFlexotraccion(epsCMin,epsSMax)
aprovSecc= comprobTnEHE.aprovFlexotraccion(epsCMin,epsSMax)

ratio1= RM
ratio2= esfMz
ratio3= (esfN-NDato)
ratio4= (cumpleFT-1)
ratio5= (RN+NDato)

''' 
print "ratio1= ",(ratio1)
print "ratio2= ",(ratio2)
print "ratio3= ",(ratio3)
print "ratio4= ",(ratio4)
print "ratio5= ",(ratio5)

print "Deformación mínima en el hormigón: ",(epsCMin)
print "Deformación máxima en el hormigón: ",(epsCMax)
print "Deformación máxima en la reinforcement: ",(epsSMax)
print "Tipo solicitación: ",strTipoSolic," (",(tipoSolic),") \n"
print "Cumple a ",strTipoSolic,": ",(cumpleFT)
print "Aprovechamiento a ",strTipoSolic,": ",(aprovSecc)
print "RN= ",(RN/1e3),"kN \n"
print "RN2= ",(RN2/1e3)
print "N= ",(esfN/1e3)
print "My= ",(esfMy/1e3)
print "Mz= ",(esfMz/1e3)
print "defMz= ",(defMz)
print "defN= ",(defN)
 '''

import os
fname= os.path.basename(__file__)
if (abs(ratio1)<1e-10) & (abs(ratio2)<1e-10) & (abs(ratio3)<1e-9) & (abs(ratio5)<1e-9) & (abs(RN2)<1e-9) & (abs(esfMy)<1e-10) & (tipoSolic == 2) & (abs(ratio4)<1e-6) & (analOk == 0.0) :
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."
