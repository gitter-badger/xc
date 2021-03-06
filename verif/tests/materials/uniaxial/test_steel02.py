# -*- coding: utf-8 -*-
# home made test

fy= 2600 # Tensión de cedencia del acero.
E= 2.1e6 # Módulo de Young del acero.
l= 1 # Distancia entre nodes
epsy= fy/E # Deformación para la que se produce la cedencia
D= 1.5*epsy # Displacement magnitude impuesto
F= 1.05*E*epsy # Fuerza a aplicar.
Nsteps= 10 # Número de pasos para el análisis.

import math
import xc_base
import geom
import xc
from solution import predefined_solutions
from model import predefined_spaces
from model import fix_node_6dof
from model import fija_nodos_lineas
from model import cargas_nodo
from materials import typical_materials

# Puntos de la función tensión - deformación
x_modelo= [0.0002,0.0004,0.0006,0.0008,0.001,0.0012,0.0014,0.0016,0.0014,0.0012,0.001,0.0008,0.0006,0.0004,0.0002,8.13151629364e-20,-0.0002,-0.0004,-0.0006,-0.0008,-0.001,-0.0012,-0.0014,-0.0016,-0.0014,-0.0012,-0.001,-0.0008,-0.0006,-0.0004,-0.0002,3.7947076037e-19,0.0002,0.0004,0.0006,0.0008,0.001,0.0012,0.0014,0.0016]
y_modelo= [420,839.99999756,1259.9983975,1679.84023129,2094.43925811,2439.74485068,2575.02268013,2597.10357884,2177.10361083,1757.10718257,1337.16070607,917.509155896,498.955465729,83.4836121405,-324.877516243,-719.184353981,-1089.3087798,-1423.15134693,-1709.72230813,-1942.88083256,-2123.30032297,-2257.38132823,-2354.30837053,-2423.31773771,-2003.32887686,-1583.61049005,-1165.29416968,-750.941478428,-344.863824637,46.9169088244,417.211303572,758.719915171,1065.35896571,1333.3932764,1561.95005251,1752.78930425,1909.55078241,2036.84608339,2139.48812589,2221.98168325]


# Model definition
prueba= xc.ProblemaEF()
preprocessor=  prueba.getPreprocessor
nodes= preprocessor.getNodeLoader

# Problem type
predefined_spaces.gdls_elasticidad2D(nodes)


nodes.defaultTag= 1 #First node number.
nod= nodes.newNodeXY(0,0)
nod= nodes.newNodeXY(l,0.0)

# Materials definition
mat= typical_materials.defSteel02(preprocessor, "acero",E,fy,0.001,0.0)
  
''' Se definen nodes en los puntos de aplicación de
la carga. Puesto que no se van a determinar tensiones
se emplea una sección arbitraria de área unidad '''
    
# Elements definition
elementos= preprocessor.getElementLoader
elementos.defaultMaterial= "acero"
elementos.dimElem= 2
elementos.defaultTag= 1 #Tag for the next element.
spring= elementos.newElement("spring",xc.ID([1,2]));
    
# Constraints
coacciones= preprocessor.getConstraintLoader
#
spc= coacciones.newSPConstraint(1,0,0.0) # Node 1
spc= coacciones.newSPConstraint(1,1,0.0)
spc= coacciones.newSPConstraint(2,1,0.0) # Node 2

# Loads definition
cargas= preprocessor.getLoadLoader
casos= cargas.getLoadPatterns
ts= casos.newTimeSeries("trig_ts","ts")
ts.factor= 1
ts.tStart= 0
ts.tFinish= 2
ts.period= 1
ts.shift= 0
casos.currentTimeSeries= "ts"
#Load case definition
lp0= casos.newLoadPattern("default","0")
lp0.newNodalLoad(2,xc.Vector([F,0]))

#We add the load case to domain.
casos.addToDomain("0")

x= []
y= []
recorder= prueba.getDomain.newRecorder("element_prop_recorder",None);
recorder.setElements(xc.ID([1]))
recorder.callbackRecord= "x.append(self.getMaterial().getStrain()); y.append(self.getN())"
recorder.callbackRestart= "print \"Restart method called.\""


''' 
        \prop_recorder

nodes= preprocessor.getNodeLoader{2
            \callback_record

                
d= .getDisp[0]
print (d*1000)

            \callback_restart{print("Se llamó al método restart."}



'''
# Procedimiento de solución
solu= prueba.getSoluProc
solCtrl= solu.getSoluControl
solModels= solCtrl.getModelWrapperContainer
sm= solModels.newModelWrapper("sm")
numberer= sm.newNumberer("default_numberer")
numberer.useAlgorithm("rcm")
cHandler= sm.newConstraintHandler("transformation_constraint_handler")
solMethods= solCtrl.getSoluMethodContainer
smt= solMethods.newSoluMethod("ldctrl","sm")
solAlgo= smt.newSolutionAlgorithm("newton_raphson_soln_algo")
ctest= smt.newConvergenceTest("energy_inc_conv_test")
ctest.tol= 1e-9
ctest.maxNumIter= 10 # Convergence Test: maximum number of iterations that will be performed before "failure to converge" is returned
ctest.printFlag= 0 # Convergence Test: flag used to print information on convergence (optional)
                   # 1: print information on each= step
integ= smt.newIntegrator("displacement_control_integrator",xc.Vector([]))
integ.nod= 2
integ.dof= 0
integ.dU1= 0.0002
soe= smt.newSystemOfEqn("band_spd_lin_soe")
solver= soe.newSolver("band_spd_lin_lapack_solver")
analysis= solu.newAnalysis("static_analysis","ldctrl","")
result= analysis.analyze(8)


integ.dU1= -0.0002 #Unload
result= analysis.analyze(16)

integ.dU1= 0.0002 #Reload
result= analysis.analyze(16)


#resta= ley-ley_modelo
resta_x= []
resta_y= []
def substract(x,y): return x-y
resta_x= map(substract,x,x_modelo)
resta_y= map(substract,y,y_modelo)

ratio1= 0
for d in resta_x:
  ratio1= ratio1+d**2
ratio3= math.sqrt(ratio1)
ratio2= 0
for d in resta_y:
  ratio2= ratio2+d**2
ratio4= math.sqrt(ratio2)

#print "x= ",x
#print "resta_x= ",resta_x
#print "ratio3= ",ratio3
#print "y= ",y
#print "y_modelo= ",y_modelo
#print "resta_y= ",resta_y
#print "ratio4= ",ratio4


import os
fname= os.path.basename(__file__)
if((ratio1<1e-17) & (ratio2<1e-7)):
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."
