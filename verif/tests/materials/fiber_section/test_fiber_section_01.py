# -*- coding: utf-8 -*-
''' Test de funcionamiento de una sección metálica rectangular de fibras de material elastoplástico.
   elaborado a partir de «Nociones de cálculo plástico». C. Benito Hernández.
   página 26 y siguientes. '''

import xc_base
import geom
import xc
from model import predefined_spaces
from solution import predefined_solutions
from materials import typical_materials
from materials import sccRectg

prueba= xc.ProblemaEF()
preprocessor=  prueba.getPreprocessor
prueba.logFileName= "/tmp/borrar.log" # Para no imprimir mensajes de advertencia.

# Rectangular cross-section definition
scc10x20= sccRectg.sccRectang()
scc10x20.b= 10 # Cross section width  [cm]
scc10x20.h= 20 # Cross section height [cm]
scc10x20.nDivIJ= 32
scc10x20.nDivJK= 32

import os
pth= os.path.dirname(__file__)
if(not pth):
  pth= "."
#print "pth= ", pth
execfile(pth+"/macros_test_fiber_section.py")

fy= 2600 # Tensión de cedencia del material expresada en kp/cm2.
E= 2.1e6 # Módulo de Young del material en kp/cm2.

# Materials definition:
epp= typical_materials.defElasticPPMaterial(preprocessor, "epp",E,fy,-fy)

# Section geometry
# creation
geomRectang= preprocessor.getMaterialLoader.newSectionGeometry("geomRectang")
#generation of a quadrilateral region of the scc10x20 sizes and number of
#divisions made of material nmbMat
reg= scc10x20.discretization(gm=geomRectang,nmbMat="epp")
rectang= preprocessor.getMaterialLoader.newMaterial("fiber_section_3d","rectang")
fiberSectionRepr= rectang.getFiberSectionRepr()
fiberSectionRepr.setGeomNamed("geomRectang")
rectang.setupFibers()
fibras= rectang.getFibers()


extraeParamSccFibras(rectang,scc10x20)
curvM= 0.005
rectang.setTrialSectionDeformation(xc.Vector([0.0,curvM,0.0]))
rectang.commitState()
Mp1= rectang.getStressResultantComponent("Mz")
rectang.revertToStart()

curvM= 0.008
rectang.setTrialSectionDeformation(xc.Vector([0.0,0.0,curvM]))
rectang.commitState()
Mp2= rectang.getStressResultantComponent("My")

yCdgTeor= 0.0
zCdgTeor= 0.0
ratio1= ((sumAreas-scc10x20.area())/scc10x20.area())
ratio2= (yCdg-yCdgTeor)
ratio3= (zCdg-zCdgTeor)
ratio4= ((I1-scc10x20.I1())/scc10x20.I1())
ratio5= ((I2-scc10x20.I2())/scc10x20.I2())
ratio6= (i1-scc10x20.i1())/scc10x20.i1()
ratio7= (i2-scc10x20.i2())/scc10x20.i2()
ratio8= (Me1-scc10x20.Me1(fy))/scc10x20.Me1(fy)
ratio9= (Me2-scc10x20.Me2(fy))/scc10x20.Me2(fy)
ratio10= (SzPosG-scc10x20.S1PosG())/scc10x20.S1PosG()
ratio11= (SyPosG-scc10x20.S2PosG())/scc10x20.S2PosG()
ratio12= ((scc10x20.Mp1(fy)-Mp1)/scc10x20.Mp1(fy))
ratio13= (scc10x20.Mp2(fy)-Mp2)/scc10x20.Mp2(fy)

'''
    \printRatios()
print "ratio12= ",ratio12
'''

fname= os.path.basename(__file__)
if (abs(ratio1)<1e-5) & (abs(ratio2)<1e-5) & (abs(ratio3)<1e-5) & (abs(ratio4)<1e-3) & (abs(ratio5)<1e-2) & (abs(ratio6)<1e-3) & (abs(ratio7)<1e-2) & (abs(ratio8)<1e-3) & (abs(ratio9)<1e-3) & (abs(ratio10)<1e-5) & (abs(ratio11)<1e-5) & (abs(ratio12)<1e-5) & (abs(ratio13)<1e-5):
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."
