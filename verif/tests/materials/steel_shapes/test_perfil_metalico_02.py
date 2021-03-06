# -*- coding: utf-8 -*-
# home made test
# Mésula sometida a carga vertical en su extremo.

import xc_base
import geom
import xc
from solution import predefined_solutions
from model import predefined_spaces
from model import fix_node_6dof
from materials import typical_materials
from materials.perfiles_metalicos.arcelor import perfiles_he_arcelor as HE_profiles
from materials import paramMetallicProfile
from materials import aceros_estructurales as steel
from materials import steelProfile
from materials import aceros_estructurales as steel
from postprocess import def_params_control as dp
from postprocess import def_vars_control as vc
from postprocess import callback_controls as cc

# Geometry
L= 10 # Bar length (m)

# Load
F= 50e3 # Load magnitude (kN)

# Perfil que forma la ménsula
S275JR= steel.S275JR
gammaM0= 1.05
S275JR.gammaM= gammaM0 
HE400B= steelProfile.SteelProfile(S275JR,"HE_400_B",HE_profiles.perfilesHE)
matHE400B=typical_materials.MaterialData(name='S275JR',E=S275JR.E,nu=S275JR.nu,rho=7850)

# Problem type
prueba= xc.ProblemaEF()
preprocessor=  prueba.getPreprocessor   
nodes= preprocessor.getNodeLoader
predefined_spaces.gdls_resist_materiales3D(nodes)
nodes.defaultTag= 1 #First node number.
nod= nodes.newNodeXYZ(0,0.0,0.0)
nod= nodes.newNodeXYZ(L,0.0,0.0)

# Geometric transformations
trfs= preprocessor.getTransfCooLoader
lin= trfs.newLinearCrdTransf3d("lin")
lin.xzVector= xc.Vector([0,0,1])
profil= HE400B.defSeccShElastica3d(preprocessor,matHE400B)

# Elements definition
elementos= preprocessor.getElementLoader
elementos.defaultTransformation= "lin"
elementos.defaultMaterial= HE400B.nmb
elem= elementos.newElement("elastic_beam_3d",xc.ID([1,2]))
elem.rho= HE400B.get('P')
dp.defParamsPerfilMetalicoRegElasticoElem(elem,HE400B)
vc.defVarsControlTensRegElastico3d([elem])

recorder= prueba.getDomain.newRecorder("element_prop_recorder",None);
recorder.setElements(xc.ID([0]))
recorder.callbackRecord= cc.controTensRecElastico3d()


# Constraints
coacciones= preprocessor.getConstraintLoader
fix_node_6dof.fixNode6DOF(coacciones,1)

# Loads definition
cargas= preprocessor.getLoadLoader
casos= cargas.getLoadPatterns
#Load modulation.
ts= casos.newTimeSeries("constant_ts","ts")
casos.currentTimeSeries= "ts"
lp0= casos.newLoadPattern("default","0") 
lp0.newNodalLoad(2,xc.Vector([0,0,-F,0,0,0]))
#We add the load case to domain.
casos.addToDomain("0")

# Solution
analisis= predefined_solutions.simple_static_linear(prueba)
result= analisis.analyze(1)


nodes= preprocessor.getNodeLoader 
nod2= nodes.getNode(2)
delta= nod2.getDisp[2]  # Node 2 yAxis displacement

elementos= preprocessor.getElementLoader

elem0= elementos.getElement(0)
elem0.getResistingForce()
M= elem0.getMy1
V= elem0.getVz
FC= elem0.getProp("FCTN")



EI=  HE400B.EIy()
deltateor= F*L**3/3/EI
ratio1= (abs(delta+deltateor)/deltateor)
ratio2= ((M-F*L)/(F*L))
ratio3= ((F-V)/F)
ratio4= ((FC-2.64674)/2.64674)

'''   
print "delta= ",delta
print "deltaTeor= ",deltateor
print "ratio1= ",ratio1
print "M= ",M
print "ratio2= ",ratio2
print "V1= ",V
print "ratio3= ",ratio3
print "FC= ",FC
print "ratio4= ",ratio4
'''

cumple= (abs(ratio1)<1e-8) & (abs(ratio2)<1e-10) & (abs(ratio3)<1e-10) & (abs(ratio4)<1e-5)
import os
fname= os.path.basename(__file__)
if cumple:
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."
