# -*- coding: utf-8 -*-
# Launcher of various calculations for RC elements of type xLamina, related to the 
# verificacion of Ultimate and Serviceability Limit States 

import os
import math
import geom
from miscUtils import LogMessages as lmsg
from materials.xLamina import extrae_combinaciones as ec
from materials.xLamina import modelo
from materials.xLamina import calculo_comb
from materials.ehe import comprobVEHE08
from materials.ehe import cortanteEHE
from materials.ehe import torsionEHE
from materials.ehe import fisuracionEHE
from materials.sia262 import shearSIA262
from materials.sia262 import fatigueControlSIA262 as fcSIA
from materials.sia262 import crackControlSIA262 as ccSIA
from postprocess import ControlVars as cv
from postprocess.reports import common_formats as fmt


###                 *** Verifications related to 
###                     ULS of failure under Normal Stresses ***

def xLaminaCompruebaTNComb(preprocessor, nmbDiagIntSec1, nmbDiagIntSec2,controller):
  '''
  Perfoms the verification under normal stresses.
  Parameters:
    preprocessor:    preprocessor name
    controller: object that control normal stress limit state.
  '''
  listaCombinaciones= []
  cargas= preprocessor.getLoadLoader
  casos= cargas.getLoadPatterns
  ts= casos.newTimeSeries("constant_ts","ts")
  casos.currentTimeSeries= "ts"
  execfile("/tmp/cargas.xci")
  listaCombinaciones= cargas.listaNombresLoadPatterns()

  for comb in listaCombinaciones:
    print("Resolviendo para acción: ",listaCombinaciones[i],"\n")
    resuelveCombEstatLin(comb)
    controller.check(comb,nmbDiagIntSec1,nmbDiagIntSec2)

  os.system("rm -f "+"/tmp/acciones.xci")
  os.system("rm -f "+"/tmp/cargas.xci")
  xLaminaPrintTN(nmbArch) # XXX Sacar de aquí la impresión de result.




'''
 Lanza la comprobación de tensiones normales en una lámina
    cuyos esfuerzos se dan en el archivo de nombre nmbArch.lst
    con los materiales que se definen en el archivo nmbArchMateriales,
    las características de las secciones que se definen en los registros
    datosScc1 y datosScc2, las combinaciones definidas en el archivo
    nmbArchDefHipELU e imprime los resultados en archivos con
    el nombre nmbArchTN.*
'''
def lanzaCalculoTNFromAnsysData(nmbArch, datosScc1, datosScc2, nmbArchDefHipELU):
  extraeDatosLST(nmbArch+".lst") 
  xLaminaConstruyeModeloFicticio(datosScc1,datosScc2)
  nmbDiagIntSec1= "diagInt"+datosScc1.sectionName
  nmbDiagIntSec2= "diagInt"+datosScc2.sectionName
  xLaminaCalculaCombEstatLin(nmbArchDefHipELU,nmbDiagIntSec1,nmbDiagIntSec2)
  meanCFs= cv.writeControlVarsFromElements("ULS_normStr",preprocessor,nmbArch+"TN",datosScc1.sectionName,datosScc2.sectionName)
  return meanCFs

def lanzaCalculoTNFromXCData(preprocessor,analysis,intForcCombFileName,outputFileName, sectionsNamesForEveryElement,mapSectionsDefinition, mapInteractionDiagrams,controller):
  '''
  Lanza la comprobación de tensiones normales en una lámina
    cuyos esfuerzos se dan en el archivo de nombre nmbArch.lst
    con los materiales que se definen en el archivo nmbArchMateriales,
    las características de las secciones que se definen en los registros
    datosScc1 y datosScc2, las combinaciones definidas en el archivo
    nmbArchDefHipELU e imprime los resultados en archivos con
    el nombre nmbArchTN.*
  Parameters:
    preprocessor:    preprocessor name
    analysis:        type of analysis
    intForcCombFileName: name of the file containing the forces and bending moments 
                     obtained for each element for the combinations analyzed
    outputFileName:  name of the output file containing tue results of the 
                     verification 
    sectionsNamesForEveryElement: file containing a dictionary  such that for each                                element of the model stores two names 
                                (for the sections 1 and 2) to be employed 
                                in verifications
    mapSectionsDefinition:      file containing a dictionary with the two 
                                sections associated with each elements to be
                                used in the verification
    mapInteractionDiagrams:     file containing a dictionary such that                                                      associates each element with the two interactions
                                diagrams of materials to be used in the verification process
  '''
  meanCFs= -1.0
  if(controller):
    ec.extraeDatos(preprocessor,intForcCombFileName, sectionsNamesForEveryElement,mapSectionsDefinition, mapInteractionDiagrams,controller.limitStateLabel)
    elements= preprocessor.getSets.getSet("total").getElements
    calculo_comb.xLaminaCalculaCombEstatLin(preprocessor,elements,analysis,controller)
    meanCFs= cv.writeControlVarsFromElements(controller.limitStateLabel,preprocessor,outputFileName)
  else:
    lmsg.error('lanzaCalculoTNFromXCData controller not defined.')
  return meanCFs

