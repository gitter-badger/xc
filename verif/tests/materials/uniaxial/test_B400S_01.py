# -*- coding: utf-8 -*-
# Home made test
import xc_base
import geom
import xc

from materials.ehe import EHE_reinforcing_steel
from materials import reinforcingSteelTest

# Model definition
prueba= xc.ProblemaEF()
prueba.logFileName= "/tmp/borrar.log" # Para no imprimir mensajes de advertencia
preprocessor=  prueba.getPreprocessor
# Definimos materiales
errMax= reinforcingSteelTest.testDiagKAceroArmar(preprocessor, EHE_reinforcing_steel.B400S)


# print "errMax= ",(errMax)
import os
fname= os.path.basename(__file__)
if errMax<1e-10:
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."
