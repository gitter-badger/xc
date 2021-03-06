# -*- coding: utf-8 -*-
# home made test
#    Prueba del funcionamiento de una hipótesis de retracción.

import xc_base
import geom
import xc
from materials.ehe import EHE_concrete

concrHA30=EHE_concrete.HA30
concrHA30.cemType='N'
fckHA30= 30e6 # Resistencia característica del hormigón HA-30.
Hrel= 0.8 # Humedad relativa del aire.
Ec= 2e5*9.81/1e-4 # Módulo de Young del hormigón en Pa.
nuC= 0.2 # Poisson's ratio del hormigón EHE-08.
hLosa= 0.2 # Espesor.
densLosa= 2500*hLosa # Densidad de la losa kg/m2.
t0= 28 # Edad de puesta en carga del hormigón
tFin= 10000 # Vida útil.
arido= "cuarcita"


# Load
F= 5.5e4 # Load magnitude en N

# Retracción del hormigón
tS= 7 # Inicio del secado.

# Armadura activa
Ep= 190e9 # Elastic modulus expresado en MPa
Ap= 140e-6 # Área de la barra expresada en metros cuadrados
fMax= 1860e6 # Carga unitaria máxima del material expresada en MPa.
fy= 1171e6 # Tensión de límite elástico del material expresada en Pa.
tInic= 0.75**2*fMax # Pretensado final (incial al 75 por ciento y 25 por ciento de pérdidas totales).

import xc_base
import geom
import xc
from solution import predefined_solutions
from model import predefined_spaces
from model import fix_node_6dof
from materials import typical_materials

# Problem type
prueba= xc.ProblemaEF()
preprocessor=  prueba.getPreprocessor
nodes= preprocessor.getNodeLoader
predefined_spaces.gdls_resist_materiales3D(nodes)
nodes.defaultTag= 1 #First node number.
nod1= nodes.newNodeXYZ(0,0,0)
nod2= nodes.newNodeXYZ(1,0,0)
nod3= nodes.newNodeXYZ(2,0,0)
nod4= nodes.newNodeXYZ(3,0,0)
nod5= nodes.newNodeXYZ(0,1,0)
nod6= nodes.newNodeXYZ(1,1,0)
nod7= nodes.newNodeXYZ(2,1,0)
nod8= nodes.newNodeXYZ(3,1,0)
nod9= nodes.newNodeXYZ(0,2,0)
nod10= nodes.newNodeXYZ(1,2,0)
nod11= nodes.newNodeXYZ(2,2,0)
nod12= nodes.newNodeXYZ(3,2,0)


# Materials definition

hLosa= typical_materials.defElasticMembranePlateSection(preprocessor, "hLosa",Ec,nuC,densLosa,hLosa)

aceroPret= typical_materials.defSteel02(preprocessor, "aceroPret",Ep,fy,0.001,tInic)

elementos= preprocessor.getElementLoader
# Losa de hormigón
elementos.defaultMaterial= "hLosa"
elementos.defaultTag= 1
elem= elementos.newElement("shell_mitc4",xc.ID([1,2,6,5]))

elem= elementos.newElement("shell_mitc4",xc.ID([2,3,7,6]))
elem= elementos.newElement("shell_mitc4",xc.ID([3,4,8,7]))
elem= elementos.newElement("shell_mitc4",xc.ID([5,6,10,9]))
elem= elementos.newElement("shell_mitc4",xc.ID([6,7,11,10]))
elem= elementos.newElement("shell_mitc4",xc.ID([7,8,12,11]))

# Armadura activa
elementos.defaultMaterial= "aceroPret"
elementos.dimElem= 3
truss= elementos.newElement("truss",xc.ID([1,2]));
truss.area= Ap
truss= elementos.newElement("truss",xc.ID([2,3]));
truss.area= Ap
truss= elementos.newElement("truss",xc.ID([3,4]));
truss.area= Ap
truss= elementos.newElement("truss",xc.ID([5,6]));
truss.area= Ap
truss= elementos.newElement("truss",xc.ID([6,7]));
truss.area= Ap
truss= elementos.newElement("truss",xc.ID([7,8]));
truss.area= Ap
truss= elementos.newElement("truss",xc.ID([9,10]));
truss.area= Ap
truss= elementos.newElement("truss",xc.ID([10,11]));
truss.area= Ap
truss= elementos.newElement("truss",xc.ID([11,12]));
truss.area= Ap

# Constraints
coacciones= preprocessor.getConstraintLoader

fix_node_6dof.fixNode6DOF(coacciones,1)
fix_node_6dof.fixNode6DOF(coacciones,5)
fix_node_6dof.fixNode6DOF(coacciones,9)

# Loads definition
cargas= preprocessor.getLoadLoader

casos= cargas.getLoadPatterns

