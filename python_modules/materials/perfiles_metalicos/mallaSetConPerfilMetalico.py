# -*- coding: utf-8 -*-
'''
Genera elementos de tipo «ElasticBeam3d» para las líneas
   del conjunto que se pasa como parámetro. El conjunto ha de tener
   definidos las siguientes variables:
   - nmbPerfil: Nombre del perfil a emplear (por ejemplo L50x50x5)
   - nmbGeomTransf: Nombre de la transformación geométrica a emplear.
   - numDivisiones: Número de elementos a generar en cada línea.
'''
def mallaSetConPerfilMetalico(preprocessor,setName):
  nmbPerfilMet= "" 
  nmbTrf= ""
  nmbTipoAcero= ""
  sectionName= ""
  setElems= preprocessor.getSetLoader.getSet(setName)
  nmbPerfilMet= setElems.getProp(nmbPerfil)
  nmbTipoAcero= setElems.getProp(nmbAcero)
  nmbTrf= setElems.getProp(nmbGeomTransf)

  sectionName= nmbPerfilMet+"_"+nmbGeomTransf
  defSeccPerfilMetalicoShElastica3d(nmbPerfilMet,sectionName)
  seedElemLoader= preprocessor.getElementLoader.seedElemLoader
  seedElemLoader.defaultMaterial= sectionName
  seedElemLoader.defaultTransformation= nmbTrf
  elem= seedElemLoader.newElement("elastic_beam_3d",xc.ID([0,0]))
  elem.rho= nmbPerfilMet.P
  defParamsPerfilMetalicoRegElasticoSet(elem,nmbPerfilMet)
  lines= setElems.getLines
  for l in lines:
    l.nDiv= numDivisiones
  setElems.genMesh(xc.meshDir,1)
  

'''
Genera elementos de tipo «Truss» para las líneas
   del conjunto que se pasa como parámetro. El conjunto ha de tener
   definidos las siguientes variables:
   - nmbPerfil: Nombre del perfil a emplear (por ejemplo L50x50x5)
   - numDivisiones: Número de elementos a generar en cada línea.
'''
def mallaSetConTruss(setName):
  nmbPerfilMet= "" 
  nmbTipoAcero= ""
  nmbMat= ""
  fydMat= 0.0 
  EMat= 0.0 
  
  setElems= preprocessor.getSetLoader.getSet(setName)
  nmbPerfilMet= setElems.getProp("nmbPerfil")
  nmbTipoAcero= setElems.getProp("nmbAcero")
  gammaMat= setElems.getProp("gammaM")
  areaBrr= nmbPerfilMet.A

  nmbMat= setName+"_"+nmbPerfilMet.nmbTipoAcero
  fydMat= nmbPerfilMet.nmbTipoAcero.fy/gammaMat
  EMat= nmbePerfilMet.nmbTipoAcero.E

  mat= typical_materials.defElasticMaterial(nmbMat,EMat)
  seedElemLoader= preprocessor.getElementLoader.seedElemLoader
  seedElemLoader.defaultMaterial= nmbMat
  seedElemLoader.dimElem= 3
  truss= seedElemLoader.newElement("truss",xc.ID([0,0]))
  truss.A= areaBrr
  truss.setProp("fyd",fydMat)
  lines= setElems.getLines
  for l in lines:
    l.nDiv= numDivisiones
  setElems.genMesh(xc.meshDir,1)