def lanzaCalculoTN2dFromXCData(preprocessor,analysis,intForcCombFileName,outputFileName, sectionsNamesForEveryElement,mapSectionsDefinition, mapInteractionDiagrams,controller):
  '''
  Parameters:
    preprocessor:        preprocessor name
    analysis:            type of analysis
    intForcCombFileName: name of the file containing the forces and bending moments 
                         obtained for each element for the combinations analyzed
    outputFileName:      name of the output file containing the results of the 
                         verification  
    sectionsNamesForEveryElement: file containing a dictionary  such that for each 
                                  element of the model stores two names 
                                (for the sections 1 and 2) to be employed 
                                in verifications
    mapSectionsDefinition:      file containing a dictionary with the two 
                                sections associated with each elements to be
                                used in the verification
    mapInteractionDiagrams:     file containing a dictionary such that
                                associates each element with the two interactions
                                diagrams of materials to be used in the verification process
  '''
  lmsg.warning('lanzaCalculoTN2dFromXCData DEPRECATED call lanzaCalculoTNFromXCData with an uniaxial bending controller.')
  meanCFs= -1.0
  if(controller):
    ec.extraeDatos(preprocessor,intForcCombFileName, sectionsNamesForEveryElement,mapSectionsDefinition, mapInteractionDiagrams,controller.limitStateLabel)
    elements= preprocessor.getSets.getSet("total").getElements
    calculo_comb.xLaminaCalculaCombEstatLin(preprocessor,elements,analysis,controller)
    meanCFs= cv.writeControlVarsFromElements(controller.limitStateLabel,preprocessor,outputFileName)
  else:
    lmsg.error('lanzaCalculoTNFromXCData controller not defined.')
  return meanCFs



###                    *** Verifications related to 
###                        ULS of failure due to Shear ***


def lanzaCalculoVFromAnsysData(preprocessor,nmbArch, nmbRegDatosScc1, nmbRegDatosScc2, nmbArchDefHipELU):
  '''
   Lanza la comprobación de cortante en una lámina
      cuyos esfuerzos se dan en el archivo de nombre nmbArch.lst
      con los materiales que se definen en el archivo nmbArchMateriales,
      las características de las secciones que se definen en los registros
      datosScc1 y datosScc2, las combinaciones definidas en el archivo
      nmbArchDefHipELU e imprime los resultados en archivos con
      el nombre nmbArchTN.*
  '''
  extraeDatosLST(nmbArch+".lst")
  xLaminaConstruyeModeloFibras(nmbRegDatosScc1,nmbRegDatosScc2)
  xLaminaCalculaCombEstatNoLin(nmbArchDefHipELU)
  cv.writeControlVarsFromElementsForAnsys('ULS_shear',preprocessor,nmbArch+"V",deref(nmbRegDatosScc1).sectionName,deref(nmbRegDatosScc2).sectionName)