#Load modulation.
ts= casos.newTimeSeries("constant_ts","ts")
casos.currentTimeSeries= "ts"

lpRETRACC= casos.newLoadPattern("default","RETRACC")
lpFLU= casos.newLoadPattern("default","FLU")

lpG= casos.newLoadPattern("default","G")
lpSC= casos.newLoadPattern("default","SC")
lpVT= casos.newLoadPattern("default","VT")
lpNV= casos.newLoadPattern("default","NV")

nodes= preprocessor.getNodeLoader
nod4= nodes.getNode(4)
nod8= nodes.getNode(8)
nod12= nodes.getNode(12)
lpG.newNodalLoad(nod4.tag,xc.Vector([F,0.0,0.0,0.0,0.0,0.0]))
lpG.newNodalLoad(nod8.tag,xc.Vector([F,0.0,0.0,0.0,0.0,0.0]))
lpG.newNodalLoad(nod12.tag,xc.Vector([F,0.0,0.0,0.0,0.0,0.0]))

lpSC.newNodalLoad(nod4.tag,xc.Vector([F,0.0,0.0,0.0,0.0,0.0]))
lpSC.newNodalLoad(nod8.tag,xc.Vector([F,0.0,0.0,0.0,0.0,0.0]))
lpSC.newNodalLoad(nod12.tag,xc.Vector([F,0.0,0.0,0.0,0.0,0.0]))

lpVT.newNodalLoad(nod4.tag,xc.Vector([F,0.0,0.0,0.0,0.0,0.0]))
lpVT.newNodalLoad(nod8.tag,xc.Vector([F,0.0,0.0,0.0,0.0,0.0]))
lpVT.newNodalLoad(nod12.tag,xc.Vector([F,0.0,0.0,0.0,0.0,0.0]))

lpNV.newNodalLoad(nod4.tag,xc.Vector([F,0.0,0.0,0.0,0.0,0.0]))
lpNV.newNodalLoad(nod8.tag,xc.Vector([F,0.0,0.0,0.0,0.0,0.0]))
lpNV.newNodalLoad(nod12.tag,xc.Vector([F,0.0,0.0,0.0,0.0,0.0]))


# Combinaciones
combs= cargas.getLoadCombinations
comb= combs.newLoadCombination("ELU001","1.00*G")
comb= combs.newLoadCombination("ELU002","1.35*G")
comb= combs.newLoadCombination("ELU003","1.00*G + 1.50*SC")
comb= combs.newLoadCombination("ELU004","1.00*G + 1.50*SC + 0.90*NV")
comb= combs.newLoadCombination("ELU005","1.00*G + 1.50*SC + 0.90*VT")
comb= combs.newLoadCombination("ELU006","1.00*G + 1.50*SC + 0.90*VT + 0.90*NV")
comb= combs.newLoadCombination("ELU007","1.00*G + 1.50*VT")
comb= combs.newLoadCombination("ELU008","1.00*G + 1.50*VT + 0.90*NV")
comb= combs.newLoadCombination("ELU009","1.00*G + 1.05*SC + 1.50*VT")
comb= combs.newLoadCombination("ELU010","1.00*G + 1.05*SC + 1.50*VT + 0.90*NV")
comb= combs.newLoadCombination("ELU011","1.00*G + 1.50*NV")
comb= combs.newLoadCombination("ELU012","1.00*G + 0.90*VT + 1.50*NV")
comb= combs.newLoadCombination("ELU013","1.00*G + 1.05*SC + 1.50*NV")
comb= combs.newLoadCombination("ELU014","1.00*G + 1.05*SC + 0.90*VT + 1.50*NV")
comb= combs.newLoadCombination("ELU015","1.35*G + 1.50*SC")
comb= combs.newLoadCombination("ELU016","1.35*G + 1.50*SC + 0.90*NV")
comb= combs.newLoadCombination("ELU017","1.35*G + 1.50*SC + 0.90*VT")
comb= combs.newLoadCombination("ELU018","1.35*G + 1.50*SC + 0.90*VT + 0.90*NV")
comb= combs.newLoadCombination("ELU019","1.35*G + 1.50*VT")
comb= combs.newLoadCombination("ELU020","1.35*G + 1.50*VT + 0.90*NV")
comb= combs.newLoadCombination("ELU021","1.35*G + 1.05*SC + 1.50*VT")
comb= combs.newLoadCombination("ELU022","1.35*G + 1.05*SC + 1.50*VT + 0.90*NV")
comb= combs.newLoadCombination("ELU023","1.35*G + 1.50*NV")
comb= combs.newLoadCombination("ELU024","1.35*G + 0.90*VT + 1.50*NV")
comb= combs.newLoadCombination("ELU025","1.35*G + 1.05*SC + 1.50*NV")
comb= combs.newLoadCombination("ELU026","1.35*G + 1.05*SC + 0.90*VT + 1.50*NV")



