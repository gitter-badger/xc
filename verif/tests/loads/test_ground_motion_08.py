# -*- coding: utf-8 -*-
'''  Comprueba el funcionamiento del comando ground_motion_record
    mediante la integración de las aceleraciones dadas por:
    x= 9*t**3+10*t**2
    xdot= 27*t**2+20*t
    xdotdot= 54*t+20  '''

import xc_base
import geom
import xc

groundMotionDuration= 0.0
groundMotionAccel= 0.0
groundMotionPeakAccel= 0.0
motionHistoryDelta= 0.0
groundMotionVel= 0.0
groundMotionPeakVel= 0.0
groundMotionDisp= 0.0
groundMotionPeakDisp= 0.0

prueba= xc.ProblemaEF()
preprocessor=  prueba.getPreprocessor


#Load modulation.
cargas= preprocessor.getLoadLoader
casos= cargas.getLoadPatterns
ts= casos.newTimeSeries("constant_ts","ts")
gm= casos.newLoadPattern("uniform_excitation","gm")
mr= gm.motionRecord
hist= mr.history
accel= casos.newTimeSeries("path_ts","accel")
accel.path= xc.Vector([20,74,128,182,236,290,344,398])
hist.accel= accel
hist.delta= 0.01

motionHistoryDelta= hist.delta
groundMotionDuration= mr.getDuration()
groundMotionAccel= mr.getAccel(0.5)
groundMotionPeakAccel= mr.getPeakAccel()
groundMotionVel= mr.getVel(0.5)
groundMotionPeakVel= mr.getPeakVel()
groundMotionDisp= mr.getDisp(0.5)
groundMotionPeakDisp= mr.getPeakDisp()

ratio1= (groundMotionDuration-8)/8
ratio2= (groundMotionAccel-47)/47
ratio3= (groundMotionPeakAccel-398)/398
ratio4= (motionHistoryDelta-0.01)/0.01
ratio5= (groundMotionVel-16.75)/16.75
ratio7= (groundMotionPeakVel-1458)/1458
ratio8= (groundMotionDisp-3.63)/3.63

''' 
print "duration= ",groundMotionDuration
print "ratio1= ",ratio1
print "accel= ",groundMotionAccel
print "ratio2= ",ratio2
print "peak accel= ",groundMotionPeakAccel
print "ratio3= ",ratio3
print "delta= ",motionHistoryDelta
print "ratio4= ",ratio4
print "vel= ",groundMotionVel
print "ratio5= ",ratio5
print "peak vel= ",groundMotionPeakVel
print "ratio7= ",ratio7
print "disp= ",groundMotionDisp
print "ratio8= ",ratio8
  '''

import os
fname= os.path.basename(__file__)
if (abs(ratio1)<1e-15) & (abs(ratio2)<1e-15) & (abs(ratio3)<1e-15) & (abs(ratio4)<1e-15) & (abs(ratio5)<motionHistoryDelta) & (abs(ratio7)<motionHistoryDelta) & (abs(ratio8)<2*motionHistoryDelta) :
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."