def lanzaCalculoV(preprocessor,analysis,intForcCombFileName,outputFileName, sectionsNamesForEveryElement,mapSectionsDefinition, mapInteractionDiagrams,controller):
  '''
   Lanza la comprobación de cortante en una lámina
      cuyos esfuerzos se dan en el archivo de nombre nmbArch.lst
      con los materiales que se definen en el archivo nmbArchMateriales,
      las características de las secciones que se definen en los registros
      datosScc1 y datosScc2, las combinaciones definidas en el archivo
      nmbArchDefHipELU e imprime los resultados en archivos con
      el nombre nmbArchTN.*
  Parameters:
    preprocessor:    preprocessor name
    analysis:        type of analysis
    intForcCombFileName: name of the file containing the forces and bending moments 
                     obtained for each element for the combinations analyzed
    outputFileName:  name of the output file containing tue results of the 
                     verification 
    sectionsNamesForEveryElement: file containing a dictionary  such that for each                                element of the model stores two names 
                                (for the sections 1 and 2) to be employed 
                                in verifications
    mapSectionsDefinition:      file containing a dictionary with the two 
                                sections associated with each elements to be
                                used in the verification
    mapInteractionDiagrams:     file containing a dictionary such that                                                      associates each element with the two interactions
                                diagrams of materials to be used in the verification process
    controller: object that controls the limit state on elements.
  '''
  meanCFs= -1.0
  if(controller):
    elems= ec.extraeDatos(preprocessor,intForcCombFileName, sectionsNamesForEveryElement,mapSectionsDefinition, mapInteractionDiagrams,controller.limitStateLabel)
    elements= preprocessor.getSets.getSet("total").getElements
    calculo_comb.xLaminaCalculaComb(preprocessor,elements,analysis,controller)
    meanCFs= cv.writeControlVarsFromElements(controller.limitStateLabel,preprocessor,outputFileName)
  else:
    lmsg.error('lanzaCalculoV controller not defined.')
  return meanCFs

###                 *** Verifications related to 
###                     ULS of Fatigue ***
def lanzaCalculoFatigueFromXCDataPlanB(preprocessor,analysis,intForcCombFileName,outputFileName, sectionsNamesForEveryElement,mapSectionsDefinition, mapInteractionDiagrams,controller):
  '''Launch the calculation for the verification of the Fatigue Limit State
  in shell elements.
  Parameters:
    preprocessor:    preprocessor name
    analysis:        type of analysis
    intForcCombFileName: name of the file containing the forces and bending moments 
                     obtained for each element for the combinations analyzed
    outputFileName:  name of the output file containing tue results of the 
                     verification 
    sectionsNamesForEveryElement: file containing a dictionary  such that for each                                element of the model stores two names 
                                (for the sections 1 and 2) to be employed 
                                in verifications
    mapSectionsDefinition:      file containing a dictionary with the two 
                                sections associated with each elements to be
                                used in the verification
    mapInteractionDiagrams:     file containing a dictionary such that                                                      associates each element with the two interactions
                                diagrams of materials to be used in the verification process
    controller: object that controls limit state on elements.
   '''
  if(controller):
    elems= ec.extraeDatos(preprocessor,intForcCombFileName, sectionsNamesForEveryElement,mapSectionsDefinition, mapInteractionDiagrams,controller.limitStateLabel)
    fcSIA.defVarsControl(elems)
    elements= preprocessor.getSets.getSet("total").getElements
    calculo_comb.xLaminaCalculaComb(preprocessor,elements,analysis,controller)
    xLaminaPrintFatigueSIA262(preprocessor,outputFileName,sectionsNamesForEveryElement)
  else:
    lmsg.error('lanzaCalculoFatigueFromXCDataPlanB controller not defined.')

def strElementProp(eTag,nmbProp,vProp):
  retval= "preprocessor.getElementLoader.getElement("
  retval+= str(eTag)
  retval+= ").setProp("
  retval+= '"' + nmbProp + '"'
  retval+= ',' + str(vProp) + ")\n"
  return retval