#printFlag= 0
#ctest.printFlag= printFlag
analysis= predefined_solutions.penalty_newton_raphson(prueba)

from solution import database_helper

def resuelveCombEstatLin(tagComb,comb,tagSaveFase0):
  preprocessor.resetLoadCase()
  db.restore(tagSaveFase0)

  #execfile("solution/database_helper_solve.xci")

  ''' 
  print "nombrePrevia= ",nombrePrevia
  print "tag= ",tagComb
  print "tagPrevia= ",tagPrevia
  print "descomp previa= ",getDescompCombPrevia
  print "resto sobre previa= ",getDescompRestoSobrePrevia
  '''

  comb.addToDomain()
  result= analysis.analyze(1)
  db.save(tagComb*100)
  comb.removeFromDomain()


dXMin=1e9
dXMax=-1e9

def procesResultVerif(tagComb, nmbComb):
  nodes= preprocessor.getNodeLoader
  nod8= nodes.getNode(8)
  deltaX= nod8.getDisp[0] # Desplazamiento del node 2 según z
  global dXMin; dXMin= min(dXMin,deltaX)
  global dXMax; dXMax= max(dXMax,deltaX)
  ''' 
  print "nmbComb= ",nmbComb
  print "tagComb= ",tagComb
  print "descomp= ",getDescomp("%3.1f")
  print "dXMin= ",(dXMin*1e3)," mm\n"
  print "dXMax= ",(dXMax*1e3)," mm\n"
   '''
import os
os.system("rm -r -f /tmp/test_retraccion_02.db")
db= prueba.newDatabase("BerkeleyDB","/tmp/test_retraccion_02.db")

# Fase 0: pretensado, retracción
# Fase 1: pretensado, retracción y fluencia

# Shrinkage strains.
sets= preprocessor.getSets

shells= preprocessor.getSets.defSet("shells")

elements= preprocessor.getSets.getSet("total").getElements
for e in elements:
  dim= e.getDimension
  if(dim==2):
    shells.getElements.append(e)

shellElems= shells.getElements
for e in shellElems:
  ladoMedio= e.getPerimeter(True)/4.0
  material= e.getPhysicalProperties.getVectorMaterials[0]
  grueso= material.h
  Ac= ladoMedio*grueso
  u= 2*ladoMedio+grueso
  espMedio= 2.0*Ac/u
  RH=Hrel*100
  h0mm=espMedio*1e3
  epsRetracc= concrHA30.getShrEpscs(tFin,tS,RH,h0mm)


#cargas.setCurrentLoadPattern("RETRACC")

for e in shellElems:
  eleLoad= lpRETRACC.newElementalLoad("shell_strain_load")
  eleLoad.elementTags= xc.ID([e.tag]) 
  eleLoad.setStrainComp(0,0,epsRetracc) #(id of Gauss point, id of component, value)
  eleLoad.setStrainComp(1,0,epsRetracc)
  eleLoad.setStrainComp(2,0,epsRetracc)
  eleLoad.setStrainComp(3,0,epsRetracc)
  eleLoad.setStrainComp(0,1,epsRetracc) #(id of Gauss point, id of component, value)
  eleLoad.setStrainComp(1,1,epsRetracc)
  eleLoad.setStrainComp(2,1,epsRetracc)
  eleLoad.setStrainComp(3,1,epsRetracc)


preprocessor.resetLoadCase()

comb= combs.newLoadCombination("FASE0","1.00*RETRACC")
tagSaveFase0= comb.tag*100
comb.addToDomain()
result= analysis.analyze(1)
combs.remove("FASE0")  # Para que no siga añadiendo retracción en cada cálculo.
db.save(tagSaveFase0)




db.restore(tagSaveFase0)

nombrePrevia="" 
tagPrevia= 0 
tagSave= 0
for key in combs.getKeys():
  comb= combs[key]
  resuelveCombEstatLin(comb.tag,comb,tagSaveFase0)
  procesResultVerif(comb.tag,comb.getName)

dXMaxTeor= -0.752509e-3
ratio1= abs(((dXMax-dXMaxTeor)/dXMaxTeor))
dXMinTeor= -0.955324e-3
ratio2= abs(((dXMin-dXMinTeor)/dXMinTeor))

#''' 
print "dXMax= ",(dXMax*1e3)," mm"
print "dXMaxTeor= ",(dXMaxTeor*1e3)," mm"
print "ratio1= ",ratio1
print "dXMin= ",(dXMin*1e3)," mm"
print "dXMinTeor= ",(dXMinTeor*1e3)," mm"
print "ratio2= ",ratio2
#   '''

import os
fname= os.path.basename(__file__)
if (ratio1<1e-5) & (ratio2<1e-5) :
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."

os.system("rm -r -f /tmp/test_retraccion_02.db") # Your garbage you clean it