def xLaminaPrintFatigueSIA262(preprocessor,outputFileName, mapSections):
  '''
  Parameters:
    preprocessor:    preprocessor name
  '''
  # Imprime los resultados de la comprobación frente a fisuración
  texOutput1= open("/tmp/texOutput1.tmp","w")
  texOutput2= open("/tmp/texOutput2.tmp","w")
  xcOutput= open(outputFileName+".py","w")
  elementos= preprocessor.getSets.getSet("total").getElements
  strHeader0= "eTag & idSection & N0 kN & My0 kN m/m & Mz0 kN m/m & Vy0 kN m/m & Vz0 kN m/m & $sg_{s,0} MPa & $sg_{c,0} MPa \\\\\n"
  strHeader1= "     &           & N1 kN & My1 kN m/m & Mz1 kN m/m & Vy1 kN m/m & Vz1 kN m/m & $sg_{s,1} MPa & $sg_{c,1} MPa \\\\\n"
  texOutput1.write(strHeader0)
  texOutput1.write(strHeader1)
  texOutput2.write(strHeader0)
  texOutput2.write(strHeader1)
  for e in elementos:
    tag= e.getProp("idElem")
    idSection= e.getProp("idSection")
    N0= e.getProp("N0")
    My0= e.getProp("My0")
    Mz0= e.getProp("Mz0")
    Vy0= e.getProp("Vy0")
    Vz0= e.getProp("Vz0")
    sg_sPos0= e.getProp("sg_sPos0")
    sg_sNeg0= e.getProp("sg_sNeg0")
    sg_c0= e.getProp("sg_c0")
    N1= e.getProp("N1")
    My1= e.getProp("My1")
    Mz1= e.getProp("Mz1")
    Vy1= e.getProp("Vy1")
    Vz1= e.getProp("Vz1")
    sg_sPos1= e.getProp("sg_sPos1")
    sg_sNeg1= e.getProp("sg_sNeg1")
    sg_c1= e.getProp("sg_c1")
    inc_sg_sPos= sg_sPos1-sg_sPos0
    inc_sg_sNeg= sg_sNeg1-sg_sNeg0
    inc_sg_s= max(inc_sg_sPos,inc_sg_sNeg)
    inc_sg_c= sg_c1-sg_c0
    Mu= e.getProp("Mu")
    Vu= e.getProp("Vu")
    lim_sg_c= e.getProp("lim_sg_c")
    fc_sg_c= e.getProp("fc_sg_c")
    lim_v= e.getProp("lim_v")
    fc_v= e.getProp("fc_v")

    strEsf0= "N0=  &"+fmt.Esf.format(N0/1e3)+" & "+"My0=  &"+fmt.Esf.format(My0/1e3)+" & "+"Mz0=  &"+fmt.Esf.format(Mz0/1e3)+" & "+"Vy0=  &"+fmt.Esf.format(Vy0/1e3)+" & "+"Vz0=  &"+fmt.Esf.format(Vz0/1e3)
    strStress0= "sgAxPos0=  &"+fmt.Stress.format(sg_sPos0/1e6)+" & "+"sgAxNeg0=  &"+fmt.Stress.format(sg_sNeg0/1e6)+" & "+"sgC0=  &"+fmt.Stress.format(sg_c0/1e6)
    strEsf1= "N1=  &"+fmt.Esf.format(N1/1e3)+" & "+"My1=  &"+fmt.Esf.format(My1/1e3)+" & "+"Mz1=  &"+fmt.Esf.format(Mz1/1e3)+" & "+"Vy1=  &"+fmt.Esf.format(Vy1/1e3)+" & "+"Vz1=  &"+fmt.Esf.format(Vz1/1e3)
    strStress1= "sgAxPos1=  &"+fmt.Stress.format(sg_sPos1/1e6)+" & "+"sgAxNeg1=  &"+fmt.Stress.format(sg_sNeg1/1e6)+" & "+"sgC1=  &"+fmt.Stress.format(sg_c1/1e6)
    strEsfUl= fmt.Esf.format(Mu/1e3)+" & "+fmt.Esf.format(Vu/1e3)

    strOut0= str(tag)+" & " +idSection + " & "+strEsf0+" & "+strStress0+"\\\\\n"
    strOut1= str(tag)+" & " +idSection + " & "+strEsf1+" & "+strStress1+" & "+strEsfUl+"\\\\\n"

    if(e.getProp("dir")==1):
      texOutput1.write(strOut0)
      texOutput1.write(strOut1)
      xcOutput.write(strElementProp(tag,"sg_sPos01",sg_sPos0/1e6))
      xcOutput.write(strElementProp(tag,"sg_sNeg01",sg_sNeg0/1e6))
      xcOutput.write(strElementProp(tag,"sg_c01",sg_c0/1e6))
      xcOutput.write(strElementProp(tag,"N01",N0/1e3))
      xcOutput.write(strElementProp(tag,"My01",My0/1e3))
      xcOutput.write(strElementProp(tag,"Mz01",Mz0/1e3))
      xcOutput.write(strElementProp(tag,"Vy01",Vy0/1e3))
      xcOutput.write(strElementProp(tag,"Vz01",Vz0/1e3))
      xcOutput.write(strElementProp(tag,"sg_sPos11",sg_sPos1/1e6))
      xcOutput.write(strElementProp(tag,"sg_sNeg11",sg_sNeg1/1e6))
      xcOutput.write(strElementProp(tag,"N11",N0/1e3))
      xcOutput.write(strElementProp(tag,"My11",My1/1e3))
      xcOutput.write(strElementProp(tag,"Mz11",Mz1/1e3))
      xcOutput.write(strElementProp(tag,"Vy11",Vy1/1e3))
      xcOutput.write(strElementProp(tag,"Vz11",Vz1/1e3))
      xcOutput.write(strElementProp(tag,"inc_sg_sPos1",inc_sg_sPos/1e6))
      xcOutput.write(strElementProp(tag,"inc_sg_sNeg1",inc_sg_sNeg/1e6))
      xcOutput.write(strElementProp(tag,"inc_sg_s1",inc_sg_s/1e6))
      xcOutput.write(strElementProp(tag,"inc_sg_c1",inc_sg_c/1e6))
      xcOutput.write(strElementProp(tag,"lim_sg_c1",lim_sg_c/1e6))
      xcOutput.write(strElementProp(tag,"fc_sg_c1",fc_sg_c))
      xcOutput.write(strElementProp(tag,"Mu1",Mu/1e3))
      xcOutput.write(strElementProp(tag,"Vu1",Vu/1e3))
      xcOutput.write(strElementProp(tag,"lim_v1",lim_v/1e6))
      xcOutput.write(strElementProp(tag,"fc_v1",fc_v))
    else:
      texOutput2.write(strOut0)
      texOutput2.write(strOut1)
      xcOutput.write(strElementProp(tag,"sg_sPos02",sg_sPos0/1e6))
      xcOutput.write(strElementProp(tag,"sg_sNeg02",sg_sNeg0/1e6))
      xcOutput.write(strElementProp(tag,"sg_c02",sg_c0/1e6))
      xcOutput.write(strElementProp(tag,"N02",N0/1e3))
      xcOutput.write(strElementProp(tag,"My02",My0/1e3))
      xcOutput.write(strElementProp(tag,"Mz02",Mz0/1e3))
      xcOutput.write(strElementProp(tag,"Vy02",Vy0/1e3))
      xcOutput.write(strElementProp(tag,"Vz02",Vz0/1e3))
      xcOutput.write(strElementProp(tag,"sg_sPos12",sg_sPos1/1e6))
      xcOutput.write(strElementProp(tag,"sg_sNeg12",sg_sNeg1/1e6))
      xcOutput.write(strElementProp(tag,"N12",N0/1e3))
      xcOutput.write(strElementProp(tag,"My12",My1/1e3))
      xcOutput.write(strElementProp(tag,"Mz12",Mz1/1e3))
      xcOutput.write(strElementProp(tag,"Vy12",Vy1/1e3))
      xcOutput.write(strElementProp(tag,"Vz12",Vz1/1e3))
      xcOutput.write(strElementProp(tag,"inc_sg_sPos2",inc_sg_sPos/1e6))
      xcOutput.write(strElementProp(tag,"inc_sg_sNeg2",inc_sg_sNeg/1e6))
      xcOutput.write(strElementProp(tag,"inc_sg_s2",inc_sg_s/1e6))
      xcOutput.write(strElementProp(tag,"inc_sg_c2",inc_sg_c/1e6))
      xcOutput.write(strElementProp(tag,"lim_sg_c2",lim_sg_c/1e6))
      xcOutput.write(strElementProp(tag,"fc_sg_c2",fc_sg_c))
      xcOutput.write(strElementProp(tag,"Mu2",Mu/1e3))
      xcOutput.write(strElementProp(tag,"Vu2",Vu/1e3))
      xcOutput.write(strElementProp(tag,"lim_v2",lim_v/1e6))
      xcOutput.write(strElementProp(tag,"fc_v2",fc_v))


  texOutput1.close()
  texOutput2.close()
  xcOutput.close()
    
  os.system("cat /tmp/texOutput1.tmp /tmp/texOutput2.tmp > "+outputFileName+".tex")
    
  # os.system("rm -f "+"/tmp/acciones.xci")
  # os.system("rm -f "+"/tmp/cargas.xci")
  # os.system("rm -f "+"/tmp/elementos.xci")
  os.system("rm -f "+"/tmp/texOutput1.tmp")
  os.system("rm -f "+"/tmp/texOutput2.tmp")


###                 *** Verifications related to 
###                     Cracking SLS  ***

def lanzaCalculoFIS(nmbArch, nmbRegDatosScc1, nmbRegDatosScc2, nmbArchDefHipELS):
  '''
   Lanza la comprobación de fisuración en una lámina
      cuyos esfuerzos se dan en el archivo de nombre nmbArch.lst
      con los materiales que se definen en el archivo nmbArchMateriales,
      las características de las secciones que se definen en los registros
      datosScc1 y datosScc2, las combinaciones definidas en el archivo
      nmbArchDefHipELS e imprime los resultados en archivos con
      el nombre nmbArchFis.*
  '''
  extraeDatosLST(nmbArch+".lst")
  xLaminaConstruyeModeloFibras(nmbRegDatosScc1,nmbRegDatosScc2)
  xLaminaCalculaCombEstatNoLin(nmbArchDefHipELS)
  xLaminaPrintFIS(nmbArch+"FIS",deref(nmbRegDatosScc1).sectionName,deref(nmbRegDatosScc2).sectionName)


def lanzaCalculoFISFromXCData(preprocessor,analysis,intForcCombFileName,outputFileName, sectionsNamesForEveryElement,controller):
  '''
   Lanza la comprobación de fisuración en una lámina
      cuyos esfuerzos se dan en el archivo de nombre nmbArch.lst
      con los materiales que se definen en el archivo nmbArchMateriales,
      las características de las secciones que se definen en mapSections,
      e imprime los resultados en archivos con
      el nombre nmbArchFis.*
  Parameters:
    preprocessor:    preprocessor name
    analysis:        type of analysis
    intForcCombFileName: name of the file containing the forces and bending moments 
                     obtained for each element for the combinations analyzed
    outputFileName:  name of the output file containing tue results of the 
                     verification 
    sectionsNamesForEveryElement: file containing a dictionary  such that for each
                                element of the model stores two names 
                                (for the sections 1 and 2) to be employed 
                                in verifications
    controller: object that controls limit state on elements      
  '''
  meanCFs= -1.0
  if(controller):
    elems= ec.creaElems(preprocessor,intForcCombFileName, sectionsNamesForEveryElement)
    ccSIA.defVarsControlFISSIA262(elems)
    elements= preprocessor.getSets.getSet("total").getElements
    calculo_comb.xLaminaCalculaComb(preprocessor,elements,analysis,controller)
    meanCFs= cv.writeControlVarsFromElements(controller.limitStateLabel,preprocessor,outputFileName,sectionsNamesForEveryElement)
  else:
    lmsg.error('lanzaCalculoFISFromXCData controller not defined.')
  return meanCFs

def lanzaCalculoFISFromXCDataPlanB(preprocessor,analysis,intForcCombFileName,outputFileName, sectionsNamesForEveryElement,mapSectionsDefinition,controller):
  '''
   Lanza la comprobación de fisuración en una lámina
      cuyos esfuerzos se dan en el archivo de nombre nmbArch.lst
      con los materiales que se definen en el archivo nmbArchMateriales,
      las características de las secciones que se definen en mapSections,
      e imprime los resultados en archivos con
      el nombre nmbArchFis.*
  Parameters:
    preprocessor:    preprocessor name
    analysis:        type of analysis
    intForcCombFileName: name of the file containing the forces and bending moments 
                     obtained for each element for the combinations analyzed
    outputFileName:  name of the output file containing tue results of the 
                     verification 
    sectionsNamesForEveryElement: file containing a dictionary  such that for each
                                element of the model stores two names 
                                (for the sections 1 and 2) to be employed 
                                in verifications
    controller: object that controls limit state on elements      
  '''
  if(controller):
    elems= ec.extraeDatos(preprocessor,intForcCombFileName, sectionsNamesForEveryElement,mapSectionsDefinition, None,controller.limitStateLabel)
    elements= preprocessor.getSets.getSet("total").getElements
    calculo_comb.xLaminaCalculaComb(elements,analysis,controller)
    cv.writeControlVarsFromElements(controller.limitStateLabel,preprocessor,outputFileName,sectionsNamesForEveryElement)
  else:
    lmsg.error('lanzaCalculoFISFromXCDataPlanB controller not defined.')
  return meanCFs

